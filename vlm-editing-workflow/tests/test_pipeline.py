"""
Test framework for the corrected 3D pipeline architecture.
Validates structured approach without natural language dependencies.
"""

import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from tool_executor import ToolExecutor, ExecutionResult

class PipelineTestFramework:
    """Test framework implementing the 'build receiver, simulate sender' approach."""
    
    def __init__(self):
        self.executor = ToolExecutor()
        self.test_cases = []
        self.results = []
    
    def add_test_case(self, name: str, tool_calls_json: dict, expected_success: bool = True):
        """Add a test case to the framework."""
        self.test_cases.append({
            "name": name,
            "input": tool_calls_json,
            "expected_success": expected_success
        })
    
    def run_all_tests(self) -> bool:
        """Run all test cases and return overall success."""
        print("=== 3D Pipeline Test Framework ===")
        print("Testing corrected architecture with structured tool calls\n")
        
        total_tests = len(self.test_cases)
        passed_tests = 0
        
        for i, test_case in enumerate(self.test_cases):
            print(f"Test {i+1}/{total_tests}: {test_case['name']}")
            
            try:
                results = self.executor.execute_tool_calls(test_case['input'])
                
                # Check if any results failed when success was expected
                any_failed = any(not r.success for r in results)
                test_passed = not any_failed if test_case['expected_success'] else any_failed
                
                if test_passed:
                    print("  ✓ PASSED")
                    passed_tests += 1
                else:
                    print("  ✗ FAILED")
                    for result in results:
                        if not result.success:
                            print(f"    Error: {result.message}")
                
                self.results.extend(results)
                
            except Exception as e:
                print(f"  ✗ EXCEPTION: {e}")
            
            print()
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"Overall Result: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
        
        return passed_tests == total_tests
    
    def generate_detailed_report(self) -> str:
        """Generate comprehensive test report."""
        return self.executor.generate_execution_report(self.results)

def create_test_cases():
    """Create test cases that demonstrate the corrected architecture."""
    
    framework = PipelineTestFramework()
    
    # Test Case 1: Basic box volume extrusion (CORRECTED APPROACH)
    framework.add_test_case(
        "Basic Box Volume Extrusion",
        {
            "tool_calls": [
                {
                    "function_name": "extrude_faces_in_volume",
                    "parameters": {
                        "volume_identifier": {
                            "type": "box",
                            "center_xyz": [15.7, -3.2, 8.5],
                            "dimensions_xyz": [4.5, 2.1, 3.0],
                            "rotation_quaternion_wxyz": [0.966, 0.0, 0.259, 0.0]
                        },
                        "extrude_vector": [0.0, 0.0, 0.5]
                    }
                }
            ]
        }
    )
    
    # Test Case 2: Sphere volume with material application
    framework.add_test_case(
        "Sphere Volume Material Application",
        {
            "tool_calls": [
                {
                    "function_name": "apply_material_to_volume",
                    "parameters": {
                        "volume_identifier": {
                            "type": "sphere",
                            "center_xyz": [0.0, 0.0, 0.0],
                            "radius": 5.0
                        },
                        "material_name": "Armored_Steel_Plate"
                    }
                }
            ]
        }
    )
    
    # Test Case 3: Multiple operations in sequence (demonstrates structured approach)
    framework.add_test_case(
        "Multi-Operation Sequence",
        {
            "tool_calls": [
                {
                    "function_name": "subdivide_faces_in_volume",
                    "parameters": {
                        "volume_identifier": {
                            "type": "cylinder",
                            "center_xyz": [10.0, 5.0, 0.0],
                            "dimensions_xyz": [3.0, 3.0, 8.0]
                        },
                        "subdivision_level": 2
                    }
                },
                {
                    "function_name": "scale_vertices_in_volume", 
                    "parameters": {
                        "volume_identifier": {
                            "type": "cylinder",
                            "center_xyz": [10.0, 5.0, 0.0],
                            "dimensions_xyz": [3.0, 3.0, 8.0]
                        },
                        "scale_factor": 1.2
                    }
                }
            ]
        }
    )
    
    # Test Case 4: Complex transformation with rotation
    framework.add_test_case(
        "Complex Rotated Volume Operation",
        {
            "tool_calls": [
                {
                    "function_name": "transform_vertices_in_volume",
                    "parameters": {
                        "volume_identifier": {
                            "type": "box",
                            "center_xyz": [-5.0, 10.0, 15.0],
                            "dimensions_xyz": [6.0, 4.0, 2.0],
                            "rotation_quaternion_wxyz": [0.707, 0.707, 0.0, 0.0]
                        },
                        "transform_matrix": [
                            [1.1, 0.0, 0.0, 0.0],
                            [0.0, 1.0, 0.1, 0.0], 
                            [0.0, 0.0, 1.1, 0.0],
                            [0.0, 0.0, 0.0, 1.0]
                        ]
                    }
                }
            ]
        }
    )
    
    # Test Case 5: Invalid schema test (should fail validation)
    framework.add_test_case(
        "Invalid Schema (Missing Required Fields)",
        {
            "tool_calls": [
                {
                    "function_name": "extrude_faces_in_volume",
                    "parameters": {
                        "volume_identifier": {
                            "type": "box",
                            # Missing center_xyz - should fail validation
                            "dimensions_xyz": [2.0, 2.0, 2.0]
                        }
                    }
                }
            ]
        },
        expected_success=False
    )
    
    return framework

