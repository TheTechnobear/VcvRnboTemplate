#!/usr/bin/env python3

import os
import shutil
import json
import sys
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
        print("Example: python3 scripts/createPlugin.py")
        sys.exit(1)
    
    return current_dir

def get_script_dir():
    """Get the directory where this script is located"""
    return Path(__file__).parent.absolute()

def get_project_root():
    """Get the project root directory (should be current working directory)"""
    return ensure_run_from_base_directory()

def prompt_user_details():
    """Prompt user for plugin details"""
    print("Creating new plugin...")
    print("Please enter the following details:")
    
    slug = input("Plugin slug (e.g., 'MyCompany', used as technical ID, no spaces): ").strip()
    while not slug:
        print("Plugin slug is required!")
        slug = input("Plugin slug (e.g., 'MyCompany', used as technical ID, no spaces): ").strip()
    
    name = input("Plugin display name (e.g., 'My Company Audio', shown to users): ").strip()
    while not name:
        print("Plugin display name is required!")
        name = input("Plugin display name (e.g., 'My Company Audio', shown to users): ").strip()
    
    brand = input("Brand name (e.g., 'MyCompany'): ").strip()
    while not brand:
        print("Brand name is required!")
        brand = input("Brand name (e.g., 'MyCompany'): ").strip()
    
    description = input("Plugin description (e.g., 'RNBO-based audio effects for VCV Rack'): ").strip()
    while not description:
        print("Plugin description is required!")
        description = input("Plugin description (e.g., 'RNBO-based audio effects for VCV Rack'): ").strip()
    
    author = input("Author name: ").strip()
    while not author:
        print("Author name is required!")
        author = input("Author name: ").strip()
    
    email = input("Author email: ").strip()
    url = input("Author/Plugin URL (optional): ").strip()
    
    return {
        '__SLUG__': slug,
        '__NAME__': name,
        '__BRAND__': brand,
        '__DESCRIPTION__': description,
        '__AUTHOR__': author,
        '__EMAIL__': email,
        '__URL__': url,
        '__MODULE_SOURCES__': ''  # Initially empty, modules will be added by createModule.py
    }

def replace_template_placeholders(content, replacements):
    """Replace template placeholders in content"""
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    return content

def copy_and_process_vcv_plugin_json(replacements):
    """Copy and process VCV plugin.json template"""
    project_root = Path.cwd()  # Use current working directory
    template_path = project_root / "templates" / "vcv" / "plugin.json"
    target_path = project_root / "VcvModules" / "plugin.json"
    
    print(f"Copying VCV plugin.json template from {template_path} to {target_path}")
    
    # Read template
    with open(template_path, 'r') as f:
        content = f.read()
    
    # Replace placeholders
    processed_content = replace_template_placeholders(content, replacements)
    
    # Write to target
    os.makedirs(target_path.parent, exist_ok=True)
    with open(target_path, 'w', newline='\n') as f:
        f.write(processed_content)
    
    print(f"[OK] Created VCV plugin.json at {target_path}")

def copy_and_process_metamodule_plugin_json(replacements):
    """Copy and process MetaModule plugin-mm.json template"""
    project_root = Path.cwd()  # Use current working directory
    template_path = project_root / "templates" / "metamodule" / "plugin-mm.json"
    target_path = project_root / "plugin-mm.json"
    
    print(f"Copying MetaModule plugin-mm.json template from {template_path} to {target_path}")
    
    # Read template
    with open(template_path, 'r') as f:
        content = f.read()
    
    # Replace placeholders
    processed_content = replace_template_placeholders(content, replacements)
    
    # Write to target
    with open(target_path, 'w', newline='\n') as f:
        f.write(processed_content)
    
    print(f"[OK] Created MetaModule plugin-mm.json at {target_path}")

