#!/usr/bin/env python3
"""
VCV Rack RNBO Template Setup and Status Checker

This script checks that the development environment is properly configured
and provides guidance on the current project status.
"""

import os
import sys
import json
import shutil
import subprocess
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
        print("Example: python3 scripts/check.py")
        sys.exit(1)
    
    return current_dir

def check_file_exists(file_path, description):
    """Check if a file exists and report status"""
    if file_path.exists():
        print(f"[PASS] {description}")
        return True
    else:
        print(f"[ERROR] {description}")
        return False

def check_command_available(command, description):
    """Check if a command is available in PATH"""
    if shutil.which(command):
        print(f"[PASS] {description}")
        return True
    else:
        print(f"[ERROR] {description}")
        return False

def check_arm_compiler():
    """Check for ARM compiler availability with Windows support"""
    arm_commands = [
        'arm-none-eabi-gcc',
        'arm-none-eabi-g++',
        'arm-none-eabi-objcopy'
    ]
    
    missing = []
    for cmd in arm_commands:
        # shutil.which automatically handles .exe on Windows
        if not shutil.which(cmd):
            missing.append(cmd)
    
    if not missing:
        print("[PASS] ARM toolchain (arm-none-eabi-gcc) available")
        return True
    else:
        print(f"[ERROR] ARM toolchain missing: {', '.join(missing)}")
        
        # Windows-specific checking and guidance
        if os.name == 'nt':  # Windows
            check_windows_arm_toolchain()
        
        return False

def check_windows_arm_toolchain():
    """Check for specific Windows ARM toolchain installation"""
    expected_path = Path("C:/Program Files (x86)/Arm GNU Toolchain arm-none-eabi/12.3 rel1")
    expected_bin_path = expected_path / "bin"
    
    print("   [NOTE] Windows ARM toolchain check:")
    
    if expected_path.exists():
        print(f"   [PASS] Found ARM toolchain installation at: {expected_path}")
        
        # Check if it's in PATH
        current_path = os.environ.get('PATH', '')
        path_to_check = "/c/Program Files (x86)/Arm GNU Toolchain arm-none-eabi/12.3 rel1/bin"
        
        if path_to_check in current_path:
            print("   [PASS] ARM toolchain is correctly added to PATH")
        else:
            print("   [WARNING] ARM toolchain found but not in PATH")
            print("   [TOOL] To fix this, run the following command each time you open MSYS64 terminal:")
            print(f"          export PATH=/c/Program\\ Files\\ \\(x86\\)/Arm\\ GNU\\ Toolchain\\ arm-none-eabi/12.3\\ rel1/bin:$PATH")
            print("   [TIP] Or add this to your ~/.bashrc file to make it permanent")
    else:
        print(f"   [ERROR] ARM toolchain not found at expected location: {expected_path}")
        print("   [TOOL] Please install ARM GNU Toolchain 12.3 rel1 to:")
        print("          C:\\Program Files (x86)\\Arm GNU Toolchain arm-none-eabi\\12.3 rel1")
        print("   [TOOL] Then run this script again to verify installation")

