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
  - Core scripts: `check.py`, `createPlugin.py`, `createModule.py`, `removeModule.py`, `addDemo.py`
  - Testing scripts: `scripts/test/` directory contains validation and debugging tools
- **`VcvModules/inc/rnbo-export/`**: RNBO C++ runtime headers (Cycling '74's audio engine)

**Development Strategy:** Create MetaModule hardware plugins but test them on desktop VCV Rack first for faster iteration.

## RNBO Integration Pattern

**Critical Understanding:** Each module wraps a single RNBO patch following this structure:
```cpp
// Required RNBO configuration defines at top of .cpp files
#define RNBO_NOTHROW
#define RNBO_FIXEDLISTSIZE 64
#define RNBO_NO_PATCHERFACTORY
#include "__MOD__-rnbo/__MOD__.cpp.h"  // Generated RNBO C++ export

struct __MOD__ : Module {
    struct RNBOPatch {
        RNBO::__MOD__Rnbo<RNBO::MinimalEngine<>> patch_;
        // Buffer management for inputs/outputs/parameters
        int nInputs_, nOutputs_, nParams_;
        RNBO::number** inputBuffers_;
        RNBO::number** outputBuffers_;
        float* lastParamVals_;
    } rnbo_;
};
```

**RNBO Buffer Management:** Always use `bufferSize_ = 1` for sample-by-sample processing in VCV Rack. The `curBufPos_` mechanism accumulates samples before calling RNBO's batch processor.

**Generic UI System:** Templates include automatic UI generation with two modes:
- **GENERIC_UI**: Auto-generated layout based on RNBO patch introspection
- **Custom UI**: Manual panel design using VCV Rack helper tools
- **GENERIC_TITLE_LABEL**: Optional module title display

## Template Substitution System

Templates use these placeholders for code generation:
- `__MOD__`: Technical module identifier/slug (e.g., "Reverb" for class names, file names, no spaces/special chars)
- `__MODNAME__`: User-facing module display name (e.g., "My Reverb Effect" - can contain spaces, special chars)
- `__PANEL__`: Panel selection for UI (Basic, Advanced, Custom)
- `__BRAND__`: Plugin brand/slug 
- `__AUTHOR__`, `__EMAIL__`, `__URL__`: Metadata fields

**Critical Substitution Order:** Process `__MODNAME__` before `__MOD__` to prevent substring conflicts since "MOD" appears in "MODNAME".

**Module Identification Strategy:**
- **Slug** (`__MOD__`): Used for technical identifiers (class names, file names, JSON keys) - must be ASCII letters, numbers, underscores only
- **Name** (`__MODNAME__`): Used for user-facing display - can contain any characters including spaces and Unicode
- **Validation**: Scripts validate slug format but allow flexible naming for display names

**Platform-Specific Templates:** 
- `templates/vcv/`: Contains VCV Rack Makefile, plugin.json, and C++ source templates
- `templates/metamodule/`: Contains MetaModule CMakeLists.txt and plugin-mm.json templates
- Scripts automatically select appropriate templates based on target platform

**Pattern:** Template files like `templates/vcv/src/template.cpp` become actual modules through automated Python script substitution, enabling users with minimal development experience to create plugins from RNBO exports.

## UI Generation Strategy

**Auto-Layout Pattern:** Modules use dynamic UI generation based on RNBO patch introspection:
```cpp
// Query RNBO patch for parameters/IO at widget construction
RNBO::__MOD__Rnbo<RNBO::MinimalEngine<>>* pPatch = module->getRnboPatch();
int nParams = pPatch->getNumParameters();
int nInputs = pPatch->getNumInputChannels();
int nOutputs = pPatch->getNumOutputChannels();
// Auto-generate knobs/ports in grid layout with wrapping
```

**UI Mode Selection:**
- **GENERIC_UI**: Automatic layout generation with parameter wrapping and labeling
- **Custom UI**: Manual panel design using `$RACK_DIR/helper.py createmodule` workflow
- **Panel Integration**: Uses `__PANEL__` placeholder for different panel styles (Basic/Advanced/Custom)

**UI Layout Features:**
- Automatic parameter name extraction from RNBO patch
- Grid-based layout with intelligent wrapping
- Responsive sizing based on panel width
- Support for both preview mode (module == null) and runtime
- Custom label styling and positioning

This eliminates manual UI coding - the widget adapts to any RNBO patch's parameter count and automatically handles layout.

## Build System

**VCV Rack (Desktop Testing):** Uses standard VCV plugin Makefile in `VcvModules/`:
- Requires C++17: `CXXFLAGS += -std=c++17`
- Include path: `-Iinc/rnbo-export/common`
- Build with: `make` in `VcvModules/` directory

**MetaModule (Hardware Target):** Uses CMake with ARM toolchain in base directory:
- ARM toolchain configured in `CMakePresets.json`
- **Windows**: Build with `cmake --fresh -B build -G "MSYS Makefiles"` then `cmake --build build`
- **macOS/Linux**: Build with `cmake --fresh -B build` then `cmake --build build`
- Requires MetaModule SDK and ARM GNU Toolchain

## Development Workflow

