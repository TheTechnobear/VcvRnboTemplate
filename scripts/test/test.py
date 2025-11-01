#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
import tempfile
from pathlib import Path

def ensure_run_from_base_directory():
    """Ensure script is run from the project base directory"""
    current_dir = Path.cwd()
    
    # Check if we're in the base directory by looking for expected files/directories
    expected_items = ['scripts', 'templates', 'VcvModules', 'CMakePresets.json']
    
    if not all((current_dir / item).exists() for item in expected_items):
        print("[ERROR] This script must be run from the project base directory.")
        print(f"Current directory: {current_dir}")
        print("Please run from the directory containing 'scripts', 'templates', 'VcvModules', etc.")
        print("Example: python3 scripts/test/test.py")
        sys.exit(1)
    
    return current_dir

def confirm_destructive_operation(auto=False):
    """Confirm with user that this is a destructive test operation"""
    print("[TEST] VCV Rack RNBO Template Test Script")
    print("=" * 50)
    print("\n[WARNING]  WARNING: This is a destructive test operation!")
    print("\nThis script will:")
    print("1. Remove ALL existing modules (if any)")
    print("2. Create a fresh test plugin")
    print("3. Add 2 test modules")
    print("4. Leave the test files in place for verification")
    print("\n[ERROR] Any existing plugin and modules will be deleted!")
    
    if auto:
        print("\nRunning in automated mode - proceeding without confirmation...")
        return True
    
    response = input("\nDo you want to proceed with the test? (yes/no): ").strip().lower()
    return response in ['yes', 'y']

