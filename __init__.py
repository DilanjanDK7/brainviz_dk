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
    get_quality_preset,
    list_quality_presets,
    QUALITY_PRESETS,
)

from .volumetric import (
    plot_volumetric_slices,
    plot_glass_brain,
    plot_mosaic,
    plot_roi_overlay,
)

from .templates import (
    TemplateManager,
    get_template,
    list_available_templates,
)

from .interactive3d import (
    plot_interactive_surface_plotly,
    PARCELLATION_SCHEMES,
)

__all__ = [
    # Surface plotting
    "plot_nifti",
    "generate_four_views",
    "generate_all_standard_views",
    "plot_3d_interactive",
    "project_volume_to_surface",
    # Interactive 3D
    "plot_interactive_surface_plotly",
    "PARCELLATION_SCHEMES",
    # Quality presets
    "get_quality_preset",
    "list_quality_presets",
    "QUALITY_PRESETS",
    # Volumetric plotting
    "plot_volumetric_slices",
    "plot_glass_brain",
    "plot_mosaic",
    "plot_roi_overlay",
    # Template management
    "TemplateManager",
    "get_template",
    "list_available_templates",
]




__version__ = '0.1.0'
