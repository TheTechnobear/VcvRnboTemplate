#!/usr/bin/env python3
"""
VCV Rack RNBO Template Reset Script

This script removes all files created by createPlugin.py and createModule.py,
effectively resetting the project to a clean slate.

WARNING: This is a destructive operation that cannot be undone!
"""

import os
import sys
import argparse
import shutil
import json
from pathlib import Path

def get_project_root():
    """Get the project root directory."""
    script_dir = Path(__file__).parent.absolute()
    return script_dir.parent.parent

def remove_file_safe(file_path):
    """Safely remove a file if it exists."""
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"✓ Removed file: {file_path}")
        return True
    return False

def remove_dir_safe(dir_path):
    """Safely remove a directory if it exists."""
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print(f"✓ Removed directory: {dir_path}")
        return True
    return False

def reset_project(force=False):
    """Reset the project by removing all generated files."""
    project_root = get_project_root()
    
    print(f"Running from project directory: {project_root}")
    
    if not force:
        print("\n⚠️  WARNING: This will permanently remove ALL generated plugin files!")
        print("\nFiles and directories that will be removed:")
        print("  • VcvModules/plugin.json")
        print("  • VcvModules/Makefile") 
        print("  • VcvModules/src/plugin.hpp")
        print("  • VcvModules/src/plugin.cpp")
        print("  • VcvModules/src/*.cpp (all module files)")
        print("  • VcvModules/src/*-rnbo/ (all RNBO directories)")
        print("  • plugin-mm.json")
        print("  • CMakeLists.txt")
        print("\n❌ This action cannot be undone!")
        
        response = input("\nAre you sure you want to reset the project? (yes/no): ")
        if response.lower() != 'yes':
            print("Operation cancelled.")
            return False
    else:
        print("Force mode: Resetting project without confirmation...")
    
    print("\nResetting project...")
    
    # Files to remove
    files_to_remove = [
        project_root / "VcvModules" / "plugin.json",
        project_root / "VcvModules" / "Makefile",
        project_root / "VcvModules" / "src" / "plugin.hpp", 
        project_root / "VcvModules" / "src" / "plugin.cpp",
        project_root / "plugin-mm.json",
        project_root / "CMakeLists.txt"
    ]
    
    # Remove main files
    for file_path in files_to_remove:
        remove_file_safe(file_path)
    
    # Remove all module .cpp files (except plugin.cpp which is already handled)
    vcv_src_dir = project_root / "VcvModules" / "src"
    if vcv_src_dir.exists():
        for cpp_file in vcv_src_dir.glob("*.cpp"):
            if cpp_file.name != "plugin.cpp":  # Don't double-remove plugin.cpp
                remove_file_safe(cpp_file)
        
        # Remove all RNBO directories (*-rnbo)
        for rnbo_dir in vcv_src_dir.glob("*-rnbo"):
            if rnbo_dir.is_dir():
                remove_dir_safe(rnbo_dir)
    
    print("\n✅ Project reset completed!")
    print("\nNext steps:")
    print("1. Run createPlugin.py to create a new plugin")
    print("2. Run createModule.py to add modules")
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Reset VCV Rack RNBO Template project to clean slate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/test/reset.py                # Interactive reset with confirmation
  python3 scripts/test/reset.py --force        # Reset without confirmation
        """
    )
    
    parser.add_argument(
        '--force', 
        action='store_true',
        help='Reset without confirmation prompt (dangerous!)'
    )
    
    args = parser.parse_args()
    
    try:
        success = reset_project(args.force)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()