#!/usr/bin/env python3
"""
Comprehensive test suite for BrainViz_DK package.
Uses actual neuroimaging data for integration testing.
"""

import os
import tempfile
import shutil
import pytest
from pathlib import Path

from brainviz_dk import (
    plot_nifti,
    generate_four_views,
    generate_all_standard_views,
    plot_3d_interactive,
    project_volume_to_surface,
)


# Test data configuration
TEST_DATA_DIR = Path("/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym")
TEST_NIFTI = TEST_DATA_DIR / "group_mean.nii.gz"


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test outputs."""
    temp_dir = tempfile.mkdtemp(prefix="brainviz_test_")
    yield temp_dir
    # Cleanup after test
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def test_nifti_path():
    """Provide path to test NIfTI file."""
    if not TEST_NIFTI.exists():
        pytest.skip(f"Test data not found: {TEST_NIFTI}")
    return str(TEST_NIFTI)


class TestProjectVolumeToSurface:
    """Test volume-to-surface projection functionality."""

    def test_project_left_hemisphere(self, test_nifti_path):
        """Test projection to left hemisphere."""
        surf_mesh, sulc_map, texture = project_volume_to_surface(
            test_nifti_path,
            hemi="lh",
            mesh="fsaverage5",  # Use faster fsaverage5 for tests
            surface_name="pial",
        )

        assert surf_mesh is not None
        assert sulc_map is not None
        assert texture is not None
        assert len(texture) > 0

    def test_project_right_hemisphere(self, test_nifti_path):
        """Test projection to right hemisphere."""
        surf_mesh, sulc_map, texture = project_volume_to_surface(
            test_nifti_path,
            hemi="rh",
            mesh="fsaverage5",
            surface_name="pial",
        )

        assert surf_mesh is not None
        assert texture is not None
        assert len(texture) > 0

    def test_different_surfaces(self, test_nifti_path):
        """Test different surface types."""
        surfaces = ["pial", "inflated", "white", "sphere"]

        for surface in surfaces:
            surf_mesh, sulc_map, texture = project_volume_to_surface(
                test_nifti_path,
                hemi="lh",
                mesh="fsaverage5",
                surface_name=surface,
            )
            assert surf_mesh is not None, f"Failed for surface: {surface}"
            assert texture is not None, f"Failed for surface: {surface}"

    def test_invalid_hemisphere(self, test_nifti_path):
        """Test that invalid hemisphere raises error."""
        with pytest.raises(ValueError, match="hemi must be"):
            project_volume_to_surface(
                test_nifti_path,
                hemi="invalid",
                mesh="fsaverage5",
            )

    def test_invalid_surface(self, test_nifti_path):
        """Test that invalid surface name raises error."""
        with pytest.raises(ValueError, match="surface_name must be"):
            project_volume_to_surface(
                test_nifti_path,
                hemi="lh",
                mesh="fsaverage5",
                surface_name="invalid_surface",
            )


class TestPlotNifti:
    """Test single view plotting functionality."""

    def test_plot_single_view_left(self, test_nifti_path, temp_output_dir):
        """Test plotting a single left hemisphere view."""
        output_path = os.path.join(temp_output_dir, "test_lh_lateral.png")

        result = plot_nifti(
            test_nifti_path,
            output_path,
            hemi="lh",
            view="lateral",
            mesh="fsaverage5",
            colormap="jet",
        )

        assert result == output_path
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0

    def test_plot_single_view_right(self, test_nifti_path, temp_output_dir):
        """Test plotting a single right hemisphere view."""
        output_path = os.path.join(temp_output_dir, "test_rh_medial.png")

        result = plot_nifti(
            test_nifti_path,
            output_path,
            hemi="rh",
            view="medial",
            mesh="fsaverage5",
            colormap="hot",
        )

        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0

    def test_all_views(self, test_nifti_path, temp_output_dir):
        """Test all available views."""
        views = ["lateral", "medial", "dorsal", "ventral", "anterior", "posterior"]

        for view in views:
            output_path = os.path.join(temp_output_dir, f"test_{view}.png")
            result = plot_nifti(
                test_nifti_path,
                output_path,
                hemi="lh",
                view=view,
                mesh="fsaverage5",
            )
            assert os.path.exists(output_path), f"Failed for view: {view}"
            assert os.path.getsize(output_path) > 0, f"Empty file for view: {view}"

    def test_different_colormaps(self, test_nifti_path, temp_output_dir):
        """Test different matplotlib colormaps."""
        colormaps = ["jet", "hot", "viridis", "plasma", "coolwarm"]

        for cmap in colormaps:
            output_path = os.path.join(temp_output_dir, f"test_{cmap}.png")
            result = plot_nifti(
                test_nifti_path,
                output_path,
                hemi="lh",
                view="lateral",
                mesh="fsaverage5",
                colormap=cmap,
            )
            assert os.path.exists(output_path), f"Failed for colormap: {cmap}"

    def test_hemisphere_naming_variations(self, test_nifti_path, temp_output_dir):
        """Test different hemisphere naming conventions."""
        hemi_variations = ["lh", "left", "rh", "right"]

        for hemi in hemi_variations:
            output_path = os.path.join(temp_output_dir, f"test_{hemi}.png")
            result = plot_nifti(
                test_nifti_path,
                output_path,
                hemi=hemi,
                view="lateral",
                mesh="fsaverage5",
            )
            assert os.path.exists(output_path), f"Failed for hemisphere: {hemi}"

    def test_invalid_hemisphere(self, test_nifti_path, temp_output_dir):
        """Test that invalid hemisphere raises error."""
        output_path = os.path.join(temp_output_dir, "test.png")

        with pytest.raises(ValueError, match="hemi must be"):
            plot_nifti(
                test_nifti_path,
                output_path,
                hemi="invalid",
                view="lateral",
            )

    def test_creates_output_directory(self, test_nifti_path, temp_output_dir):
        """Test that output directory is created if it doesn't exist."""
        nested_dir = os.path.join(temp_output_dir, "nested", "output", "dir")
        output_path = os.path.join(nested_dir, "test.png")

        result = plot_nifti(
            test_nifti_path,
            output_path,
            hemi="lh",
            view="lateral",
            mesh="fsaverage5",
        )

        assert os.path.exists(output_path)


