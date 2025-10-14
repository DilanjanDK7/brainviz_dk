"""
Interactive 3D Brain Surface Visualization with Plotly
=======================================================

This module provides fully interactive 3D brain surface visualization using Plotly.
Users can rotate, zoom, and pan to view the brain from any angle, including perfect
dorsal (top-down) views.

Key Features:
- Full 3D rotation with mouse
- High-quality fsaverage mesh rendering
- Projects any NIfTI volume to cortical surface
- Saves as standalone HTML (shareable, no Python needed)
- Supports both hemispheres
- Customizable colormaps and thresholds
"""

import os
import logging
from typing import Optional, Tuple, Dict, Any, Union
import numpy as np
import nibabel as nib
from nilearn import datasets as nilearn_datasets
from nilearn import surface

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

logger = logging.getLogger(__name__)


def _check_plotly():
    """Check if plotly is installed."""
    if not PLOTLY_AVAILABLE:
        raise ImportError(
            "Plotly is required for interactive 3D visualization. "
            "Install with: pip install plotly"
        )


def _load_fsaverage_mesh_data(mesh: str = 'fsaverage', hemi: str = 'lh', template: str = 'fsaverage'):
    """
    Load brain surface mesh geometry data.

    Args:
        mesh: Mesh resolution ('fsaverage', 'fsaverage5', 'fsaverage6', 'MNI152NLin2009cAsym')
        hemi: Hemisphere ('lh' or 'rh')
        template: Template to use ('fsaverage' or 'MNI152NLin2009cAsym')

    Returns:
        Tuple of (vertices, faces) as numpy arrays
    """
    # Handle ICBM152/MNI152NLin2009cAsym template via TemplateFlow
    if template == 'MNI152NLin2009cAsym' or mesh == 'MNI152NLin2009cAsym':
        try:
            import templateflow.api as tflow
            # Get pial surface from TemplateFlow
            hemi_suffix = 'L' if hemi == 'lh' else 'R'
            mesh_file = tflow.get(
                'MNI152NLin2009cAsym',
                hemi=hemi_suffix,
                density='32k',  # 32k vertices per hemisphere
                suffix='pial',
                extension='surf.gii'
            )
            # Load mesh geometry
            coords, faces = surface.load_surf_mesh(mesh_file)
            logger.info(f"Loaded MNI152NLin2009cAsym {hemi} surface ({coords.shape[0]} vertices)")
            return coords, faces
        except ImportError:
            logger.warning("TemplateFlow not available. Install with: pip install templateflow")
            logger.info("Falling back to fsaverage template...")
        except Exception as e:
            logger.warning(f"Could not load MNI152NLin2009cAsym surfaces: {e}")
            logger.info("Falling back to fsaverage template...")

    # Default: use fsaverage from nilearn
    # If mesh is 'MNI152NLin2009cAsym' but TemplateFlow not available, fall back to fsaverage
    if mesh == 'MNI152NLin2009cAsym':
        mesh = 'fsaverage'  # Use default fsaverage as fallback
        logger.info("Using fsaverage as fallback for MNI152NLin2009cAsym")

    fsaverage = nilearn_datasets.fetch_surf_fsaverage(mesh=mesh)

    # Get mesh file path
    if hemi == 'lh':
        mesh_file = fsaverage.pial_left
    else:
        mesh_file = fsaverage.pial_right

    # Load mesh geometry
    coords, faces = surface.load_surf_mesh(mesh_file)

    return coords, faces


