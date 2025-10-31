# VCV Rack RNBO Template

Create VCV Rack and 4ms MetaModule plugins without programming! This project enables musicians and sound designers to build audio modules using Max RNBO's visual programming language. Simple scripts generate complete plugins from your RNBO patches, perfect for rapid prototyping or as a starting point for custom development. Test your DSP algorithms in Max, then seamlessly deploy to VCV Rack desktop for experimentation before finalizing on MetaModule hardware.

Learn more about RNBO visual programming at https://rnbo.cycling74.com

## Key Features

- **No Programming Required** - Use visual Max RNBO patches to create modules
- **Dual Platform** - Deploy to both VCV Rack (desktop) and 4ms MetaModule (hardware)  
- **Rapid Prototyping** - Quick workflow from idea to working module
- **Test Progression** - Max → VCV Rack → MetaModule hardware
- **Flexible Foundation** - Generated code can be customized further
- **Easy Sharing** - Share modules without requiring Max/RNBO for end users

## Requirements

**For Module Creation:**
- Max 8 or 9 with RNBO 1.4.2+ (license or subscription required)
- Development environment (free - see setup)

**For Using Created Modules:**
- No Max/RNBO required for end users

⚠️ **Before Purchasing Max/RNBO**: Complete the setup and test the demo to ensure everything works on your system!

## Quick Start

**👉 Start Here**: **[Setup Environment](docs/setup.md)** - Install build tools and SDKs

[My YouTube Video showing the how to setup and create your first module](https://youtu.be/paO0zy8WzZU)

**Note**: Commands below use the terminal/command line. Windows users should use MSYS2 MinGW 64-bit shell (see setup guide).

### Test Demo (No Max/RNBO Required)
Before investing in Max/RNBO, test your setup with the included demo:

```bash
python3 scripts/check.py           # Verify environment
python3 scripts/createPlugin.py    # Create test plugin  
python3 scripts/addDemo.py         # Add demo module
cd VcvModules && make install      # Build and install in VCV Rack
```

This builds a working module and confirms your setup works!

### Create Your First Module (With Max/RNBO)

Creating your first modules is simple, though you wil need Max and RNBO.

**💡 Try Before You Buy**: Cycling 74 offer a 30-day demo for Max/RNBO that includes export functionality - perfect for testing this template! Note: the demo doesn't allow saving Max patches, so you'll need to complete your patch in one session or purchase a license / subscription to save your work.


```bash
# 1. Create module template
python3 scripts/createModule.py

# 2. Export your RNBO patch to: VcvModules/src/[ModuleName]-rnbo/
#    (in Max: Export → C++ → [ModuleName].cpp.h)

# 3. Build
cd VcvModules && make install      # build and add to vcv rack
cd .. && cmake --fresh -B build && cmake --build build  # For MetaModule (optional)
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
