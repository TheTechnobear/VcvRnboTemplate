#!/usr/bin/env python3

import os
import sys
import argparse
import shutil
import json
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
        print("Example: python3 scripts/removeModule.py ModuleName")
        sys.exit(1)
    
    return current_dir

def check_plugin_exists():
    """Check that createPlugin.py has been run by looking for plugin.json and plugin-mm.json"""
    project_root = Path.cwd()
    vcv_plugin_json = project_root / "VcvModules" / "plugin.json"
    mm_plugin_json = project_root / "plugin-mm.json"
    
    if not vcv_plugin_json.exists():
        print("Error: VcvModules/plugin.json not found.")
        print("Please run 'python3 scripts/createPlugin.py' first to create the plugin.")
        sys.exit(1)
    
    if not mm_plugin_json.exists():
        print("Error: plugin-mm.json not found.")
        print("Please run 'python3 scripts/createPlugin.py' first to create the plugin.")
        sys.exit(1)
    
    return vcv_plugin_json, mm_plugin_json

def check_module_exists(module_name):
    """Check if module exists and list what will be deleted"""
    project_root = Path.cwd()
    
    files_to_delete = []
    dirs_to_delete = []
    
    # Check for module source file
    module_cpp = project_root / "VcvModules" / "src" / f"{module_name}.cpp"
    if module_cpp.exists():
        files_to_delete.append(module_cpp)
    
    # Check for RNBO directory
    rnbo_dir = project_root / "VcvModules" / "src" / f"{module_name}-rnbo"
    if rnbo_dir.exists():
        dirs_to_delete.append(rnbo_dir)
    
    if not files_to_delete and not dirs_to_delete:
        print(f"Error: Module '{module_name}' not found.")
        print(f"Expected files:")
        print(f"  - {module_cpp}")
        print(f"  - {rnbo_dir}/")
        return None, None
    
    return files_to_delete, dirs_to_delete

def confirm_deletion(module_name, files_to_delete, dirs_to_delete, force=False):
    """Confirm with user before deletion"""
    if force:
        print(f"Force mode: Removing module '{module_name}' without confirmation...")
        return True
    
    print(f"\n⚠️  WARNING: This will permanently delete module '{module_name}'!")
    print("\nThe following files and directories will be deleted:")
    
    for file_path in files_to_delete:
        print(f"  📄 {file_path}")
    
    for dir_path in dirs_to_delete:
        print(f"  📁 {dir_path}/ (and all contents)")
    
    print("\nThe following will be updated:")
    print("  📝 VcvModules/src/plugin.hpp (remove model declaration)")
    print("  📝 VcvModules/src/plugin.cpp (remove model registration)")
    print("  📝 VcvModules/Makefile (remove from SOURCES)")
    print("  📝 CMakeLists.txt (remove from target_sources)")
    print("  📝 VcvModules/plugin.json (remove module definition)")
    print("  📝 plugin-mm.json (remove module definition)")
    
    print(f"\n❌ This action cannot be undone!")
    
    response = input(f"\nAre you sure you want to remove module '{module_name}'? (yes/no): ").strip().lower()
    return response in ['yes', 'y']

def remove_files_and_dirs(files_to_delete, dirs_to_delete):
    """Remove the module files and directories"""
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"✓ Deleted file: {file_path}")
        except Exception as e:
            print(f"✗ Error deleting file {file_path}: {e}")
    
    for dir_path in dirs_to_delete:
        try:
            shutil.rmtree(dir_path)
            print(f"✓ Deleted directory: {dir_path}")
        except Exception as e:
            print(f"✗ Error deleting directory {dir_path}: {e}")

def remove_from_plugin_hpp(module_name):
    """Remove extern Model* modelMOD; declaration from plugin.hpp"""
    project_root = Path.cwd()
    plugin_hpp_path = project_root / "VcvModules" / "src" / "plugin.hpp"
    
    if not plugin_hpp_path.exists():
        print(f"Warning: {plugin_hpp_path} not found! Skipping plugin.hpp update.")
        return False
    
    # Read current content
    with open(plugin_hpp_path, 'r') as f:
        content = f.read()
    
    # Find and remove the model declaration
    model_declaration = f"extern Model* model{module_name};"
    if model_declaration not in content:
        print(f"✓ Model declaration for {module_name} not found in plugin.hpp (already removed)")
        return True
    
    # Remove the declaration line
    lines = content.split('\n')
    updated_lines = [line for line in lines if line.strip() != model_declaration]
    
    # Write back to file
    with open(plugin_hpp_path, 'w') as f:
        f.write('\n'.join(updated_lines))
    
    print(f"✓ Removed model declaration from plugin.hpp: {model_declaration}")
    return True

