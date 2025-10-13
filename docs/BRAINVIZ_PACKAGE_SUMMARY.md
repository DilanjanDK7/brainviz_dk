# BrainViz_DK Package - Complete Summary

## 📦 Package Overview

**BrainViz_DK** is a lightweight, self-contained Python package for creating high-quality 3D brain visualizations from NIfTI files without requiring MNE-Python or FreeSurfer.

### Key Capabilities
- ✅ All standard neuroimaging views (lateral, medial, dorsal, ventral, anterior, posterior)
- ✅ Interactive 3D plots (HTML-based, browser-compatible)
- ✅ Self-contained templates (auto-downloads fsaverage/fsaverage5)
- ✅ Works with any .nii/.nii.gz file
- ✅ Compatible with any Python interface (Jupyter, IPython, scripts)
- ✅ Simple API (both Python and CLI)

---

## 📁 Package Structure

```
brainviz_dk/
├── __init__.py                      # Package initialization & exports
├── __main__.py                      # Command-line interface (CLI)
├── plot.py                          # Core plotting functions
├── setup.py                         # Installation script
├── README.md                        # Technical documentation
└── examples/
    └── batch_process_features.py   # Batch processing example
```

### Core Files

1. **`__init__.py`**
   - Exports: `plot_nifti`, `generate_four_views`, `generate_all_standard_views`, `plot_3d_interactive`, `project_volume_to_surface`

2. **`plot.py`**
   - Core plotting engine
   - Surface projection utilities
   - Auto-scaling and thresholding
   - Support for multiple views, colormaps, surfaces

3. **`__main__.py`**
   - Full-featured CLI
   - Supports all views, 3D plots, custom configurations
   - Verbose mode and help text

4. **`setup.py`**
   - Package installation configuration
   - Dependencies management
   - Console script entry point

---

## 🚀 Installation & Setup

### Option 1: Use Directly (No Installation)
```python
import sys
sys.path.insert(0, '/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748')
from brainviz_dk import generate_all_standard_views
```

### Option 2: Install as Package
```bash
cd /media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748/brainviz_dk
pip install -e .
```

### Dependencies
```bash
pip install nilearn nibabel matplotlib numpy
```

---

## 🎯 Quick Start

### Command Line
```bash
# All standard views
python -m brainviz_dk --in brain.nii.gz --out ./plots --all-views

# 3D interactive
python -m brainviz_dk --in brain.nii.gz --out ./plots --3d --html brain.html

# Custom views
python -m brainviz_dk --in brain.nii.gz --out ./plots --views lateral,dorsal --colormap hot
```

### Python API
```python
from brainviz_dk import generate_all_standard_views, plot_3d_interactive

# Static plots
generate_all_standard_views("brain.nii.gz", "./plots/")

# Interactive 3D
view = plot_3d_interactive("brain.nii.gz")
view.save_as_html("brain.html")
```

---

## 📊 Available Functions

### 1. `plot_nifti()`
Plot a single specific view to PNG.

**Parameters:**
- `nifti_path`: Input NIfTI file
- `out_path`: Output PNG file
- `hemi`: Hemisphere ('left'/'lh' or 'right'/'rh')
- `view`: View type (lateral/medial/dorsal/ventral/anterior/posterior)
- `colormap`: Matplotlib colormap (default: 'jet')
- `mesh`: Surface mesh ('fsaverage' or 'fsaverage5')
- `surface_name`: Surface type ('pial', 'inflated', 'white', 'sphere')
- `alpha`, `darkness`, `radius`, `dpi`: Rendering parameters

**Example:**
```python
plot_nifti("map.nii.gz", "output.png", hemi="left", view="lateral")
```

### 2. `generate_four_views()`
Generate multiple views for specified hemispheres.

**Parameters:**
- `nifti_path`: Input NIfTI file
- `out_dir`: Output directory
- `hemis`: Tuple of hemispheres (default: ('lh', 'rh'))
- `views`: Tuple of views (default: ('lateral', 'medial', 'dorsal', 'ventral'))
- `mesh`, `surface_name`, `colormap`, `prefix`: As above

**Example:**
```python
outputs = generate_four_views(
    "map.nii.gz",
    "./plots/",
    views=("lateral", "medial"),
    colormap="hot"
)
```

### 3. `generate_all_standard_views()`
Generate all 6 standard neuroimaging views for both hemispheres (12 total).

**Parameters:**
- Same as `generate_four_views()` but views are fixed to all standard ones

