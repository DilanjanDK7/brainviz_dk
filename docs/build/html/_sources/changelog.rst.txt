Changelog
=========

All notable changes to BrainViz_DK will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[0.1.0] - 2025-10-13
--------------------

Initial release of BrainViz_DK with comprehensive brain visualization capabilities.

Added
~~~~~

**Surface Plotting**

- High-quality cortical surface visualization using nilearn
- Support for multiple viewing angles: lateral, medial, dorsal, ventral, anterior, posterior
- Multiple hemispheres: left, right, or both
- Surface types: pial, inflated, white, sphere
- Mesh resolutions: fsaverage, fsaverage5, fsaverage6
- Quality presets: draft, standard, publication, print
- Output formats: PNG, SVG, PDF, EPS
- DPI range: 1-2400 for high-resolution output
- Custom figure sizes
- Interpolation options: linear, nearest, cubic
- Optional FWHM smoothing

**Functions:**

- ``plot_nifti()``: Single surface plot with full control
- ``generate_four_views()``: Generate multiple views
- ``generate_all_standard_views()``: All 12 standard views
- ``plot_3d_interactive()``: Interactive 3D visualization
- ``get_quality_preset()``: Get preset configurations
- ``list_quality_presets()``: Display available presets

**Volumetric Rendering**

- Orthogonal slice visualization (3-plane view)
- Glass brain visualization (transparent 3D)
- Mosaic displays (multi-slice views)
- ROI/parcellation overlays
- Multiple display modes: ortho, x, y, z, yx, xz, yz, lyrz, lr
- Customizable slice selection
- Threshold support for statistical maps
- Colormap support
- Black/white background options

**Functions:**

- ``plot_volumetric_slices()``: Slice visualization
- ``plot_glass_brain()``: Glass brain plots
- ``plot_mosaic()``: Mosaic displays
- ``plot_roi_overlay()``: ROI overlays

**Template Management**

- Unified template access system
- MNI152 templates (T1w, brain mask, GM mask, WM mask)
- TemplateFlow integration (ICBM152NLin2009cAsym)
- Multiple resolutions (1mm, 2mm)
- Automatic template downloading and caching

**Functions:**

- ``get_template()``: Load templates
- ``list_available_templates()``: Show available templates
- ``TemplateManager`` class: Manage templates

**Command-Line Interface**

- Comprehensive CLI for all visualization tasks
- 6 plot types: surface, volume, glass-brain, mosaic, roi, 3d
- Quality preset integration via --quality flag
- Template selection via --template flag
- Utility commands: --list-presets, --list-templates
- Organized argument groups
- Extensive help documentation with examples

**Quality & Output**

- Four quality presets optimized for different use cases
- draft: Fast preview (150 DPI, PNG, fsaverage5)
- standard: General use (300 DPI, PNG, fsaverage)
- publication: High quality (600 DPI, SVG, fsaverage)
- print: Very high quality (1200 DPI, PDF, fsaverage)

**Documentation**

- Comprehensive Sphinx documentation
- ReadTheDocs integration
- API reference with examples
- Quick start guide
- CLI usage guide
- Quality presets guide
- Template documentation
- Contributing guide

**Testing**

- Comprehensive test suite with pytest
- Unit tests for all major functions
- Integration tests with real neuroimaging data
- 100% test success rate on validation dataset

Changed
~~~~~~~

- Improved error handling with informative messages
- Enhanced input validation for all functions
- Better memory management for large files

Fixed
~~~~~

- MANIFEST.in path errors (brainviz → brainviz_dk)
- Empty data handling in auto-scaling functions
- nilearn display savefig parameter compatibility
- Quality preset metadata handling

Dependencies
~~~~~~~~~~~~

**Core:**

- numpy >= 1.19.0
- nibabel >= 3.0.0
- nilearn >= 0.9.0
- matplotlib >= 3.3.0

**Optional:**

- templateflow >= 0.8.0 (for ICBM152NLin2009cAsym templates)

**Development:**

- pytest >= 6.0.0
- pytest-cov >= 2.10.0
- sphinx >= 4.0.0
- sphinx_rtd_theme >= 1.0.0

Known Limitations
~~~~~~~~~~~~~~~~~

1. TemplateFlow templates require separate installation: ``pip install templateflow``
2. Volumetric plots don't support all matplotlib savefig options (only DPI)
3. Very high DPI (>1200) may cause memory issues with large datasets
4. SVG output for surface plots can be large (20-100 MB)

Future Plans
------------

[Unreleased]
~~~~~~~~~~~~

Planned features for future releases:

**Enhancements:**

- Additional surface mesh resolutions
- More template options from TemplateFlow
- Batch processing utilities with progress bars
- Configuration file support (.brainvizrc)
- Logging system with verbosity levels
- Memory-efficient processing for large datasets

**New Features:**

- Statistical overlay support (p-values, effect sizes)
- Multi-subject visualization
- Time-series visualization (4D data)
- Connectivity visualization
- Region labeling and annotation
- Custom color scheme support

**Documentation:**

- Video tutorials
- Gallery of examples
- Best practices guide
- Performance optimization guide

**Infrastructure:**

- GitHub Actions CI/CD
- PyPI package distribution
- Docker container
- Conda package

Version History
---------------

* **0.1.0** (2025-10-13) - Initial release

Migration Guide
---------------

This is the first release, no migration needed.

For future versions, breaking changes will be documented here with migration instructions.

Contributing
------------

See :doc:`contributing` for guidelines on how to contribute to BrainViz_DK.

Report bugs and request features at: https://github.com/yourusername/brainviz_dk/issues
