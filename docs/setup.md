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
Download ARM GNU Toolchain 12.3 from [ARM Developer Downloads](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads). 
Get the package for your host computer ending in `arm-none-eabi`, you can use the exe for windows, and pkg for mac. 
use defaults when installing.

**Setup your path**
To ensure you the correct version of the tools you have installed above you will want to set up your path correctly,
every time you use these tools - see section at the base of this page.


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
# Windows (MSYS2)
cd .. && cmake --fresh -B build -G "MSYS Makefiles" && cmake --build build

# macOS/Linux  
cd .. && cmake --fresh -B build && cmake --build build
```
*If any build fails, run `python3 scripts/check.py` to verify your setup*

If all builds succeed, you're ready to create modules!

## Optional: Test in VCV Rack

```bash
cd VcvModules && make dist
```
*If build fails, run `python3 scripts/check.py` to verify your setup*

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

**💡 Tip**: You can usually copy-paste commands directly from this guide into your terminal.

### Basic Terminal Usage
- Commands are the text shown in code blocks (e.g., `python3 scripts/check.py`)
- Type or copy-paste commands and press Enter
- Use `cd [directory]` to change directories
- Use `ls`


This project uses command line tools. You'll need to open a terminal and run text commands, 

you will also need to ensure, that your path is set correctly, to ensure correct versions of tools are used.

### Windows Users ⚠️
**Critical**: Install [MSYS2](https://www.msys2.org/) and **always use the MinGW 64-bit shell** from the Start menu for all commands in this guide. 

- ❌ **Don't use**: Command Prompt, PowerShell, or Git Bash
- ✅ **Do use**: MSYS2 MinGW 64-bit shell

The VCV Rack setup guide will walk you through MSYS2 installation.

It's important to note we are using MSYS2 as a terminal for windows usage, this provides a 'unix like' experience.
so if you need help with using the terminal, guides on the 'windows terminal/power sheel' are not useful.
instead, you need check on MSYS2 website, or even linux terminal usage.

why do we use msys2? vcv dev tools are based on/require it.
why did vcv use it? because this means tools/scripts between mac/linux and windows can be similar.




#### Setting path
you will need to add the arm toolchain you installed to your path.
assuming you installed to the default location you can use.
```bash 
export PATH=/c/Program\ Files\ \(x86\)/Arm\ GNU\ Toolchain\ arm-none-eabi/12.3\ rel1/bin:$PATH
```

#### Keeping path across sessions (optional)
if you enter the above, you will have to do this every time you start a session.
if you wish to 'save' this, you can add this to .bash_profile
by default you'll find it here:  ```C:\MSYS2\home\[username]`\.bash_profile```

-----

### macOS Users  
Use the built-in **Terminal** app (Applications → Utilities → Terminal).
first, we need to add homebrew to our path, this varies based on your mac.
apple silicon 
```bash
export PATH="/opt/homebrew/bin:${PATH}"
```
intel macs
```bash
export PATH="/opt/local/bin:${PATH}"
```

next, you will need to add the arm toolchain you installed to your path.
make sure use use the directory you installed to.
e.g.
```bash
export PATH="/Applications/ArmGNUToolchain/12.3.rel1/arm-none-eabi/bin:${PATH}"
```

#### Keeping path across sessions (optional)
if you enter the above, you will have to do this every time you start a session.
if you wish to 'save' this, you can add this to your.zshrc in your home directory
e.g ```/Users/[username]/.zshrc```

note: older versions of macOS use .bash_profile instead.

videos/chatgpt can show you how search for "how to change your path on macos".


-----

### Linux Users
Use your distribution's terminal (usually Ctrl+Alt+T).

On Linux, tools are usually added to your path automatically.
if you get errors you may need to add or edit your path, 
unfortunately, this will be dependent on the shell you use (bash/zsh etc) and install location.
so is beyond the scope of this guide. 
however, there are many resources online that can help you set this up correctly 

note: if you get errors, that are not 'command not found' (etc), check that the correct version of the tool is being used.
useful command to debug errors : 
- use ```which [command]``` to determine find where a command is being picked up from.
- use ```echo $PATH``` to see what your current path is.

generally, Id consider Linux for more advance users that are familar with command line usage, as this is the nature of the beast for linux.








