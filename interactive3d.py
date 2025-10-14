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
from typing import Optional, Tuple, Dict, Any, Union, List
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

# Available parcellation schemes
PARCELLATION_SCHEMES = {
    'yeo-7-thin': {
        'name': 'Yeo 2011 7 Networks (Thin)',
        'n_networks': 7,
        'thickness': 'thin',
    },
    'yeo-7-thick': {
        'name': 'Yeo 2011 7 Networks (Thick)',
        'n_networks': 7,
        'thickness': 'thick',
    },
    'yeo-17-thin': {
        'name': 'Yeo 2011 17 Networks (Thin)',
        'n_networks': 17,
        'thickness': 'thin',
    },
    'yeo-17-thick': {
        'name': 'Yeo 2011 17 Networks (Thick)',
        'n_networks': 17,
        'thickness': 'thick',
    },
}


def _check_plotly():
    """Check if plotly is installed."""
    if not PLOTLY_AVAILABLE:
        raise ImportError(
            "Plotly is required for interactive 3D visualization. "
            "Install with: pip install plotly"
        )


def _load_parcellation(parcellation: str, surf_mesh: str) -> np.ndarray:
    """
    Load and project parcellation to surface.

    Args:
        parcellation: Parcellation scheme (e.g., 'yeo-7-thick', 'yeo-17-thin')
        surf_mesh: Surface mesh file path for projection

    Returns:
        Array of network labels for each vertex
    """
    if parcellation not in PARCELLATION_SCHEMES:
        raise ValueError(
            f"Unknown parcellation '{parcellation}'. "
            f"Available: {list(PARCELLATION_SCHEMES.keys())}"
        )

    scheme = PARCELLATION_SCHEMES[parcellation]
    logger.info(f"Loading {scheme['name']}...")

    # Fetch Yeo atlas
    yeo = nilearn_datasets.fetch_atlas_yeo_2011()

    # Select appropriate volume based on parameters
    if scheme['n_networks'] == 7:
        vol_file = yeo[f"{scheme['thickness']}_7"]
    else:
        vol_file = yeo[f"{scheme['thickness']}_17"]

    # Load volumetric parcellation
    parc_img = nib.load(vol_file)

    # Project to surface using nearest neighbor interpolation
    parc_surf = surface.vol_to_surf(
        parc_img,
        surf_mesh,
        radius=3.0,  # Larger radius for parcellations
        interpolation='nearest',  # Use nearest to preserve integer labels
    )

    logger.info(f"Projected parcellation to surface: {len(np.unique(parc_surf[parc_surf > 0]))} networks")
    return parc_surf


def _find_network_boundaries(faces: np.ndarray, network_labels: np.ndarray) -> List[Tuple[int, int]]:
    """
    Find edges at network boundaries.

    Args:
        faces: Array of triangle faces (N, 3)
        network_labels: Network label for each vertex

    Returns:
        List of vertex pairs (edges) at network boundaries
    """
    boundary_edges = set()

    # For each triangle face
    for face in faces:
        v1, v2, v3 = face
        labels = network_labels[[v1, v2, v3]]

        # Check each edge of the triangle
        edges = [(v1, v2), (v2, v3), (v3, v1)]

        for i, (va, vb) in enumerate(edges):
            # If vertices have different labels (and both are valid networks)
            if labels[i % 3] != labels[(i + 1) % 3]:
                if labels[i % 3] > 0 and labels[(i + 1) % 3] > 0:
                    # Add edge (sorted to avoid duplicates)
                    edge = tuple(sorted([va, vb]))
                    boundary_edges.add(edge)

    logger.info(f"Found {len(boundary_edges)} boundary edges")
    return list(boundary_edges)


