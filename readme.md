# VCV Rack RNBO Template

Create VCV Rack and 4ms MetaModule plugins without programming! This project enables musicians and sound designers to build audio modules using Max RNBO's visual programming language. Simple scripts generate complete plugins from your RNBO patches, perfect for rapid prototyping or as a starting point for custom development. Test your DSP algorithms in Max, then seamlessly deploy to VCV Rack desktop for experimentation before finalizing on MetaModule hardware.

## Key Features

- **No Programming Required** - Use visual Max RNBO patches to create modules
- **Dual Platform** - Deploy to both VCV Rack (desktop) and 4ms MetaModule (hardware)  
- **Rapid Prototyping** - Quick workflow from idea to working module
- **Test Progression** - Max → VCV Rack → MetaModule hardware
- **Flexible Foundation** - Generated code can be customized further
- **Easy Sharing** - Share modules without requiring Max/RNBO for end users

## Requirements

**For Module Creation:**s
- Max 8 or 9 with RNBO 1.4.2+ (license or subscription required)
- Development environment (free - see setup)

**For Using Created Modules:**
- No Max/RNBO required for end users

⚠️ **Before Purchasing Max/RNBO**: Complete the setup and test the demo to ensure everything works on your system!

## Quick Start

**👉 Start Here**: **[Setup Environment](docs/setup.md)** - Install build tools and SDKs

**Note**: Commands below use the terminal/command line. Windows users should use MSYS2 MinGW 64-bit shell (see setup guide).

### Test Demo (No Max Required)
Before investing in Max/RNBO, test your setup with the included demo:

```bash
python3 scripts/check.py           # Verify environment
python3 scripts/createPlugin.py    # Create test plugin  
python3 scripts/addDemo.py         # Add demo module
cd VcvModules && make              # Build for VCV Rack
```

This builds a working module and confirms your setup works!

### Create Your First Module (With Max/RNBO)

Once you have Max/RNBO, creating modules is simple:

```bash
# 1. Create module template
python3 scripts/createModule.py

# 2. Export your RNBO patch to: VcvModules/src/[ModuleName]-rnbo/
#    (in Max: Export → C++ → [ModuleName].cpp.h)

# 3. Build
cd VcvModules && make              # For VCV Rack
cd .. && cmake --fresh -B build && cmake --build build  # For MetaModule
```

**That's it!** Your RNBO patch is now a working VCV/MetaModule module.

📖 **Detailed Guide**: **[Creating Modules](docs/createmodules.md)**

## Documentation

- **[Setup Guide](docs/setup.md)** - Environment setup, testing, and first steps
- **[Creating Modules](docs/createmodules.md)** - Complete workflow from RNBO to module  
- **[Advanced Topics](docs/more.md)** - Customization, updates, and development
- **[Cross-Platform Notes](docs/crossplatformnotes.md)** - Windows/macOS compatibility

## Support & Community

- **Forum**: [4ms MetaModule Community](https://forum.4ms.info)
- **Issues**: GitHub Issues for bugs and feature requests
- **YouTube**: [@thetechnobear](https://youtube.com/@thetechnobear) for tutorials

## About

Created by TheTechnobear - supporting the open source music tech community.

**Support this project**: [Ko-fi](https://ko-fi.com/thetechnobear)

## Credits

Thanks to the open source communities that make this possible:
- [VCV Rack](https://vcvrack.com) - Open source modular synthesizer  
- [4ms Company](https://4mscompany.com) - MetaModule hardware platform
- [Cycling '74](https://cycling74.com) - Max and RNBO visual programming

