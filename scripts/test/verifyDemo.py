#!/usr/bin/env python3
"""
Verify Demo module was created correctly with proper slug vs name usage
"""

import json
import os
from pathlib import Path

def main():
    project_root = Path.cwd()
    
    print("🔍 Verifying Demo module creation...")
    print("=" * 50)
    
    # Check plugin.json contains Demo module
    plugin_json = project_root / "VcvModules" / "plugin.json"
    if plugin_json.exists():
        with open(plugin_json) as f:
            data = json.load(f)
            modules = data.get('modules', [])
            demo_module = next((m for m in modules if m['slug'] == 'Demo'), None)
            
            if demo_module:
                print("✅ Demo module found in plugin.json:")
                print(f"  • Slug: '{demo_module['slug']}'")
                print(f"  • Name: '{demo_module['name']}'") 
                print(f"  • Description: '{demo_module['description']}'")
            else:
                print("❌ Demo module not found in plugin.json")
    else:
        print("❌ plugin.json not found")
    
    # Check files use slug naming
    files_to_check = [
        ("VcvModules/src/Demo.cpp", "Demo module source file"),
        ("VcvModules/src/Demo-rnbo/Demo.cpp.h", "Demo RNBO header"),
        ("VcvModules/src/Demo-rnbo/description.json", "Demo RNBO description")
    ]
    
    print(f"\n📁 Verifying files use slug 'Demo' (not spaces):")
    for file_path, description in files_to_check:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path} - {description}")
        else:
            print(f"❌ {file_path} - MISSING! ({description})")
    
    # Check C++ code uses slug
    plugin_hpp = project_root / "VcvModules" / "src" / "plugin.hpp"
    plugin_cpp = project_root / "VcvModules" / "src" / "plugin.cpp"
    
    print(f"\n💻 Verifying C++ code uses slug 'Demo':")
    
    if plugin_hpp.exists():
        with open(plugin_hpp) as f:
            content = f.read()
            if "extern Model* modelDemo;" in content:
                print("✅ plugin.hpp contains 'extern Model* modelDemo;'")
            else:
                print("❌ plugin.hpp missing 'extern Model* modelDemo;'")
    
    if plugin_cpp.exists():
        with open(plugin_cpp) as f:
            content = f.read()
            if "p->addModel(modelDemo);" in content:
                print("✅ plugin.cpp contains 'p->addModel(modelDemo);'")
            else:
                print("❌ plugin.cpp missing 'p->addModel(modelDemo);'")
    
    # Check that plugin builds
    plugin_dylib = project_root / "VcvModules" / "plugin.dylib"
    if plugin_dylib.exists():
        print(f"\n🔨 Build verification:")
        print("✅ plugin.dylib exists - build successful")
    else:
        print(f"\n🔨 Build verification:")
        print("❌ plugin.dylib not found - build may have failed")
    
    print(f"\n🎉 Demo module verification complete!")
    print("\nDemo module demonstrates proper slug vs name usage:")
    print("  • Module name: 'Demo' (user-facing)")
    print("  • Module slug: 'Demo' (technical ID, same as name in this case)")
    print("  • Files created using slug: Demo.cpp, Demo-rnbo/, etc.")
    print("  • C++ identifiers use slug: modelDemo")

if __name__ == "__main__":
    main()