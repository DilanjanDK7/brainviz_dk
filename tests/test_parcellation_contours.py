#!/usr/bin/env python3
"""
Test Network Parcellation Contours with Plotly 3D
==================================================

Tests the Yeo 7 and 17 network parcellation overlays with contour lines.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from brainviz_dk import plot_interactive_surface_plotly, PARCELLATION_SCHEMES

# Test file
TEST_FILE = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym/group_mean.nii.gz'
OUTPUT_DIR = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym/PLOTLY_3D_COMPLETE_TEST'

print("=" * 80)
print(" TESTING NETWORK PARCELLATION CONTOURS")
print("=" * 80)
print(f"\nTest file: {TEST_FILE}")
print(f"Output: {OUTPUT_DIR}\n")

print("Available parcellation schemes:")
for key, info in PARCELLATION_SCHEMES.items():
    print(f"  • {key:20s} - {info['name']}")
print()

tests = [
    {
        'name': 'yeo7_thick_contours',
        'parcellation': 'yeo-7-thick',
        'opacity': 0.7,
        'colormap': 'hot',
        'contour_color': 'black',
        'contour_width': 2.0,
    },
    {
        'name': 'yeo17_thick_contours',
        'parcellation': 'yeo-17-thick',
        'opacity': 0.7,
        'colormap': 'plasma',
        'contour_color': 'white',
        'contour_width': 1.5,
    },
    {
        'name': 'yeo7_thin_transparent',
        'parcellation': 'yeo-7-thin',
        'opacity': 0.5,
        'colormap': 'viridis',
        'contour_color': 'black',
        'contour_width': 2.5,
    },
    {
        'name': 'yeo17_thin_transparent',
        'parcellation': 'yeo-17-thin',
        'opacity': 0.6,
        'colormap': 'coolwarm',
        'contour_color': 'yellow',
        'contour_width': 2.0,
    },
]

print(f"Running {len(tests)} tests...\n")

successful = 0
failed = []

for idx, test in enumerate(tests, 1):
    print(f"[{idx}/{len(tests)}] {test['name']:30s}", end=" ")
    print(f"({test['parcellation']}, opacity={test['opacity']})")
    print(f"        Contour: {test['contour_color']}, width={test['contour_width']}")
    print(f"        ", end="")

    try:
        output_file = os.path.join(OUTPUT_DIR, f"{test['name']}.html")

        plot_interactive_surface_plotly(
            TEST_FILE,
            output_file,
            hemi='both',
            mesh='fsaverage5',
            colormap=test['colormap'],
            opacity=test['opacity'],
            parcellation=test['parcellation'],
            contour_color=test['contour_color'],
            contour_width=test['contour_width'],
        )

        size_mb = os.path.getsize(output_file) / (1024**2)
        print(f"✓ ({size_mb:.2f} MB)")
        successful += 1

    except Exception as e:
        print(f"✗ Error: {str(e)[:70]}")
        failed.append((test['name'], str(e)))
        import traceback
        traceback.print_exc()

    print()

# Summary
print("=" * 80)
print(" SUMMARY")
print("=" * 80)
print(f"Total tests: {len(tests)}")
print(f"Successful: {successful}")
print(f"Failed: {len(failed)}")
print()

if failed:
    print("Failed tests:")
    for name, err in failed:
        print(f"  ❌ {name}")
        print(f"     {err[:100]}")
    print()

if successful > 0:
    print(f"✅ Output: {OUTPUT_DIR}")
    print()
    print("=" * 80)
    print(" HOW TO VIEW")
    print("=" * 80)
    print("""
Open any HTML file in a web browser and you'll see:
  • Brain activation data (colored by intensity)
  • Network boundary contour lines overlaid
  • Fully rotatable 3D view

The contour lines show the boundaries between different resting-state networks:
  • Yeo 7: Visual, Somatomotor, Dorsal Attention, Ventral Attention,
           Limbic, Frontoparietal, Default Mode
  • Yeo 17: Same networks but split into subnetworks

Rotate the brain to see:
  • How networks are distributed across the cortex
  • Where your activation overlaps with known networks
  • Network boundaries in different perspectives (lateral, medial, dorsal)

CONTOUR COLORS:
  • Black contours: Good contrast on most colormaps
  • White contours: Good for dark backgrounds or cool colormaps
  • Yellow contours: High visibility on bidirectional colormaps
    """)
    print("=" * 80)

print("🎉 PARCELLATION CONTOUR TESTING COMPLETE!")
print("=" * 80)
