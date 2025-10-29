# VCV Rack RNBO Template - AI Coding Instructions

## Architecture Overview

This is a template system for creating VCV Rack plugins that wrap Cycling '74 RNBO (audio DSP) patches. It supports dual-platform deployment: VCV Rack modules and MetaModule hardware.

**Key Components:**
- **Base directory**: 4ms MetaModule hardware-specific build configuration (CMake with ARM toolchain)
- **`VcvModules/`**: Cross-platform VCV Rack plugin source for desktop testing (contains example `Demo` module)
- **`templates/`**: Platform-specific template files with placeholder substitution (`__MOD__`, `__BRAND__`, etc.)
  - `templates/vcv/`: VCV Rack-specific templates (Makefile, plugin.json, source templates)
  - `templates/metamodule/`: MetaModule-specific templates (CMakeLists.txt, plugin-mm.json)
- **`scripts/`**: Python automation enabling users with minimal development experience to create plugins from RNBO exports
- `inc/rnbo-export/`: RNBO C++ runtime headers (Cycling '74's audio engine)

**Development Strategy:** Create MetaModule hardware plugins but test them on desktop VCV Rack first for faster iteration.

## RNBO Integration Pattern

**Critical Understanding:** Each module wraps a single RNBO patch following this structure:
```cpp
// Required RNBO configuration defines at top of .cpp files
#define RNBO_NOTHROW
#define RNBO_FIXEDLISTSIZE 64
#define RNBO_NO_PATCHERFACTORY
#include "__MOD__-rnbo/__MOD__.cpp.h"  // Generated RNBO C++ export

struct ModuleName : Module {
    struct RNBOPatch {
        RNBO::ModuleNameRnbo<RNBO::MinimalEngine<>> patch_;
        // Buffer management for inputs/outputs/parameters
    } rnbo_;
};
```

**RNBO Buffer Management:** Always use `bufferSize_ = 1` for sample-by-sample processing in VCV Rack. The `curBufPos_` mechanism accumulates samples before calling RNBO's batch processor.

## Template Substitution System

Templates use these placeholders for code generation:
- `__MOD__`: Module class name (e.g., "Reverb" → "ReverbRnbo")
- `__BRAND__`: Plugin brand/slug 
- `__AUTHOR__`, `__EMAIL__`, `__URL__`: Metadata fields

**Platform-Specific Templates:** 
- `templates/vcv/`: Contains VCV Rack Makefile, plugin.json, and C++ source templates
- `templates/metamodule/`: Contains MetaModule CMakeLists.txt and plugin-mm.json templates
- Scripts automatically select appropriate templates based on target platform

**Pattern:** Template files like `templates/vcv/src/template.cpp` become actual modules through automated Python script substitution, enabling users with minimal development experience to create plugins from RNBO exports.

## UI Generation Strategy

**Auto-Layout Pattern:** Modules use dynamic UI generation based on RNBO patch introspection:
```cpp
// Query RNBO patch for parameters/IO at widget construction
int nParams = pPatch->getNumParameters();
int nInputs = pPatch->getNumInputChannels();
// Auto-generate knobs/ports in grid layout
```

This eliminates manual UI coding - the widget adapts to any RNBO patch's parameter count.

## Build System

**VCV Rack (Desktop Testing):** Uses standard VCV plugin Makefile in `VcvModules/`:
- Requires C++17: `CXXFLAGS += -std=c++17`
- Include path: `-Iinc/rnbo-export/common`
- Build with: `make` in `VcvModules/` directory

**MetaModule (Hardware Target):** Uses CMake with ARM toolchain in base directory:
- ARM toolchain configured in `CMakePresets.json`
- Build with: `cmake --fresh -B build` then `cmake --build build`
- Requires MetaModule SDK and ARM GNU Toolchain

## Development Workflow

**Script-Based Development Process:**
1. **`reset.py`** - Reset project to have no plugin (clean slate)
2. **`addDemo.py`** - Add demo files from templates to test development environment setup for both VCV and MetaModule builds
3. **`createPlugin.py`** - Enter plugin metadata (name, maintainer, etc.) to populate `plugin.json` and `plugin-mm.json`
4. **`createModule.py`** - Create and add a module to the plugin using templates, updates plugin manifests automatically

**RNBO Integration Steps:**
1. **Export RNBO patch** from Max/MSP to `ModuleName-rnbo/` directory (contains `.cpp.h` and JSON metadata)
   - **Critical:** Use minimal export settings to reduce external dependencies
   - Disable unnecessary features like file I/O, networking, or advanced MIDI
2. **Run `createModule.py`** to generate module from template (substitutes placeholders)
3. **Build** using appropriate build system (Make for VCV, CMake for MetaModule)

**Important:** A plugin is a collection of modules. Each RNBO patch becomes one module within a plugin.

**Important:** Never manually edit generated modules - always modify templates and regenerate.

**Important:** Never manually edit generated modules - always modify templates and regenerate.

## File Naming Conventions

- **Plugin manifests:** `plugin.json` (VCV) and `plugin-mm.json` (MetaModule) - contain plugin metadata and module listings
- **RNBO exports:** `ModuleName-rnbo/ModuleName.cpp.h` - one per module
- **Module source:** `ModuleName.cpp` (generated from `template.cpp`) - one per module
- **UI panels:** `res/ModuleName.svg` - one per module
- **Models registered as:** `modelModuleName` in `plugin.cpp` - one per module

**Plugin Structure:** One plugin contains multiple modules, each wrapping a single RNBO patch.

## Parameter Synchronization

Parameters sync only on change to avoid unnecessary RNBO calls:
```cpp
if (rnbo_.lastParamVals_[i] != param) {
    rnbo_.patch_.setParameterValue(i, param, RNBO::TimeNow);
    rnbo_.lastParamVals_[i] = param;
}
```

This pattern is essential for performance with RNBO patches.

## RNBO Export Configuration

**Minimal Export Strategy:** To minimize external dependencies and ensure compatibility:
- Use C++ export with minimal feature set
- Avoid file I/O, networking, or system-dependent features
- Keep patches simple with basic audio processing objects
- Test exports work with the provided RNBO defines (`RNBO_NOTHROW`, `RNBO_NO_PATCHERFACTORY`, etc.)