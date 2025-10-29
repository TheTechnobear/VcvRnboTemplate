#!/usr/bin/env python3

import os
import json
import sys
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
        print("Example: python3 scripts/createModule.py")
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
    
    print("✓ Found existing plugin configuration files")
    return vcv_plugin_json, mm_plugin_json

def get_module_name():
    """Prompt user for module name"""
    print("\nAdding new module to plugin...")
    
    module_name = input("Enter module name (e.g., 'Reverb', 'Filter'): ").strip()
    while not module_name:
        print("Module name is required!")
        module_name = input("Enter module name (e.g., 'Reverb', 'Filter'): ").strip()
    
    # Basic validation - check for valid identifier characters
    if not module_name.replace('_', '').isalnum():
        print("Warning: Module name should only contain letters, numbers, and underscores")
        confirm = input(f"Continue with module name '{module_name}'? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Module creation cancelled.")
            sys.exit(0)
    
    return module_name

def copy_and_process_template(module_name):
    """Copy template.cpp to MOD.cpp and replace __MOD__ placeholder"""
    project_root = Path.cwd()
    template_path = project_root / "templates" / "vcv" / "src" / "template.cpp"
    target_path = project_root / "VcvModules" / "src" / f"{module_name}.cpp"
    
    if not template_path.exists():
        print(f"Error: Template file not found at {template_path}")
        sys.exit(1)
    
    if target_path.exists():
        print(f"Error: Module file {target_path} already exists!")
        overwrite = input("Overwrite existing file? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Module creation cancelled.")
            sys.exit(0)
    
    print(f"Copying template from {template_path} to {target_path}")
    
    # Read template
    with open(template_path, 'r') as f:
        content = f.read()
    
    # Replace __MOD__ placeholder with module name
    processed_content = content.replace('__MOD__', module_name)
    
    # Ensure target directory exists
    os.makedirs(target_path.parent, exist_ok=True)
    
    # Write processed content
    with open(target_path, 'w') as f:
        f.write(processed_content)
    
    print(f"✓ Created module source file: {target_path}")
    return target_path

def create_rnbo_directory(module_name):
    """Create MOD-rnbo subdirectory"""
    project_root = Path.cwd()
    rnbo_dir = project_root / "VcvModules" / "src" / f"{module_name}-rnbo"
    
    if rnbo_dir.exists():
        print(f"Warning: RNBO directory {rnbo_dir} already exists")
    else:
        os.makedirs(rnbo_dir, exist_ok=True)
        print(f"✓ Created RNBO directory: {rnbo_dir}")
    
    return rnbo_dir

