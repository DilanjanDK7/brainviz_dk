#!/usr/bin/env python3
"""
Plot ALL Testing Files with Plotly 3D Interactive Viewer
=========================================================

Creates interactive 3D brain visualizations for all NIfTI files in the testing directory.
You can rotate each visualization to any angle, including perfect dorsal (top-down) view!

Features:
- Fully interactive 3D in browser
- Both hemispheres displayed closer together
- Rotate/zoom/pan with mouse
- Perfect for dorsal view visualization
"""

import os
import glob
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interactive3d import plot_interactive_surface_plotly

# Configuration
DATA_DIR = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym'
OUTPUT_DIR = os.path.join(DATA_DIR, 'PLOTLY_3D_ALL')

print("=" * 70)
print(" Plotly 3D Interactive Viewer - ALL FILES")
print("=" * 70)
print(f"\nData directory: {DATA_DIR}")
print(f"Output directory: {OUTPUT_DIR}\n")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get all NIfTI files
nifti_files = sorted(glob.glob(f'{DATA_DIR}/*.nii.gz'))

if not nifti_files:
    print("❌ No NIfTI files found!")
    sys.exit(1)

print(f"Found {len(nifti_files)} files\n")
print("Creating interactive 3D visualizations...")
print("This will take a few minutes...\n")

successful = 0
failed = []
total_size = 0

for idx, nifti_file in enumerate(nifti_files, 1):
    basename = os.path.basename(nifti_file).replace('.nii.gz', '')

    print(f"[{idx:2d}/{len(nifti_files)}] {basename:25s}...", end=" ")

    try:
        output_file = os.path.join(OUTPUT_DIR, f'{basename}_interactive3d.html')

        # Create interactive 3D visualization
        plot_interactive_surface_plotly(
            nifti_file,
            output_file,
            hemi='both',  # Both hemispheres (1mm spacing - extremely close!)
            mesh='fsaverage5',  # fsaverage5 for good quality and reasonable file size
            template='fsaverage',
            colormap='hot',
            initial_camera={'eye': {'x': 0, 'y': 0, 'z': 2.0}}  # Start with dorsal-ish view
        )

        size_mb = os.path.getsize(output_file) / (1024**2)
        total_size += size_mb
        print(f"✓ ({size_mb:.2f} MB)")
        successful += 1

    except Exception as e:
        print(f"✗ Error: {str(e)[:50]}")
        failed.append((basename, str(e)))

# Summary
print("\n" + "=" * 70)
print(" Summary")
print("=" * 70)
print(f"Total files: {len(nifti_files)}")
print(f"Successfully created: {successful}")
print(f"Failed: {len(failed)}")
print(f"Total size: {total_size:.2f} MB")
print()

if failed:
    print("Failed files:")
    for name, err in failed:
        print(f"  - {name}: {err[:60]}")
    print()

print(f"✅ Output directory: {OUTPUT_DIR}")
print("\n" + "=" * 70)
print(" How to Use:")
print("=" * 70)
print("1. Open any HTML file in a web browser")
print("2. Drag with mouse to ROTATE the brain to any angle")
print("3. Scroll to ZOOM in/out")
print("4. Right-click drag to PAN")
print("\n✨ You can now see perfect DORSAL (top-down) views!")
print("   Just rotate the brain with your mouse until you see the top!")
print("=" * 70)