**Script-Based Development Process:**
1. **`scripts/check.py`** - Verify environment setup and dependencies before starting
2. **`scripts/test/reset.py`** - Reset project to have no plugin (clean slate)
3. **`scripts/addDemo.py`** - Add demo files from templates to test development environment setup for both VCV and MetaModule builds
4. **`scripts/createPlugin.py`** - Enter plugin metadata (name, maintainer, etc.) to populate `plugin.json` and `plugin-mm.json`
5. **`scripts/createModule.py`** - Create and add a module to the plugin using templates, updates plugin manifests automatically
6. **`scripts/removeModule.py`** - Remove a module from the plugin (cleans up all associated files and manifest entries)

**Enhanced createModule.py Workflow:**
1. **Slug Input First**: Prompts for module slug with validation (letters, numbers, underscores only)
   - Provides helpful error messages with examples for invalid input
   - Explains slug is used for technical identifiers (file names, class names)
2. **Module Name Input**: Prompts for user-facing display name (no restrictions, can contain spaces/Unicode)
3. **Panel Selection**: Choose from Basic, Advanced, or Custom panel templates
4. **Template Processing**: Substitutes `__MODNAME__` first, then `__MOD__` to avoid conflicts

**RNBO Integration Steps:**
1. **Export RNBO patch** from Max/MSP to `ModuleName-rnbo/` directory (contains `.cpp.h` and JSON metadata)
   - **Critical:** Use minimal export settings to reduce external dependencies
   - Disable unnecessary features like file I/O, networking, or advanced MIDI
2. **Run `createModule.py`** to generate module from template (substitutes placeholders)
3. **Build** using appropriate build system (Make for VCV, CMake for MetaModule)

**Cross-Platform Compatibility:**
- All Python scripts use ASCII-only characters for maximum compatibility
- Unicode symbols replaced with ASCII equivalents (e.g., `[ERROR]`, `[OK]`, `[TOOL]`)
- Ensures scripts work on systems with limited Unicode support

**Important:** A plugin is a collection of modules. Each RNBO patch becomes one module within a plugin.

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

## Development Context & Troubleshooting

**Recent Enhancements (November 2024 - January 2025):**
- Enhanced template system with dual placeholders: `__MOD__` (technical) and `__MODNAME__` (display)
- Improved user experience in `createModule.py` with slug-first input flow and validation
- Cross-platform compatibility improvements with ASCII-only characters in all scripts
- Panel selection system integrated into module creation workflow
- Added `removeModule.py` script for clean module removal
- Enhanced debugging and testing scripts in `scripts/test/` directory

**Common Issues & Solutions:**

**Template Substitution Problems:**
- **Issue**: Placeholder conflicts when `__MOD__` gets replaced inside `__MODNAME__`
- **Solution**: Always process `__MODNAME__` before `__MOD__` in substitution order
- **Code Pattern**: `content = content.replace('__MODNAME__', module_name).replace('__MOD__', module_slug)`

**Slug Validation:**
- **Issue**: Module slugs with spaces or special characters cause build failures
- **Solution**: Validate slugs using regex `^[a-zA-Z][a-zA-Z0-9_]*$` 
- **User Guidance**: Provide clear error messages with valid examples

**Script Compatibility:**
- **Issue**: Unicode characters in scripts cause failures on some systems
- **Solution**: Use ASCII equivalents (`[ERROR]`, `[OK]`, `[TOOL]` instead of Unicode symbols)
- **Testing**: Verify scripts work across different terminal environments

**RNBO Integration Best Practices:**
- Always use `bufferSize_ = 1` for VCV Rack sample-by-sample processing
- Implement parameter change detection to avoid unnecessary RNBO calls
- Include required RNBO defines at the top of generated C++ files
- Test with minimal RNBO exports before adding complex features
- Use proper compiler warning suppression around RNBO includes:
  ```cpp
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wsign-compare"
  #pragma GCC diagnostic ignored "-Wswitch"
  #pragma GCC diagnostic ignored "-Wunused-variable"
  #include "__MOD__-rnbo/__MOD__.cpp.h"
  #pragma GCC diagnostic pop
  ```

**Template System Features:**
- **Conditional UI compilation**: `#ifdef GENERIC_UI` allows switching between auto and custom layouts
- **Title label control**: `#define GENERIC_TITLE_LABEL` enables/disables module title display
- **Panel placeholder**: `__PANEL__` supports Basic.svg, Advanced.svg, Custom.svg panel selection
- **RNBO platform customization**: Custom print functions and platform-specific defines
- **Memory management**: Proper allocation/deallocation of RNBO buffers and parameter arrays
- **Preview mode support**: UI generation works both in runtime and VCV Rack's preview mode

**File Structure Validation:**
- Ensure RNBO exports are in `ModuleName-rnbo/ModuleName.cpp.h` format
- Verify template files exist before attempting substitution
- Check that panel SVG files are created in `res/` directory
- Validate plugin manifest updates for both VCV and MetaModule platforms

**Testing and Validation Workflow:**
- Use `scripts/test/verifyDemo.py` to validate demo module functionality
- Use `scripts/test/testSlugValidation.py` to test module naming validation
- Use `scripts/test/verifyPlaceholders.py` to check template substitution
- Use `scripts/check.py` to verify complete environment setup before starting development

**Build System Debugging:**
- VCV Rack: Check `CXXFLAGS += -std=c++17` and include paths
- MetaModule: Verify ARM toolchain installation and CMake preset configuration
- **Windows**: Use MSYS Makefiles generator: `cmake -G "MSYS Makefiles"`
- Cross-platform: Test builds on both desktop (VCV) and hardware (MetaModule) targets