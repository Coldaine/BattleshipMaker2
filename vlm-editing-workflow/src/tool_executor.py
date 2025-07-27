"""
Tool execution engine that implements the corrected structured approach.
Eliminates natural language parsing with direct function calls.
"""

import json
import jsonschema
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ExecutionResult:
    """Result of a tool call execution."""
    success: bool
    message: str
    affected_elements: Optional[List[int]] = None
    
class ToolExecutor:
    """Executes structured tool calls without natural language ambiguity."""
    
    def __init__(self, schema_path: str = "schema/tool_calls_schema.json"):
        """Initialize with JSON schema for validation."""
        if Path(schema_path).exists():
            with open(schema_path, 'r') as f:
                self.schema = json.load(f)
        else:
            self.schema = None
    
    def validate_tool_calls(self, tool_calls_json: Dict[str, Any]) -> bool:
        """Validate tool calls against schema."""
        if not self.schema:
            print("Warning: No schema loaded, skipping validation")
            return True
            
        try:
            jsonschema.validate(tool_calls_json, self.schema)
            return True
        except jsonschema.ValidationError as e:
            print(f"Schema validation failed: {e}")
            return False
    
    def execute_tool_calls(self, tool_calls_json: Dict[str, Any]) -> List[ExecutionResult]:
        """
        Execute a list of tool calls with structured parameters.
        
        Args:
            tool_calls_json: Validated JSON containing tool_calls array
            
        Returns:
            List of execution results for each tool call
        """
        if not self.validate_tool_calls(tool_calls_json):
            return [ExecutionResult(False, "Schema validation failed")]
        
        results = []
        tool_calls = tool_calls_json.get("tool_calls", [])
        
        for i, tool_call in enumerate(tool_calls):
            function_name = tool_call["function_name"]
            parameters = tool_call["parameters"]
            
            try:
                result = self._execute_single_tool(function_name, parameters)
                results.append(result)
            except Exception as e:
                results.append(ExecutionResult(
                    False, 
                    f"Error executing {function_name}: {str(e)}"
                ))
        
        return results
    
    def _execute_single_tool(self, function_name: str, parameters: Dict[str, Any]) -> ExecutionResult:
        """Execute a single tool call."""
        volume_id = parameters["volume_identifier"]
        
        # Simulate tool execution with structured logging
        if function_name == "extrude_faces_in_volume":
            return self._extrude_faces_in_volume(volume_id, parameters)
        elif function_name == "scale_vertices_in_volume":
            return self._scale_vertices_in_volume(volume_id, parameters)
        elif function_name == "transform_vertices_in_volume":
            return self._transform_vertices_in_volume(volume_id, parameters)
        elif function_name == "apply_material_to_volume":
            return self._apply_material_to_volume(volume_id, parameters)
        elif function_name == "deform_volume_lattice":
            return self._deform_volume_lattice(volume_id, parameters)
        elif function_name == "subdivide_faces_in_volume":
            return self._subdivide_faces_in_volume(volume_id, parameters)
        elif function_name == "inset_faces_in_volume":
            return self._inset_faces_in_volume(volume_id, parameters)
        else:
            return ExecutionResult(False, f"Unknown function: {function_name}")
    
    def _extrude_faces_in_volume(self, volume_id: Dict[str, Any], params: Dict[str, Any]) -> ExecutionResult:
        """Execute extrude operation on faces within volume."""
        extrude_vector = params.get("extrude_vector", [0, 0, 1])
        
        # Simulate volume-based face selection and extrusion
        center = volume_id["center_xyz"]
        vol_type = volume_id["type"]
        
        # In real implementation, this would:
        # 1. Select faces within volume using VolumeSelector
        # 2. Apply bmesh.ops.extrude_face_region
        # 3. Translate extruded faces by extrude_vector
        
        return ExecutionResult(
            True,
            f"Extruded faces in {vol_type} volume at {center} by vector {extrude_vector}",
            affected_elements=[1, 4, 7, 12]  # Simulated face indices
        )
    
    def _scale_vertices_in_volume(self, volume_id: Dict[str, Any], params: Dict[str, Any]) -> ExecutionResult:
        """Execute scale operation on vertices within volume."""
        scale_factor = params.get("scale_factor", 1.0)
        
        center = volume_id["center_xyz"] 
        vol_type = volume_id["type"]
        
        return ExecutionResult(
            True,
            f"Scaled vertices in {vol_type} volume at {center} by factor {scale_factor}",
            affected_elements=[5, 8, 11, 15, 22]  # Simulated vertex indices
        )
    
    def _transform_vertices_in_volume(self, volume_id: Dict[str, Any], params: Dict[str, Any]) -> ExecutionResult:
        """Execute transformation matrix on vertices within volume."""
        transform_matrix = params.get("transform_matrix", [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
        
        center = volume_id["center_xyz"]
        vol_type = volume_id["type"]
        
        return ExecutionResult(
            True,
            f"Applied transformation to vertices in {vol_type} volume at {center}",
            affected_elements=[3, 6, 9, 13, 18, 21]  # Simulated vertex indices
        )
    
    def _apply_material_to_volume(self, volume_id: Dict[str, Any], params: Dict[str, Any]) -> ExecutionResult:
        """Apply material to faces within volume."""
        material_name = params.get("material_name", "DefaultMaterial")
        
        center = volume_id["center_xyz"]
        vol_type = volume_id["type"]
        
        return ExecutionResult(
            True,
            f"Applied material '{material_name}' to {vol_type} volume at {center}",
            affected_elements=[2, 5, 8, 14]  # Simulated face indices
        )
    
    def _deform_volume_lattice(self, volume_id: Dict[str, Any], params: Dict[str, Any]) -> ExecutionResult:
        """Apply lattice deformation to volume."""
        deformation_matrix = params.get("deformation_matrix", [[1,0,0],[0,1,0],[0,0,1]])
        
        center = volume_id["center_xyz"]
        vol_type = volume_id["type"]
        
        return ExecutionResult(
            True,
            f"Applied lattice deformation to {vol_type} volume at {center}",
            affected_elements=[1, 4, 7, 10, 16, 19]  # Simulated vertex indices
        )
    
    def _subdivide_faces_in_volume(self, volume_id: Dict[str, Any], params: Dict[str, Any]) -> ExecutionResult:
        """Subdivide faces within volume."""
        subdivision_level = params.get("subdivision_level", 1)
        
        center = volume_id["center_xyz"]
        vol_type = volume_id["type"]
        
        return ExecutionResult(
            True,
            f"Subdivided faces in {vol_type} volume at {center} (level {subdivision_level})",
            affected_elements=[3, 7, 11, 17, 23]  # Simulated face indices
        )
    
    def _inset_faces_in_volume(self, volume_id: Dict[str, Any], params: Dict[str, Any]) -> ExecutionResult:
        """Inset faces within volume."""
        inset_depth = params.get("inset_depth", 0.1)
        
        center = volume_id["center_xyz"]
        vol_type = volume_id["type"]
        
        return ExecutionResult(
            True,
            f"Inset faces in {vol_type} volume at {center} (depth {inset_depth})",
            affected_elements=[2, 6, 12, 18]  # Simulated face indices
        )
    
    def generate_execution_report(self, results: List[ExecutionResult]) -> str:
        """Generate a detailed execution report."""
        total_operations = len(results)
        successful_operations = sum(1 for r in results if r.success)
        failed_operations = total_operations - successful_operations
        
        report = f"""
=== Tool Execution Report ===
Total Operations: {total_operations}
Successful: {successful_operations}
Failed: {failed_operations}
Success Rate: {(successful_operations/total_operations)*100:.1f}%

=== Operation Details ===
"""
        
        for i, result in enumerate(results):
            status = "✓ SUCCESS" if result.success else "✗ FAILED"
            elements = f" (affected: {len(result.affected_elements)} elements)" if result.affected_elements else ""
            report += f"{i+1}. {status}: {result.message}{elements}\n"
        
        return report