import os
import logging
from typing import Iterable, List, Optional, Tuple

import numpy as np
import nibabel as nib
from nilearn import datasets as nilearn_datasets
from nilearn import surface, plotting, image
import matplotlib
import matplotlib.pyplot as plt

# Non-interactive backend for headless servers
matplotlib.use("Agg", force=True)

# Setup logging
logger = logging.getLogger(__name__)


def _auto_scaling_from_img(img: nib.spatialimages.SpatialImage) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    """Compute automatic scaling parameters from image data.

    Returns (vmin, vmax, threshold) for plotting.
    Raises ValueError if image contains no positive finite values.
    """
    data = np.asanyarray(img.get_fdata())
    data = data[np.isfinite(data)]
    data = data[data > 0]
    if data.size == 0:
        raise ValueError(
            "NIfTI file contains no positive finite values to plot. "
            "Check that your data has the expected range and contains valid values."
        )
    vmin = 0.0
    vmax = float(np.percentile(data, 99))
    threshold = float(np.percentile(data, 10))
    return vmin, vmax, threshold


def project_volume_to_surface(
    nifti_path: str,
    hemi: str,
    mesh: str = "fsaverage",
    surface_name: str = "pial",
    radius: float = 2.0,
    interpolation: str = "linear",
    kind: str = "line",
    smooth_fwhm_mm: Optional[float] = None,
):
    """Project a NIfTI volume to a cortical surface texture.

    Args:
        nifti_path: Path to NIfTI file (.nii or .nii.gz)
        hemi: Hemisphere to project ('lh' or 'rh')
        mesh: Surface mesh resolution ('fsaverage' or 'fsaverage5')
        surface_name: Surface type ('pial', 'inflated', 'white', 'sphere')
        radius: Sampling radius in mm
        interpolation: Interpolation method
        kind: Sampling kind
        smooth_fwhm_mm: Optional smoothing kernel size in mm

    Returns:
        Tuple of (surf_mesh_path, sulc_map_path, texture_array)

    Raises:
        ValueError: If parameters are invalid
        FileNotFoundError: If NIfTI file doesn't exist
    """
    # Validate inputs
    if not os.path.exists(nifti_path):
        raise FileNotFoundError(f"NIfTI file not found: {nifti_path}")

    if hemi not in {"lh", "rh"}:
        raise ValueError(f"hemi must be 'lh' or 'rh', got '{hemi}'")

    img = nib.load(nifti_path)
    if smooth_fwhm_mm is not None and smooth_fwhm_mm > 0:
        img = image.smooth_img(img, fwhm=smooth_fwhm_mm)

    fsaverage = nilearn_datasets.fetch_surf_fsaverage(mesh=mesh)
    
    # Map surface names to fsaverage attributes
    # fsaverage has: pial, white, inflated, sphere (each _left and _right)
    surface_attr_map = {
        "pial": "pial",
        "inflated": "infl",  # Note: it's 'infl' not 'inflated'
        "white": "white",
        "sphere": "sphere",
    }
    
    if surface_name not in surface_attr_map:
        raise ValueError(f"surface_name must be one of {list(surface_attr_map.keys())}, got {surface_name}")
    
    surf_attr = surface_attr_map[surface_name]
    surf_mesh = getattr(fsaverage, f"{surf_attr}_left" if hemi == "lh" else f"{surf_attr}_right")
    sulc_map = fsaverage.sulc_left if hemi == "lh" else fsaverage.sulc_right

    texture = surface.vol_to_surf(
        img,
        surf_mesh,
        radius=radius,
        interpolation=interpolation,
        kind=kind,
    )
    return surf_mesh, sulc_map, texture


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def plot_nifti(
    nifti_path: str,
    out_path: str,
    *,
    hemi: str,
    view: str,
    mesh: str = "fsaverage",
    surface_name: str = "pial",
    colormap: str = "jet",
    alpha: float = 0.8,
    darkness: float = 0.8,
    radius: float = 2.0,
    dpi: int = 300,
) -> str:
    """Render a single surface view with sulcal shading.

    Args:
        nifti_path: Path to NIfTI file
        out_path: Output path for PNG file
        hemi: Hemisphere ('left', 'right', 'lh', or 'rh')
        view: View angle ('lateral', 'medial', 'dorsal', 'ventral', 'anterior', 'posterior')
        mesh: Surface mesh resolution ('fsaverage' or 'fsaverage5')
        surface_name: Surface type ('pial', 'inflated', 'white', 'sphere')
        colormap: Matplotlib colormap name
        alpha: Transparency of overlay (0-1)
        darkness: Darkness of sulcal shading (0-1)
        radius: Sampling radius in mm
        dpi: Output resolution in dots per inch

    Returns:
        Path to saved PNG file

    Raises:
        FileNotFoundError: If NIfTI file doesn't exist
        ValueError: If parameters are invalid
    """
    # Validate inputs
    if not os.path.exists(nifti_path):
        raise FileNotFoundError(f"NIfTI file not found: {nifti_path}")

    # Normalize hemisphere naming
    hemi_map = {"lh": "left", "rh": "right", "left": "left", "right": "right"}
    if hemi not in hemi_map:
        raise ValueError(f"hemi must be one of {list(hemi_map.keys())}, got '{hemi}'")
    hemi_nilearn = hemi_map[hemi]
    hemi_fetch = "lh" if hemi in ("lh", "left") else "rh"

    # Validate DPI
    if dpi <= 0:
        raise ValueError(f"dpi must be positive, got {dpi}")

    # Validate alpha and darkness
    if not 0 <= alpha <= 1:
        raise ValueError(f"alpha must be between 0 and 1, got {alpha}")
    if not 0 <= darkness <= 1:
        raise ValueError(f"darkness must be between 0 and 1, got {darkness}")

    img = nib.load(nifti_path)
    vmin, vmax, threshold = _auto_scaling_from_img(img)

    surf_mesh, sulc_map, texture = project_volume_to_surface(
        nifti_path,
        hemi=hemi_fetch,
        mesh=mesh,
        surface_name=surface_name,
        radius=radius,
    )

    _ensure_dir(os.path.dirname(out_path))

    fig = plotting.plot_surf_stat_map(
        surf_mesh,
        texture,
        bg_map=sulc_map,
        bg_on_data=True,
        hemi=hemi_nilearn,
        view=view,
        cmap=colormap,
        colorbar=True,
        darkness=darkness,
        threshold=threshold,
        vmin=vmin,
        vmax=vmax,
        alpha=alpha,
    )
    fig.savefig(out_path, dpi=dpi, bbox_inches='tight')

    # Close matplotlib figure to free memory
    plt.close(fig)

    return out_path


