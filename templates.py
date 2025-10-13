"""
Brain template management module.

Provides unified access to brain templates from multiple sources
(nilearn, templateflow, local files).
"""

import os
import logging
from typing import Optional, Dict, Tuple
from pathlib import Path

import nibabel as nib
from nilearn import datasets as nilearn_datasets

logger = logging.getLogger(__name__)

# Try to import templateflow (optional dependency)
try:
    import templateflow.api as tflow
    TEMPLATEFLOW_AVAILABLE = True
except ImportError:
    TEMPLATEFLOW_AVAILABLE = False
    logger.warning(
        "TemplateFlow not available. Install with: pip install templateflow\n"
        "Advanced templates (MNI152NLin2009cAsym) will not be available."
    )


class TemplateManager:
    """
    Manage brain templates from multiple sources.

    Supports templates from:
    - Nilearn (MNI152, fsaverage surfaces)
    - TemplateFlow (MNI152NLin2009cAsym, MNI152NLin6Asym, etc.)
    - Local files (custom templates)

    Example:
        >>> tm = TemplateManager()
        >>> template = tm.get_template('mni152', resolution=1)
        >>> template_path = tm.get_template_path('MNI152NLin2009cAsym')
    """

    # Available templates and their sources
    TEMPLATES = {
        # Nilearn templates
        "mni152": {
            "source": "nilearn",
            "description": "MNI152 T1 template (1mm or 2mm)",
            "resolutions": [1, 2],
            "space": "MNI152",
        },
        "mni152_brain_mask": {
            "source": "nilearn",
            "description": "MNI152 whole brain mask",
            "resolutions": [1, 2],
            "space": "MNI152",
        },
        "mni152_gm_mask": {
            "source": "nilearn",
            "description": "MNI152 gray matter mask",
            "resolutions": [1, 2],
            "space": "MNI152",
        },
        "mni152_wm_mask": {
            "source": "nilearn",
            "description": "MNI152 white matter mask",
            "resolutions": [1, 2],
            "space": "MNI152",
        },
        # TemplateFlow templates (require templateflow package)
        "MNI152NLin2009cAsym": {
            "source": "templateflow",
            "description": "MNI152 nonlinear asymmetric 2009c (fMRIPrep default)",
            "resolutions": [1, 2],
            "space": "MNI152NLin2009cAsym",
        },
        "MNI152NLin6Asym": {
            "source": "templateflow",
            "description": "MNI152 nonlinear asymmetric 6th generation",
            "resolutions": [1, 2],
            "space": "MNI152NLin6Asym",
        },
        # Surface templates
        "fsaverage": {
            "source": "nilearn",
            "description": "FreeSurfer average surface template",
            "type": "surface",
            "variants": ["fsaverage", "fsaverage5", "fsaverage6"],
        },
    }

    def __init__(self):
        """Initialize template manager."""
        self.cache_dir = self._get_cache_dir()

    def _get_cache_dir(self) -> Path:
        """Get template cache directory."""
        # Use nilearn's cache directory
        return Path(nilearn_datasets.get_data_dirs()[0])

    def list_templates(self) -> None:
        """Print available templates and their descriptions."""
        print("Available Brain Templates:")
        print("=" * 80)

        for name, info in self.TEMPLATES.items():
            source = info["source"]
            desc = info["description"]
            available = "✓" if self._is_template_available(name) else "✗"

            print(f"\n{available} {name}")
            print(f"   Source: {source}")
            print(f"   Description: {desc}")

            if "resolutions" in info:
                resolutions = ", ".join(map(str, info["resolutions"]))
                print(f"   Resolutions: {resolutions}mm")

            if "variants" in info:
                variants = ", ".join(info["variants"])
                print(f"   Variants: {variants}")

            if source == "templateflow" and not TEMPLATEFLOW_AVAILABLE:
                print(f"   ⚠ Requires: pip install templateflow")

        print("\n" + "=" * 80)

    def _is_template_available(self, template_name: str) -> bool:
        """Check if a template is available."""
        if template_name not in self.TEMPLATES:
            return False

        info = self.TEMPLATES[template_name]
        source = info["source"]

        if source == "templateflow":
            return TEMPLATEFLOW_AVAILABLE
        elif source == "nilearn":
            return True
        else:
            return False

    def get_template(
        self,
        template_name: str,
        resolution: int = 1,
        **kwargs
    ) -> nib.Nifti1Image:
        """
        Get a brain template image.

        Args:
            template_name: Name of template (see list_templates())
            resolution: Resolution in mm (1 or 2)
            **kwargs: Additional arguments for template loading

        Returns:
            Nibabel image object

        Raises:
            ValueError: If template is invalid or unavailable
            ImportError: If required package is not installed

        Example:
            >>> tm = TemplateManager()
            >>> template = tm.get_template('mni152', resolution=1)
            >>> template = tm.get_template('MNI152NLin2009cAsym', resolution=2)
        """
        if template_name not in self.TEMPLATES:
            available = ", ".join(self.TEMPLATES.keys())
            raise ValueError(
                f"Unknown template '{template_name}'. "
                f"Available templates: {available}"
            )

        info = self.TEMPLATES[template_name]
        source = info["source"]

        if source == "nilearn":
            return self._get_nilearn_template(template_name, resolution, **kwargs)
        elif source == "templateflow":
            return self._get_templateflow_template(template_name, resolution, **kwargs)
        else:
            raise ValueError(f"Unknown template source: {source}")

    def _get_nilearn_template(
        self,
        template_name: str,
        resolution: int,
        **kwargs
    ) -> nib.Nifti1Image:
        """Get template from nilearn."""
        if template_name == "mni152":
            return nilearn_datasets.load_mni152_template(resolution=resolution)
        elif template_name == "mni152_brain_mask":
            return nilearn_datasets.load_mni152_brain_mask(resolution=resolution)
        elif template_name == "mni152_gm_mask":
            return nilearn_datasets.load_mni152_gm_mask(resolution=resolution)
        elif template_name == "mni152_wm_mask":
            return nilearn_datasets.load_mni152_wm_mask(resolution=resolution)
        elif template_name == "fsaverage":
            mesh = kwargs.get('mesh', 'fsaverage')
            return nilearn_datasets.fetch_surf_fsaverage(mesh=mesh)
        else:
            raise ValueError(f"Unknown nilearn template: {template_name}")

    def _get_templateflow_template(
        self,
        template_name: str,
        resolution: int,
        **kwargs
    ) -> nib.Nifti1Image:
        """Get template from TemplateFlow."""
        if not TEMPLATEFLOW_AVAILABLE:
            raise ImportError(
                f"Template '{template_name}' requires TemplateFlow. "
                "Install with: pip install templateflow"
            )

        # Get template path from TemplateFlow
        template_path = tflow.get(
            template_name,
            resolution=resolution,
            suffix='T1w',
            desc=kwargs.get('desc', None),
            **kwargs
        )

        # Load and return
        return nib.load(str(template_path))

    def get_template_path(
        self,
        template_name: str,
        resolution: int = 1,
        **kwargs
    ) -> str:
        """
        Get path to a template file.

        Args:
            template_name: Name of template
            resolution: Resolution in mm
            **kwargs: Additional arguments

        Returns:
            Path to template file

        Example:
            >>> tm = TemplateManager()
            >>> path = tm.get_template_path('mni152', resolution=1)
        """
        img = self.get_template(template_name, resolution=resolution, **kwargs)

        if hasattr(img, 'get_filename'):
            # Nilearn image
            return img.get_filename()
        elif hasattr(img, 'filename'):
            # Nibabel image
            return img.filename
        else:
            # Last resort: save to temp and return path
            import tempfile
            fd, path = tempfile.mkstemp(suffix='.nii.gz')
            os.close(fd)
            nib.save(img, path)
            return path

    def get_surface_mesh(
        self,
        mesh: str = "fsaverage",
        hemi: str = "left",
        surface: str = "pial"
    ) -> Tuple[str, str]:
        """
        Get surface mesh and sulcal depth map.

        Args:
            mesh: Mesh resolution ('fsaverage', 'fsaverage5', 'fsaverage6')
            hemi: Hemisphere ('left' or 'right')
            surface: Surface type ('pial', 'inflated', 'white', 'sphere')

        Returns:
            Tuple of (surface_mesh_path, sulc_map_path)

        Example:
            >>> tm = TemplateManager()
            >>> mesh, sulc = tm.get_surface_mesh('fsaverage', 'left', 'pial')
        """
        fsaverage = nilearn_datasets.fetch_surf_fsaverage(mesh=mesh)

        # Map surface names
        surface_map = {
            "pial": "pial",
            "inflated": "infl",
            "white": "white",
            "sphere": "sphere",
        }

        if surface not in surface_map:
            raise ValueError(
                f"Invalid surface '{surface}'. "
                f"Available: {list(surface_map.keys())}"
            )

        surf_attr = surface_map[surface]
        hemi_suffix = "left" if hemi == "left" else "right"

        surf_mesh = getattr(fsaverage, f"{surf_attr}_{hemi_suffix}")
        sulc_map = getattr(fsaverage, f"sulc_{hemi_suffix}")

        return surf_mesh, sulc_map


# Convenience function
def get_template(template_name: str, resolution: int = 1, **kwargs) -> nib.Nifti1Image:
    """
    Get a brain template (convenience function).

    Args:
        template_name: Name of template
        resolution: Resolution in mm
        **kwargs: Additional arguments

    Returns:
        Nibabel image object

    Example:
        >>> from brainviz_dk.templates import get_template
        >>> template = get_template('mni152', resolution=1)
    """
    tm = TemplateManager()
    return tm.get_template(template_name, resolution=resolution, **kwargs)


def list_available_templates() -> None:
    """
    List all available templates (convenience function).

    Example:
        >>> from brainviz_dk.templates import list_available_templates
        >>> list_available_templates()
    """
    tm = TemplateManager()
    tm.list_templates()