def check_environment_setup():
    """Check basic environment setup"""
    print("[TOOL] Checking Development Environment Setup")
    print("=" * 50)
    
    project_root = Path.cwd()
    issues = []
    
    # Check MetaModule SDK
    metamodule_version = project_root / "metamodule-plugin-sdk" / "version.hh"
    if not check_file_exists(metamodule_version, "MetaModule SDK (submodule initialized)"):
        issues.append("Run: git submodule update --init --recursive")
    
    # Check Rack SDK
    rack_sdk_plugin = project_root / "Rack-SDK" / "plugin.mk"
    if not check_file_exists(rack_sdk_plugin, "VCV Rack SDK (Rack-SDK/plugin.mk)"):
        issues.append("Download and unpack Rack SDK to Rack-SDK/ directory")
    
    # Check build tools
    if not check_command_available("make", "make command available"):
        issues.append("Install make (part of build tools)")
    
    if not check_command_available("cmake", "cmake command available"):
        issues.append("Install cmake")
    
    # Check ARM compiler
    if not check_arm_compiler():
        if os.name == 'nt':  # Windows
            issues.append("Install ARM GNU Toolchain and add to PATH (see Windows-specific guidance above)")
        else:
            issues.append("Install ARM GNU Toolchain (arm-none-eabi-gcc)")
    
    if issues:
        print(f"\n[ERROR] Environment setup issues found:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print("\nPlease fix these issues before continuing.")
        return False
    else:
        print("\n[PASS] Environment setup is complete!")
        return True

def check_plugin_exists():
    """Check if plugin has been created"""
    project_root = Path.cwd()
    plugin_json = project_root / "VcvModules" / "plugin.json"
    plugin_mm_json = project_root / "plugin-mm.json"
    
    if plugin_json.exists() and plugin_mm_json.exists():
        return True, plugin_json
    else:
        return False, None

def get_modules_from_plugin_json(plugin_json_path):
    """Get list of modules from plugin.json"""
    try:
        with open(plugin_json_path, 'r') as f:
            data = json.load(f)
        return data.get('modules', [])
    except Exception as e:
        print(f"[ERROR] Error reading plugin.json: {e}")
        return []

def check_module_status(module_slug):
    """Check the status of a specific module"""
    project_root = Path.cwd()
    
    # Check if module source file exists
    module_cpp = project_root / "VcvModules" / "src" / f"{module_slug}.cpp"
    if not module_cpp.exists():
        return "missing_source", f"Module source file missing: {module_cpp}"
    
    # Check RNBO directory
    rnbo_dir = project_root / "VcvModules" / "src" / f"{module_slug}-rnbo"
    if not rnbo_dir.exists():
        return "missing_rnbo_dir", f"RNBO directory missing: {rnbo_dir}"
    
    # Check for RNBO export files
    expected_cpp_h = rnbo_dir / f"{module_slug}.cpp.h"
    
    if expected_cpp_h.exists():
        return "complete", "Module complete with RNBO export"
    
    # Check for any .cpp.h files
    cpp_h_files = list(rnbo_dir.glob("*.cpp.h"))
    if cpp_h_files:
        return "wrong_name", f"RNBO export found but wrong name: {cpp_h_files[0].name} (should be {module_slug}.cpp.h)"
    
    # Check if directory is empty
    if not any(rnbo_dir.iterdir()):
        return "no_export", "RNBO directory exists but no export files found"
    
    # Check for common incorrect export filenames
    incorrect_cpp = rnbo_dir / f"{module_slug}.cpp"
    if incorrect_cpp.exists():
        return "wrong_extension", f"Found {module_slug}.cpp but need {module_slug}.cpp.h - incorrect export format from Max"
    
    # Check for any .cpp files (without .h)
    cpp_files = list(rnbo_dir.glob("*.cpp"))
    if cpp_files:
        return "wrong_extension", f"Found .cpp file: {cpp_files[0].name} but need .cpp.h - check Max export settings"
    
    # Check for other common files
    files_found = list(rnbo_dir.iterdir())
    if files_found:
        file_names = [f.name for f in files_found]
        return "unknown_files", f"RNBO directory contains: {', '.join(file_names)} but missing {module_slug}.cpp.h"
    
    return "unknown_files", f"RNBO directory contains files but no .cpp.h export"

def check_project_status():
    """Check current project status and provide guidance"""
    print("\n[TARGET] Checking Project Status")
    print("=" * 50)
    
    # Check if plugin exists
    plugin_exists, plugin_json_path = check_plugin_exists()
    
    if not plugin_exists:
        print("[ERROR] No plugin found")
        print("\n[NEXT] Next step: Create a plugin")
        print("   Run: python3 scripts/createPlugin.py")
        return
    
    print("[PASS] Plugin configuration found")
    
    # Get modules from plugin.json
    modules = get_modules_from_plugin_json(plugin_json_path)
    
    if not modules:
        print("[ERROR] No modules defined in plugin")
        print("\n[NEXT] Next step: Create a module")
        print("   Run: python3 scripts/createModule.py")
        return
    
    print(f"[PASS] Found {len(modules)} module(s) in plugin configuration")
    
    # Check each module
    all_complete = True
    issues = []
    
    for module in modules:
        module_slug = module.get('slug', 'unknown')
        print(f"\n[CHECK] Checking module: {module_slug}")
        
        status, message = check_module_status(module_slug)
        
        if status == "complete":
            print(f"   [PASS] {message}")
        elif status == "missing_source":
            print(f"   [ERROR] {message}")
            issues.append(f"Module {module_slug}: Run 'python3 scripts/createModule.py' to recreate")
            all_complete = False
        elif status == "missing_rnbo_dir":
            print(f"   [ERROR] {message}")
            issues.append(f"Module {module_slug}: Run 'python3 scripts/createModule.py' to recreate")
            all_complete = False
        elif status == "no_export":
            print(f"   [WARNING]  {message}")
            issues.append(f"Module {module_slug}: Export RNBO patch from Max to VcvModules/src/{module_slug}-rnbo/")
            all_complete = False
        elif status == "wrong_name":
            print(f"   [WARNING]  {message}")
            issues.append(f"Module {module_slug}: Re-export with correct name '{module_slug}.cpp.h'")
            all_complete = False
        elif status == "wrong_extension":
            print(f"   [WARNING]  {message}")
            issues.append(f"Module {module_slug}: Re-export from Max using 'C++ Code Export' format (not 'Audio Unit')")
            all_complete = False
        else:
            print(f"   [WARNING]  {message}")
            issues.append(f"Module {module_slug}: Check RNBO export directory and re-export as '{module_slug}.cpp.h'")
            all_complete = False
    
    if all_complete:
        print(f"\n[SUCCESS] All modules are complete and ready to build!")
        print("\n[NEXT] Next steps:")
        print("   1. Build VCV Rack: cd VcvModules && make")
        print("   2. Build MetaModule: cmake --fresh -B build && cmake --build build")
    else:
        print(f"\n[ERROR] Issues found with modules:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")

def main():
    """Main function"""
    try:
        # Ensure we're in the right directory
        project_root = ensure_run_from_base_directory()
        print(f"Running from project directory: {project_root}")
        
        print("\n[TEST] VCV Rack RNBO Template - Setup Checker")
        print("=" * 60)
        
        # Check environment setup
        env_ok = check_environment_setup()
        
        if env_ok:
            # Check project status
            check_project_status()
        else:
            print("\n[WARNING]  Fix environment issues before checking project status.")
            return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())