# BrainViz_DK

**Lightweight 3D brain plotting utilities without MNE**

BrainViz_DK is a simple Python package for creating high-quality 3D brain visualizations from NIfTI files. It uses Nilearn for volume-to-surface projection and matplotlib for rendering, providing beautiful sulcal-shaded brain plots without requiring MNE-Python or FreeSurfer.

## Features

- **No MNE required**: Uses only Nilearn, Nibabel, and Matplotlib
- **Automatic surface projection**: Projects volumetric NIfTI data to cortical surfaces
- **Beautiful sulcal shading**: Uses fsaverage sulcal depth maps for anatomical detail
- **All standard neuroimaging views**: Lateral, medial, dorsal, ventral, anterior, and posterior
- **3D Interactive plots**: Generate HTML files with rotatable, zoomable 3D brain views
- **Self-contained templates**: Automatically downloads and caches fsaverage templates
- **Flexible customization**: Multiple colormaps, surfaces, and mesh resolutions
- **Simple API**: Both Python API and command-line interface
- **Works anywhere**: Compatible with Jupyter, IPython, scripts, and any Python environment

## Installation

```bash
pip install nilearn nibabel matplotlib numpy
```

That's it! No FreeSurfer installation needed.

## Quick Start

### Command Line Interface

```bash
# Generate all standard neuroimaging views (12 images: 6 views × 2 hemispheres)
python -m brainviz_dk \
  --in /path/to/your_file.nii.gz \
  --out /path/to/output_directory \
  --all-views

# Generate specific views only
python -m brainviz_dk \
  --in /path/to/your_file.nii.gz \
  --out /path/to/output_directory \
  --views lateral,medial,dorsal,ventral \
  --colormap jet

# Generate interactive 3D plot (opens in browser)
python -m brainviz_dk \
  --in /path/to/your_file.nii.gz \
  --out /path/to/output_directory \
  --3d

# Save interactive 3D plot to HTML
python -m brainviz_dk \
  --in /path/to/your_file.nii.gz \
  --out /path/to/output_directory \
  --3d --html brain_plot.html

# Customize hemispheres, surface, and colormap
python -m brainviz_dk \
  --in /path/to/your_file.nii.gz \
  --out /path/to/output_directory \
  --hemi left \
  --views lateral,anterior \
  --surface inflated \
  --colormap hot \
  --mesh fsaverage5
```

### Python API

```python
from brainviz_dk import (
    generate_four_views,
    generate_all_standard_views,
    plot_3d_interactive,
    plot_nifti
)

# 1. Generate ALL standard neuroimaging views (lateral, medial, dorsal, ventral, anterior, posterior)
outputs = generate_all_standard_views(
    "/path/to/your_file.nii.gz",
    "/path/to/output_directory",
    colormap="jet",
    mesh="fsaverage",
    surface_name="pial",
    prefix="brain_map"
)
print(f"Generated {len(outputs)} views")

# 2. Generate specific views only
outputs = generate_four_views(
    "/path/to/your_file.nii.gz",
    "/path/to/output_directory",
    hemis=("lh", "rh"),
    views=("lateral", "medial", "dorsal", "ventral"),
    colormap="jet",
    mesh="fsaverage",
    surface_name="pial",
    prefix="my_brain_map"
)

# 3. Generate interactive 3D plot
view = plot_3d_interactive(
    "/path/to/your_file.nii.gz",
    colormap="jet",
    title="My Brain Map"
)
# Open in browser
view.open_in_browser()
# Or save to HTML
view.save_as_html("/path/to/output.html")

# 4. Plot a single specific view
plot_nifti(
    "/path/to/your_file.nii.gz",
    "/path/to/output.png",
    hemi="left",  # or 'lh', 'right', 'rh'
    view="lateral",  # 'lateral', 'medial', 'dorsal', 'ventral', 'anterior', 'posterior'
    colormap="jet",
    alpha=0.8,
    dpi=300
)
```

## Parameters

### Surfaces
- `pial`: Default, shows cortical surface with sharp sulci/gyri
- `inflated`: Smoothed surface, easier to see buried sulci
- `white`: White matter surface
- `sphere`: Spherical projection

### Colormaps
Any matplotlib colormap works:
- `jet`: Rainbow colormap (default)
- `hot`: Black-red-yellow-white
- `plasma`, `viridis`, `inferno`, `magma`: Perceptually uniform
- `coolwarm`, `RdYlBu_r`: Diverging colormaps
- `Spectral_r`: Reversed spectral

### Mesh Resolution
- `fsaverage`: High resolution (~163k vertices per hemisphere)
- `fsaverage5`: Lower resolution (~10k vertices, faster)

### Views
- `lateral`: Outside view of hemisphere
- `medial`: Inside view of hemisphere  
- `dorsal`: Top view (from above)
- `ventral`: Bottom view (from below)
- `anterior`: Front view
- `posterior`: Back view

