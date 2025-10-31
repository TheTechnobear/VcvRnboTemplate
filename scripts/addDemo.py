#!/usr/bin/env python3
"""
VCV Rack RNBO Template Demo Script

This script creates a Demo module using createModule.py and then copies
the demo RNBO files to provide a working example module.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def ensure_run_from_base_directory():
    """Ensure script is run from the project base directory"""
    current_dir = Path.cwd()
    
    # Check if we're in the base directory by looking for expected files/directories
    expected_items = ['scripts', 'templates', 'VcvModules', 'CMakePresets.json']
    
    if not all((current_dir / item).exists() for item in expected_items):
        print("Error: This script must be run from the project base directory.")
        print(f"Current directory: {current_dir}")
        print("Please run from the directory containing 'scripts', 'templates', 'VcvModules', etc.")
        print("Example: python3 scripts/addDemo.py")
        sys.exit(1)
    
    return current_dir

def check_plugin_exists():
    """Check if plugin configuration files exist"""
    project_root = Path.cwd()
    plugin_json = project_root / "VcvModules" / "plugin.json"
    plugin_mm_json = project_root / "plugin-mm.json"
    
    if not plugin_json.exists() or not plugin_mm_json.exists():
        print("❌ Plugin configuration files not found!")
        print("You need to create a plugin first using createPlugin.py")
        print("\nRun: python3 scripts/createPlugin.py")
        return False
    
    return True

def create_demo_module():
    """Create Demo module using createModule.py"""
    project_root = Path.cwd()
    create_module_script = project_root / "scripts" / "createModule.py"
    
    if not create_module_script.exists():
        print(f"❌ {create_module_script} not found!")
        return False
    
    print("🔧 Creating Demo module...")
    
    # Module input for Demo module - includes panel selection (1 = Blank10U.svg)
    # Input format: slug, name, panel_selection, description, tags
    demo_input = """Demo
Demo
1
Demo RNBO module for testing
audio, demo
"""
    
    try:
        result = subprocess.run(
            [sys.executable, str(create_module_script)],
            input=demo_input,
            text=True,
            capture_output=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ Demo module created successfully")
            print("Output:")
            print(result.stdout)
            return True
        else:
            print(f"❌ Error creating Demo module:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ createModule.py timed out")
        return False
    except Exception as e:
        print(f"❌ Error running createModule.py: {e}")
        return False

def copy_demo_rnbo_files():
    """Copy demo RNBO files to the Demo module directory"""
    project_root = Path.cwd()
    
    # Source: demo template RNBO directory
    demo_template_dir = project_root / "templates" / "vcv" / "demo" / "Demo-rnbo"
    
    # Target: created Demo module RNBO directory
    demo_target_dir = project_root / "VcvModules" / "src" / "Demo-rnbo"
    
    if not demo_template_dir.exists():
        print(f"❌ Demo template directory not found: {demo_template_dir}")
        return False
    
    if not demo_target_dir.exists():
        print(f"❌ Demo module directory not found: {demo_target_dir}")
        print("The Demo module should have been created by createModule.py")
        return False
    
    print("📁 Copying demo RNBO files...")
    
    try:
        # Copy all files from demo template to target directory
        for file_path in demo_template_dir.iterdir():
            if file_path.is_file():
                target_file = demo_target_dir / file_path.name
                shutil.copy2(file_path, target_file)
                print(f"✓ Copied {file_path.name}")
        
        print("✅ Demo RNBO files copied successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error copying demo files: {e}")
        return False

def main():
    """Main function"""
    try:
        # Ensure we're running from the correct directory
        project_root = ensure_run_from_base_directory()
        print(f"Running from project directory: {project_root}")
        
        print("🎯 VCV Rack RNBO Template - Add Demo Module")
        print("=" * 50)
        
        # Check if plugin exists
        if not check_plugin_exists():
            return 1
        
        # Create Demo module
        if not create_demo_module():
            print("❌ Failed to create Demo module")
            return 1
        
        # Copy demo RNBO files
        if not copy_demo_rnbo_files():
            print("❌ Failed to copy demo RNBO files")
            return 1
        
        print("\n🎉 Demo module added successfully!")
        print("\nNext steps:")
        print("1. Build your plugin: cd VcvModules && make")
        print("2. Test the Demo module in VCV Rack")
        print("3. Use the Demo module as a reference for creating your own modules")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())