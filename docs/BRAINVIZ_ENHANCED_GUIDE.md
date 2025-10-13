# BrainViz_DK Enhanced - Complete Guide

## 🚀 What's New in BrainViz_DK Enhanced

Your lightweight brain plotting package now includes:

### ✨ New Features

1. **All Standard Neuroimaging Views**
   - Lateral, Medial, Dorsal, Ventral, Anterior, Posterior
   - 6 views per hemisphere = 12 total views

2. **3D Interactive Plots**
   - Fully rotatable, zoomable brain views
   - Self-contained HTML files
   - No external dependencies
   - Works in any web browser

3. **Self-Contained Templates**
   - Automatic template download and caching
   - fsaverage and fsaverage5 included
   - No FreeSurfer installation required

4. **Universal Compatibility**
   - Works with any Python interface (Jupyter, IPython, scripts)
   - Compatible with all .nii and .nii.gz files
   - Flexible API for any workflow

---

## 📦 Installation

```bash
# Minimal dependencies - that's it!
pip install nilearn nibabel matplotlib numpy
```

No FreeSurfer, no MNE, no complex setup!

---

## 🎯 Quick Start Examples

### 1. Generate All Standard Views (CLI)

```bash
# All 12 standard neuroimaging views
python -m brainviz_dk \
  --in /path/to/brain_map.nii.gz \
  --out ./plots/ \
  --all-views \
  --colormap jet \
  --prefix my_analysis

# This creates:
# - my_analysis_lh_lateral.png
# - my_analysis_lh_medial.png
# - my_analysis_lh_dorsal.png
# - my_analysis_lh_ventral.png
# - my_analysis_lh_anterior.png
# - my_analysis_lh_posterior.png
# ... and same for right hemisphere (rh)
```

### 2. Generate 3D Interactive Plot (CLI)

```bash
# Interactive 3D plot saved to HTML
python -m brainviz_dk \
  --in /path/to/brain_map.nii.gz \
  --out ./plots/ \
  --3d \
  --html interactive_brain.html \
  --colormap hot
```

### 3. Custom View Selection (CLI)

```bash
# Only specific views you want
python -m brainviz_dk \
  --in /path/to/brain_map.nii.gz \
  --out ./plots/ \
  --views lateral,anterior,dorsal \
  --hemi left \
  --surface pial \
  --colormap viridis
```

---

## 🐍 Python API Examples

### Example 1: All Standard Views

```python
import sys
sys.path.insert(0, '/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748')

from brainviz_dk import generate_all_standard_views

# Generate all 6 views for both hemispheres (12 total)
outputs = generate_all_standard_views(
    "/path/to/brain_map.nii.gz",
    "/path/to/output_dir/",
    colormap="jet",
    mesh="fsaverage",
    surface_name="pial",
    prefix="analysis"
)

print(f"Generated {len(outputs)} plots:")
for path in outputs:
    print(f"  ✓ {path}")
```

### Example 2: Interactive 3D Plot

```python
from brainviz_dk import plot_3d_interactive

# Create interactive 3D view
view = plot_3d_interactive(
    "/path/to/brain_map.nii.gz",
    colormap="hot",
    title="My Brain Analysis"
)

# Save to HTML
view.save_as_html("./plots/interactive_brain.html")
print("✓ Open interactive_brain.html in any browser!")

# Or open immediately
# view.open_in_browser()
```

### Example 3: Custom Views for Specific Needs

```python
from brainviz_dk import generate_four_views

# Only dorsal and ventral views, both hemispheres
outputs = generate_four_views(
    "/path/to/brain_map.nii.gz",
    "/path/to/output_dir/",
    hemis=("lh", "rh"),
    views=("dorsal", "ventral"),
    colormap="plasma",
    surface_name="pial",
    prefix="top_bottom_view"
)
```

### Example 4: Single Specific View

```python
from brainviz_dk import plot_nifti

# Just one specific view
plot_nifti(
    "/path/to/brain_map.nii.gz",
    "/path/to/output/anterior_view.png",
    hemi="left",
    view="anterior",
    colormap="jet",
    dpi=300
)
```

### Example 5: Batch Processing Multiple Features

