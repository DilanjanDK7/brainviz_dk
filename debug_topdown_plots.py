#!/usr/bin/env python3
"""
Debug Script: Plot True Top-Down View of All Testing Data
==========================================================

This script plots TRUE top-down (axial slices) views using volumetric rendering,
not surface projection. This shows the brain looking from directly above.

Output: Saves plots to a 'topdown_debug' subfolder in the testing directory
"""

import os
import glob
import sys
from pathlib import Path

# Add current directory to path to import brainviz_dk
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from volumetric import plot_volumetric_slices

# Configuration
DATA_DIR = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym'
OUTPUT_DIR = os.path.join(DATA_DIR, 'topdown_debug')

print("=" * 70)
print(" BrainViz_DK: True Top-Down (Axial) View Debug Script")
print("=" * 70)
print(f"\nData directory: {DATA_DIR}")
print(f"Output directory: {OUTPUT_DIR}")
print(f"\nUsing volumetric rendering with axial slices (z-axis)")
print(f"This shows the brain from directly above (top-down view)\n")

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get all NIfTI files
nifti_files = sorted(glob.glob(f'{DATA_DIR}/*.nii.gz'))

if not nifti_files:
    print("❌ No NIfTI files found!")
    sys.exit(1)

print(f"Found {len(nifti_files)} NIfTI files to process\n")

successful = 0
failed = []

# Process each file - using axial slices for true top-down view
for idx, nifti_file in enumerate(nifti_files, 1):
    basename = os.path.basename(nifti_file).replace('.nii.gz', '')

    print(f"[{idx}/{len(nifti_files)}] {basename}")

    try:
        output_file = os.path.join(OUTPUT_DIR, f'{basename}_topdown_axial.png')

        print(f"  → Plotting axial slices (top-down view)...", end=" ")

        # Use volumetric plotting with z-axis (axial) for true top-down view
        plot_volumetric_slices(
            nifti_file,
            output_file,
            template='mni152',
            display_mode='z',  # z-axis = axial slices = top-down view
            cut_coords=7,  # Show 7 slices from bottom to top
            colormap='hot',
            annotate=True,
            draw_cross=True,
            dpi=300
        )

        # Check file was created
        if os.path.exists(output_file):
            size_kb = os.path.getsize(output_file) / 1024
            print(f"✓ ({size_kb:.1f} KB)")
            successful += 1
        else:
            print("✗ File not created")
            failed.append((basename, "File not created"))

    except Exception as e:
        print(f"✗ Error: {str(e)[:60]}")
        failed.append((basename, str(e)))

    print()

# Summary
print("=" * 70)
print(" Summary")
print("=" * 70)
print(f"Total files processed: {len(nifti_files)}")
print(f"Successful plots: {successful}")
print(f"Failed plots: {len(failed)}")
print()

if failed:
    print("Failed plots:")
    for basename, error in failed:
        print(f"  - {basename}: {error[:60]}")
    print()

print(f"✓ Output directory: {OUTPUT_DIR}")
print("\nNote: These are AXIAL slices showing the brain from above.")
print("This is the true 'top-down' view for volumetric data.")
print("=" * 70)

# Exit with appropriate code
sys.exit(0 if not failed else 1)
