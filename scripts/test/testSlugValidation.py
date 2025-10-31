#!/usr/bin/env python3
"""
Test slug validation in createModule.py
"""

import subprocess
import sys
from pathlib import Path

def test_slug_validation():
    """Test various slug inputs to verify validation"""
    project_root = Path.cwd()
    script_path = project_root / "scripts" / "createModule.py"
    
    # Test cases: (input, should_be_valid)
    test_cases = [
        ("My Filter", False, "contains space"),
        ("123Filter", False, "starts with number"),
        ("Filter-Delay", False, "contains hyphen"),
        ("Filter.Reverb", False, "contains dot"),
        ("MyFilter", True, "valid slug"),
        ("My_Filter", True, "valid with underscore"),
        ("Filter2", True, "valid with number"),
        ("", False, "empty slug"),
    ]
    
    print("🧪 Testing slug validation...")
    print("=" * 50)
    
    for slug_input, should_be_valid, description in test_cases:
        print(f"\nTesting: '{slug_input}' ({description})")
        
        # Create input that immediately exits after slug validation
        test_input = f"{slug_input}\n" + "\x03"  # Ctrl+C to exit
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                input=test_input,
                text=True,
                capture_output=True,
                timeout=5
            )
            
            output = result.stdout + result.stderr
            
            if should_be_valid:
                if "Module slug can only contain" in output or "Module slug should start with a letter" in output:
                    print(f"❌ Expected valid but got validation error")
                else:
                    print(f"✅ Correctly accepted valid slug")
            else:
                if "Module slug can only contain" in output or "Module slug should start with a letter" in output or "Module slug is required" in output:
                    print(f"✅ Correctly rejected invalid slug")
                else:
                    print(f"❌ Expected validation error but slug was accepted")
                    
        except subprocess.TimeoutExpired:
            print("⏰ Test timed out (expected for valid slugs)")
        except KeyboardInterrupt:
            print("⚠️  Test interrupted")
        except Exception as e:
            print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_slug_validation()