def plot_interactive_surface_plotly(
    nifti_path: str,
    out_html: str,
    *,
    hemi: str = 'both',
    mesh: str = 'fsaverage5',
    template: str = 'fsaverage',
    colormap: str = 'hot',
    threshold: Optional[float] = None,
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    radius: float = 2.0,
    interpolation: str = 'linear',
    surface_name: str = 'pial',
    title: Optional[str] = None,
    initial_camera: Optional[Dict[str, Any]] = None,
    show_colorbar: bool = True,
    opacity: float = 1.0,
) -> str:
    """
    Create fully interactive 3D brain surface visualization with Plotly.

    This function creates a 3D mesh visualization of brain data projected onto
    the cortical surface. The result is a standalone HTML file that can be
    rotated, zoomed, and panned with mouse controls.

    Args:
        nifti_path: Path to input NIfTI file
        out_html: Output HTML file path
        hemi: Hemisphere ('lh', 'rh', or 'both'). Default: 'both' with 1mm spacing
        mesh: Surface mesh resolution ('fsaverage5', 'fsaverage', 'fsaverage6', 'MNI152NLin2009cAsym'). Default: 'fsaverage5'
        template: Template to use ('fsaverage' or 'MNI152NLin2009cAsym' for ICBM152)
        colormap: Matplotlib colormap name ('hot', 'jet', 'viridis', etc.)
        threshold: Value threshold (values below this are transparent)
        vmin: Minimum value for colormap
        vmax: Maximum value for colormap
        radius: Sampling radius in mm for volume-to-surface projection
        interpolation: Interpolation method ('linear' or 'nearest')
        surface_name: Surface type ('pial', 'inflated', 'white', 'sphere')
        title: Plot title (default: filename)
        initial_camera: Camera position dict (e.g., {'eye': {'x': 0, 'y': 0, 'z': 2.5}})
        show_colorbar: Whether to show colorbar
        opacity: Mesh opacity (0-1)

    Returns:
        Path to saved HTML file

    Raises:
        ImportError: If plotly is not installed
        FileNotFoundError: If NIfTI file doesn't exist
        ValueError: If parameters are invalid

    Example:
        >>> plot_interactive_surface_plotly(
        ...     'brain.nii.gz',
        ...     'brain_3d.html',
        ...     hemi='both',
        ...     colormap='hot'
        ... )
        >>> # Opens HTML in browser - rotate to any angle!
    """
    _check_plotly()

    # Validate inputs
    if not os.path.exists(nifti_path):
        raise FileNotFoundError(f"NIfTI file not found: {nifti_path}")

    if hemi not in {'lh', 'rh', 'both', 'left', 'right'}:
        raise ValueError(f"hemi must be 'lh', 'rh', or 'both', got '{hemi}'")

    # Normalize hemisphere naming
    if hemi in ('left', 'lh'):
        hemis = ['lh']
    elif hemi in ('right', 'rh'):
        hemis = ['rh']
    else:
        hemis = ['lh', 'rh']

    # Load NIfTI data
    img = nib.load(nifti_path)

    # Auto-compute thresholds if not provided
    if vmin is None or vmax is None or threshold is None:
        data = np.asanyarray(img.get_fdata())
        data = data[np.isfinite(data) & (data > 0)]
        if data.size > 0:
            if vmin is None:
                vmin = 0.0
            if vmax is None:
                vmax = float(np.percentile(data, 99))
            if threshold is None:
                threshold = float(np.percentile(data, 10))
        else:
            vmin, vmax, threshold = 0.0, 1.0, 0.0

    logger.info(f"Value range: [{vmin:.3f}, {vmax:.3f}], threshold: {threshold:.3f}")

    # Create Plotly figure
    fig = go.Figure()

    # Process each hemisphere
    for hemi_code in hemis:
        logger.info(f"Processing {hemi_code} hemisphere...")

        # Load mesh geometry
        vertices, faces = _load_fsaverage_mesh_data(mesh=mesh, hemi=hemi_code, template=template)

        # Project volume to surface
        # For MNI152NLin2009cAsym, use TemplateFlow surfaces for projection
        if template == 'MNI152NLin2009cAsym' or mesh == 'MNI152NLin2009cAsym':
            try:
                import templateflow.api as tflow
                hemi_suffix = 'L' if hemi_code == 'lh' else 'R'
                surf_mesh = tflow.get(
                    'MNI152NLin2009cAsym',
                    hemi=hemi_suffix,
                    density='32k',
                    suffix='pial',
                    extension='surf.gii'
                )
            except:
                # Fall back to fsaverage
                fallback_mesh = 'fsaverage' if mesh == 'MNI152NLin2009cAsym' else mesh
                fsaverage = nilearn_datasets.fetch_surf_fsaverage(mesh=fallback_mesh)
                surf_mesh = fsaverage.pial_left if hemi_code == "lh" else fsaverage.pial_right
        else:
            # Use fsaverage surfaces
            fsaverage = nilearn_datasets.fetch_surf_fsaverage(mesh=mesh)
            surface_attr_map = {
                "pial": "pial",
                "inflated": "infl",
                "white": "white",
                "sphere": "sphere",
            }
            if surface_name not in surface_attr_map:
                raise ValueError(f"surface_name must be one of {list(surface_attr_map.keys())}")
            surf_attr = surface_attr_map[surface_name]
            surf_mesh = getattr(fsaverage, f"{surf_attr}_left" if hemi_code == "lh" else f"{surf_attr}_right")

        texture = surface.vol_to_surf(
            img,
            surf_mesh,
            radius=radius,
            interpolation=interpolation,
        )

        # Apply threshold
        texture_display = texture.copy()
        texture_display[texture < threshold] = np.nan

        # Normalize values for colormap
        texture_norm = (texture_display - vmin) / (vmax - vmin)
        texture_norm = np.clip(texture_norm, 0, 1)

        # Convert colormap to RGB colors
        colors = _apply_colormap(texture_norm, colormap)

        # Shift right hemisphere to the side if plotting both
        if hemi == 'both' and hemi_code == 'rh':
            vertices = vertices.copy()
            vertices[:, 0] += 1  # Shift 1mm to the right (extremely close spacing)

        # Create mesh trace
        mesh_trace = go.Mesh3d(
            x=vertices[:, 0],
            y=vertices[:, 1],
            z=vertices[:, 2],
            i=faces[:, 0],
            j=faces[:, 1],
            k=faces[:, 2],
            vertexcolor=colors,
            opacity=opacity,
            name=f'{hemi_code.upper()} Hemisphere',
            hoverinfo='skip',
            lighting=dict(
                ambient=0.5,
                diffuse=0.8,
                fresnel=0.2,
                specular=0.3,
                roughness=0.5
            ),
            lightposition=dict(
                x=100,
                y=200,
                z=0
            )
        )

        fig.add_trace(mesh_trace)

    # Configure layout
    plot_title = title or os.path.basename(nifti_path)

    # Set initial camera position
    if initial_camera is None:
        # Default: slightly angled dorsal view for best visibility
        initial_camera = dict(
            eye=dict(x=0, y=0, z=2.0),
            center=dict(x=0, y=0, z=0),
            up=dict(x=0, y=1, z=0)
        )

    fig.update_layout(
        title=dict(
            text=plot_title,
            x=0.5,
            xanchor='center',
            font=dict(size=20)
        ),
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            camera=initial_camera,
            aspectmode='data',
            bgcolor='white'
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        width=1200,
        height=800,
        showlegend=False,
        margin=dict(l=0, r=0, t=50, b=0),
    )

    # Add colorbar if requested
    if show_colorbar:
        # Create a dummy scatter trace for colorbar
        colorbar_trace = go.Scatter3d(
            x=[None],
            y=[None],
            z=[None],
            mode='markers',
            marker=dict(
                colorscale=_get_plotly_colorscale(colormap),
                cmin=vmin,
                cmax=vmax,
                colorbar=dict(
                    title="Intensity",
                    thickness=20,
                    len=0.7,
                    x=1.02
                ),
                showscale=True
            ),
            hoverinfo='skip',
            showlegend=False
        )
        fig.add_trace(colorbar_trace)

    # Save to HTML
    os.makedirs(os.path.dirname(out_html) or '.', exist_ok=True)
    fig.write_html(
        out_html,
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'brain_3d',
                'height': 1200,
                'width': 1600,
                'scale': 2
            }
        }
    )

    logger.info(f"Saved interactive 3D visualization: {out_html}")
    logger.info(f"File size: {os.path.getsize(out_html) / (1024**2):.2f} MB")
    logger.info("Open in browser to rotate, zoom, and explore!")

    return out_html


