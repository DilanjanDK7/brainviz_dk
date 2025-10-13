"""
Volumetric brain visualization module.

Provides functions for plotting volumetric NIfTI data using MNI152/ICBM152 templates.
Includes slice plotting, glass brain visualization, and mosaic views.
"""

import os
import logging
from typing import Optional, Tuple, List, Union

import numpy as np
import nibabel as nib
from nilearn import datasets as nilearn_datasets
from nilearn import plotting, image
import matplotlib
import matplotlib.pyplot as plt

# Non-interactive backend for headless servers
matplotlib.use("Agg", force=True)

logger = logging.getLogger(__name__)


def plot_volumetric_slices(
    nifti_path: str,
    out_path: str,
    *,
    template: str = "mni152",
    display_mode: str = "ortho",
    cut_coords: Optional[Union[int, List[float]]] = None,
    colormap: str = "hot",
    threshold: Optional[float] = None,
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    symmetric_cbar: bool = False,
    annotate: bool = True,
    draw_cross: bool = True,
    black_bg: bool = False,
    dpi: int = 300,
    figsize: Optional[Tuple[float, float]] = None,
    output_format: Optional[str] = None,
    title: Optional[str] = None,
) -> str:
    """Plot volumetric slices with anatomical template underlay.

    Args:
        nifti_path: Path to NIfTI file
        out_path: Output path for image file
        template: Template to use ('mni152', 'icbm152', or path to template)
        display_mode: Display mode ('ortho', 'x', 'y', 'z', 'yx', 'xz', 'yz')
        cut_coords: Slice coordinates (int=number of slices, list=specific coords)
        colormap: Matplotlib colormap name
        threshold: Value threshold for display
        vmin: Minimum value for colormap
        vmax: Maximum value for colormap
        symmetric_cbar: Use symmetric colorbar
        annotate: Show slice coordinates
        draw_cross: Draw crosshair at cut coordinates
        black_bg: Use black background
        dpi: Output resolution in dots per inch
        figsize: Figure size as (width, height) in inches
        output_format: Output format ('png', 'svg', 'pdf', 'eps')
        title: Plot title

    Returns:
        Path to saved image file

    Example:
        >>> plot_volumetric_slices(
        ...     'stat_map.nii.gz',
        ...     'slices.png',
        ...     display_mode='ortho',
        ...     cut_coords=(0, 0, 0),
        ...     colormap='hot'
        ... )
    """
    # Validate inputs
    if not os.path.exists(nifti_path):
        raise FileNotFoundError(f"NIfTI file not found: {nifti_path}")

    # Load statistical map
    stat_img = nib.load(nifti_path)

    # Load template
    if template == "mni152":
        bg_img = nilearn_datasets.load_mni152_template(resolution=1)
    elif template == "icbm152":
        # Use MNI152 as fallback (same space)
        bg_img = nilearn_datasets.load_mni152_template(resolution=1)
        logger.info("Using MNI152 template (ICBM152 compatible)")
    elif os.path.exists(template):
        bg_img = nib.load(template)
    else:
        raise ValueError(f"Invalid template: {template}")

    # Auto-compute threshold if not provided
    if threshold is None:
        data = np.asanyarray(stat_img.get_fdata())
        data_pos = data[np.isfinite(data) & (data > 0)]
        if data_pos.size > 0:
            threshold = float(np.percentile(data_pos, 80))
        else:
            threshold = 0

    # Set figure size if specified
    if figsize is not None:
        plt.rcParams['figure.figsize'] = figsize

    # Create the plot
    display = plotting.plot_stat_map(
        stat_img,
        bg_img=bg_img,
        display_mode=display_mode,
        cut_coords=cut_coords,
        threshold=threshold,
        cmap=colormap,
        vmin=vmin,
        vmax=vmax,
        symmetric_cbar=symmetric_cbar,
        colorbar=True,
        annotate=annotate,
        draw_cross=draw_cross,
        black_bg=black_bg,
        title=title or os.path.basename(nifti_path),
    )

    # Determine output format
    if output_format is None:
        ext = os.path.splitext(out_path)[1].lower()
        if ext in ['.png', '.svg', '.pdf', '.eps']:
            output_format = ext[1:]
        else:
            output_format = 'png'

    # Ensure correct file extension
    base, ext = os.path.splitext(out_path)
    if ext.lower() != f'.{output_format}':
        out_path = f"{base}.{output_format}"

    # Save with high quality settings
    # Note: nilearn display objects only accept dpi parameter
    display.savefig(out_path, dpi=dpi)
    display.close()

    # Reset figsize if it was changed
    if figsize is not None:
        plt.rcParams['figure.figsize'] = plt.rcParamsDefault['figure.figsize']

    logger.info(f"Saved volumetric slices: {out_path}")
    return out_path