def _create_contour_lines(
    vertices: np.ndarray,
    boundary_edges: List[Tuple[int, int]],
    color: str = 'black',
    width: float = 2.0
) -> go.Scatter3d:
    """
    Create Plotly scatter plot for network boundary contours.

    Args:
        vertices: Vertex coordinates (N, 3)
        boundary_edges: List of vertex index pairs
        color: Line color
        width: Line width

    Returns:
        Plotly Scatter3d trace for the contour lines
    """
    # Create line segments
    x_lines = []
    y_lines = []
    z_lines = []

    for v1, v2 in boundary_edges:
        # Add line segment
        x_lines.extend([vertices[v1, 0], vertices[v2, 0], None])
        y_lines.extend([vertices[v1, 1], vertices[v2, 1], None])
        z_lines.extend([vertices[v1, 2], vertices[v2, 2], None])

    # Create trace
    contour_trace = go.Scatter3d(
        x=x_lines,
        y=y_lines,
        z=z_lines,
        mode='lines',
        line=dict(color=color, width=width),
        name='Network Boundaries',
        hoverinfo='skip',
        showlegend=False
    )

    return contour_trace


def _load_fsaverage_mesh_data(mesh: str = 'fsaverage', hemi: str = 'lh', template: str = 'fsaverage'):
    """
    Load brain surface mesh geometry data.

    Args:
        mesh: Mesh resolution ('fsaverage', 'fsaverage5', 'fsaverage6', 'MNI152NLin2009cAsym')
        hemi: Hemisphere ('lh' or 'rh')
        template: Template to use ('fsaverage' or 'MNI152NLin2009cAsym')

    Returns:
        Tuple of (vertices, faces) as numpy arrays

    Note:
        MNI152NLin2009cAsym template uses fsaverage surfaces for visualization.
        This is the standard approach in neuroimaging (e.g., fMRIPrep workflow).
        Data in MNI152NLin2009cAsym space is projected to fsaverage surfaces.
    """
    # Handle ICBM152/MNI152NLin2009cAsym template
    # Note: TemplateFlow has volumetric templates but not surface meshes for MNI152NLin2009cAsym
    # Standard practice: use fsaverage surfaces with MNI space data
    if template == 'MNI152NLin2009cAsym' or mesh == 'MNI152NLin2009cAsym':
        logger.info(f"Using fsaverage surfaces for MNI152NLin2009cAsym template (standard approach)")
        # Use fsaverage or fsaverage5 as the actual mesh
        actual_mesh = 'fsaverage' if mesh == 'MNI152NLin2009cAsym' else mesh
    else:
        actual_mesh = mesh

    # Load fsaverage surfaces from nilearn
    fsaverage = nilearn_datasets.fetch_surf_fsaverage(mesh=actual_mesh)

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
    parcellation: Optional[str] = None,
    contour_color: str = 'black',
    contour_width: float = 2.0,
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
        parcellation: Network parcellation scheme ('yeo-7-thin', 'yeo-7-thick', 'yeo-17-thin', 'yeo-17-thick')
        contour_color: Color for network boundary contours (default: 'black')
        contour_width: Width of network boundary lines (default: 2.0)

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
        # Determine actual mesh to use
        if template == 'MNI152NLin2009cAsym' or mesh == 'MNI152NLin2009cAsym':
            # Use fsaverage surfaces for MNI152NLin2009cAsym (standard practice)
            actual_mesh = 'fsaverage' if mesh == 'MNI152NLin2009cAsym' else mesh
        else:
            actual_mesh = mesh

        # Load fsaverage surfaces
        fsaverage = nilearn_datasets.fetch_surf_fsaverage(mesh=actual_mesh)
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

        # Add network parcellation contours if requested
        if parcellation is not None:
            logger.info(f"Adding {parcellation} network boundaries...")

            # Load parcellation and project to surface
            network_labels = _load_parcellation(parcellation, surf_mesh)

            # Find network boundaries
            boundary_edges = _find_network_boundaries(faces, network_labels)

            # Create contour lines
            if len(boundary_edges) > 0:
                contour_trace = _create_contour_lines(
                    vertices,
                    boundary_edges,
                    color=contour_color,
                    width=contour_width
                )
                fig.add_trace(contour_trace)
                logger.info(f"Added {len(boundary_edges)} network boundary edges")
            else:
                logger.warning(f"No network boundaries found for {hemi_code} hemisphere")

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
