"""
brainviz: Lightweight 3D brain plotting utilities without MNE.

- Volume→surface projection via nilearn.surface.vol_to_surf
- High-quality sulcal shading using fsaverage sulc background
- Simple API and CLI for plotting arbitrary .nii(.gz) files

Dependencies: numpy, nibabel, nilearn, matplotlib, Pillow (optional for mosaics)
"""

from .plot import (
    plot_nifti,
    generate_four_views,
    generate_all_standard_views,
    plot_3d_interactive,
    project_volume_to_surface,
)

__all__ = [
    "plot_nifti",
    "generate_four_views",
    "generate_all_standard_views",
    "plot_3d_interactive",
    "project_volume_to_surface",
]




__version__ = '0.1.0'