def plot_glass_brain(
    nifti_path: str,
    out_path: str,
    *,
    display_mode: str = "lyrz",
    colormap: str = "hot",
    threshold: Optional[float] = None,
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    plot_abs: bool = True,
    alpha: float = 0.7,
    black_bg: bool = False,
    dpi: int = 600,
    figsize: Optional[Tuple[float, float]] = None,
    output_format: Optional[str] = None,
    title: Optional[str] = None,
) -> str:
    """Create a glass brain visualization.

    Glass brain shows activation projected onto a transparent brain surface,
    making it easy to see through the brain and visualize 3D activation patterns.

    Args:
        nifti_path: Path to NIfTI file
        out_path: Output path for image file
        display_mode: Display mode ('ortho', 'lyrz', 'lzry', 'lr', 'l', 'r')
        colormap: Matplotlib colormap name
        threshold: Value threshold for display
        vmin: Minimum value for colormap
        vmax: Maximum value for colormap
        plot_abs: Plot absolute values
        alpha: Transparency of overlay (0-1)
        black_bg: Use black background
        dpi: Output resolution (600 recommended for glass brain)
        figsize: Figure size as (width, height) in inches
        output_format: Output format ('png', 'svg', 'pdf')
        title: Plot title

    Returns:
        Path to saved image file

    Example:
        >>> plot_glass_brain(
        ...     'stat_map.nii.gz',
        ...     'glass_brain.png',
        ...     display_mode='lyrz',
        ...     dpi=600
        ... )
    """
    # Validate inputs
    if not os.path.exists(nifti_path):
        raise FileNotFoundError(f"NIfTI file not found: {nifti_path}")

    # Load statistical map
    stat_img = nib.load(nifti_path)

    # Auto-compute threshold if not provided
    if threshold is None:
        data = np.asanyarray(stat_img.get_fdata())
        data = data[np.isfinite(data)]
        if plot_abs:
            data = np.abs(data)
        if data.size > 0:
            threshold = float(np.percentile(data, 85))
        else:
            threshold = 0

    # Set figure size if specified
    if figsize is not None:
        plt.rcParams['figure.figsize'] = figsize

    # Create glass brain plot
    display = plotting.plot_glass_brain(
        stat_img,
        display_mode=display_mode,
        threshold=threshold,
        cmap=colormap,
        vmin=vmin,
        vmax=vmax,
        colorbar=True,
        plot_abs=plot_abs,
        alpha=alpha,
        black_bg=black_bg,
        title=title or os.path.basename(nifti_path),
    )

    # Determine output format
    if output_format is None:
        ext = os.path.splitext(out_path)[1].lower()
        if ext in ['.png', '.svg', '.pdf', '.eps']:
            output_format = ext[1:]
        else:
            output_format = 'png'

    # Ensure correct file extension
    base, ext = os.path.splitext(out_path)
    if ext.lower() != f'.{output_format}':
        out_path = f"{base}.{output_format}"

    # Save with high quality settings
    # Note: nilearn display objects only accept dpi parameter
    display.savefig(out_path, dpi=dpi)
    display.close()

    # Reset figsize if it was changed
    if figsize is not None:
        plt.rcParams['figure.figsize'] = plt.rcParamsDefault['figure.figsize']

    logger.info(f"Saved glass brain: {out_path}")
    return out_path


