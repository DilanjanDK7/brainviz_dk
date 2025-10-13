# BrainViz_DK Package - Quick Start Guide

## What is BrainViz_DK?

**BrainViz_DK** is a lightweight Python package created to generate high-quality 3D brain plots from NIfTI files **without requiring MNE-Python**. It uses only Nilearn, Nibabel, and Matplotlib to create beautiful, publication-ready brain visualizations with clear sulcal definition.

### Key Features
- ✅ **No MNE required** - Uses only Nilearn and standard Python libraries
- ✅ **No FreeSurfer installation needed** - Surfaces automatically downloaded
- ✅ **Beautiful sulcal shading** - Clear gyri and sulci definition
- ✅ **Multiple views** - Lateral, medial, dorsal, ventral
- ✅ **Flexible colormaps** - Jet, hot, plasma, viridis, and more
- ✅ **Simple API** - Both Python and command-line interfaces

---

## Installation

### Option 1: Use Locally (Current Setup)
The package is already available in your workspace:
```bash
cd /media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748
```

Just make sure you have the dependencies:
```bash
pip install nilearn nibabel matplotlib numpy
```

### Option 2: Install as Package (Optional)
```bash
cd /media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748/brainviz_dk
pip install -e .
```

---

## Quick Examples

### Example 1: Command Line - Generate All Views

```bash
# Basic usage
python -m brainviz_dk \
  --in /path/to/your_brain_map.nii.gz \
  --out /path/to/output_folder \
  --colormap jet

# This generates 8 images (4 views × 2 hemispheres):
# - {prefix}_lh_lateral.png
# - {prefix}_lh_medial.png
# - {prefix}_lh_dorsal.png
# - {prefix}_lh_ventral.png
# - {prefix}_rh_lateral.png
# - {prefix}_rh_medial.png
# - {prefix}_rh_dorsal.png
# - {prefix}_rh_ventral.png
```

### Example 2: Command Line - Custom Options

```bash
# Only left hemisphere, only lateral and medial views
python -m brainviz_dk \
  --in qie_mean.nii.gz \
  --out ./plots/ \
  --colormap hot \
  --hemi left \
  --views lateral,medial \
  --surface pial \
  --prefix qie_group_mean
```

### Example 3: Python API - Single Plot

```python
import sys
sys.path.insert(0, '/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748')

from brainviz_dk import plot_nifti

# Generate a single specific view
plot_nifti(
    "/path/to/brain_map.nii.gz",
    "/path/to/output.png",
    hemi="left",        # 'left', 'right', 'lh', or 'rh'
    view="lateral",     # 'lateral', 'medial', 'dorsal', 'ventral'
    colormap="jet",
    dpi=300
)
```

### Example 4: Python API - All Four Views

```python
import sys
sys.path.insert(0, '/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748')

from brainviz_dk import generate_four_views

# Generate all views for both hemispheres
outputs = generate_four_views(
    "/path/to/brain_map.nii.gz",
    "/path/to/output_folder/",
    hemis=("lh", "rh"),
    views=("lateral", "medial", "dorsal", "ventral"),
    colormap="jet",
    mesh="fsaverage",
    surface_name="pial",
    prefix="my_analysis"
)

print(f"Generated {len(outputs)} plots")
for path in outputs:
    print(f"  - {path}")
```

### Example 5: Batch Process Multiple Features

```python
import sys
sys.path.insert(0, '/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748')

from brainviz_dk import generate_four_views

base = "/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748"

features = ["alff", "falff", "reho", "hurst", "qie", "simple_fourier"]

for feature in features:
    nifti_file = f"{base}/{feature}/whole_brain/MNI152NLin2009cAsym/group_mean.nii.gz"
    output_dir = f"{base}/Plots_BrainViz_DK/{feature}/"
    
    generate_four_views(
        nifti_file,
        output_dir,
        colormap="jet",
        prefix=f"{feature}_group_mean"
    )
    print(f"✓ {feature} complete")
```

---

## Available Options

### Hemispheres (`--hemi` or `hemi=`)
- `both` - Both hemispheres (default)
- `left` or `lh` - Left hemisphere only
- `right` or `rh` - Right hemisphere only

### Views (`--views` or `views=`)
- `lateral` - Outside view of hemisphere
- `medial` - Inside view of hemisphere
- `dorsal` - Top view (from above)
- `ventral` - Bottom view (from below)

### Surfaces (`--surface` or `surface_name=`)
- `pial` - Cortical surface with sharp sulci (default, recommended)
- `inflated` - Smoothed surface for buried sulci
- `white` - White matter surface
- `sphere` - Spherical projection

