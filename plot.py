import os
from typing import Iterable, List, Optional, Tuple

import numpy as np
import nibabel as nib
from nilearn import datasets as nilearn_datasets
from nilearn import surface, plotting, image
import matplotlib

# Non-interactive backend for headless servers
matplotlib.use("Agg", force=True)


def _auto_scaling_from_img(img: nib.spatialimages.SpatialImage) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    data = np.asanyarray(img.get_fdata())
    data = data[np.isfinite(data)]
    data = data[data > 0]
    if data.size == 0:
        return 0.0, None, None
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

    Returns (surf_mesh_path, sulc_map_path, texture_array).
    
    Available surfaces: pial, inflated, white, sphere
    """
    if hemi not in {"lh", "rh"}:
        raise ValueError("hemi must be 'lh' or 'rh'")

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
        hemi: 'left' or 'right' (or 'lh'/'rh' for convenience)
    
    Saves a PNG to out_path and returns it.
    """
    # Normalize hemisphere naming
    hemi_map = {"lh": "left", "rh": "right", "left": "left", "right": "right"}
    if hemi not in hemi_map:
        raise ValueError(f"hemi must be one of {list(hemi_map.keys())}, got {hemi}")
    hemi_nilearn = hemi_map[hemi]
    hemi_fetch = "lh" if hemi in ("lh", "left") else "rh"
    
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
    import matplotlib.pyplot as plt
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
    """Create lateral/medial/dorsal/ventral images for the requested hemispheres.

    Returns list of output file paths.
    """
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
) -> "nilearn.plotting.displays.SurfaceView":
    """Create an interactive 3D plot that opens in a web browser.
    
    Returns a view_img_on_surf object that can be opened in browser
    or saved to HTML.
    
    Example:
        view = plot_3d_interactive("map.nii.gz", colormap="hot")
        view.open_in_browser()
        view.save_as_html("plot.html")
    """
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



