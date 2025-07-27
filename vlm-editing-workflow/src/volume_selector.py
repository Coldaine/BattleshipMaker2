"""
Volume-based selection engine for Blender integration.
Addresses critical flaw: eliminates natural language ambiguity with precise geometric operations.
"""

import bpy
import bmesh
from mathutils import Vector, Quaternion, Matrix
from typing import Dict, List, Tuple, Optional, Any
import json
import jsonschema

class VolumeSelector:
    """Handles 3D volume-based selection and validation for structured tool calls."""
    
    def __init__(self, schema_path: str = "schema/tool_calls_schema.json"):
        """Initialize with JSON schema for validation."""
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
    
    def validate_tool_calls(self, tool_calls_json: Dict[str, Any]) -> bool:
        """Validate tool calls against schema to prevent malformed input."""
        try:
            jsonschema.validate(tool_calls_json, self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            print(f"Schema validation failed: {e}")
            return False
    
    def select_vertices_in_volume(self, obj: bpy.types.Object, volume_id: Dict[str, Any]) -> List[int]:
        """
        Select vertices within specified 3D volume.
        
        Args:
            obj: Blender mesh object
            volume_id: Volume identifier with type, center, dimensions, rotation
            
        Returns:
            List of vertex indices within the volume
        """
        if obj.type != 'MESH':
            raise ValueError("Object must be a mesh")
        
        # Get mesh data
        mesh = obj.data
        vertices = [obj.matrix_world @ v.co for v in mesh.vertices]
        
        # Parse volume parameters
        volume_type = volume_id["type"]
        center = Vector(volume_id["center_xyz"])
        
        # Create transformation matrix for volume space
        transform_matrix = Matrix.Translation(center)
        if "rotation_quaternion_wxyz" in volume_id:
            q = Quaternion(volume_id["rotation_quaternion_wxyz"])
            transform_matrix = transform_matrix @ q.to_matrix().to_4x4()
        
        # Transform vertices to volume-local space
        inv_transform = transform_matrix.inverted()
        local_vertices = [inv_transform @ v for v in vertices]
        
        # Select based on volume type
        selected_indices = []
        
        if volume_type == "box":
            dims = Vector(volume_id["dimensions_xyz"]) / 2.0  # Half-extents
            for i, v in enumerate(local_vertices):
                if (abs(v.x) <= dims.x and abs(v.y) <= dims.y and abs(v.z) <= dims.z):
                    selected_indices.append(i)
                    
        elif volume_type == "sphere":
            radius = volume_id["radius"]
            for i, v in enumerate(local_vertices):
                if v.length <= radius:
                    selected_indices.append(i)
                    
        elif volume_type == "cylinder":
            dims = Vector(volume_id["dimensions_xyz"])
            radius = dims.x  # Use x as radius
            height = dims.z / 2.0  # Half-height
            for i, v in enumerate(local_vertices):
                # Check cylinder bounds (infinite along Y-axis for now)
                xy_dist = Vector((v.x, v.y)).length
                if xy_dist <= radius and abs(v.z) <= height:
                    selected_indices.append(i)
                    
        else:
            raise ValueError(f"Unsupported volume type: {volume_type}")
        
        return selected_indices
    
    def select_faces_in_volume(self, obj: bpy.types.Object, volume_id: Dict[str, Any]) -> List[int]:
        """
        Select faces with centers within specified 3D volume.
        
        Args:
            obj: Blender mesh object
            volume_id: Volume identifier
            
        Returns:
            List of face indices within the volume
        """
        if obj.type != 'MESH':
            raise ValueError("Object must be a mesh")
        
        mesh = obj.data
        selected_faces = []
        
        for i, face in enumerate(mesh.polygons):
            # Calculate face center in world space
            face_center = obj.matrix_world @ face.center
            
            # Create a dummy vertex at face center for volume testing
            dummy_vertices = [face_center]
            volume_id_copy = volume_id.copy()
            
            # Test if face center is in volume
            # (Reuse vertex selection logic with face center as vertex)
            center = Vector(volume_id["center_xyz"])
            transform_matrix = Matrix.Translation(center)
            if "rotation_quaternion_wxyz" in volume_id:
                q = Quaternion(volume_id["rotation_quaternion_wxyz"])
                transform_matrix = transform_matrix @ q.to_matrix().to_4x4()
            
            inv_transform = transform_matrix.inverted()
            local_center = inv_transform @ face_center
            
            volume_type = volume_id["type"]
            in_volume = False
            
            if volume_type == "box":
                dims = Vector(volume_id["dimensions_xyz"]) / 2.0
                if (abs(local_center.x) <= dims.x and 
                    abs(local_center.y) <= dims.y and 
                    abs(local_center.z) <= dims.z):
                    in_volume = True
                    
            elif volume_type == "sphere":
                radius = volume_id["radius"]
                if local_center.length <= radius:
                    in_volume = True
                    
            elif volume_type == "cylinder":
                dims = Vector(volume_id["dimensions_xyz"])
                radius = dims.x
                height = dims.z / 2.0
                xy_dist = Vector((local_center.x, local_center.y)).length
                if xy_dist <= radius and abs(local_center.z) <= height:
                    in_volume = True
            
            if in_volume:
                selected_faces.append(i)
        
        return selected_faces
    
    def visualize_volume(self, volume_id: Dict[str, Any], name: str = "VolumeVisualization") -> bpy.types.Object:
        """
        Create a visual representation of the volume for debugging.
        
        Args:
            volume_id: Volume identifier
            name: Name for the visualization object
            
        Returns:
            Blender object representing the volume
        """
        volume_type = volume_id["type"]
        center = Vector(volume_id["center_xyz"])
        
        if volume_type == "box":
            # Create cube and scale to dimensions
            bpy.ops.mesh.primitive_cube_add(location=center)
            obj = bpy.context.active_object
            obj.name = name
            
            dims = Vector(volume_id["dimensions_xyz"])
            obj.scale = dims
            
        elif volume_type == "sphere":
            # Create UV sphere
            radius = volume_id["radius"]
            bpy.ops.mesh.primitive_uv_sphere_add(location=center, radius=radius)
            obj = bpy.context.active_object
            obj.name = name
            
        elif volume_type == "cylinder":
            # Create cylinder
            dims = Vector(volume_id["dimensions_xyz"])
            radius = dims.x
            depth = dims.z
            bpy.ops.mesh.primitive_cylinder_add(location=center, radius=radius, depth=depth)
            obj = bpy.context.active_object
            obj.name = name
            
        else:
            raise ValueError(f"Unsupported volume type for visualization: {volume_type}")
        
        # Apply rotation if specified
        if "rotation_quaternion_wxyz" in volume_id:
            q = Quaternion(volume_id["rotation_quaternion_wxyz"])
            obj.rotation_mode = 'QUATERNION'
            obj.rotation_quaternion = q
        
        # Make it wireframe for visualization
        if obj.data.materials:
            mat = obj.data.materials[0]
        else:
            mat = bpy.data.materials.new(name=f"{name}_Material")
            obj.data.materials.append(mat)
        
        mat.use_nodes = True
        mat.blend_method = 'BLEND'
        mat.node_tree.nodes["Principled BSDF"].inputs[21].default_value = 0.8  # Alpha
        
        return obj
    
    def get_scene_bounds(self) -> Tuple[Vector, Vector]:
        """Get bounding box of all objects in scene for coordinate validation."""
        min_coords = Vector((float('inf'), float('inf'), float('inf')))
        max_coords = Vector((float('-inf'), float('-inf'), float('-inf')))
        
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                for vertex in obj.data.vertices:
                    world_co = obj.matrix_world @ vertex.co
                    min_coords.x = min(min_coords.x, world_co.x)
                    min_coords.y = min(min_coords.y, world_co.y)
                    min_coords.z = min(min_coords.z, world_co.z)
                    max_coords.x = max(max_coords.x, world_co.x)
                    max_coords.y = max(max_coords.y, world_co.y)
                    max_coords.z = max(max_coords.z, world_co.z)
        
        return min_coords, max_coords
    
    def validate_coordinates(self, volume_id: Dict[str, Any]) -> bool:
        """Validate that volume coordinates are within reasonable scene bounds."""
        center = Vector(volume_id["center_xyz"])
        min_bounds, max_bounds = self.get_scene_bounds()
        
        # Add some tolerance for volumes extending beyond current geometry
        tolerance = 10.0
        expanded_min = min_bounds - Vector((tolerance, tolerance, tolerance))
        expanded_max = max_bounds + Vector((tolerance, tolerance, tolerance))
        
        return (expanded_min.x <= center.x <= expanded_max.x and
                expanded_min.y <= center.y <= expanded_max.y and
                expanded_min.z <= center.z <= expanded_max.z)