**Example:**
```python
outputs = generate_all_standard_views(
    "map.nii.gz",
    "./plots/",
    colormap="jet",
    prefix="analysis"
)
# Generates 12 PNG files
```

### 4. `plot_3d_interactive()`
Create interactive 3D plot viewable in web browser.

**Parameters:**
- `nifti_path`: Input NIfTI file
- `threshold`: Value threshold (auto if None)
- `colormap`: Colormap (default: 'jet')
- `symmetric_cmap`: Use symmetric colormap (bool)
- `title`: Plot title

**Returns:** Nilearn SurfaceView object

**Example:**
```python
view = plot_3d_interactive("map.nii.gz", colormap="hot", title="Results")
view.save_as_html("interactive.html")
# or
view.open_in_browser()
```

### 5. `project_volume_to_surface()`
Low-level function to project NIfTI volume to cortical surface.

**Returns:** (surf_mesh, sulc_map, texture_array)

---

## 🎨 Configuration Options

### Views
- `lateral` - Outside view of hemisphere
- `medial` - Inside view of hemisphere
- `dorsal` - Top view
- `ventral` - Bottom view
- `anterior` - Front view
- `posterior` - Back view

### Hemispheres
- `left`, `lh` - Left hemisphere
- `right`, `rh` - Right hemisphere
- `both` - Both hemispheres

### Surfaces
- `pial` - Cortical surface (sharp sulci/gyri)
- `inflated` - Smoothed surface (see buried sulci)
- `white` - White matter surface
- `sphere` - Spherical projection

### Colormaps
- Sequential: `jet`, `hot`, `plasma`, `viridis`, `inferno`, `magma`
- Diverging: `coolwarm`, `RdYlBu_r`, `Spectral_r`

### Mesh Resolution
- `fsaverage` - High res (~163k vertices/hemi)
- `fsaverage5` - Lower res (~10k vertices/hemi)

---

## 📚 Documentation Files

### In Package Directory
1. **`README.md`** - Technical documentation
   - Installation instructions
   - API reference
   - Examples
   - Parameters guide

2. **`setup.py`** - Package metadata
   - Dependencies
   - Version info
   - Entry points

### In Project Root
1. **`BRAINVIZ_USAGE.md`** - Original quick start guide
   - Basic usage
   - CLI examples
   - Python API examples
   - Comparison with MNE-Python

2. **`BRAINVIZ_ENHANCED_GUIDE.md`** - Comprehensive guide
   - All new features
   - 3D interactive plots
   - Template management
   - Best practices
   - Troubleshooting

3. **`BRAINVIZ_PACKAGE_SUMMARY.md`** - This file
   - Package overview
   - File structure
   - Function reference

### Test Scripts
1. **`test_brainviz_dk.py`** - Basic functionality tests
   - Single views
   - Multiple views
   - Different colormaps
   - Different surfaces

2. **`test_brainviz_dk_enhanced.py`** - Enhanced features tests
   - All standard views
   - 3D interactive plots
   - Custom view selection
   - Surface/colormap/mesh comparisons

### Example Scripts
1. **`brainviz_dk/examples/batch_process_features.py`**
   - Batch processing example
   - Process multiple features
   - Organized output structure

---

## ✅ Testing Status

All tests passed successfully:

### Basic Tests ✓
- [x] Single view rendering
- [x] Multiple view generation
- [x] Different colormaps (jet, hot)
- [x] Different surfaces (pial, inflated)
- [x] Different hemispheres (lh, rh)

### Enhanced Tests ✓
- [x] All standard views (12 views)
- [x] Custom view selection
- [x] 3D interactive HTML generation
- [x] Surface type comparison
- [x] Colormap comparison (jet, hot, viridis)
- [x] Mesh resolution comparison (fsaverage, fsaverage5)

### Sample Outputs
- Static PNGs: `/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748/Plots_BrainViz_DK_Test/`
- Enhanced outputs: `/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748/Plots_BrainViz_DK_Enhanced/`
- Interactive 3D HTML: `Plots_BrainViz_DK_Enhanced/interactive_3d/qie_interactive_3d.html` (35MB)

---

## 🔄 Template Management

### Automatic Download
- First run downloads fsaverage from Nilearn (~200 MB)
- Cached in `~/nilearn_data/fsaverage/`
- Subsequent runs use cached version

### No Manual Setup Required
- ✅ No FreeSurfer installation
- ✅ No `SUBJECTS_DIR` configuration
- ✅ No manual downloads
- ✅ Works out-of-the-box

