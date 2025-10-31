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
        print("❌ This script must be run from the project base directory.")
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
        print("❌ VcvModules/plugin.json not found.")
        print("Please run 'python3 scripts/createPlugin.py' first to create the plugin.")
        sys.exit(1)
    
    if not mm_plugin_json.exists():
        print("❌ plugin-mm.json not found.")
        print("Please run 'python3 scripts/createPlugin.py' first to create the plugin.")
        sys.exit(1)
    
    print("✓ Found existing plugin configuration files")
    return vcv_plugin_json, mm_plugin_json

def get_module_slug():
    """Prompt user for module slug with validation"""
    print("\nAdding new module to plugin...")
    print("First, we need a module slug - this is used for technical identifiers (filenames, C++ code, etc.)")
    print("The slug must contain only letters, numbers, and underscores (no spaces).")
    
    while True:
        module_slug = input("Enter module slug (e.g., 'Reverb', 'MultiFilter', 'MyDelay'): ").strip()
        
        if not module_slug:
            print("❌ Module slug is required!")
            continue
        
        # Validate slug - only letters, numbers, and underscores
        if not module_slug.replace('_', '').isalnum():
            print("❌ Module slug can only contain letters, numbers, and underscores (no spaces or special characters)")
            print("Examples: 'Reverb', 'MultiFilter', 'My_Delay'")
            continue
        
        # Additional check to ensure it starts with a letter (good C++ practice)
        if not module_slug[0].isalpha():
            print("❌ Module slug should start with a letter")
            continue
            
        return module_slug

def get_module_name():
    """Prompt user for module name (user-facing display name)"""
    print("\nNow enter the module name - this is the user-facing display name.")
    print("The name can contain spaces and special characters (e.g., 'My Great Filter', 'Reverb & Delay').")
    
    module_name = input("Enter module name: ").strip()
    while not module_name:
        print("❌ Module name is required!")
        module_name = input("Enter module name: ").strip()
    
    return module_name

def select_panel():
    """Present user with list of available panels and let them choose"""
    project_root = Path.cwd()
    res_dir = project_root / "VcvModules" / "res"
    
    if not res_dir.exists():
        print("❌ VcvModules/res directory not found!")
        sys.exit(1)
    
    # Find all .svg files in res directory
    svg_files = list(res_dir.glob("*.svg"))
    
    if not svg_files:
        print("❌ No SVG panel files found in VcvModules/res/")
        print("Please add some panel files (e.g., Blank10U.svg) to the res directory")
        sys.exit(1)
    
    # Sort by name for consistent ordering
    svg_files.sort(key=lambda x: x.name.lower())
    
    print("\nAvailable panels:")
    for i, svg_file in enumerate(svg_files, 1):
        print(f"  {i}. {svg_file.name}")
    
    # Get user selection
    while True:
        try:
            choice = input(f"\nSelect panel (1-{len(svg_files)}): ").strip()
            if not choice:
                # Default to first panel if user just presses enter
                selected_panel = svg_files[0].name
                break
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(svg_files):
                selected_panel = svg_files[choice_num - 1].name
                break
            else:
                print(f"Please enter a number between 1 and {len(svg_files)}")
        except ValueError:
            print("Please enter a valid number")
    
    print(f"Selected panel: {selected_panel}")
    return selected_panel

def copy_and_process_template(module_name, module_slug, panel_filename):
    """Copy module.cpp to MOD.cpp and replace __MOD__, __MODNAME__, and __PANEL__ placeholders"""
    project_root = Path.cwd()
    template_path = project_root / "templates" / "vcv" / "src" / "module.cpp"
    target_path = project_root / "VcvModules" / "src" / f"{module_slug}.cpp"
    
    if not template_path.exists():
        print(f"❌ Template file not found at {template_path}")
        sys.exit(1)
    
    if target_path.exists():
        print(f"❌ Module file {target_path} already exists!")
        overwrite = input("Overwrite existing file? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Module creation cancelled.")
            sys.exit(0)
    
    print(f"Copying template from {template_path} to {target_path}")
    
    # Read template
    with open(template_path, 'r') as f:
        content = f.read()
    
    # Replace placeholders (do longer placeholders first to avoid conflicts):
    # __MODNAME__ -> module name (for user-facing display)
    # __MOD__ -> module slug (for technical identifiers, filenames)  
    # __PANEL__ -> selected panel filename
    processed_content = content.replace('__MODNAME__', module_name)
    processed_content = processed_content.replace('__MOD__', module_slug)
    processed_content = processed_content.replace('__PANEL__', panel_filename)
    
    # Ensure target directory exists
    os.makedirs(target_path.parent, exist_ok=True)
    
    # Write processed content
    with open(target_path, 'w', newline='\n') as f:
        f.write(processed_content)
    
    print(f"✓ Created module source file: {target_path}")
    return target_path

def create_rnbo_directory(module_slug):
    """Create MOD-rnbo subdirectory"""
    project_root = Path.cwd()
    rnbo_dir = project_root / "VcvModules" / "src" / f"{module_slug}-rnbo"
    
    if rnbo_dir.exists():
        print(f"Warning: RNBO directory {rnbo_dir} already exists")
    else:
        os.makedirs(rnbo_dir, exist_ok=True)
        print(f"✓ Created RNBO directory: {rnbo_dir}")
    
    return rnbo_dir