def _apply_colormap(values: np.ndarray, colormap: str) -> np.ndarray:
    """
    Apply matplotlib colormap to normalized values (0-1).

    Args:
        values: Normalized values (0-1, can contain NaN)
        colormap: Matplotlib colormap name

    Returns:
        RGB colors as (N, 3) array
    """
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors

    # Get colormap
    cmap = plt.get_cmap(colormap)

    # Apply colormap
    colors = cmap(values)[:, :3]  # RGB only (drop alpha)

    # Handle NaN values (make them transparent gray)
    nan_mask = np.isnan(values)
    colors[nan_mask] = [0.8, 0.8, 0.8]  # Light gray for below threshold

    # Convert to RGB strings for Plotly
    colors_rgb = ['rgb({},{},{})'.format(
        int(r*255), int(g*255), int(b*255)
    ) for r, g, b in colors]

    return colors_rgb


def _get_plotly_colorscale(colormap: str) -> list:
    """
    Convert matplotlib colormap to Plotly colorscale.

    Args:
        colormap: Matplotlib colormap name

    Returns:
        Plotly colorscale list
    """
    import matplotlib.pyplot as plt

    cmap = plt.get_cmap(colormap)

    # Sample colormap at regular intervals
    n_samples = 20
    positions = np.linspace(0, 1, n_samples)

    colorscale = []
    for pos in positions:
        rgba = cmap(pos)
        rgb = rgba[:3]
        color_str = f'rgb({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)})'
        colorscale.append([pos, color_str])

    return colorscale