def copy_and_process_vcv_makefile(replacements):
    """Copy and process VCV Makefile template"""
    project_root = Path.cwd()
    template_path = project_root / "templates" / "vcv" / "Makefile"
    target_path = project_root / "VcvModules" / "Makefile"
    
    print(f"Copying VCV Makefile template from {template_path} to {target_path}")
    
    # Read template
    with open(template_path, 'r') as f:
        content = f.read()
    
    # Replace placeholders
    processed_content = replace_template_placeholders(content, replacements)
    
    # Write to target
    os.makedirs(target_path.parent, exist_ok=True)
    with open(target_path, 'w', newline='\n') as f:
        f.write(processed_content)
    
    print(f"[OK] Created VCV Makefile at {target_path}")

def copy_and_process_metamodule_cmake(replacements):
    """Copy and process MetaModule CMakeLists.txt template"""
    project_root = Path.cwd()
    template_path = project_root / "templates" / "metamodule" / "CMakeLists.txt"
    target_path = project_root / "CMakeLists.txt"
    
    print(f"Copying MetaModule CMakeLists.txt template from {template_path} to {target_path}")
    
    # Read template
    with open(template_path, 'r') as f:
        content = f.read()
    
    # Replace placeholders
    processed_content = replace_template_placeholders(content, replacements)
    
    # Write to target
    with open(target_path, 'w', newline='\n') as f:
        f.write(processed_content)
    
    print(f"[OK] Created MetaModule CMakeLists.txt at {target_path}")

def copy_vcv_plugin_sources():
    """Copy VCV plugin.cpp and plugin.hpp templates"""
    project_root = Path.cwd()
    
    # Copy plugin.hpp
    template_hpp = project_root / "templates" / "vcv" / "src" / "plugin.hpp"
    target_hpp = project_root / "VcvModules" / "src" / "plugin.hpp"
    
    print(f"Copying VCV plugin.hpp template from {template_hpp} to {target_hpp}")
    os.makedirs(target_hpp.parent, exist_ok=True)
    with open(template_hpp, 'r') as f:
        content = f.read()
    with open(target_hpp, 'w', newline='\n') as f:
        f.write(content)
    print(f"[OK] Created VCV plugin.hpp at {target_hpp}")
    
    # Copy plugin.cpp
    template_cpp = project_root / "templates" / "vcv" / "src" / "plugin.cpp"
    target_cpp = project_root / "VcvModules" / "src" / "plugin.cpp"
    
    print(f"Copying VCV plugin.cpp template from {template_cpp} to {target_cpp}")
    with open(template_cpp, 'r') as f:
        content = f.read()
    with open(target_cpp, 'w', newline='\n') as f:
        f.write(content)
    print(f"[OK] Created VCV plugin.cpp at {target_cpp}")

def main():
    """Main function"""
    try:
        # Ensure we're running from the correct directory
        project_root = get_project_root()
        print(f"Running from project directory: {project_root}")
        
        # Get user input
        replacements = prompt_user_details()
        
        print(f"\nCreating plugin with the following details:")
        print(f"  Slug: {replacements['__SLUG__']}")
        print(f"  Name: {replacements['__NAME__']}")
        print(f"  Brand: {replacements['__BRAND__']}")
        print(f"  Description: {replacements['__DESCRIPTION__']}")
        print(f"  Author: {replacements['__AUTHOR__']}")
        print(f"  Email: {replacements['__EMAIL__']}")
        print(f"  URL: {replacements['__URL__']}")
        print()
        
        # Copy and process templates
        copy_and_process_vcv_plugin_json(replacements)
        copy_and_process_vcv_makefile(replacements)
        copy_vcv_plugin_sources()
        copy_and_process_metamodule_plugin_json(replacements)
        copy_and_process_metamodule_cmake(replacements)
        
        print("\n[OK] Plugin created successfully!")
        print("Next steps:")
        print("1. Use createModule.py to add modules to your plugin")
        print("2. Build for VCV Rack: cd VcvModules && make")
        print("3. Build for MetaModule: cmake --fresh -B build && cmake --build build")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