def demonstrate_flawed_vs_corrected():
    """Demonstrate the difference between flawed and corrected approaches."""
    
    print("=== ARCHITECTURAL COMPARISON ===\n")
    
    print("❌ FLAWED APPROACH (from original critique):")
    flawed_example = {
        "suggested_action": "Reshape the volume in the upper-left; apply 'Armored Steel Plate' texture."
    }
    print(json.dumps(flawed_example, indent=2))
    print("Problems:")
    print("  - Natural language ambiguity")
    print("  - Requires complex NLP parsing")
    print("  - 'Reshape' is undefined")
    print("  - 'upper-left' is spatially imprecise")
    print("  - Brittle and error-prone")
    
    print("\n" + "="*50 + "\n")
    
    print("✅ CORRECTED APPROACH (implemented here):")
    corrected_example = {
        "tool_calls": [
            {
                "function_name": "extrude_faces_in_volume",
                "parameters": {
                    "volume_identifier": {
                        "type": "box",
                        "center_xyz": [15.7, -3.2, 8.5],
                        "dimensions_xyz": [4.5, 2.1, 3.0],
                        "rotation_quaternion_wxyz": [0.966, 0.0, 0.259, 0.0]
                    },
                    "extrude_vector": [0.0, 0.0, 0.5]
                }
            },
            {
                "function_name": "apply_material_to_volume",
                "parameters": {
                    "volume_identifier": {
                        "type": "box", 
                        "center_xyz": [15.7, -3.2, 8.5],
                        "dimensions_xyz": [4.5, 2.1, 3.0]
                    },
                    "material_name": "Armored_Steel_Plate"
                }
            }
        ]
    }
    print(json.dumps(corrected_example, indent=2))
    print("Advantages:")
    print("  - Precise 3D spatial coordinates")
    print("  - Structured function calls")
    print("  - No NLP parsing required") 
    print("  - Mathematically exact operations")
    print("  - Robust and deterministic")
    print("  - JSON schema validation")

if __name__ == "__main__":
    # Demonstrate architectural differences
    demonstrate_flawed_vs_corrected()
    
    print("\n" + "="*60 + "\n")
    
    # Run comprehensive tests
    framework = create_test_cases()
    all_passed = framework.run_all_tests()
    
    print("\n" + "="*40 + "\n")
    print(framework.generate_detailed_report())
    
    if all_passed:
        print("\n🎉 All tests passed! Architecture is ready for implementation.")
    else:
        print("\n⚠️  Some tests failed. Review implementation before proceeding.")