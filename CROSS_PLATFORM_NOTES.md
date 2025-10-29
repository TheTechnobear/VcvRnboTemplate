# Cross-Platform Compatibility Notes

## Overview
This VCV Rack RNBO Template system has been designed and tested for cross-platform compatibility, primarily between macOS and Windows. The automation scripts handle platform-specific differences automatically.

## Python Requirements
- **Python 3.6+** required for f-string support
- Use `python3` command explicitly on systems where `python` defaults to Python 2.7
- All scripts tested with Python 3.x on macOS

## Windows Compatibility

### Line Endings
- All Python scripts now use `newline='\n'` parameter when writing files
- This ensures consistent Unix-style line endings across all platforms
- Critical for C++ source files and Makefiles that expect Unix line endings

### ARM Toolchain Detection
- `scripts/check.py` includes Windows-specific guidance for ARM toolchain setup
- Detects Windows platform (`os.name == 'nt'`) and provides appropriate instructions
- Recommends MinGW-w64 or MSYS2 for ARM cross-compilation on Windows

### File Path Handling
- All scripts use `pathlib.Path` for cross-platform path handling
- Automatically handles Windows vs Unix path separators
- Uses `Path.resolve()` for absolute path resolution

## Platform-Specific Notes

### macOS/Linux
- Native support for `arm-none-eabi-gcc` toolchain
- Standard Unix tools (make, cmake) work out of the box
- Uses system Python 3.x installation

### Windows
- ARM toolchain requires manual installation (MinGW-w64/MSYS2)
- May need to adjust PATH environment variable for tools
- PowerShell or Command Prompt both supported
- Git Bash recommended for Unix-like environment

## Build System Compatibility

### VCV Rack Modules (Desktop)
- Uses standard GNU Make (cross-platform)
- Requires RACK_DIR environment variable or defaults to ../Rack-SDK
- C++17 compiler required (GCC, Clang, or MSVC with C++17 support)

### MetaModule (Hardware)
- Uses CMake (cross-platform)
- Requires ARM cross-compilation toolchain
- Target: ARM Cortex-A7 (32-bit)

## Testing Recommendations

### Before Release
1. Test all Python scripts on Windows with Python 3.x
2. Verify line endings in generated files are consistent
3. Test ARM toolchain detection on Windows
4. Validate that generated C++ code compiles on both platforms

### User Instructions
- Always use `python3` command in documentation
- Provide Windows-specific ARM toolchain setup instructions
- Include PATH environment variable setup for Windows users
- Test with both PowerShell and Command Prompt on Windows

## Known Issues
- Unicode characters in output may not display correctly in some Windows terminals
- ARM toolchain installation is more complex on Windows
- File permissions may differ between platforms (affects executable scripts)

## Future Improvements
- Consider providing pre-compiled ARM toolchain for Windows
- Add Windows batch file alternatives to Python scripts
- Implement automatic line ending detection and conversion
- Add Windows-specific installation documentation