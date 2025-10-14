#!/usr/bin/env python3
"""
Comprehensive test of all BrainViz_DK features.
Tests Phase 1 (quality enhancements) and Phase 2 (volumetric rendering).
"""

import os
import sys
from pathlib import Path

# Test data paths
TEST_DATA_DIR = Path("/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym")
OUTPUT_DIR = Path("/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/BrainViz_Complete_Test")

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Import BrainViz
try:
    from brainviz_dk import (
        # Surface plotting
        plot_nifti,
        generate_four_views,
        plot_3d_interactive,
        # Quality presets
        get_quality_preset,
        list_quality_presets,
        # Volumetric plotting
        plot_volumetric_slices,
        plot_glass_brain,
        plot_mosaic,
        plot_roi_overlay,
        # Template management
        TemplateManager,
        list_available_templates,
    )
except ImportError as e:
    print(f"ERROR: Failed to import brainviz_dk: {e}")
    sys.exit(1)


def test_phase1_quality_enhancements():
    """Test Phase 1: High-resolution output and quality presets."""
    print("\n" + "="*80)
    print("PHASE 1 TESTS: Quality Enhancements & High-Resolution Output")
    print("="*80)

    test_file = TEST_DATA_DIR / "group_mean.nii.gz"
    if not test_file.exists():
        print(f"⚠️  Test file not found: {test_file}")
        return

    phase1_dir = OUTPUT_DIR / "phase1_quality"
    phase1_dir.mkdir(exist_ok=True)

    results = []

    # Test 1: Standard quality (PNG, 300 DPI)
    print("\n1️⃣  Standard quality (300 DPI PNG)...")
    try:
        out = plot_nifti(
            str(test_file),
            str(phase1_dir / "standard_quality.png"),
            hemi="lh",
            view="lateral",
            dpi=300,
            mesh="fsaverage5",
        )
        size = os.path.getsize(out) / 1024
        print(f"   ✓ {Path(out).name} ({size:.1f} KB)")
        results.append(("Standard PNG", "✓", f"{size:.1f} KB"))
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results.append(("Standard PNG", "✗", str(e)))

    # Test 2: High-resolution PNG (600 DPI)
    print("\n2️⃣  High-resolution PNG (600 DPI)...")
    try:
        out = plot_nifti(
            str(test_file),
            str(phase1_dir / "high_res_600dpi.png"),
            hemi="lh",
            view="lateral",
            dpi=600,
            mesh="fsaverage",
        )
        size = os.path.getsize(out) / 1024
        print(f"   ✓ {Path(out).name} ({size:.1f} KB)")
        results.append(("High-res PNG", "✓", f"{size:.1f} KB"))
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results.append(("High-res PNG", "✗", str(e)))

    # Test 3: Publication quality preset (SVG)
    print("\n3️⃣  Publication quality preset (SVG, 600 DPI)...")
    try:
        preset = get_quality_preset('publication')
        out = plot_nifti(
            str(test_file),
            str(phase1_dir / "publication_quality.svg"),
            hemi="lh",
            view="lateral",
            **preset
        )
        size = os.path.getsize(out) / 1024
        print(f"   ✓ {Path(out).name} ({size:.1f} KB)")
        results.append(("Publication SVG", "✓", f"{size:.1f} KB"))
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results.append(("Publication SVG", "✗", str(e)))

    # Test 4: Custom figure size
    print("\n4️⃣  Custom figure size (10x8 inches)...")
    try:
        out = plot_nifti(
            str(test_file),
            str(phase1_dir / "custom_figsize.png"),
            hemi="lh",
            view="lateral",
            figsize=(10, 8),
            dpi=300,
            mesh="fsaverage5",
        )
        size = os.path.getsize(out) / 1024
        print(f"   ✓ {Path(out).name} ({size:.1f} KB)")
        results.append(("Custom figsize", "✓", f"{size:.1f} KB"))
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results.append(("Custom figsize", "✗", str(e)))

    # Test 5: Multiple views with quality settings
    print("\n5️⃣  Multiple views (4 views, both hemispheres, 600 DPI)...")
    try:
        outputs = generate_four_views(
            str(test_file),
            str(phase1_dir),
            hemis=("lh", "rh"),
            views=("lateral", "medial"),
            mesh="fsaverage5",
            dpi=600,
            output_format="png",
            prefix="multi_view"
        )
        total_size = sum(os.path.getsize(f) for f in outputs) / 1024
        print(f"   ✓ Generated {len(outputs)} files ({total_size:.1f} KB total)")
        results.append(("Multiple views", "✓", f"{len(outputs)} files"))
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results.append(("Multiple views", "✗", str(e)))

    # Test 6: Different output formats
    print("\n6️⃣  Different output formats (PNG, SVG, PDF)...")
    for fmt in ['png', 'svg', 'pdf']:
        try:
            out = plot_nifti(
                str(test_file),
                str(phase1_dir / f"format_test.{fmt}"),
                hemi="rh",
                view="medial",
                output_format=fmt,
                dpi=300,
                mesh="fsaverage5",
            )
            size = os.path.getsize(out) / 1024
            print(f"   ✓ {fmt.upper()}: {Path(out).name} ({size:.1f} KB)")
            results.append((f"Format {fmt.upper()}", "✓", f"{size:.1f} KB"))
        except Exception as e:
            print(f"   ✗ {fmt.upper()} Failed: {e}")
            results.append((f"Format {fmt.upper()}", "✗", str(e)))

    return results