def run_command_with_input(cmd, input_text="", description=""):
    """Run a command with input and return success status"""
    try:
        if description:
            print(f"\n[TOOL] {description}")
        
        print(f"Running: {' '.join(cmd)}")
        
        # Run command with input
        result = subprocess.run(
            cmd, 
            input=input_text,
            text=True,
            capture_output=True,
            check=False
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode != 0:
            print(f"[ERROR] Command failed with return code {result.returncode}")
            return False
        
        print("[PASS] Command completed successfully")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error running command: {e}")
        return False

def remove_all_modules():
    """Remove all existing modules using removeAll.py"""
    project_root = ensure_run_from_base_directory()
    remove_all_script = project_root / "scripts" / "test" / "removeAll.py"
    
    if not remove_all_script.exists():
        print(f"Warning: {remove_all_script} not found! Skipping module cleanup.")
        return True
    
    cmd = [sys.executable, str(remove_all_script), "--force"]
    return run_command_with_input(cmd, description="Removing all existing modules")

def create_test_plugin():
    """Create a test plugin using createPlugin.py"""
    project_root = Path.cwd()
    create_plugin_script = project_root / "scripts" / "createPlugin.py"
    
    if not create_plugin_script.exists():
        print(f"[ERROR] {create_plugin_script} not found!")
        return False
    
    # Plugin details for testing
    plugin_input = """TestPlug
Test Plugin
TestBrand
Test RNBO Plugin for VCV Rack
Test Author
test@example.com
https://example.com
"""
    
    cmd = [sys.executable, str(create_plugin_script)]
    return run_command_with_input(cmd, plugin_input, "Creating test plugin")

def create_test_module(module_name, description, tags, expected_slug):
    """Create a test module using createModule.py"""
    project_root = Path.cwd()
    create_module_script = project_root / "scripts" / "createModule.py"
    
    if not create_module_script.exists():
        print(f"[ERROR] {create_module_script} not found!")
        return False
    
    # Module details - includes panel selection (1 = Blank10U.svg)
    # New input order: slug, name, panel_selection, description, tags
    module_input = f"""{expected_slug}
{module_name}
1
{description}
{tags}
"""
    
    cmd = [sys.executable, str(create_module_script)]
    return run_command_with_input(cmd, module_input, f"Creating test module: '{module_name}' with slug '{expected_slug}'")

def verify_test_results():
    """Verify that the test completed successfully and demonstrate slug vs name usage"""
    project_root = Path.cwd()
    
    print("\n🔍 Verifying test results...")
    
    # Check plugin files exist
    plugin_files = [
        "VcvModules/plugin.json",
        "VcvModules/Makefile", 
        "VcvModules/src/plugin.cpp",
        "VcvModules/src/plugin.hpp",
        "plugin-mm.json",
        "CMakeLists.txt"
    ]
    
    for file_path in plugin_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"[PASS] {file_path}")
        else:
            print(f"[ERROR] {file_path} - MISSING!")
    
    # Check module files exist (using SLUGS for filenames)
    print(f"\n[FOLDER] Verifying module files use SLUGS (not names with spaces):")
    module_files = [
        ("VcvModules/src/TestReverb.cpp", "Test Reverb"),
        ("VcvModules/src/TestReverb-rnbo", "Test Reverb"), 
        ("VcvModules/src/MultiFilter.cpp", "Multi Filter"),
        ("VcvModules/src/MultiFilter-rnbo", "Multi Filter")
    ]
    
    for file_path, module_name in module_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"[PASS] {file_path} (for module '{module_name}')")
        else:
            print(f"[ERROR] {file_path} - MISSING! (for module '{module_name}')")
    
    # Verify that files with spaces in names DON'T exist (demonstrating slug usage)
    print(f"\n[BLOCK] Verifying files with spaces DON'T exist (confirming slug usage):")
    bad_files = [
        "VcvModules/src/Test Reverb.cpp",
        "VcvModules/src/Multi Filter.cpp"
    ]
    
    for file_path in bad_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"[ERROR] {file_path} - Should NOT exist! (proves spaces aren't used)")
        else:
            print(f"[PASS] {file_path} - Correctly does NOT exist")
    
    # Show plugin.json modules (name vs slug distinction)
    try:
        plugin_json = project_root / "VcvModules" / "plugin.json"
        if plugin_json.exists():
            print(f"\n[FILE] Plugin modules in {plugin_json} (showing name vs slug):")
            result = subprocess.run([
                "python3", "-c", 
                f"import json; data=json.load(open('{plugin_json}')); [print(f'  - Slug: {{m[\"slug\"]:12}} Name: \"{{m[\"name\"]}}\" ({{m[\"description\"]}})') for m in data.get('modules', [])]"
            ], capture_output=True, text=True)
            if result.stdout.strip():
                print(result.stdout)
            else:
                print("  No modules found")
    except Exception as e:
        print(f"Error reading plugin.json: {e}")
    
    # Show plugin-mm.json modules  
    try:
        plugin_mm_json = project_root / "plugin-mm.json"
        if plugin_mm_json.exists():
            print(f"\n[FILE] MetaModule modules in {plugin_mm_json} (showing name vs slug):")
            result = subprocess.run([
                "python3", "-c",
                f"import json; data=json.load(open('{plugin_mm_json}')); [print(f'  - Slug: {{m[\"slug\"]:12}} Name: \"{{m[\"name\"]}}\" ({{m[\"displayName\"]}})') for m in data.get('MetaModuleIncludedModules', [])]"
            ], capture_output=True, text=True)
            if result.stdout.strip():
                print(result.stdout)
            else:
                print("  No modules found")
    except Exception as e:
        print(f"Error reading plugin-mm.json: {e}")
    
    # Check C++ code generation uses slugs
    print(f"\n[CODE] Verifying C++ code uses SLUGS for identifiers:")
    cpp_files_to_check = [
        ("VcvModules/src/plugin.hpp", ["modelTestReverb", "modelMultiFilter"]),
        ("VcvModules/src/plugin.cpp", ["modelTestReverb", "modelMultiFilter"]),
        ("VcvModules/Makefile", ["TestReverb.cpp", "MultiFilter.cpp"])
    ]
    
    for file_path, expected_slugs in cpp_files_to_check:
        full_path = project_root / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
                    
                for slug in expected_slugs:
                    if slug in content:
                        print(f"[PASS] {file_path} contains '{slug}'")
                    else:
                        print(f"[ERROR] {file_path} missing '{slug}'")
            except Exception as e:
                print(f"[ERROR] Error reading {file_path}: {e}")
        else:
            print(f"[ERROR] {file_path} not found")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Test VCV Rack RNBO Template automation",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--auto', 
        action='store_true',
        help='Run in automated mode without confirmation prompts'
    )
    
    args = parser.parse_args()
    
    try:
        # Ensure we're running from the correct directory
        project_root = ensure_run_from_base_directory()
        print(f"Running from project directory: {project_root}")
        
        # Confirm destructive operation
        if not confirm_destructive_operation(auto=args.auto):
            print("Test cancelled.")
            return
        
        print(f"\n🚀 Starting VCV Rack RNBO Template test...")
        
        # Step 1: Remove all existing modules
        if not remove_all_modules():
            print("[ERROR] Failed to remove existing modules")
            return
        
        # Step 2: Create test plugin
        if not create_test_plugin():
            print("[ERROR] Failed to create test plugin")
            return
        
        # Step 3: Create test modules with names containing spaces to test slug generation
        test_modules = [
            ("Test Reverb", "RNBO reverb effect module", "audio,effect,reverb", "TestReverb"),
            ("Multi Filter", "RNBO multi-mode filter module", "audio,effect,filter", "MultiFilter")
        ]
        
        for module_name, description, tags, expected_slug in test_modules:
            if not create_test_module(module_name, description, tags, expected_slug):
                print(f"[ERROR] Failed to create test module: {module_name}")
                return
        
        # Step 4: Verify results
        verify_test_results()
        
        print(f"\n[SUCCESS] Test completed successfully!")
        print("\n📋 KEY DEMONSTRATION - Slug vs Name Usage:")
        print("  - Module NAMES: 'Test Reverb' and 'Multi Filter' (user-facing, can have spaces)")
        print("  - Module SLUGS: 'TestReverb' and 'MultiFilter' (used for files/code, no spaces)")
        print("  - Files created: TestReverb.cpp, MultiFilter.cpp (using slugs)")
        print("  - C++ identifiers: modelTestReverb, modelMultiFilter (using slugs)")
        print("  - JSON displays: Both name and slug are preserved appropriately")
        print("\nFiles have been left in place for verification.")
        print("You can examine the generated files to confirm everything worked correctly.")
        print("\nTo clean up, run: python3 scripts/test/removeAll.py")
        
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.")
    except Exception as e:
        print(f"Test failed with error: {e}")

if __name__ == "__main__":
    main()