```python
from brainviz_dk import generate_all_standard_views

base_dir = "/path/to/your/analysis"
features = ["alff", "falff", "reho", "hurst", "qie"]

for feature in features:
    nifti_file = f"{base_dir}/{feature}/whole_brain/MNI152NLin2009cAsym/group_mean.nii.gz"
    output_dir = f"{base_dir}/plots/{feature}/"
    
    outputs = generate_all_standard_views(
        nifti_file,
        output_dir,
        colormap="jet",
        prefix=f"{feature}_group"
    )
    print(f"✓ {feature}: {len(outputs)} plots generated")
```

---

## 🎨 Available Options

### Standard Neuroimaging Views

| View | Description |
|------|-------------|
| `lateral` | Outside view of hemisphere |
| `medial` | Inside view of hemisphere |
| `dorsal` | Top view (from above) |
| `ventral` | Bottom view (from below) |
| `anterior` | Front view |
| `posterior` | Back view |

### Hemispheres

| Option | Description |
|--------|-------------|
| `both` | Both hemispheres (default) |
| `left` or `lh` | Left hemisphere only |
| `right` or `rh` | Right hemisphere only |

### Surface Types

| Surface | Description | Use Case |
|---------|-------------|----------|
| `pial` | Cortical surface | Sharp sulci/gyri (default) |
| `inflated` | Smoothed surface | See buried sulci |
| `white` | White matter | Anatomical reference |
| `sphere` | Spherical | Unfolded cortex |

### Colormaps

| Colormap | Type | Best For |
|----------|------|----------|
| `jet` | Rainbow | General purpose |
| `hot` | Sequential | Activations |
| `plasma`, `viridis`, `inferno`, `magma` | Perceptually uniform | Publication quality |
| `coolwarm`, `RdYlBu_r` | Diverging | Positive/negative values |

### Mesh Resolution

| Mesh | Vertices/Hemisphere | Speed | Quality |
|------|---------------------|-------|---------|
| `fsaverage` | ~163k | Slower | High detail |
| `fsaverage5` | ~10k | Faster | Good detail |

---

## 🌐 3D Interactive Features

The 3D interactive plots (`--3d` or `plot_3d_interactive()`) generate self-contained HTML files with:

### Interactive Controls
- **Rotate**: Click and drag
- **Zoom**: Mouse wheel / pinch
- **Pan**: Right-click drag
- **Reset**: Double-click

### HTML File Features
- **Self-contained**: No internet or external files needed
- **Portable**: Share via email, cloud, USB
- **Cross-platform**: Works on any device with a browser
- **Embeddable**: Can be included in presentations/websites

### Example Use Cases
```python
from brainviz_dk import plot_3d_interactive

# For collaborators
view = plot_3d_interactive("results.nii.gz", colormap="hot")
view.save_as_html("share_with_team.html")

# For presentations
view = plot_3d_interactive("key_finding.nii.gz", 
                          colormap="viridis",
                          title="Main Result")
view.save_as_html("presentation_slide.html")

# For supplementary materials
view = plot_3d_interactive("supp_figure.nii.gz")
view.save_as_html("supplementary_fig_S1.html")
```

---

## 🗄️ Template Management (Self-Contained)

BrainViz_DK handles all templates automatically:

### First Run
```python
from brainviz_dk import generate_all_standard_views

# First time: Downloads fsaverage template (~200 MB)
# This happens automatically, just wait for download
outputs = generate_all_standard_views("map.nii.gz", "./plots/")
```

### Subsequent Runs
```python
# Template is cached in ~/nilearn_data/
# No download needed - instant access!
outputs = generate_all_standard_views("map.nii.gz", "./plots/")
```

### Template Location
- **Linux/Mac**: `~/nilearn_data/fsaverage/`
- **Windows**: `C:\Users\YourName\nilearn_data\fsaverage\`

### No FreeSurfer Needed!
- ✅ No FreeSurfer installation
- ✅ No `SUBJECTS_DIR` environment variable
- ✅ No manual downloads
- ✅ Works out-of-the-box

---

## 💡 Tips & Best Practices

### 1. For Publication Figures
```python
# High resolution, publication-quality
from brainviz_dk import generate_all_standard_views

generate_all_standard_views(
    "statistical_map.nii.gz",
    "./figures/",
    mesh="fsaverage",      # High resolution
    surface_name="pial",   # Sharp anatomical detail
    colormap="hot",        # Classic activation colormap
    prefix="Figure1"
)
```

### 2. For Quick Exploration
```python
# Fast preview
from brainviz_dk import generate_four_views

