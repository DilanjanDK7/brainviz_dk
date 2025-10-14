#!/usr/bin/env python3
"""
Enhanced test script for BrainViz package with all new features.
Tests: all standard views, 3D interactive plots, and various configurations.
"""

import os
import sys

from brainviz_dk import (
    generate_four_views,
    generate_all_standard_views,
    plot_3d_interactive,
    plot_nifti
)
from test_config import test_config, get_test_nifti_path


def main():
    print("="*70)
    print("BrainViz_DK Enhanced Testing Suite")
    print("="*70)
    
    # Get test file
    test_nifti = get_test_nifti_path()
    if test_nifti is None:
        print("ERROR: No test data available.")
        print("Please set BRAINVIZ_TEST_DATA_DIR environment variable or place test data in test_data/")
        return 1
    
    output_base = test_config.temp_dir / "Plots_BrainViz_Enhanced"
    
    # Test 1: All standard neuroimaging views
    print("\n" + "="*70)
    print("Test 1: Generate ALL Standard Neuroimaging Views")
    print("  (lateral, medial, dorsal, ventral, anterior, posterior)")
    print("="*70)
    
    try:
        output_dir = os.path.join(output_base, "all_standard_views")
        outputs = generate_all_standard_views(
            str(test_nifti),
            str(output_dir),
            mesh="fsaverage",
            surface_name="pial",
            colormap="jet",
            prefix="test_all_views"
        )
        print(f"✓ SUCCESS: Generated {len(outputs)} views")
        for out in outputs[:3]:  # Show first 3
            print(f"  - {os.path.basename(out)}")
        if len(outputs) > 3:
            print(f"  ... and {len(outputs)-3} more")
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Custom view selection
    print("\n" + "="*70)
    print("Test 2: Custom View Selection (anterior + posterior only)")
    print("="*70)
    
    try:
        output_dir = os.path.join(output_base, "custom_views")
        outputs = generate_four_views(
            str(test_nifti),
            str(output_dir),
            hemis=("lh", "rh"),
            views=("anterior", "posterior"),
            mesh="fsaverage",
            surface_name="pial",
            colormap="plasma",
            prefix="test_custom"
        )
        print(f"✓ SUCCESS: Generated {len(outputs)} custom views")
        for out in outputs:
            print(f"  - {os.path.basename(out)}")
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: 3D Interactive HTML
    print("\n" + "="*70)
    print("Test 3: 3D Interactive Plot (save to HTML)")
    print("="*70)
    
    try:
        output_dir = os.path.join(output_base, "interactive_3d")
        os.makedirs(output_dir, exist_ok=True)
        
        view = plot_3d_interactive(
            str(test_nifti),
            colormap="jet",
            title="Test Group Mean - Interactive 3D"
        )
        
        html_path = os.path.join(output_dir, "test_interactive_3d.html")
        view.save_as_html(html_path)
        
        print(f"✓ SUCCESS: Saved interactive 3D HTML")
        print(f"  - {html_path}")
        print(f"  - Open this file in a web browser to explore interactively!")
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Different surface types
    print("\n" + "="*70)
    print("Test 4: Different Surface Types (pial vs inflated)")
    print("="*70)
    
    for surface in ["pial", "inflated"]:
        try:
            output_dir = os.path.join(output_base, f"surface_{surface}")
            outputs = generate_four_views(
                str(test_nifti),
                str(output_dir),
                hemis=("lh",),
                views=("lateral",),
                mesh="fsaverage",
                surface_name=surface,
                colormap="jet",
                prefix=f"test_{surface}"
            )
            print(f"✓ {surface.upper()}: {os.path.basename(outputs[0])}")
        except Exception as e:
            print(f"✗ {surface.upper()} FAILED: {e}")
    
    # Test 5: Different colormaps comparison
    print("\n" + "="*70)
    print("Test 5: Colormap Comparison (jet, hot, viridis)")
    print("="*70)
    
    colormaps = ["jet", "hot", "viridis"]
    for cmap in colormaps:
        try:
            output_dir = os.path.join(output_base, "colormap_comparison")
            outputs = generate_four_views(
                str(test_nifti),
                str(output_dir),
                hemis=("lh",),
                views=("lateral",),
                mesh="fsaverage",
                surface_name="pial",
                colormap=cmap,
                prefix=f"test_{cmap}"
            )
            print(f"✓ {cmap.upper()}: {os.path.basename(outputs[0])}")
        except Exception as e:
            print(f"✗ {cmap.upper()} FAILED: {e}")
    
    # Test 6: Mesh resolution comparison
    print("\n" + "="*70)
    print("Test 6: Mesh Resolution (fsaverage vs fsaverage5)")
    print("="*70)
    
    for mesh in ["fsaverage", "fsaverage5"]:
        try:
            output_dir = os.path.join(output_base, f"mesh_{mesh}")
            outputs = generate_four_views(
                str(test_nifti),
                str(output_dir),
                hemis=("lh",),
                views=("lateral",),
                mesh=mesh,
                surface_name="pial",
                colormap="jet",
                prefix=f"test_{mesh}"
            )
            print(f"✓ {mesh}: {os.path.basename(outputs[0])}")
        except Exception as e:
            print(f"✗ {mesh} FAILED: {e}")
    
    print("\n" + "="*70)
    print("TESTING COMPLETE!")
    print("="*70)
    print(f"\nAll outputs saved to: {output_base}")
    print("\nKey features tested:")
    print("  ✓ All standard neuroimaging views (6 per hemisphere)")
    print("  ✓ Custom view selection")
    print("  ✓ 3D interactive HTML plots")
    print("  ✓ Different surface types (pial, inflated)")
    print("  ✓ Multiple colormaps (jet, hot, viridis)")
    print("  ✓ Mesh resolution options (fsaverage, fsaverage5)")
    print("\n" + "="*70)
    
    return 0


if __name__ == "__main__":
    exit(main())

