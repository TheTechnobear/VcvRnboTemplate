#!/usr/bin/env python3
"""
Verify that __MOD__ and __MODNAME__ placeholders are working correctly
"""

import json
from pathlib import Path

def main():
    project_root = Path.cwd()
    
    print("🔍 Verifying __MOD__ and __MODNAME__ placeholder substitution...")
    print("=" * 60)
    
    # Check plugin.json for Demo module
    plugin_json = project_root / "VcvModules" / "plugin.json"
    if plugin_json.exists():
        with open(plugin_json) as f:
            data = json.load(f)
            modules = data.get('modules', [])
            demo_module = next((m for m in modules if m['slug'] == 'Demo'), None)
            
            if demo_module:
                print("[PASS] Demo module found in plugin.json:")
                print(f"  - Slug: '{demo_module['slug']}' (used for technical IDs)")
                print(f"  - Name: '{demo_module['name']}' (user-facing display)")
    
    # Check Demo.cpp for correct placeholder substitution
    demo_cpp = project_root / "VcvModules" / "src" / "Demo.cpp"
    if demo_cpp.exists():
        with open(demo_cpp) as f:
            content = f.read()
            
        print(f"\n[CODE] Verifying placeholder substitution in Demo.cpp:")
        
        # Check __MODNAME__ -> "Demo" (user-facing display in label)
        if '"Demo"' in content and 'addLabel' in content:
            print("[PASS] __MODNAME__ correctly replaced with \"Demo\" for user display")
        else:
            print("[ERROR] __MODNAME__ substitution not found")
            
        # Check __MOD__ -> Demo (technical identifiers)
        technical_usages = [
            'struct Demo : Module',
            'RNBO::DemoRnbo<',
            'Model* modelDemo =',
            'struct DemoWidget :',
            '#include "Demo-rnbo/Demo.cpp.h"'
        ]
        
        for usage in technical_usages:
            if usage in content:
                print(f"[PASS] __MOD__ correctly replaced: {usage}")
            else:
                print(f"[ERROR] __MOD__ substitution missing: {usage}")
        
        # Check __PANEL__ -> Blank10U.svg
        if 'res/Blank10U.svg' in content:
            print("[PASS] __PANEL__ correctly replaced with 'Blank10U.svg'")
        else:
            print("[ERROR] __PANEL__ substitution not found")
    
    print(f"\n[TARGET] Summary:")
    print("  - __MODNAME__ is used for user-facing display text (can have spaces)")
    print("  - __MOD__ is used for technical identifiers (no spaces, safe for C++)")
    print("  - __PANEL__ is used for SVG panel filename")
    print("  - Both name and slug are preserved in JSON for proper identification")

if __name__ == "__main__":
    main()