def test_phase2_volumetric_rendering():
    """Test Phase 2: Volumetric rendering and templates."""
    print("\n" + "="*80)
    print("PHASE 2 TESTS: Volumetric Rendering & Template Integration")
    print("="*80)

    test_file = TEST_DATA_DIR / "group_mean.nii.gz"
    if not test_file.exists():
        print(f"⚠️  Test file not found: {test_file}")
        return

    phase2_dir = OUTPUT_DIR / "phase2_volumetric"
    phase2_dir.mkdir(exist_ok=True)

    results = []

    # Test 1: Orthogonal slices (MNI152)
    print("\n1️⃣  Orthogonal slice view (MNI152 template)...")
    try:
        out = plot_volumetric_slices(
            str(test_file),
            str(phase2_dir / "ortho_slices.png"),
            template="mni152",
            display_mode="ortho",
            colormap="hot",
            dpi=300
        )
        size = os.path.getsize(out) / 1024
        print(f"   ✓ {Path(out).name} ({size:.1f} KB)")
        results.append(("Ortho slices", "✓", f"{size:.1f} KB"))
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results.append(("Ortho slices", "✗", str(e)))

    # Test 2: Glass brain
    print("\n2️⃣  Glass brain visualization (600 DPI)...")
    try:
        out = plot_glass_brain(
            str(test_file),
            str(phase2_dir / "glass_brain.png"),
            display_mode="lyrz",
            colormap="hot",
            dpi=600
        )
        size = os.path.getsize(out) / 1024
        print(f"   ✓ {Path(out).name} ({size:.1f} KB)")
        results.append(("Glass brain", "✓", f"{size:.1f} KB"))
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results.append(("Glass brain", "✗", str(e)))

    # Test 3: Mosaic view (axial)
    print("\n3️⃣  Mosaic view - Axial (15 slices)...")
    try:
        out = plot_mosaic(
            str(test_file),
            str(phase2_dir / "mosaic_axial.png"),
            template="mni152",
            display_mode="z",
            n_slices=15,
            colormap="hot",
            dpi=300
        )
        size = os.path.getsize(out) / 1024
        print(f"   ✓ {Path(out).name} ({size:.1f} KB)")
        results.append(("Mosaic axial", "✓", f"{size:.1f} KB"))
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results.append(("Mosaic axial", "✗", str(e)))

    # Test 4: Sagittal slices
    print("\n4️⃣  Sagittal slice view (5 slices)...")
    try:
        out = plot_volumetric_slices(
            str(test_file),
            str(phase2_dir / "sagittal_slices.png"),
            template="mni152",
            display_mode="x",
            cut_coords=5,
            colormap="hot",
            dpi=300
        )
        size = os.path.getsize(out) / 1024
        print(f"   ✓ {Path(out).name} ({size:.1f} KB)")
        results.append(("Sagittal slices", "✓", f"{size:.1f} KB"))
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results.append(("Sagittal slices", "✗", str(e)))

    # Test 5: Coronal slices
    print("\n5️⃣  Coronal slice view (7 slices)...")
    try:
        out = plot_volumetric_slices(
            str(test_file),
            str(phase2_dir / "coronal_slices.png"),
            template="mni152",
            display_mode="y",
            cut_coords=7,
            colormap="viridis",
            dpi=300
        )
        size = os.path.getsize(out) / 1024
        print(f"   ✓ {Path(out).name} ({size:.1f} KB)")
        results.append(("Coronal slices", "✓", f"{size:.1f} KB"))
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        results.append(("Coronal slices", "✗", str(e)))

    # Test 6: Different colormaps
    print("\n6️⃣  Glass brain with different colormaps...")
    for cmap in ['hot', 'plasma', 'coolwarm']:
        try:
            out = plot_glass_brain(
                str(test_file),
                str(phase2_dir / f"glass_{cmap}.png"),
                display_mode="lr",
                colormap=cmap,
                dpi=400
            )
            size = os.path.getsize(out) / 1024
            print(f"   ✓ {cmap}: {Path(out).name} ({size:.1f} KB)")
            results.append((f"Glass {cmap}", "✓", f"{size:.1f} KB"))
        except Exception as e:
            print(f"   ✗ {cmap} Failed: {e}")
            results.append((f"Glass {cmap}", "✗", str(e)))

    return results