def plot_mosaic(
    nifti_path: str,
    out_path: str,
    *,
    template: str = "mni152",
    display_mode: str = "z",
    n_slices: int = 12,
    colormap: str = "hot",
    threshold: Optional[float] = None,
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    black_bg: bool = False,
    dpi: int = 300,
    figsize: Optional[Tuple[float, float]] = None,
    output_format: Optional[str] = None,
    title: Optional[str] = None,
) -> str:
    """Create a mosaic view of multiple slices.

    Args:
        nifti_path: Path to NIfTI file
        out_path: Output path for image file
        template: Template to use ('mni152', 'icbm152')
        display_mode: Axis to slice ('x', 'y', 'z')
        n_slices: Number of slices to display
        colormap: Matplotlib colormap name
        threshold: Value threshold for display
        vmin: Minimum value for colormap
        vmax: Maximum value for colormap
        black_bg: Use black background
        dpi: Output resolution in dots per inch
        figsize: Figure size as (width, height) in inches
        output_format: Output format ('png', 'svg', 'pdf')
        title: Plot title

    Returns:
        Path to saved image file

    Example:
        >>> plot_mosaic(
        ...     'stat_map.nii.gz',
        ...     'mosaic.png',
        ...     display_mode='z',
        ...     n_slices=20
        ... )
    """
    # Validate inputs
    if not os.path.exists(nifti_path):
        raise FileNotFoundError(f"NIfTI file not found: {nifti_path}")

    if display_mode not in {'x', 'y', 'z'}:
        raise ValueError(f"display_mode must be 'x', 'y', or 'z', got '{display_mode}'")

    # Load statistical map
    stat_img = nib.load(nifti_path)

    # Load template
    if template == "mni152":
        bg_img = nilearn_datasets.load_mni152_template(resolution=2)  # Lower res for speed
    elif template == "icbm152":
        bg_img = nilearn_datasets.load_mni152_template(resolution=2)
        logger.info("Using MNI152 template (ICBM152 compatible)")
    else:
        raise ValueError(f"Invalid template: {template}")

    # Auto-compute threshold if not provided
    if threshold is None:
        data = np.asanyarray(stat_img.get_fdata())
        data_pos = data[np.isfinite(data) & (data > 0)]
        if data_pos.size > 0:
            threshold = float(np.percentile(data_pos, 80))
        else:
            threshold = 0

    # Set figure size if specified
    if figsize is not None:
        plt.rcParams['figure.figsize'] = figsize

    # Create mosaic plot
    display = plotting.plot_stat_map(
        stat_img,
        bg_img=bg_img,
        display_mode=display_mode,
        cut_coords=n_slices,
        threshold=threshold,
        cmap=colormap,
        vmin=vmin,
        vmax=vmax,
        colorbar=True,
        black_bg=black_bg,
        title=title or os.path.basename(nifti_path),
    )

    # Determine output format
    if output_format is None:
        ext = os.path.splitext(out_path)[1].lower()
        if ext in ['.png', '.svg', '.pdf', '.eps']:
            output_format = ext[1:]
        else:
            output_format = 'png'

    # Ensure correct file extension
    base, ext = os.path.splitext(out_path)
    if ext.lower() != f'.{output_format}':
        out_path = f"{base}.{output_format}"

    # Save with high quality settings
    # Note: nilearn display objects only accept dpi parameter
    display.savefig(out_path, dpi=dpi)
    display.close()

    # Reset figsize if it was changed
    if figsize is not None:
        plt.rcParams['figure.figsize'] = plt.rcParamsDefault['figure.figsize']

    logger.info(f"Saved mosaic view: {out_path}")
    return out_path


def plot_roi_overlay(
    nifti_path: str,
    out_path: str,
    *,
    template: str = "mni152",
    display_mode: str = "ortho",
    cut_coords: Optional[Union[int, List[float]]] = None,
    colormap: str = "Paired",
    alpha: float = 0.7,
    black_bg: bool = False,
    dpi: int = 300,
    figsize: Optional[Tuple[float, float]] = None,
    output_format: Optional[str] = None,
    title: Optional[str] = None,
) -> str:
    """Plot ROI (Region of Interest) overlay on anatomical template.

    Useful for parcellation maps, atlas overlays, or discrete label maps.

    Args:
        nifti_path: Path to NIfTI file with ROIs
        out_path: Output path for image file
        template: Template to use ('mni152', 'icbm152')
        display_mode: Display mode ('ortho', 'x', 'y', 'z')
        cut_coords: Slice coordinates
        colormap: Colormap for discrete labels ('Paired', 'tab20', etc.)
        alpha: Transparency of overlay
        black_bg: Use black background
        dpi: Output resolution
        figsize: Figure size
        output_format: Output format
        title: Plot title

    Returns:
        Path to saved image file
    """
    # Validate inputs
    if not os.path.exists(nifti_path):
        raise FileNotFoundError(f"NIfTI file not found: {nifti_path}")

    # Load ROI map
    roi_img = nib.load(nifti_path)

    # Load template
    if template == "mni152":
        bg_img = nilearn_datasets.load_mni152_template(resolution=1)
    elif template == "icbm152":
        bg_img = nilearn_datasets.load_mni152_template(resolution=1)
        logger.info("Using MNI152 template (ICBM152 compatible)")
    else:
        raise ValueError(f"Invalid template: {template}")

    # Set figure size if specified
    if figsize is not None:
        plt.rcParams['figure.figsize'] = figsize

    # Create ROI overlay plot
    display = plotting.plot_roi(
        roi_img,
        bg_img=bg_img,
        display_mode=display_mode,
        cut_coords=cut_coords,
        cmap=colormap,
        alpha=alpha,
        black_bg=black_bg,
        title=title or os.path.basename(nifti_path),
    )

    # Determine output format
    if output_format is None:
        ext = os.path.splitext(out_path)[1].lower()
        if ext in ['.png', '.svg', '.pdf', '.eps']:
            output_format = ext[1:]
        else:
            output_format = 'png'

    # Ensure correct file extension
    base, ext = os.path.splitext(out_path)
    if ext.lower() != f'.{output_format}':
        out_path = f"{base}.{output_format}"

    # Save
    save_kwargs = {
        'dpi': dpi,
        'bbox_inches': 'tight',
        'format': output_format,
        'facecolor': 'black' if black_bg else 'white',
    }

    display.savefig(out_path, **save_kwargs)
    display.close()

    # Reset figsize
    if figsize is not None:
        plt.rcParams['figure.figsize'] = plt.rcParamsDefault['figure.figsize']

    logger.info(f"Saved ROI overlay: {out_path}")
    return out_path