def remove_from_plugin_cpp(module_name):
    """Remove p->addModel(modelMOD); from plugin.cpp"""
    project_root = Path.cwd()
    plugin_cpp_path = project_root / "VcvModules" / "src" / "plugin.cpp"
    
    if not plugin_cpp_path.exists():
        print(f"Warning: {plugin_cpp_path} not found! Skipping plugin.cpp update.")
        return False
    
    # Read current content
    with open(plugin_cpp_path, 'r') as f:
        content = f.read()
    
    # Find and remove the addModel call
    model_add = f"p->addModel(model{module_name});"
    model_add_with_indent = f"\tp->addModel(model{module_name});"
    
    if model_add not in content and model_add_with_indent not in content:
        print(f"✓ Model {module_name} not found in plugin.cpp (already removed)")
        return True
    
    # Remove the addModel line (try both with and without tab)
    lines = content.split('\n')
    updated_lines = [line for line in lines if line.strip() != model_add and line != model_add_with_indent]
    
    # Write back to file
    with open(plugin_cpp_path, 'w') as f:
        f.write('\n'.join(updated_lines))
    
    print(f"✓ Removed model from plugin.cpp: {model_add}")
    return True

def remove_from_vcv_makefile(module_name):
    """Remove module source file from VCV Makefile"""
    project_root = Path.cwd()
    makefile_path = project_root / "VcvModules" / "Makefile"
    
    if not makefile_path.exists():
        print(f"Warning: {makefile_path} not found! Skipping Makefile update.")
        return False
    
    # Read current content
    with open(makefile_path, 'r') as f:
        content = f.read()
    
    # Find and remove the module source
    module_source = f"src/{module_name}.cpp"
    module_source_with_backslash = f"{module_source} \\"
    
    if module_source not in content:
        print(f"✓ Module {module_name} not found in VCV Makefile (already removed)")
        return True
    
    # Remove the source line
    lines = content.split('\n')
    updated_lines = []
    for line in lines:
        if module_source_with_backslash in line or line.strip() == module_source:
            continue
        updated_lines.append(line)
    
    # Write back to file
    with open(makefile_path, 'w') as f:
        f.write('\n'.join(updated_lines))
    
    print(f"✓ Removed {module_source} from VCV Makefile")
    return True

def remove_from_metamodule_cmake(module_name):
    """Remove module source file from MetaModule CMakeLists.txt"""
    project_root = Path.cwd()
    cmake_path = project_root / "CMakeLists.txt"
    
    if not cmake_path.exists():
        print(f"Warning: {cmake_path} not found! Skipping CMakeLists.txt update.")
        return False
    
    # Read current content
    with open(cmake_path, 'r') as f:
        content = f.read()
    
    # Find and remove the module source
    module_source = f"${{SOURCE_DIR}}/src/{module_name}.cpp"
    
    if module_source not in content:
        print(f"✓ Module {module_name} not found in MetaModule CMakeLists.txt (already removed)")
        return True
    
    # Remove the source line
    lines = content.split('\n')
    updated_lines = []
    for line in lines:
        if module_source in line.strip():
            continue
        updated_lines.append(line)
    
    # Write back to file
    with open(cmake_path, 'w') as f:
        f.write('\n'.join(updated_lines))
    
    print(f"✓ Removed {module_source} from MetaModule CMakeLists.txt")
    return True

