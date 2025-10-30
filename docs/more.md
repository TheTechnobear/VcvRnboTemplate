# Advanced Topics

Detailed information for extending your RNBO module development.

## Development Tools

**Recommended Code Editor**: [VSCode](https://code.visualstudio.com) (free)
- Excellent C++ support with extensions
- Integrated terminal and Git support
- IntelliSense for code completion

## Template Updates

Stay current with improvements and bug fixes:

### Forked Repository (Recommended)
```bash
git fetch upstream
git merge upstream/master
git submodule update --init --recursive
```

### Direct Clone
```bash
git pull
git submodule update --init --recursive
```

**Note**: Template updates preserve your modules and plugin configurations. You may need to resolve merge conflicts if you've customized template files.

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `check.py` | Environment and project status validation |
| `createPlugin.py` | Initialize new plugin project |
| `createModule.py` | Add module to your plugin |
| `addDemo.py` | Add working demo module |
| `removeModule.py` | Remove specific module |

## Project Structure

```
[YourRepoName]/
├── Rack-SDK/             # VCV Rack SDK
├── VcvModules/           # VCV Rack plugin source
│   ├── src/              # Plugin source code
│   │   ├── plugin.hpp    # Plugin header declarations
│   │   ├── plugin.cpp    # Plugin initialization
│   │   ├── ModuleName.cpp    # Module implementations
│   │   └── ModuleName-rnbo/  # RNBO export directories
│   └── max/              # Max patches (optional organization)
├── scripts/              # Automation scripts
├── templates/            # Code generation templates
├── metamodule-plugin-sdk/ # MetaModule build system
└── plugin-mm.json        # MetaModule configuration
```

## Custom UI Development

The generated UI is generic but functional. For custom panels:

1. **Create SVG Panel**: Design in Inkscape or similar (see existing panels for reference)
2. **Generate Assets**: Use MetaModule asset generation tools
3. **Modify Code**: Update module code to use custom controls

*Detailed UI tutorial coming soon...*

## Code Customization

Generated modules are fully customizable:

- **Preserved Changes**: Your modifications persist across template updates
- **API Access**: Full access to VCV Rack and MetaModule APIs
- **RNBO Integration**: Direct access to RNBO parameter and I/O systems

## Platform-Specific Notes

### Windows Development
- See [Cross-Platform Notes](crossplatformnotes.md) for Windows setup
- ARM toolchain installation more complex on Windows
- Recommend Git Bash or WSL for Unix-like environment

### macOS/Linux
- Native toolchain support
- Standard Unix development workflow

## Manual SDK Updates (Advanced)

**⚠️ Warning**: Manual updates may cause template incompatibilities. Use template updates instead.

### MetaModule SDK
```bash
git submodule update --init --recursive
```

### VCV Rack SDK
```bash
rm -rf Rack-SDK
# Download new SDK from VCV website
# Extract to ./Rack-SDK/
```

### RNBO Runtime (Expert Only)
The RNBO runtime is in `VcvModules/inc/rnbo-export/common/`. To update:

1. Export an RNBO patch with "Copy C++ library code" enabled
2. Replace the `common/` directory with the exported version
3. Rebuild all modules

## External Resources

- **[MetaModule SDK Documentation](https://github.com/4ms/metamodule-plugin-sdk)**
- **[VCV Rack Plugin Tutorial](https://vcvrack.com/manual/PluginDevelopmentTutorial)**
- **[RNBO Documentation](https://rnbo.cycling74.com/)**

## Getting Help

- **Community**: [4ms MetaModule Forum](https://forum.4ms.info)
- **Tutorials**: [@thetechnobear YouTube channel](https://youtube.com/@thetechnobear)