def generate_four_views(
    nifti_path: str,
    out_dir: str,
    *,
    hemis: Iterable[str] = ("lh", "rh"),
    views: Iterable[str] = ("lateral", "medial", "dorsal", "ventral"),
    mesh: str = "fsaverage",
    surface_name: str = "pial",
    colormap: str = "jet",
    prefix: Optional[str] = None,
) -> List[str]:
    """Create multiple surface view images for requested hemispheres.

    Args:
        nifti_path: Path to NIfTI file
        out_dir: Output directory for PNG files
        hemis: Tuple of hemispheres to render ('lh', 'rh', 'left', 'right')
        views: Tuple of views to render
        mesh: Surface mesh resolution
        surface_name: Surface type
        colormap: Matplotlib colormap name
        prefix: Optional filename prefix (default: NIfTI filename)

    Returns:
        List of paths to generated PNG files

    Raises:
        FileNotFoundError: If NIfTI file doesn't exist
    """
    # Validate input file exists
    if not os.path.exists(nifti_path):
        raise FileNotFoundError(f"NIfTI file not found: {nifti_path}")

    outputs: List[str] = []
    base = prefix or os.path.splitext(os.path.basename(nifti_path))[0]

    for hemi in hemis:
        for view in views:
            fn = f"{base}_{hemi}_{view}.png"
            out_path = os.path.join(out_dir, fn)
            try:
                plot_nifti(
                    nifti_path,
                    out_path,
                    hemi=hemi,
                    view=view,
                    mesh=mesh,
                    surface_name=surface_name,
                    colormap=colormap,
                )
                outputs.append(out_path)
            except Exception as e:
                # Continue other renders even if one fails
                logger.warning(f"Failed to render {hemi} {view}: {e}")
                print(f"✗ Failed {hemi} {view}: {e}")
    return outputs


def generate_all_standard_views(
    nifti_path: str,
    out_dir: str,
    *,
    mesh: str = "fsaverage",
    surface_name: str = "pial",
    colormap: str = "jet",
    prefix: Optional[str] = None,
) -> List[str]:
    """Generate all standard neuroimaging views.
    
    Creates 10 views total:
    - Left hemisphere: lateral, medial, dorsal, ventral, anterior, posterior
    - Right hemisphere: lateral, medial, dorsal, ventral, anterior, posterior
    
    Returns list of output file paths.
    """
    standard_views = ["lateral", "medial", "dorsal", "ventral", "anterior", "posterior"]
    
    return generate_four_views(
        nifti_path,
        out_dir,
        hemis=("lh", "rh"),
        views=standard_views,
        mesh=mesh,
        surface_name=surface_name,
        colormap=colormap,
        prefix=prefix,
    )


def plot_3d_interactive(
    nifti_path: str,
    *,
    threshold: Optional[float] = None,
    colormap: str = "jet",
    symmetric_cmap: bool = False,
    title: Optional[str] = None,
):
    """Create an interactive 3D plot that opens in a web browser.

    Args:
        nifti_path: Path to NIfTI file
        threshold: Value threshold for display (auto-computed if None)
        colormap: Matplotlib colormap name
        symmetric_cmap: Use symmetric colormap
        title: Plot title (default: filename)

    Returns:
        Nilearn view object with methods:
            - open_in_browser(): Open in web browser
            - save_as_html(path): Save to HTML file

    Raises:
        FileNotFoundError: If NIfTI file doesn't exist

    Example:
        view = plot_3d_interactive("map.nii.gz", colormap="hot")
        view.open_in_browser()
        view.save_as_html("plot.html")
    """
    # Validate input file exists
    if not os.path.exists(nifti_path):
        raise FileNotFoundError(f"NIfTI file not found: {nifti_path}")

    from nilearn import plotting

    img = nib.load(nifti_path)
    
    # Auto threshold if not provided
    if threshold is None:
        data = np.asanyarray(img.get_fdata())
        data = data[np.isfinite(data) & (data > 0)]
        if data.size > 0:
            threshold = float(np.percentile(data, 10))
        else:
            threshold = 0
    
    view = plotting.view_img_on_surf(
        img,
        threshold=threshold,
        cmap=colormap,
        symmetric_cmap=symmetric_cmap,
        surf_mesh='fsaverage',
        title=title or os.path.basename(nifti_path),
    )
    
    return view



