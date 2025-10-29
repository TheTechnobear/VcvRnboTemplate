#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
from pathlib import Path

def ensure_run_from_base_directory():
    """Ensure script is run from the project base directory"""
    current_dir = Path.cwd()
    
    # Check if we're in the base directory by looking for expected files/directories
    expected_items = ['scripts', 'templates', 'VcvModules', 'CMakePresets.json']
    
    if not all((current_dir / item).exists() for item in expected_items):
        print("❌ This script must be run from the project base directory.")
        print(f"Current directory: {current_dir}")
        print("Please run from the directory containing 'scripts', 'templates', 'VcvModules', etc.")
        print("Example: python3 helpers/removeAll.py")
        sys.exit(1)
    
    return current_dir

def find_all_modules():
    """Find all module .cpp files in VcvModules/src/"""
    project_root = Path.cwd()
    src_dir = project_root / "VcvModules" / "src"
    
    if not src_dir.exists():
        return []
    
    modules = []
    for cpp_file in src_dir.glob("*.cpp"):
        # Skip plugin.cpp
        if cpp_file.name != "plugin.cpp":
            module_name = cpp_file.stem
            modules.append(module_name)
    
    return sorted(modules)

def confirm_removal(modules, force=False):
    """Confirm with user before removing all modules"""
    if not modules:
        print("No modules found to remove.")
        return False
    
    if force:
        print(f"Force mode: Removing {len(modules)} modules without confirmation...")
        return True
    
    print(f"\n⚠️  WARNING: This will permanently remove ALL {len(modules)} modules!")
    print("\nModules to be removed:")
    for module in modules:
        print(f"  • {module}")
    
    print(f"\n❌ This action cannot be undone!")
    print("Each module will be removed using scripts/removeModule.py")
    
    response = input(f"\nAre you sure you want to remove ALL {len(modules)} modules? (yes/no): ").strip().lower()
    return response in ['yes', 'y']

def remove_module(module_name, force=False):
    """Remove a single module using removeModule.py"""
    project_root = Path.cwd()
    remove_script = project_root / "scripts" / "removeModule.py"
    
    if not remove_script.exists():
        print(f"❌ {remove_script} not found!")
        return False
    
    # Build command
    cmd = [sys.executable, str(remove_script)]
    if force:
        cmd.append("--force")
    cmd.append(module_name)
    
    try:
        print(f"\nRemoving module: {module_name}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error removing module {module_name}:")
        print(e.stdout)
        print(e.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error removing module {module_name}: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Remove all modules from the VCV Rack RNBO plugin')
    parser.add_argument('--force', '-f', action='store_true', 
                       help='Force removal without confirmation')
    
    args = parser.parse_args()
    force = args.force
    
    try:
        # Ensure we're running from the correct directory
        project_root = ensure_run_from_base_directory()
        print(f"Running from project directory: {project_root}")
        
        # Find all modules
        modules = find_all_modules()
        
        if not modules:
            print("No modules found to remove.")
            return
        
        # Confirm removal with user
        if not confirm_removal(modules, force):
            print("Operation cancelled.")
            return
        
        print(f"\nRemoving {len(modules)} modules...")
        
        # Remove each module
        success_count = 0
        failed_modules = []
        
        for module in modules:
            if remove_module(module, force=True):  # Use force for individual removals to avoid double confirmation
                success_count += 1
            else:
                failed_modules.append(module)
        
        # Summary
        print(f"\n{'='*50}")
        print(f"Removal Summary:")
        print(f"  Successfully removed: {success_count} modules")
        if failed_modules:
            print(f"  Failed to remove: {len(failed_modules)} modules")
            print(f"  Failed modules: {', '.join(failed_modules)}")
        
        if success_count == len(modules):
            print(f"\n✅ All {len(modules)} modules removed successfully!")
        elif success_count > 0:
            print(f"\n⚠️  {success_count} modules removed, but {len(failed_modules)} failed.")
        else:
            print(f"\n❌ Failed to remove any modules.")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"❌ {e}")

if __name__ == "__main__":
    main()