class TestGenerateFourViews:
    """Test batch view generation functionality."""

    def test_generate_default_views(self, test_nifti_path, temp_output_dir):
        """Test generating default four views for both hemispheres."""
        outputs = generate_four_views(
            test_nifti_path,
            temp_output_dir,
            hemis=("lh", "rh"),
            views=("lateral", "medial", "dorsal", "ventral"),
            mesh="fsaverage5",
            prefix="test",
        )

        # Should generate 2 hemispheres × 4 views = 8 files
        assert len(outputs) == 8

        for output in outputs:
            assert os.path.exists(output)
            assert os.path.getsize(output) > 0

    def test_generate_single_hemisphere(self, test_nifti_path, temp_output_dir):
        """Test generating views for single hemisphere."""
        outputs = generate_four_views(
            test_nifti_path,
            temp_output_dir,
            hemis=("lh",),
            views=("lateral", "medial"),
            mesh="fsaverage5",
            prefix="test_lh",
        )

        # Should generate 1 hemisphere × 2 views = 2 files
        assert len(outputs) == 2

        for output in outputs:
            assert "lh" in output
            assert os.path.exists(output)

    def test_custom_views(self, test_nifti_path, temp_output_dir):
        """Test custom view selection."""
        outputs = generate_four_views(
            test_nifti_path,
            temp_output_dir,
            hemis=("lh", "rh"),
            views=("anterior", "posterior"),
            mesh="fsaverage5",
            prefix="test_custom",
        )

        assert len(outputs) == 4  # 2 hemis × 2 views

        for output in outputs:
            assert "anterior" in output or "posterior" in output

    def test_different_surfaces(self, test_nifti_path, temp_output_dir):
        """Test batch generation with different surfaces."""
        surfaces = ["pial", "inflated"]

        for surface in surfaces:
            outputs = generate_four_views(
                test_nifti_path,
                temp_output_dir,
                hemis=("lh",),
                views=("lateral",),
                mesh="fsaverage5",
                surface_name=surface,
                prefix=f"test_{surface}",
            )
            assert len(outputs) == 1
            assert os.path.exists(outputs[0])

    def test_filename_prefix(self, test_nifti_path, temp_output_dir):
        """Test that filename prefix is applied correctly."""
        prefix = "my_custom_prefix"
        outputs = generate_four_views(
            test_nifti_path,
            temp_output_dir,
            hemis=("lh",),
            views=("lateral",),
            mesh="fsaverage5",
            prefix=prefix,
        )

        assert len(outputs) == 1
        assert prefix in os.path.basename(outputs[0])