generate_four_views(
    "quick_check.nii.gz",
    "./preview/",
    hemis=("lh",),         # Just one hemisphere
    views=("lateral",),    # Just one view
    mesh="fsaverage5",     # Lower resolution = faster
    colormap="jet"
)
```

### 3. For Interactive Sharing
```python
# Best for collaborators
from brainviz_dk import plot_3d_interactive

view = plot_3d_interactive(
    "group_results.nii.gz",
    colormap="plasma",
    title="Group Analysis Results"
)
view.save_as_html("share_results.html")
# Email this HTML file to anyone!
```

### 4. For Batch Processing
```python
# Process multiple files efficiently
from brainviz_dk import generate_all_standard_views
import os

nifti_files = [
    "alff/group_mean.nii.gz",
    "falff/group_mean.nii.gz",
    "reho/group_mean.nii.gz"
]

for nifti in nifti_files:
    feature = os.path.basename(os.path.dirname(nifti))
    generate_all_standard_views(
        nifti,
        f"./plots/{feature}/",
        prefix=feature
    )
```

---

## 🔧 Troubleshooting

### Issue: "Module not found: brainviz_dk"
**Solution:**
```python
import sys
sys.path.insert(0, '/path/to/brainviz_dk/parent/directory')
from brainviz_dk import generate_all_standard_views
```

### Issue: First run takes long time
**Solution:** This is normal! Nilearn is downloading the fsaverage template (~200 MB). Subsequent runs will be instant.

### Issue: HTML file is large (30-40 MB)
**Solution:** This is expected. The HTML is self-contained with all 3D data embedded. It's portable but large.

### Issue: Want different template (not fsaverage)
**Current limitation:** BrainViz_DK currently supports fsaverage and fsaverage5. For other templates, you would need to extend the `project_volume_to_surface()` function.

---

## 📊 Output File Naming

### Static Plots
Format: `{prefix}_{hemisphere}_{view}.png`

Examples:
- `qie_group_mean_lh_lateral.png`
- `alff_analysis_rh_dorsal.png`
- `results_lh_anterior.png`

### Interactive 3D
Format: User-specified HTML filename

Examples:
- `interactive_brain.html`
- `group_results_3d.html`
- `supplementary_S1.html`

---

## 🎯 Use Cases

### Academic Research
- ✅ Generate all views for supplementary materials
- ✅ Create interactive figures for online publications
- ✅ Batch process multiple analyses

### Clinical Applications
- ✅ Visualize patient-specific activations
- ✅ Share results with clinical team (HTML)
- ✅ Compare different analysis methods

### Teaching
- ✅ Interactive demos in web browser
- ✅ Self-contained teaching materials
- ✅ No software installation needed for students

---

## 📝 Summary

**BrainViz_DK Enhanced is now:**
- ✅ Fully self-contained (auto-downloads templates)
- ✅ Compatible with any Python environment
- ✅ Supports all standard neuroimaging views
- ✅ Can generate 3D interactive plots
- ✅ Works with any .nii/.nii.gz file
- ✅ No MNE, no FreeSurfer, no complexity!

**Perfect for:**
- Quick brain visualizations
- Publication-quality figures
- Interactive result sharing
- Batch processing workflows
- Teaching and demonstrations

---

## 🔗 Quick Reference

```bash
# CLI - All views
python -m brainviz_dk --in map.nii.gz --out ./plots --all-views

# CLI - 3D interactive
python -m brainviz_dk --in map.nii.gz --out ./plots --3d --html brain.html

# Python - All views
from brainviz_dk import generate_all_standard_views
generate_all_standard_views("map.nii.gz", "./plots/")

# Python - 3D interactive
from brainviz_dk import plot_3d_interactive
view = plot_3d_interactive("map.nii.gz")
view.save_as_html("brain.html")
```

**Package Location:**
`/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748/brainviz_dk/`

**Test Scripts:**
- `test_brainviz_dk.py` - Basic functionality
- `test_brainviz_dk_enhanced.py` - All new features

**Documentation:**
- `brainviz_dk/README.md` - Complete technical documentation
- `BRAINVIZ_USAGE.md` - Original quick start guide
- `BRAINVIZ_ENHANCED_GUIDE.md` - This guide

---

🎉 **Enjoy your enhanced brain plotting package!**

