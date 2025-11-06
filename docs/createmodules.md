# Creating RNBO Modules

Transform your Max RNBO patches into VCV Rack and MetaModule plugins!

**Prerequisites**: Complete the [Setup Guide](setup.md) and test with the demo module.

## Understanding Plugins vs Modules

- **Plugin**: A collection of one or more modules (you create one plugin per project)
- **Module**: Individual audio processors within a plugin (you can create many modules)

## Workflow Overview

```
Max RNBO Patch → Export C++ → Build VCV → Test → Build MetaModule → Deploy
```

## Creating Your First Module

### 1. Design in Max

Create your audio patch in Max/MSP using RNBO objects. Test thoroughly in Max before exporting.
You can learn more about RNBO patching [here](https://rnbo.cycling74.com)

**💡 Tip**: Save your Max (.maxpat) **and** RNBO patch (.rnbopat) in `VcvModules/max/`for organization.

### 2. Create Plugin
If you have not already created your plugin.
note: setup will have already asked you to do this.

```bash
python3 scripts/createPlugin.py
```


### 3. Create Module Structure

```bash
python3 scripts/createModule.py
```

Follow prompts for:
- **Module Slug** (e.g., "MyReverb")  
- **Module Name** (e.g., "My Reverb")
- **Select Panel** (e.g. 1 for Blank10U.svg) 
- **Description** (e.g., "RNBO reverb module")
- **Tags** (audio, effect, reverb, etc.)

This creates the module source code (in `VcvModules/src`) and `VcvModules/src/[ModuleSlug]-rnbo/` directory.

### 4. Export from Max

In Max, export your RNBO patch with these **exact settings**:

**For module named "Reverb":**
- **Export Type**: C++ 
- **Output Directory**: `VcvModules/src/Reverb-rnbo/` 
- **Export Name**: `Reverb.cpp.h`
- **Codegen Class Name**: `ReverbRnbo`
- **Export Options**:
  - ✅ Minimal Export
  - ❌ Copy C++ library code

⚠️ **Critical**: Codegen class name must be `[ModuleSlug]Rnbo`

### 5. Build and Test

**Build for VCV Rack:**
```bash
cd VcvModules && make
```
*If build fails, run `python3 scripts/check.py` to verify your setup*

**Test in VCV Rack (Recommended):**
copy and install plugin into VCV rack
```bash
make install
```

**Build for MetaModule:**
```bash
# Windows (MSYS2)
cmake --fresh -B build -G "MSYS Makefiles" && cmake --build build

# macOS/Linux
cmake --fresh -B build && cmake --build build

```
*If build fails, run `python3 scripts/check.py` to verify your setup*

## 6. Run and test on your 4ms MetaModule 
- Copy .mmplugin to MetaModule SD card into metamodule-plugins directory
- Restart 4ms metamodule, use scan plugins to find new plugin

## Development Tips

### Quick Iteration
- **Update RNBO**: Just re-export (step 3) and rebuild (step 4)
- **No need to recreate**: Module structure persists across RNBO updates

### Testing Strategy
1. **Max**: Test patch functionality
2. **VCV Rack**: Verify module integration and UI
3. **MetaModule**: Final hardware validation

### Troubleshooting

**Check Environment**: `python3 scripts/check.py`

**Common Issues**:
- Wrong export filename → Use exact naming: `[ModuleSlug].cpp.h`
- Missing codegen class → Set to `[ModuleSlug]Rnbo`
- Build errors → Check toolchain installation and on path
- Windows users use :  MSYS2 MinGW 64-bit shell (not command prompt/powershell)

**Get Help**: [4ms MetaModule Forum](https://forum.4ms.info)

## Advanced Topics

### Custom UI
The generated UI is generic but functional. You can create custom panel designs with basic SVG editing.

### Code Customization  
Generated C++ code can be modified for advanced features. Your changes persist across template updates.

### Module Management
```bash
# Remove a module
python3 scripts/removeModule.py [ModuleSlug]

# Reset entire project
python3 scripts/test/reset.py
```

### Platform Flexibility
- **VCV Only**: Skip MetaModule build steps
- **MetaModule Only**: Skip VCV steps (though testing in VCV first is recommended)

## Next Steps

- **[Advanced Topics](more.md)** - Customization and development
- **[Cross-Platform](crossplatformnotes.md)** - Windows/macOS compatibility
