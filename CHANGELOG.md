# Changelog

All notable changes to BrainViz_DK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-14

### Added

#### Core Features
- Initial release of BrainViz_DK package
- High-resolution cortical surface visualization using nilearn
- Multiple viewing angles: lateral, medial, dorsal, ventral, anterior, posterior
- Quality presets system: draft, standard, publication, print
- Support for multiple output formats: PNG, SVG, PDF, EPS
- DPI configuration from 1-2400 for flexible resolution needs

#### Surface Plotting
- `plot_nifti()` - Single view surface plotting
- `generate_four_views()` - Multi-view surface plotting
- `generate_all_standard_views()` - All 12 standard views (6 views × 2 hemispheres)
- `plot_3d_interactive()` - Interactive 3D visualization (nilearn-based)
- Support for pial, inflated, white, and sphere surface types
- Multiple mesh resolutions: fsaverage, fsaverage5, fsaverage6

#### Volumetric Rendering
- `plot_volumetric_slices()` - Orthogonal slice visualization
- `plot_glass_brain()` - Transparent 3D glass brain plots
- `plot_mosaic()` - Multi-slice mosaic displays
- `plot_roi_overlay()` - ROI/parcellation overlay support
- Multiple display modes: ortho, x, y, z, yx, xz, yz, lyrz, lr
- Statistical map support with thresholding

#### Interactive 3D (Plotly)
- `plot_interactive_surface_plotly()` - Fully rotatable 3D brain meshes
- Perfect dorsal (top-down) view capability
- ICBM152/MNI152NLin2009cAsym template support
- Extremely close hemisphere spacing (1mm)
- Transparency/opacity control (0.0-1.0)
- Network parcellation overlay support (Yeo 7/17 networks)
- Contour visualization for network boundaries
- Standalone HTML output (no Python runtime needed)

#### Template Management
- `TemplateManager` class for unified template access
- `get_template()` - Load neuroimaging templates
- `list_available_templates()` - Display available templates
- Support for nilearn built-in templates (MNI152, fsaverage)
- TemplateFlow integration for ICBM152 and other templates

#### Command-Line Interface
- Comprehensive CLI with `brainviz_dk` command
- Support for all plotting types via `--plot-type` flag
- Quality preset integration via `--quality` flag
- Batch processing capabilities
- Extensive help documentation and examples
- `--list-presets` - List available quality presets
- `--list-templates` - List available brain templates

#### Documentation
- Complete README with examples
- Comprehensive CLI usage documentation
- API reference documentation structure
- Sphinx documentation configuration
- ReadTheDocs integration setup

#### Package Infrastructure
- setuptools and pyproject.toml configuration
- Entry point for CLI command
- Core dependencies: numpy, nibabel, nilearn, matplotlib
- Optional dependencies: templateflow, plotly, Pillow
- Test suite with pytest
- Example scripts for common use cases
- MIT License

### Quality Presets
- **draft** (150 DPI, PNG, fsaverage5) - Quick preview (~2s)
- **standard** (300 DPI, PNG, fsaverage) - General use (~5s)
- **publication** (600 DPI, SVG, fsaverage) - Journal submission (~10s)
- **print** (1200 DPI, PDF, fsaverage) - Large format printing (~20s)

### Dependencies
- Python >= 3.7
- numpy >= 1.19.0
- nibabel >= 3.0.0
- nilearn >= 0.9.0
- matplotlib >= 3.3.0
- templateflow >= 0.8.0 (optional, for ICBM152 templates)
- plotly >= 5.0.0 (optional, for interactive 3D)
- Pillow >= 8.0.0 (optional, for enhanced mosaics)

## [Unreleased]

### Planned Features
- Additional parcellation schemes
- Connectivity visualization
- Animation support for 3D views
- More template options
- Enhanced batch processing
- Performance optimizations

---

**Legend:**
- `Added` - New features
- `Changed` - Changes in existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security improvements