### Template Contents
- Surfaces: pial, white, inflated, sphere
- Sulcal depth maps for anatomical shading
- Both hemispheres (left & right)
- Two resolutions: fsaverage (high), fsaverage5 (lower)

---

## 🌟 Key Advantages

### vs MNE-Python
| Feature | BrainViz_DK | MNE-Python |
|---------|----------|------------|
| **Dependencies** | Minimal (nilearn, nibabel, matplotlib) | Complex (MNE, PyVista, Qt) |
| **Installation** | `pip install` 4 packages | Often requires conda |
| **Primary Focus** | NIfTI visualization | MEG/EEG + visualization |
| **3D Rendering** | HTML (portable) | PyVista (interactive window) |
| **Batch Processing** | Simple | Requires Qt backend handling |
| **File Formats** | .nii, .nii.gz | Many formats |

### vs FreeSurfer
| Feature | BrainViz_DK | FreeSurfer |
|---------|----------|------------|
| **Installation** | pip install | Complex binary installation |
| **Setup** | None | SUBJECTS_DIR, environment vars |
| **Usage** | Python/CLI | Command-line tools |
| **Templates** | Auto-download | Manual setup |
| **Learning Curve** | Low | High |

### vs Brainstorm
| Feature | BrainViz_DK | Brainstorm |
|---------|----------|------------|
| **Platform** | Python | MATLAB |
| **Interface** | Code/CLI | GUI |
| **Automation** | Easy (scriptable) | Limited |
| **Output** | PNG, HTML | Screenshots, limited export |
| **Cost** | Free | Requires MATLAB |

---

## 💡 Use Cases

### Research
- ✅ Generate supplementary figures
- ✅ Batch process multiple analyses
- ✅ Create publication-quality plots
- ✅ Share interactive results online

### Clinical
- ✅ Visualize patient activations
- ✅ Share results with team (HTML)
- ✅ Compare different protocols

### Teaching
- ✅ Interactive demonstrations
- ✅ No software installation for students
- ✅ Self-contained teaching materials

### Collaboration
- ✅ Email HTML files
- ✅ Embed in presentations
- ✅ Include in supplementary materials

---

## 🚀 Next Steps

### For Users
1. **Try basic examples:**
   ```bash
   python3 test_brainviz_dk.py
   ```

2. **Try enhanced features:**
   ```bash
   python3 test_brainviz_dk_enhanced.py
   ```

3. **Use in your workflow:**
   - Import brainviz_dk in your scripts
   - Use CLI for quick visualizations
   - Generate interactive 3D for sharing

### For Developers
1. **Extend functionality:**
   - Add new view presets
   - Support additional templates
   - Custom colormap functions

2. **Package distribution:**
   - Upload to PyPI
   - Create conda package
   - Add to neuroimaging tools registry

3. **Integration:**
   - Create Jupyter widgets
   - Add BIDS app wrapper
   - Integrate with analysis pipelines

---

## 📞 Package Information

**Location:** `/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748/brainviz_dk/`

**Version:** 0.1.0

**Author:** BrainLab UWO

**License:** MIT

**Dependencies:**
- numpy >= 1.19.0
- nibabel >= 3.0.0
- nilearn >= 0.9.0
- matplotlib >= 3.3.0

**Python Support:** 3.7+

**Platforms:** Linux, macOS, Windows

---

## 📖 Quick Reference Card

```bash
# CLI Quick Commands
python -m brainviz_dk --in file.nii.gz --out ./plots --all-views
python -m brainviz_dk --in file.nii.gz --out ./plots --3d --html brain.html
python -m brainviz_dk --in file.nii.gz --out ./plots --views lateral,dorsal --colormap hot

# Python Quick Start
from brainviz_dk import generate_all_standard_views, plot_3d_interactive
generate_all_standard_views("file.nii.gz", "./plots/")
view = plot_3d_interactive("file.nii.gz")
view.save_as_html("brain.html")
```

---

## ✨ Summary

BrainViz_DK is now a **complete, self-contained brain visualization package** that:

- Works with **any .nii file** from any analysis
- Runs in **any Python environment** (Jupyter, scripts, IPython)
- Generates **all standard neuroimaging views**
- Creates **interactive 3D plots** for sharing
- **Auto-manages templates** (no manual setup)
- Has **minimal dependencies** (no MNE, no FreeSurfer)
- Provides **both CLI and Python API**
- Is **fully tested and documented**

**Perfect for researchers, clinicians, and educators who need quick, high-quality brain visualizations!**

---

*Last Updated: October 2025*
*Package Status: ✅ Complete and Tested*

