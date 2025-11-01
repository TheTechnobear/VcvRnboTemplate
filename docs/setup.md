# Setup Guide

This guide covers setting up your development environment and testing it with a demo project.

⚠️ **Recommendation**: Complete this setup and test the demo before purchasing Max/RNBO to ensure everything works on your system.

## Prerequisites

- **Free**: Development tools (covered in this guide)
- **Paid**: Max 8/9 with RNBO 1.4.2+ (needed only for creating modules, not using them)

## Installation Steps

### 1. Install Build Requirements

**VCV Rack Build Tools:**
Follow the [VCV Rack Building Guide](https://vcvrack.com/manual/Building) for your platform. **Only complete the setup steps** - we're not creating a module yet, just installing build requirements.

**Windows Users**: The VCV guide will tell you to install MSYS2. After installation, always use the **MinGW 64-bit shell** from your Start menu for all commands in this project.

**ARM Toolchain (for MetaModule):**
Download ARM GNU Toolchain 12.2 or 12.3 from [ARM Developer Downloads](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads). Get the package for your host computer ending in `arm-none-eabi`. 
Ensure it's on your PATH.
e.g. for windows using MSYS32, assuming default install
```bash 
export PATH=/c/Program\ Files\ \(x86\)/Arm\ GNU\ Toolchain\arm-none-eabi/12.3\ rel1/bin:$PATH
```

### 2. Get the Project

**Option A: Fork Repository (Recommended)**

This allows you to save your work and share plugins:

1. Create a free GitHub account at [github.com](https://github.com)
2. Go to [https://github.com/TheTechnobear/VcvRnboTemplate](https://github.com/TheTechnobear/VcvRnboTemplate)
3. Click "Fork" and name it meaningfully (e.g., `MyVcvModules`)
4. Clone your fork:

```bash
git clone https://github.com/[YourUsername]/[YourRepoName].git
cd [YourRepoName]
git submodule update --init --recursive
git remote add upstream https://github.com/TheTechnobear/VcvRnboTemplate.git
```

**Option B: Direct Clone (Not Recommended)**

```bash
git clone https://github.com/TheTechnobear/VcvRnboTemplate.git
cd VcvRnboTemplate
git submodule update --init --recursive
```

### 3. Install VCV Rack SDK

Download the Rack SDK from the [VCV Rack Building Guide](https://vcvrack.com/manual/Building). Extract it to the project root:

```
./Rack-SDK/
```

## Test Your Setup

Verify everything works with the included demo:

```bash
# Check environment
python3 scripts/check.py

# Create test plugin
python3 scripts/createPlugin.py

# Add demo module
python3 scripts/addDemo.py

# Build for VCV Rack
cd VcvModules && make

# Build for MetaModule
cd .. && cmake --fresh -B build && cmake --build build
```

If all builds succeed, you're ready to create modules!

## Optional: Test in VCV Rack

```bash
cd VcvModules && make dist
```

Copy the generated plugin to your VCV Rack plugins directory and test the Demo module.

## Cleanup (Optional)

Remove the demo when ready to create your own modules:

```bash
python3 scripts/removeModule.py Demo
```

## Next Steps

- **[Creating Modules](createmodules.md)** - Build your first RNBO module
- **[More Information](more.md)** - Advanced topics and customization


---------


## Tips - Terminal/Command Line Setup

This project uses command line tools. You'll need to open a terminal and run text commands.

### Windows Users ⚠️
**Critical**: Install [MSYS2](https://www.msys2.org/) and **always use the MinGW 64-bit shell** from the Start menu for all commands in this guide. 

- ❌ **Don't use**: Command Prompt, PowerShell, or Git Bash
- ✅ **Do use**: MSYS2 MinGW 64-bit shell

The VCV Rack setup guide will walk you through MSYS2 installation.

### macOS Users  
Use the built-in **Terminal** app (Applications → Utilities → Terminal).

### Linux Users
Use your distribution's terminal (usually Ctrl+Alt+T).

### Basic Terminal Usage
- Commands are the text shown in code blocks (e.g., `python3 scripts/check.py`)
- Type or copy-paste commands and press Enter
- Use `cd [directory]` to change directories
- Use `ls` (Mac/Linux) or `dir` (Windows) to list files

**💡 Tip**: You can usually copy-paste commands directly from this guide into your terminal.