### Hemispheres
- `left` or `lh`: Left hemisphere
- `right` or `rh`: Right hemisphere
- `both`: Both hemispheres (default for generate_four_views)

## 3D Interactive Plots

BrainViz can generate fully interactive 3D brain plots that can be viewed in any web browser:

```python
from brainviz_dk import plot_3d_interactive

# Create interactive 3D view
view = plot_3d_interactive(
    "my_statistical_map.nii.gz",
    colormap="hot",
    title="My Analysis Results"
)

# Option 1: Open immediately in browser
view.open_in_browser()

# Option 2: Save to HTML file for sharing
view.save_as_html("interactive_brain.html")
```

The HTML file is **self-contained** (no external dependencies) and can be:
- Shared with collaborators
- Embedded in presentations
- Included in supplementary materials
- Viewed on any device with a web browser

Users can:
- **Rotate** the brain by clicking and dragging
- **Zoom** in/out with mouse wheel
- **Pan** by right-click dragging
- View from any angle interactively

## Template Management

BrainViz is **self-contained** and handles all templates automatically:

1. **First Run**: Downloads fsaverage template from Nilearn (~200 MB)
2. **Cached Locally**: Stored in `~/nilearn_data/` for future use
3. **No FreeSurfer Needed**: Everything works out-of-the-box

Available templates:
- `fsaverage`: High-resolution (163k vertices/hemisphere)
- `fsaverage5`: Lower-resolution (10k vertices/hemisphere, faster)

Both templates include:
- Pial, white, inflated, and sphere surfaces
- Sulcal depth maps for anatomical shading
- Left and right hemisphere data

## Examples

### Example 1: Publication-Quality Plots

```python
from brainviz_dk import generate_four_views

# Generate high-resolution plots with hot colormap
outputs = generate_four_views(
    "statistical_map.nii.gz",
    "publication_figures/",
    colormap="hot",
    mesh="fsaverage",  # High resolution
    surface_name="pial",
    prefix="Figure1"
)
```

### Example 2: Quick Preview

```python
from brainviz_dk import plot_nifti

# Just a quick lateral view
plot_nifti(
    "my_map.nii.gz",
    "preview.png",
    hemi="left",
    view="lateral",
    colormap="viridis"
)
```

### Example 3: Batch Processing

```python
from brainviz_dk import generate_four_views
import os

features = ["alff", "falff", "reho", "hurst"]
for feature in features:
    nifti_file = f"/data/{feature}/group_mean.nii.gz"
    output_dir = f"/plots/{feature}/"
    
    generate_four_views(
        nifti_file,
        output_dir,
        colormap="jet",
        prefix=f"{feature}_group_mean"
    )
```

### Example 4: CLI with Custom Views

```bash
# Only dorsal and ventral views
python -m brainviz_dk \
  --in activation_map.nii.gz \
  --out ./plots/ \
  --views dorsal,ventral \
  --colormap plasma \
  --prefix activation

# Only left hemisphere, lateral view
python -m brainviz_dk \
  --in left_activation.nii.gz \
  --out ./plots/ \
  --hemi left \
  --views lateral \
  --colormap hot
```

## How It Works

1. **Load NIfTI**: Loads your volumetric brain data
2. **Fetch Surface**: Downloads fsaverage template from Nilearn (cached locally)
3. **Project to Surface**: Uses `nilearn.surface.vol_to_surf` to project volume data onto cortical surface
4. **Render with Sulci**: Uses sulcal depth maps as background for anatomical detail
5. **Save High-Quality PNG**: Saves with customizable DPI and colormap

## Output File Naming

Files are automatically named using the pattern:
```
{prefix}_{hemisphere}_{view}.png
```

Examples:
- `qie_group_mean_lh_lateral.png`
- `qie_group_mean_rh_medial.png`
- `activation_map_lh_dorsal.png`

## Requirements

- Python 3.7+
- numpy
- nibabel
- nilearn
- matplotlib

## Notes

- Input NIfTI files should be in MNI space for best results
- First run will download fsaverage template (~200 MB, cached for future use)
- Surfaces are automatically fetched from Nilearn, no FreeSurfer needed
- Memory efficient: closes figures after saving

## Comparison to MNE-Python

While MNE-Python provides excellent brain visualization tools, BrainViz offers:
- **Simpler installation**: No FreeSurfer or MNE dependencies
- **Lighter weight**: Fewer dependencies, smaller footprint
- **NIfTI-focused**: Designed specifically for volumetric neuroimaging data
- **Easy batch processing**: Simple API for processing multiple files

## License

This package is provided as-is for neuroimaging research.

## Author

**Dilanjan DK** - ddiyabal@uwo.ca

## Credits

Built on top of:
- [Nilearn](https://nilearn.github.io/): For surface projection and fsaverage templates
- [Nibabel](https://nipy.org/nibabel/): For NIfTI file I/O
- [Matplotlib](https://matplotlib.org/): For rendering and saving figures