def test_multiple_nifti_files():
    """Test with multiple NIfTI files."""
    print("\n" + "="*80)
    print("MULTI-FILE TESTS: Processing Multiple Statistical Maps")
    print("="*80)

    multi_dir = OUTPUT_DIR / "multi_file_test"
    multi_dir.mkdir(exist_ok=True)

    results = []

    # Get all available NIfTI files
    nifti_files = list(TEST_DATA_DIR.glob("*.nii.gz"))
    print(f"\nFound {len(nifti_files)} NIfTI files in test directory")

    for nifti_file in nifti_files[:4]:  # Test first 4 files
        file_name = nifti_file.stem.replace('.nii', '')
        print(f"\n📊 Processing: {file_name}")

        # Test surface plot
        try:
            out = plot_nifti(
                str(nifti_file),
                str(multi_dir / f"{file_name}_surface.png"),
                hemi="lh",
                view="lateral",
                dpi=300,
                mesh="fsaverage5",
            )
            size = os.path.getsize(out) / 1024
            print(f"   ✓ Surface: {size:.1f} KB")
            results.append((f"{file_name} surface", "✓", f"{size:.1f} KB"))
        except Exception as e:
            print(f"   ✗ Surface failed: {e}")
            results.append((f"{file_name} surface", "✗", str(e)))

        # Test volumetric plot
        try:
            out = plot_glass_brain(
                str(nifti_file),
                str(multi_dir / f"{file_name}_glass.png"),
                display_mode="lr",
                colormap="hot",
                dpi=400
            )
            size = os.path.getsize(out) / 1024
            print(f"   ✓ Glass brain: {size:.1f} KB")
            results.append((f"{file_name} glass", "✓", f"{size:.1f} KB"))
        except Exception as e:
            print(f"   ✗ Glass brain failed: {e}")
            results.append((f"{file_name} glass", "✗", str(e)))

    return results


def test_template_manager():
    """Test template management system."""
    print("\n" + "="*80)
    print("TEMPLATE MANAGER TESTS")
    print("="*80)

    print("\n📋 Available templates:")
    print("-" * 80)
    list_available_templates()

    print("\n" + "-" * 80)
    print("Testing template loading...")

    results = []

    tm = TemplateManager()

    # Test MNI152 templates
    for template_name in ["mni152", "mni152_brain_mask"]:
        try:
            template = tm.get_template(template_name, resolution=1)
            print(f"✓ Loaded {template_name}: shape {template.shape}")
            results.append((template_name, "✓", str(template.shape)))
        except Exception as e:
            print(f"✗ Failed to load {template_name}: {e}")
            results.append((template_name, "✗", str(e)))

    return results


def print_summary(all_results):
    """Print test summary."""
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    total_tests = len(all_results)
    passed = sum(1 for _, status, _ in all_results if status == "✓")
    failed = total_tests - passed

    print(f"\nTotal Tests: {total_tests}")
    print(f"✓ Passed: {passed}")
    print(f"✗ Failed: {failed}")
    print(f"Success Rate: {passed/total_tests*100:.1f}%")

    if failed > 0:
        print("\n❌ Failed Tests:")
        for test_name, status, info in all_results:
            if status == "✗":
                print(f"  • {test_name}: {info}")

    print("\n" + "="*80)
    print(f"📁 All outputs saved to: {OUTPUT_DIR}")
    print("="*80)


def main():
    """Run all tests."""
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "BrainViz_DK Complete Feature Test" + " "*25 + "║")
    print("╚" + "="*78 + "╝")

    print(f"\n📍 Test data directory: {TEST_DATA_DIR}")
    print(f"📁 Output directory: {OUTPUT_DIR}")

    if not TEST_DATA_DIR.exists():
        print(f"\n❌ ERROR: Test data directory not found!")
        print(f"   Expected: {TEST_DATA_DIR}")
        sys.exit(1)

    all_results = []

    try:
        # Phase 1 tests
        results = test_phase1_quality_enhancements()
        if results:
            all_results.extend(results)

        # Phase 2 tests
        results = test_phase2_volumetric_rendering()
        if results:
            all_results.extend(results)

        # Multi-file tests
        results = test_multiple_nifti_files()
        if results:
            all_results.extend(results)

        # Template manager tests
        results = test_template_manager()
        if results:
            all_results.extend(results)

        # Print summary
        print_summary(all_results)

        print("\n🎉 Testing complete!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