class TestGenerateAllStandardViews:
    """Test generation of all standard neuroimaging views."""

    def test_generate_all_views(self, test_nifti_path, temp_output_dir):
        """Test generating all 12 standard views (6 per hemisphere)."""
        outputs = generate_all_standard_views(
            test_nifti_path,
            temp_output_dir,
            mesh="fsaverage5",
            prefix="test_all",
        )

        # Should generate 2 hemispheres × 6 views = 12 files
        assert len(outputs) == 12

        # Check that all expected views are present
        expected_views = ["lateral", "medial", "dorsal", "ventral", "anterior", "posterior"]
        for view in expected_views:
            matching = [o for o in outputs if view in o]
            assert len(matching) == 2, f"Expected 2 files for {view}, got {len(matching)}"

        # Check all files exist and have content
        for output in outputs:
            assert os.path.exists(output)
            assert os.path.getsize(output) > 0

    def test_all_views_different_colormap(self, test_nifti_path, temp_output_dir):
        """Test all views with different colormap."""
        outputs = generate_all_standard_views(
            test_nifti_path,
            temp_output_dir,
            mesh="fsaverage5",
            colormap="hot",
            prefix="test_hot",
        )

        assert len(outputs) == 12


class TestPlot3DInteractive:
    """Test interactive 3D plotting functionality."""

    def test_create_3d_view(self, test_nifti_path):
        """Test creating an interactive 3D view."""
        view = plot_3d_interactive(
            test_nifti_path,
            colormap="jet",
            title="Test 3D View",
        )

        assert view is not None
        # Check that view object has expected methods
        assert hasattr(view, "save_as_html")
        assert hasattr(view, "open_in_browser")

    def test_save_3d_html(self, test_nifti_path, temp_output_dir):
        """Test saving 3D view to HTML file."""
        view = plot_3d_interactive(
            test_nifti_path,
            colormap="viridis",
        )

        html_path = os.path.join(temp_output_dir, "test_3d.html")
        view.save_as_html(html_path)

        assert os.path.exists(html_path)
        assert os.path.getsize(html_path) > 0

        # Check that HTML contains expected content
        with open(html_path, 'r') as f:
            content = f.read()
            assert "html" in content.lower()

    def test_different_colormaps_3d(self, test_nifti_path, temp_output_dir):
        """Test 3D plotting with different colormaps."""
        colormaps = ["jet", "hot", "plasma"]

        for cmap in colormaps:
            view = plot_3d_interactive(
                test_nifti_path,
                colormap=cmap,
            )
            assert view is not None

            html_path = os.path.join(temp_output_dir, f"test_3d_{cmap}.html")
            view.save_as_html(html_path)
            assert os.path.exists(html_path)


class TestMultipleNiftiFiles:
    """Test with different NIfTI files from test data."""

    def test_different_nifti_files(self, temp_output_dir):
        """Test plotting different types of group statistics."""
        if not TEST_DATA_DIR.exists():
            pytest.skip("Test data directory not found")

        # Test files with different statistical measures
        test_files = [
            "group_mean.nii.gz",
            "group_median.nii.gz",
            "group_t.nii.gz",
            "group_d.nii.gz",
        ]

        for filename in test_files:
            nifti_path = TEST_DATA_DIR / filename
            if not nifti_path.exists():
                continue

            output_path = os.path.join(temp_output_dir, f"{filename.replace('.nii.gz', '')}_lh_lateral.png")

            result = plot_nifti(
                str(nifti_path),
                output_path,
                hemi="lh",
                view="lateral",
                mesh="fsaverage5",
            )

            assert os.path.exists(output_path), f"Failed for file: {filename}"
            assert os.path.getsize(output_path) > 0


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_nonexistent_file(self, temp_output_dir):
        """Test handling of nonexistent NIfTI file."""
        fake_path = "/nonexistent/path/to/file.nii.gz"
        output_path = os.path.join(temp_output_dir, "test.png")

        with pytest.raises(Exception):  # nibabel will raise FileNotFoundError
            plot_nifti(
                fake_path,
                output_path,
                hemi="lh",
                view="lateral",
            )

    def test_empty_views_list(self, test_nifti_path, temp_output_dir):
        """Test with empty views list."""
        outputs = generate_four_views(
            test_nifti_path,
            temp_output_dir,
            hemis=("lh",),
            views=(),  # Empty tuple
            mesh="fsaverage5",
        )

        assert len(outputs) == 0


def test_package_imports():
    """Test that all public functions are importable."""
    from brainviz_dk import (
        plot_nifti,
        generate_four_views,
        generate_all_standard_views,
        plot_3d_interactive,
        project_volume_to_surface,
    )

    assert plot_nifti is not None
    assert generate_four_views is not None
    assert generate_all_standard_views is not None
    assert plot_3d_interactive is not None
    assert project_volume_to_surface is not None


def test_package_version():
    """Test that package has version attribute."""
    import brainviz_dk
    assert hasattr(brainviz_dk, "__version__")
    assert brainviz_dk.__version__ == "0.1.0"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