def update_plugin_hpp(module_slug):
    """Add extern Model* modelMOD; declaration to plugin.hpp"""
    project_root = Path.cwd()
    plugin_hpp_path = project_root / "VcvModules" / "src" / "plugin.hpp"
    
    if not plugin_hpp_path.exists():
        print(f"❌ {plugin_hpp_path} not found!")
        return False
    
    # Read current content
    with open(plugin_hpp_path, 'r') as f:
        content = f.read()
    
    # Check if model declaration already exists
    model_declaration = f"extern Model* model{module_slug};"
    if model_declaration in content:
        print(f"✓ Model declaration for {module_slug} already exists in plugin.hpp")
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
    with open(plugin_hpp_path, 'w', newline='\n') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ Added model declaration to plugin.hpp: {model_declaration}")
    return True

def update_plugin_cpp(module_slug):
    """Add p->addModel(modelMOD); to plugin.cpp"""
    project_root = Path.cwd()
    plugin_cpp_path = project_root / "VcvModules" / "src" / "plugin.cpp"
    
    if not plugin_cpp_path.exists():
        print(f"❌ {plugin_cpp_path} not found!")
        return False
    
    # Read current content
    with open(plugin_cpp_path, 'r') as f:
        content = f.read()
    
    # Check if model is already added
    model_add = f"p->addModel(model{module_slug});"
    if model_add in content:
        print(f"✓ Model {module_slug} already added in plugin.cpp")
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
        print("❌ Could not find appropriate location to add model in plugin.cpp")
        return False
    
    # Insert the new addModel call with proper indentation
    lines.insert(insert_position, f"\tp->addModel(model{module_slug});")
    
    # Write back to file
    with open(plugin_cpp_path, 'w', newline='\n') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ Added model to plugin.cpp: {model_add}")
    return True

def update_vcv_makefile(module_slug):
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
    module_source = f"src/{module_slug}.cpp"
    if module_source in content:
        print(f"✓ Module {module_slug} already in VCV Makefile")
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
    with open(makefile_path, 'w', newline='\n') as f:
        f.write(content)
    
    print(f"✓ Added {module_source} to VCV Makefile")
    return True

def update_metamodule_cmake(module_slug):
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
    module_source = f"${{SOURCE_DIR}}/src/{module_slug}.cpp"
    if module_source in content:
        print(f"✓ Module {module_slug} already in MetaModule CMakeLists.txt")
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
    with open(cmake_path, 'w', newline='\n') as f:
        f.write(content)
    
    print(f"✓ Added {module_source} to MetaModule CMakeLists.txt")
    return True

def get_module_details(module_name, module_slug):
    """Prompt user for additional module details for plugin.json"""
    print(f"\nModule details for plugin.json:")
    print(f"  • Slug: {module_slug} (technical identifier)")
    print(f"  • Name: {module_name} (display name)")
    
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
        "slug": module_slug,
        "name": module_name,
        "description": description,
        "tags": tags
    }

def update_plugin_json(module_slug, module_details):
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
        with open(plugin_json_path, 'w', newline='\n') as f:
            json.dump(plugin_data, f, indent=2)
        
        print(f"✓ Added module to plugin.json:")
        print(f"  Slug: {module_details['slug']}")
        print(f"  Name: {module_details['name']}")
        print(f"  Description: {module_details['description']}")
        print(f"  Tags: {', '.join(module_details['tags'])}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {plugin_json_path}: {e}")
        return False
    except Exception as e:
        print(f"Error updating plugin.json: {e}")
        return False

def update_plugin_mm_json(module_slug, module_details):
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
        with open(plugin_mm_json_path, 'w', newline='\n') as f:
            json.dump(plugin_data, f, indent=2)
        
        print(f"✓ Added module to plugin-mm.json:")
        print(f"  Slug: {mm_module['slug']}")
        print(f"  Name: {mm_module['name']}")
        print(f"  DisplayName: {mm_module['displayName']}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {plugin_mm_json_path}: {e}")
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
        
        # Get module slug first (with validation)
        module_slug = get_module_slug()
        
        # Get module name (user-facing, no validation needed)
        module_name = get_module_name()
        
        # Select panel
        panel_filename = select_panel()
        
        # Get additional module details for plugin.json
        module_details = get_module_details(module_name, module_slug)
        
        print(f"\nCreating module '{module_name}' with slug '{module_slug}'...")
        
        # Copy and process template
        module_file = copy_and_process_template(module_name, module_slug, panel_filename)
        
        # Create RNBO directory
        rnbo_dir = create_rnbo_directory(module_slug)
        
        # Update plugin.hpp to add model declaration
        update_plugin_hpp(module_slug)
        
        # Update plugin.cpp to add model to plugin
        update_plugin_cpp(module_slug)
        
        # Update build systems to include module source
        update_vcv_makefile(module_slug)
        update_metamodule_cmake(module_slug)
        
        # Add module to plugin.json
        update_plugin_json(module_slug, module_details)
        
        # Add module to plugin-mm.json
        update_plugin_mm_json(module_slug, module_details)
        
        print(f"\n✓ Module '{module_name}' created successfully!")
        print("\nNext steps:")
        print(f"1. Export your RNBO patch to: {rnbo_dir}/")
        print(f"   - The export should create {module_slug}.cpp.h")
        print("2. Build and test your module")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"❌ {e}")

if __name__ == "__main__":
    main()