### Colormaps (`--colormap` or `colormap=`)
- `jet` - Rainbow colormap (default)
- `hot` - Black → Red → Yellow → White
- `plasma`, `viridis`, `inferno`, `magma` - Perceptually uniform
- `coolwarm`, `RdYlBu_r` - Diverging colormaps
- Any matplotlib colormap name

### Mesh Resolution (`--mesh` or `mesh=`)
- `fsaverage` - High resolution (163k vertices, default)
- `fsaverage5` - Lower resolution (10k vertices, faster)

---

## Test Results

**All tests passed successfully!** ✅

Generated sample plots include:
- Left/right hemisphere lateral views
- Left/right hemisphere medial views  
- Left/right hemisphere dorsal views
- Left/right hemisphere ventral views
- Different colormaps (jet, hot)
- Different surfaces (pial, inflated)

Sample outputs are in:
```
/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748/Plots_BrainViz_DK_Test/
```

---

## How It Works

1. **Loads NIfTI** → Reads your volumetric brain data
2. **Fetches Surface** → Downloads fsaverage template (cached after first use)
3. **Projects to Surface** → Maps volume data to cortical surface using `nilearn.surface.vol_to_surf`
4. **Adds Sulcal Detail** → Uses sulcal depth maps for anatomical shading
5. **Renders & Saves** → Creates high-quality PNG with matplotlib

---

## Comparison: BrainViz_DK vs MNE-Python

| Feature | BrainViz_DK | MNE-Python |
|---------|----------|------------|
| **Dependencies** | Nilearn, Nibabel, Matplotlib | MNE, PyVista, PyVistaQt, FreeSurfer (optional) |
| **Installation** | `pip install nilearn nibabel matplotlib` | Complex (conda recommended) |
| **Primary Use Case** | Volumetric NIfTI visualization | MEG/EEG source analysis + visualization |
| **Surface Rendering** | Nilearn (matplotlib-based) | PyVista (VTK-based, more interactive) |
| **Ease of Use** | Very simple API | More complex API |
| **3D Interactivity** | No (static PNGs) | Yes (interactive 3D window) |
| **Batch Processing** | Excellent | Good (requires handling Qt backend) |
| **File Formats** | NIfTI focus | Source estimates, NIfTI, more |

**When to use BrainViz_DK:**
- You want simple, reproducible static plots
- You're working with NIfTI files in MNI space
- You need easy batch processing
- You want minimal dependencies

**When to use MNE-Python:**
- You need interactive 3D exploration
- You're working with MEG/EEG source data
- You need advanced statistical visualizations
- You want to rotate/zoom plots in real-time

---

## Troubleshooting

### Issue: "Module not found: brainviz_dk"
**Solution:** Make sure you add the path to sys.path:
```python
import sys
sys.path.insert(0, '/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748')
from brainviz_dk import generate_four_views
```

### Issue: "fsaverage not found"
**Solution:** First run will download fsaverage (~200 MB). Ensure internet connection and wait for download to complete. It will be cached in `~/nilearn_data/`.

### Issue: Plots look different from MNE
**Solution:** This is expected. BrainViz_DK uses matplotlib-based rendering (2D projection of 3D surface) while MNE uses PyVista (true 3D). For publication, BrainViz_DK often produces cleaner, more reproducible images.

### Issue: "Invalid hemispheres definition"
**Solution:** Use `'left'`/`'right'` or `'lh'`/`'rh'` (BrainViz_DK handles both). Nilearn internally requires `'left'`/`'right'`.

---

## File Structure

```
brainviz_dk/
├── __init__.py          # Package initialization
├── __main__.py          # CLI entry point
├── plot.py              # Core plotting functions
├── setup.py             # Installation script
├── README.md            # Full documentation
└── examples/
    └── batch_process_features.py  # Batch processing example
```

---

## Next Steps

1. **Try the test script:**
   ```bash
   cd /media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748
   python3 test_brainviz_dk.py
   ```

2. **Run batch processing example:**
   ```bash
   python3 brainviz_dk/examples/batch_process_features.py
   ```

3. **Create your own script** using the examples above

4. **Share the package** - The `brainviz_dk/` folder is self-contained and can be copied to other projects

---

## Credits

**Built with:**
- [Nilearn](https://nilearn.github.io/) - Brain imaging in Python
- [Nibabel](https://nipy.org/nibabel/) - Neuroimaging file I/O
- [Matplotlib](https://matplotlib.org/) - Plotting library

**Inspired by:**
- MNE-Python's excellent visualization tools
- Brainstorm's beautiful surface rendering
- The neuroimaging community's need for simple, reproducible plotting tools