def update_plugin_hpp(module_name):
    """Add extern Model* modelMOD; declaration to plugin.hpp"""
    project_root = Path.cwd()
    plugin_hpp_path = project_root / "VcvModules" / "src" / "plugin.hpp"
    
    if not plugin_hpp_path.exists():
        print(f"Error: {plugin_hpp_path} not found!")
        return False
    
    # Read current content
    with open(plugin_hpp_path, 'r') as f:
        content = f.read()
    
    # Check if model declaration already exists
    model_declaration = f"extern Model* model{module_name};"
    if model_declaration in content:
        print(f"✓ Model declaration for {module_name} already exists in plugin.hpp")
        return True
    
    # Find the best insertion point: after existing model declarations or at the end
    lines = content.split('\n')
    insert_position = -1
    
    # Look for existing model declarations first
    for i, line in enumerate(lines):
        if line.strip().startswith('extern Model* model') and line.strip().endswith(';'):
            insert_position = i + 1
    
    # If no existing model declarations, add at the end of the file
    if insert_position == -1:
        # Remove any trailing empty lines and add at the very end
        while lines and lines[-1].strip() == '':
            lines.pop()
        insert_position = len(lines)
    
    # Insert the new declaration
    lines.insert(insert_position, model_declaration)
    
    # Write back to file
    with open(plugin_hpp_path, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ Added model declaration to plugin.hpp: {model_declaration}")
    return True

def update_plugin_cpp(module_name):
    """Add p->addModel(modelMOD); to plugin.cpp"""
    project_root = Path.cwd()
    plugin_cpp_path = project_root / "VcvModules" / "src" / "plugin.cpp"
    
    if not plugin_cpp_path.exists():
        print(f"Error: {plugin_cpp_path} not found!")
        return False
    
    # Read current content
    with open(plugin_cpp_path, 'r') as f:
        content = f.read()
    
    # Check if model is already added
    model_add = f"p->addModel(model{module_name});"
    if model_add in content:
        print(f"✓ Model {module_name} already added in plugin.cpp")
        return True
    
    # Find the init function and add the model before the closing brace
    lines = content.split('\n')
    insert_position = -1
    in_init_function = False
    
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        
        # Check if we're in the init function
        if 'void init(Plugin* p)' in line:
            in_init_function = True
            continue
            
        if in_init_function:
            # Look for existing addModel calls to insert after them
            if stripped_line.startswith('p->addModel(model') and stripped_line.endswith(');'):
                insert_position = i + 1
            # Look for the closing brace of the init function
            elif stripped_line == '}':
                insert_position = i
                break
    
    if insert_position == -1:
        print("Error: Could not find appropriate location to add model in plugin.cpp")
        return False
    
    # Insert the new addModel call with proper indentation
    lines.insert(insert_position, f"\tp->addModel(model{module_name});")
    
    # Write back to file
    with open(plugin_cpp_path, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ Added model to plugin.cpp: {model_add}")
    return True

def update_vcv_makefile(module_name):
    """Add module source file to VCV Makefile"""
    project_root = Path.cwd()
    makefile_path = project_root / "VcvModules" / "Makefile"
    
    if not makefile_path.exists():
        print(f"Warning: {makefile_path} not found! Skipping Makefile update.")
        return False
    
    # Read current content
    with open(makefile_path, 'r') as f:
        content = f.read()
    
    # Check if module is already in Makefile
    module_source = f"src/{module_name}.cpp"
    if module_source in content:
        print(f"✓ Module {module_name} already in VCV Makefile")
        return True
    
    # Replace the __MODULE_SOURCES__ placeholder or add to existing sources
    if '__MODULE_SOURCES__' in content:
        # Replace placeholder with the module source
        content = content.replace('__MODULE_SOURCES__', f'{module_source} \\\n__MODULE_SOURCES__')
    else:
        # Find SOURCES section and add module
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('src/plugin.cpp') and (i + 1 < len(lines)):
                # Add after plugin.cpp line
                lines.insert(i + 1, f'{module_source} \\')
                break
    
        content = '\n'.join(lines)
    
    # Write back to file
    with open(makefile_path, 'w') as f:
        f.write(content)
    
    print(f"✓ Added {module_source} to VCV Makefile")
    return True

def update_metamodule_cmake(module_name):
    """Add module source file to MetaModule CMakeLists.txt"""
    project_root = Path.cwd()
    cmake_path = project_root / "CMakeLists.txt"
    
    if not cmake_path.exists():
        print(f"Warning: {cmake_path} not found! Skipping CMakeLists.txt update.")
        return False
    
    # Read current content
    with open(cmake_path, 'r') as f:
        content = f.read()
    
    # Check if module is already in CMakeLists.txt
    module_source = f"${{SOURCE_DIR}}/src/{module_name}.cpp"
    if module_source in content:
        print(f"✓ Module {module_name} already in MetaModule CMakeLists.txt")
        return True
    
    # Replace the __MODULE_SOURCES__ placeholder or add to existing sources
    if '__MODULE_SOURCES__' in content:
        # Replace placeholder with the module source
        content = content.replace('__MODULE_SOURCES__', f'{module_source}\n    __MODULE_SOURCES__')
    else:
        # Find target_sources section and add module
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '${SOURCE_DIR}/src/plugin.cpp' in line:
                # Add after plugin.cpp line
                lines.insert(i + 1, f'    {module_source}')
                break
        
        content = '\n'.join(lines)
    
    # Write back to file
    with open(cmake_path, 'w') as f:
        f.write(content)
    
    print(f"✓ Added {module_source} to MetaModule CMakeLists.txt")
    return True

def get_module_details(module_name):
    """Prompt user for module details for plugin.json"""
    print(f"\nModule details for plugin.json:")
    
    # Use module name directly as default slug (no prefix)
    default_slug = module_name
    
    slug = input(f"Module slug (default: {default_slug}): ").strip()
    if not slug:
        slug = default_slug
    
    description = input(f"Module description (e.g., 'RNBO reverb module'): ").strip()
    if not description:
        description = f"RNBO {module_name} module"
    
    print("Module tags (enter tags separated by commas, or press enter for defaults)")
    print("Common tags: audio, effect, reverb, delay, filter, oscillator, utility, sequencer, midi")
    tags_input = input("Tags: ").strip()
    
    if tags_input:
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
    else:
        tags = ["audio", "effect"]  # Default tags
    
    return {
        "slug": slug,
        "name": module_name,
        "description": description,
        "tags": tags
    }

def update_plugin_json(module_name, module_details):
    """Add module definition to plugin.json"""
    project_root = Path.cwd()
    plugin_json_path = project_root / "VcvModules" / "plugin.json"
    
    if not plugin_json_path.exists():
        print(f"Warning: {plugin_json_path} not found! Skipping plugin.json update.")
        return False
    
    try:
        # Read current plugin.json
        with open(plugin_json_path, 'r') as f:
            plugin_data = json.load(f)
        
        # Check if module already exists
        modules = plugin_data.get('modules', [])
        for existing_module in modules:
            if existing_module.get('slug') == module_details['slug']:
                print(f"✓ Module with slug '{module_details['slug']}' already exists in plugin.json")
                return True
        
        # Add the new module
        modules.append(module_details)
        plugin_data['modules'] = modules
        
        # Write back to file with proper formatting
        with open(plugin_json_path, 'w') as f:
            json.dump(plugin_data, f, indent=2)
        
        print(f"✓ Added module to plugin.json:")
        print(f"  Slug: {module_details['slug']}")
        print(f"  Name: {module_details['name']}")
        print(f"  Description: {module_details['description']}")
        print(f"  Tags: {', '.join(module_details['tags'])}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {plugin_json_path}: {e}")
        return False
    except Exception as e:
        print(f"Error updating plugin.json: {e}")
        return False

def update_plugin_mm_json(module_name, module_details):
    """Add module definition to plugin-mm.json"""
    project_root = Path.cwd()
    plugin_mm_json_path = project_root / "plugin-mm.json"
    
    if not plugin_mm_json_path.exists():
        print(f"Warning: {plugin_mm_json_path} not found! Skipping plugin-mm.json update.")
        return False
    
    try:
        # Read current plugin-mm.json
        with open(plugin_mm_json_path, 'r') as f:
            plugin_data = json.load(f)
        
        # Check if module already exists
        modules = plugin_data.get('MetaModuleIncludedModules', [])
        for existing_module in modules:
            if existing_module.get('slug') == module_details['slug']:
                print(f"✓ Module with slug '{module_details['slug']}' already exists in plugin-mm.json")
                return True
        
        # Create MetaModule module entry
        mm_module = {
            "slug": module_details['slug'],
            "name": module_details['name'],
            "displayName": module_details['description']
        }
        
        # Add the new module
        modules.append(mm_module)
        plugin_data['MetaModuleIncludedModules'] = modules
        
        # Write back to file with proper formatting
        with open(plugin_mm_json_path, 'w') as f:
            json.dump(plugin_data, f, indent=2)
        
        print(f"✓ Added module to plugin-mm.json:")
        print(f"  Slug: {mm_module['slug']}")
        print(f"  Name: {mm_module['name']}")
        print(f"  DisplayName: {mm_module['displayName']}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {plugin_mm_json_path}: {e}")
        return False
    except Exception as e:
        print(f"Error updating plugin-mm.json: {e}")
        return False

def main():
    """Main function"""
    try:
        # Ensure we're running from the correct directory
        project_root = ensure_run_from_base_directory()
        print(f"Running from project directory: {project_root}")
        
        # Check that createPlugin.py has been run
        vcv_plugin_json, mm_plugin_json = check_plugin_exists()
        
        # Get module name from user
        module_name = get_module_name()
        
        # Get module details for plugin.json
        module_details = get_module_details(module_name)
        
        print(f"\nCreating module '{module_name}'...")
        
        # Copy and process template
        module_file = copy_and_process_template(module_name)
        
        # Create RNBO directory
        rnbo_dir = create_rnbo_directory(module_name)
        
        # Update plugin.hpp to add model declaration
        update_plugin_hpp(module_name)
        
        # Update plugin.cpp to add model to plugin
        update_plugin_cpp(module_name)
        
        # Update build systems to include module source
        update_vcv_makefile(module_name)
        update_metamodule_cmake(module_name)
        
        # Add module to plugin.json
        update_plugin_json(module_name, module_details)
        
        # Add module to plugin-mm.json
        update_plugin_mm_json(module_name, module_details)
        
        print(f"\n✓ Module '{module_name}' created successfully!")
        print("\nNext steps:")
        print(f"1. Export your RNBO patch to: {rnbo_dir}/")
        print(f"   - The export should create {module_name}.cpp.h")
        print("2. Build and test your module")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