def remove_from_plugin_json(module_name):
    """Remove module definition from plugin.json"""
    project_root = Path.cwd()
    plugin_json_path = project_root / "VcvModules" / "plugin.json"
    
    if not plugin_json_path.exists():
        print(f"Warning: {plugin_json_path} not found! Skipping plugin.json update.")
        return False
    
    try:
        # Read current plugin.json
        with open(plugin_json_path, 'r') as f:
            plugin_data = json.load(f)
        
        # Find and remove the module
        modules = plugin_data.get('modules', [])
        original_count = len(modules)
        
        # Remove modules that match the module name (check module name and slug)
        updated_modules = []
        removed_module = None
        
        for module in modules:
            module_slug = module.get('slug', '')
            module_name_field = module.get('name', '')
            
            if module_slug == module_name or module_name_field == module_name:
                removed_module = module
                continue
            updated_modules.append(module)
        
        if len(updated_modules) == original_count:
            print(f"✓ Module {module_name} not found in plugin.json (already removed)")
            return True
        
        # Update the modules array
        plugin_data['modules'] = updated_modules
        
        # Write back to file with proper formatting
        with open(plugin_json_path, 'w') as f:
            json.dump(plugin_data, f, indent=2)
        
        if removed_module:
            print(f"✓ Removed module from plugin.json:")
            print(f"  Slug: {removed_module.get('slug', 'N/A')}")
            print(f"  Name: {removed_module.get('name', 'N/A')}")
        else:
            print(f"✓ Removed module {module_name} from plugin.json")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {plugin_json_path}: {e}")
        return False
    except Exception as e:
        print(f"Error updating plugin.json: {e}")
        return False

def remove_from_plugin_mm_json(module_name):
    """Remove module definition from plugin-mm.json"""
    project_root = Path.cwd()
    plugin_mm_json_path = project_root / "plugin-mm.json"
    
    if not plugin_mm_json_path.exists():
        print(f"Warning: {plugin_mm_json_path} not found! Skipping plugin-mm.json update.")
        return False
    
    try:
        # Read current plugin-mm.json
        with open(plugin_mm_json_path, 'r') as f:
            plugin_data = json.load(f)
        
        # Find and remove the module
        modules = plugin_data.get('MetaModuleIncludedModules', [])
        original_count = len(modules)
        
        # Remove modules that match the module name (check module name and slug)
        updated_modules = []
        removed_module = None
        
        for module in modules:
            module_slug = module.get('slug', '')
            module_name_field = module.get('name', '')
            
            if module_slug == module_name or module_name_field == module_name:
                removed_module = module
                continue
            updated_modules.append(module)
        
        if len(updated_modules) == original_count:
            print(f"✓ Module {module_name} not found in plugin-mm.json (already removed)")
            return True
        
        # Update the modules array
        plugin_data['MetaModuleIncludedModules'] = updated_modules
        
        # Write back to file with proper formatting
        with open(plugin_mm_json_path, 'w') as f:
            json.dump(plugin_data, f, indent=2)
        
        if removed_module:
            print(f"✓ Removed module from plugin-mm.json:")
            print(f"  Slug: {removed_module.get('slug', 'N/A')}")
            print(f"  Name: {removed_module.get('name', 'N/A')}")
        else:
            print(f"✓ Removed module {module_name} from plugin-mm.json")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {plugin_mm_json_path}: {e}")
        return False
    except Exception as e:
        print(f"Error updating plugin-mm.json: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Remove a module from the VCV Rack RNBO plugin')
    parser.add_argument('module_name', help='Name of the module to remove')
    parser.add_argument('--force', '-f', action='store_true', 
                       help='Force removal without confirmation')
    
    args = parser.parse_args()
    module_name = args.module_name
    force = args.force
    
    try:
        # Ensure we're running from the correct directory
        project_root = ensure_run_from_base_directory()
        print(f"Running from project directory: {project_root}")
        
        # Check that createPlugin.py has been run
        check_plugin_exists()
        
        # Check if module exists and what will be deleted
        files_to_delete, dirs_to_delete = check_module_exists(module_name)
        if files_to_delete is None:
            sys.exit(1)
        
        # Confirm deletion with user
        if not confirm_deletion(module_name, files_to_delete, dirs_to_delete, force):
            print("Module removal cancelled.")
            sys.exit(0)
        
        print(f"\nRemoving module '{module_name}'...")
        
        # Remove files and directories
        remove_files_and_dirs(files_to_delete, dirs_to_delete)
        
        # Update build system files
        remove_from_plugin_hpp(module_name)
        remove_from_plugin_cpp(module_name)
        remove_from_vcv_makefile(module_name)
        remove_from_metamodule_cmake(module_name)
        
        # Remove from plugin.json
        remove_from_plugin_json(module_name)
        
        # Remove from plugin-mm.json
        remove_from_plugin_mm_json(module_name)
        
        print(f"\n✓ Module '{module_name}' removed successfully!")
        print("\nNext steps:")
        print("1. Build and test your plugin to ensure everything still works")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()