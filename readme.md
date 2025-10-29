# VCV Rack RNBO Template

Create VCV Rack and 4ms MetaModule plugins without programming! This project enables musicians and sound designers to build audio modules using Max RNBO's visual programming language. Simple scripts generate complete plugins from your RNBO patches, perfect for rapid prototyping or as a starting point for custom development. Test your DSP algorithms in Max, then seamlessly deploy to VCV Rack desktop for experimentation before finalizing on MetaModule hardware.

## Setup

### 1. Install VCV Rack Build Requirements

Follow the setup instructions at [VCV Rack Building Guide](https://vcvrack.com/manual/Building) for your platform. 
**Only complete the setup steps**, we only need build requiremetns fulfilled, we are not creating a module (yet)

### 2. Fork and Clone Repository

1. **Fork this repository** on GitHub:
   - Go to [https://github.com/TheTechnobear/VcvRnboTemplate](https://github.com/TheTechnobear/VcvRnboTemplate)
   - Click the "Fork" button
   - Give it a meaningful name like `MyVcvModules` or `[YourName]RnboModules`

2. **Clone your fork**:
```bash
git clone https://github.com/[YourUsername]/[YourRepoName].git
cd [YourRepoName]
git submodule update --init --recursive
```

3. **Set up upstream remote** (to pull template updates):
```bash
git remote add upstream https://github.com/TheTechnobear/VcvRnboTemplate.git
```

This way you can save and version control your modules as you create them, and pull template improvements when available!


### 3. Download VCV Rack SDK

Download the Rack SDK for your platform from the [VCV Rack Building Guide](https://vcvrack.com/manual/Building). Unpack the zip file and place it in root directoy of this project
```
./Rack-SDK/
```

### 4. Install ARM Toolchain (for MetaModule)

Download the ARM GNU Toolchain 12.2 or 12.3 from [ARM Developer Downloads](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads). 

**Important**: Get the package for your host computer that ends in `arm-none-eabi`.

Ensure the compiler is on your PATH. See [MetaModule Plugin Examples](https://github.com/4ms/metamodule-plugin-examples) for detailed setup.

## Test Your Environment

Verify your setup is working correctly:

```bash
# Check environment and project status
python3 scripts/check.py

# If environment is ready, test with demo:
# a) Create a test plugin
python3 scripts/createPlugin.py

# b) Add demo module
python3 scripts/addDemo.py

# c) Build for VCV Rack desktop
cd VcvModules
make

# d) test Demo module within VCV (optional)
make dist
# copy the plugin to your VCV plugins directory

# e) Build for MetaModule hardware
# from the project directory
cd ..
cmake --fresh -B build 
cmake --build build

# f) Test module on the Metamodule (optional)
# copy the mmplugin file to your metamodule sdcard plugins folder


# e) remove demo plugin (optional)
python3 scripts/removeModule Demo
```

If all builds succeed, your environment is correctly configured!

## Create Plugin

if you did the above, you will have already created your plugin (which holds all your modules.
if not, then you will need to create the plugin before creating any modules.

```bash
python3 scripts/createPlugin.py
```



## Creating RNBO Module(s)

### 1. Create RNBO Patch in Max

Create your audio patch in Max/MSP using RNBO objects.

### 2. Test in Max

Test your RNBO patch thoroughly in Max to ensure it works as expected.

### 3. Save Max Patch

Save your Max patch in the VcvModules/max directory:
```
VcvModules/max/YourPatchName.maxpat
```

### 4. Create Module Structure

```bash
python3 scripts/createModule.py
```

Follow the prompts to enter module name, description, and tags. This creates the module structure including the `[ModuleName]-rnbo/` directory for export.

### 5. Export RNBO Module

In Max, export your RNBO patch with these **exact settings**:

**Example for module named "Demo":**
- **Export Type**: C++ 
- **Output Directory**: `VcvModules/src/Demo-rnbo/`
- **Export Name**: `Demo.cpp.h`
- **Export Options**:
  - ✅ Minimal Export (checked)
  - ❌ Copy C++ library code (unchecked) 
  - **Codegen Class Name**: `DemoRnbo`

**Critical**: The codegen class name must be `[ModuleName]Rnbo` (e.g., "Demo" → "DemoRnbo").

### 6. Build VCV Module

```bash
cd VcvModules 
make
```

### 7. Test in VCV Rack
```bash
make dist
```
Copy the plugin to your vcv rack plugin folder
Launch VCV Rack and test your module to ensure it works correctly on desktop.

### 8. Build MetaModule

From this project directory
```bash
cd ..
cmake --fresh -B build
cmake --build build
```

### 9. Test on MetaModule

Copy the mmplugin file to your metamodule sdcard plugins folder, and test on your hardware.


# Further information 

## Generated module code
You only need to use createModule once for each module.
if you wish to change the rnbo code, just re-export as you did the first time, then rebuild.

also, the code generated is 'separate' from the original template, so you can modify the code if you wish.
in this way, you can create fully customised UI (more details later), or edit the code for more advanced features.

## Editing code
if you want to go further, then Id recommend you use a code editor to edit code.
I use [VSCode](https://code.visualstudio.com) aka Visual Studio Code , which is free


## External Documentation

- [4ms MetaModule Plugin SDK](https://github.com/4ms/metamodule-plugin-sdk) - Complete MetaModule development documentation
- [VCV Rack Plugin Development Tutorial](https://vcvrack.com/manual/PluginDevelopmentTutorial) - Official VCV Rack plugin development guide

## Scripts Reference

- `check.py` - Check environment setup and project status
- `createPlugin.py` - Initialize a new plugin project
- `createModule.py` - Add a module to your plugin
- `addDemo.py` - Add a working demo module
- `removeModule.py` - Remove a specific module

## Directory Structure

```
[YourRepoName]/
├── Rack-SDK/             # VCV Rack SDK (download and place here)
├── VcvModules/           # VCV Rack plugin source
│   ├── src/              # Plugin source code
│   │   ├── plugin.hpp    # Plugin header declarations
│   │   ├── plugin.cpp    # Plugin initialization
│   │   └── ModuleName.cpp/ # module implementation (can be multiple)
│   │   └── ModuleName-rnbo/ # RNBO export directory for a module (and be multiple)
│   ├── max/              # Max patches
├── scripts/              # Automation scripts
├── templates/            # Code generation templates
├── metamodule-plugin-sdk/ # MetaModule build system
└── plugin-mm.json        # MetaModule configuration
```

## Updating Template

To pull the latest template improvements and bug fixes:

```bash
# Fetch updates from the original template
git fetch upstream

# Merge updates into your main branch
git merge upstream/master

# Update submodules if needed
git submodule update --init --recursive
```

**Note**: If you've customized template files or scripts, you may need to resolve merge conflicts. Your modules and plugin configurations will be preserved.
