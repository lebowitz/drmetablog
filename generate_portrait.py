#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse, Circle, Arc, PathPatch
from matplotlib.path import Path
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

# Ensure output directory exists
os.makedirs('output', exist_ok=True)

# Create figure with appropriate dimensions
fig, ax = plt.subplots(figsize=(10, 12), dpi=100)

# Background - soft cream color for a scholarly feel
ax.add_patch(Rectangle((0, 0), 1, 1, transform=ax.transAxes, facecolor='#FFF8E7', edgecolor='none', zorder=-10))

# Add some texture to the background - like old paper
for _ in range(500):
    x, y = np.random.rand(), np.random.rand()
    size = np.random.uniform(0.001, 0.003)
    alpha = np.random.uniform(0.03, 0.08)
    ax.add_patch(Circle((x, y), size, facecolor='#8B7355', alpha=alpha, edgecolor=None, transform=ax.transAxes, zorder=-9))

# Draw bookshelf in background
bookshelf_y = 0.2
bookshelf_height = 0.6
ax.add_patch(Rectangle((0.05, bookshelf_y), 0.9, bookshelf_height, facecolor='#8B4513', edgecolor='#654321', linewidth=2, alpha=0.3, zorder=-8))

# Add books on shelf
book_colors = ['#9B0000', '#00008B', '#006400', '#8B008B', '#FF8C00', '#228B22', '#4B0082']
book_positions = np.linspace(0.1, 0.85, 20)
for pos in book_positions:
    height = np.random.uniform(0.1, 0.25)
    width = np.random.uniform(0.02, 0.05)
    color = np.random.choice(book_colors)
    ax.add_patch(Rectangle((pos, bookshelf_y + 0.05), width, height, facecolor=color, edgecolor='#000000', linewidth=0.5, alpha=0.4, zorder=-7))

# Draw a desk/table with some papers
desk_y = 0.1
ax.add_patch(Rectangle((0.2, desk_y), 0.6, 0.05, facecolor='#8B4513', edgecolor='#654321', linewidth=1, alpha=0.5, zorder=-6))

# Add some papers on the desk
paper_positions = [(0.3, desk_y + 0.01), (0.4, desk_y + 0.02), (0.5, desk_y + 0.01)]
for pos in paper_positions:
    ax.add_patch(Rectangle(pos, 0.08, 0.1, facecolor='#FFFAFA', edgecolor='#A9A9A9', linewidth=0.5, alpha=0.7, angle=np.random.uniform(-10, 10), zorder=-5))

# Face and head shape - older gentleman
# Create a face that suggests an elderly scholarly gentleman with kind eyes
face_center_x, face_center_y = 0.5, 0.6
face_width, face_height = 0.18, 0.24

# Face oval
face = Ellipse((face_center_x, face_center_y), face_width, face_height, facecolor='#F5DEB3', edgecolor='#DEB887', linewidth=1.5, zorder=1)
ax.add_patch(face)

# Slightly receding hairline with gray hair
hair_color = '#D3D3D3'  # Light gray
ax.add_patch(Ellipse((face_center_x, face_center_y + 0.06), face_width + 0.02, 0.15, facecolor=hair_color, edgecolor=None, zorder=0))

# Add some thinning on top
for x in np.linspace(face_center_x - 0.05, face_center_x + 0.05, 6):
    y = face_center_y + 0.11
    plt.plot([x, x], [y, y + 0.03], color='#F5DEB3', linewidth=3, zorder=1)

# Wrinkles - subtle lines for age (forehead)
for i in range(3):
    y = face_center_y + 0.06 - i * 0.015
    curve_x = np.linspace(face_center_x - 0.07, face_center_x + 0.07, 20)
    curve_y = [y + 0.002 * np.sin(x * 30) for x in curve_x]
    plt.plot(curve_x, curve_y, color='#CD853F', alpha=0.4, linewidth=1, zorder=2)

# Eyes - thoughtful, kind eyes with glasses
eye_level = face_center_y + 0.015
eye_size = 0.022
left_eye_x = face_center_x - 0.06
right_eye_x = face_center_x + 0.06

# Glasses
glasses_color = '#696969'
# Left lens
ax.add_patch(Ellipse((left_eye_x, eye_level), 0.06, 0.04, facecolor='none', edgecolor=glasses_color, linewidth=1.5, zorder=5))
# Right lens
ax.add_patch(Ellipse((right_eye_x, eye_level), 0.06, 0.04, facecolor='none', edgecolor=glasses_color, linewidth=1.5, zorder=5))
# Bridge
plt.plot([left_eye_x + 0.03, right_eye_x - 0.03], [eye_level, eye_level], color=glasses_color, linewidth=1.5, zorder=5)
# Temple pieces
plt.plot([left_eye_x - 0.03, left_eye_x - 0.08], [eye_level, eye_level - 0.01], color=glasses_color, linewidth=1.5, zorder=5)
plt.plot([right_eye_x + 0.03, right_eye_x + 0.08], [eye_level, eye_level - 0.01], color=glasses_color, linewidth=1.5, zorder=5)

# Actual eyes behind glasses
ax.add_patch(Ellipse((left_eye_x, eye_level), eye_size, eye_size * 0.6, facecolor='white', edgecolor='#696969', linewidth=1, zorder=3))
ax.add_patch(Ellipse((right_eye_x, eye_level), eye_size, eye_size * 0.6, facecolor='white', edgecolor='#696969', linewidth=1, zorder=3))

# Pupils - looking slightly to the side for a thoughtful gaze
pupil_size = eye_size * 0.5
ax.add_patch(Circle((left_eye_x + 0.005, eye_level), pupil_size, facecolor='#000080', zorder=4))
ax.add_patch(Circle((right_eye_x + 0.005, eye_level), pupil_size, facecolor='#000080', zorder=4))

# Light reflection in eyes to give them life
ax.add_patch(Circle((left_eye_x + 0.005, eye_level + 0.005), pupil_size * 0.3, facecolor='white', zorder=5))
ax.add_patch(Circle((right_eye_x + 0.005, eye_level + 0.005), pupil_size * 0.3, facecolor='white', zorder=5))

# Eyebrows - bushy, academic eyebrows
left_brow_y = eye_level + 0.04
right_brow_y = eye_level + 0.04
left_brow_x = np.linspace(left_eye_x - 0.05, left_eye_x + 0.05, 20)
right_brow_x = np.linspace(right_eye_x - 0.05, right_eye_x + 0.05, 20)

# Add some randomness to make them look bushier
left_brow_y_points = [left_brow_y + 0.004 * np.sin(5 * x) for x in left_brow_x]
right_brow_y_points = [right_brow_y + 0.004 * np.sin(5 * x) for x in right_brow_x]

plt.plot(left_brow_x, left_brow_y_points, color=hair_color, linewidth=2.5, zorder=6)
plt.plot(right_brow_x, right_brow_y_points, color=hair_color, linewidth=2.5, zorder=6)

# Nose - distinguished nose for a distinguished scholar
nose_top = eye_level - 0.01
nose_bottom = face_center_y - 0.05
nose_width = 0.03

# Basic nose shape
nose_x = [face_center_x, face_center_x - nose_width/2, face_center_x, face_center_x + nose_width/2]
nose_y = [nose_top, nose_bottom - 0.02, nose_bottom, nose_bottom - 0.02]

# Add nostril suggestion
plt.plot([face_center_x - 0.02, face_center_x - 0.01], [nose_bottom, nose_bottom], color='#8B4513', linewidth=1, zorder=7)
plt.plot([face_center_x + 0.01, face_center_x + 0.02], [nose_bottom, nose_bottom], color='#8B4513', linewidth=1, zorder=7)

# Mouth - slight, thoughtful smile
mouth_x = face_center_x
mouth_y = face_center_y - 0.1
mouth_width = 0.08

# Lips with slight smile
upper_lip_left = (mouth_x - mouth_width/2, mouth_y)
upper_lip_center = (mouth_x, mouth_y - 0.005)
upper_lip_right = (mouth_x + mouth_width/2, mouth_y)

lower_lip_left = (mouth_x - mouth_width/2, mouth_y)
lower_lip_center = (mouth_x, mouth_y + 0.01)
lower_lip_right = (mouth_x + mouth_width/2, mouth_y)

# Draw upper and lower lips with control points
verts_upper = [
    upper_lip_left,
    (mouth_x - mouth_width/4, mouth_y - 0.005),
    upper_lip_center,
    (mouth_x + mouth_width/4, mouth_y - 0.005),
    upper_lip_right,
]

verts_lower = [
    lower_lip_left,
    (mouth_x - mouth_width/4, mouth_y + 0.015),
    lower_lip_center,
    (mouth_x + mouth_width/4, mouth_y + 0.015),
    lower_lip_right,
]

codes = [Path.MOVETO] + [Path.CURVE4] * 4

path_upper = Path(verts_upper, codes)
path_lower = Path(verts_lower, codes)

patch_upper = PathPatch(path_upper, facecolor='none', edgecolor='#8B4513', linewidth=1.5, zorder=7)
patch_lower = PathPatch(path_lower, facecolor='none', edgecolor='#8B4513', linewidth=1.5, zorder=7)

ax.add_patch(patch_upper)
ax.add_patch(patch_lower)

# More facial details

# Subtle cheekbones and creases around the mouth for an older face
# Left cheek
plt.plot(
    [face_center_x - 0.07, face_center_x - 0.04], 
    [face_center_y - 0.07, face_center_y - 0.06],
    color='#CD853F', alpha=0.4, linewidth=1, zorder=2
)
# Right cheek
plt.plot(
    [face_center_x + 0.04, face_center_x + 0.07], 
    [face_center_y - 0.06, face_center_y - 0.07],
    color='#CD853F', alpha=0.4, linewidth=1, zorder=2
)

# Lines from nose to mouth corners
plt.plot(
    [face_center_x - 0.02, face_center_x - mouth_width/2 - 0.01], 
    [nose_bottom, mouth_y + 0.01],
    color='#CD853F', alpha=0.5, linewidth=1, zorder=2
)
plt.plot(
    [face_center_x + 0.02, face_center_x + mouth_width/2 + 0.01], 
    [nose_bottom, mouth_y + 0.01],
    color='#CD853F', alpha=0.5, linewidth=1, zorder=2
)

# Chin detail - slight cleft and shadow
chin_y = face_center_y - 0.15
plt.plot(
    [face_center_x - 0.01, face_center_x, face_center_x + 0.01], 
    [chin_y + 0.02, chin_y, chin_y + 0.02],
    color='#CD853F', alpha=0.4, linewidth=1, zorder=2
)

# Ear shape - left ear
ear_height = 0.06
ear_x = face_center_x - face_width/2 - 0.01
ear_y = eye_level

# Simple ear shape
ear_y_points = np.linspace(ear_y - ear_height/2, ear_y + ear_height/2, 20)
ear_x_points = [ear_x - 0.01 * np.sin(np.pi * (y - ear_y) / ear_height) for y in ear_y_points]
plt.plot(ear_x_points, ear_y_points, color='#DEB887', linewidth=2, zorder=0)

# Inner ear detail
inner_ear_y_points = np.linspace(ear_y - ear_height/3, ear_y + ear_height/3, 10)
inner_ear_x_points = [ear_x - 0.005 - 0.005 * np.sin(np.pi * (y - ear_y) / ear_height) for y in inner_ear_y_points]
plt.plot(inner_ear_x_points, inner_ear_y_points, color='#CD853F', linewidth=1, zorder=0)

# Right ear (partially hidden by hair)
ear_x = face_center_x + face_width/2 + 0.01
ear_y_points = np.linspace(ear_y - ear_height/2, ear_y + ear_height/2, 20)
ear_x_points = [ear_x + 0.01 * np.sin(np.pi * (y - ear_y) / ear_height) for y in ear_y_points]
plt.plot(ear_x_points, ear_y_points, color='#DEB887', linewidth=2, zorder=0)

# Neck
neck_top_y = face_center_y - face_height/2 - 0.01
neck_width = 0.1
neck_height = 0.08
ax.add_patch(Rectangle((face_center_x - neck_width/2, neck_top_y - neck_height), neck_width, neck_height, facecolor='#F5DEB3', edgecolor='#DEB887', linewidth=1, zorder=0))

# Shirt collar
collar_angle = 30  # Degrees
collar_length = 0.06
collar_x1 = face_center_x - neck_width/2
collar_x2 = face_center_x + neck_width/2
collar_y = neck_top_y - neck_height + 0.01

# Left collar
plt.plot(
    [collar_x1, collar_x1 - np.cos(np.radians(collar_angle)) * collar_length],
    [collar_y, collar_y - np.sin(np.radians(collar_angle)) * collar_length],
    color='#F0F0F0', linewidth=3, zorder=0
)

# Right collar
plt.plot(
    [collar_x2, collar_x2 + np.cos(np.radians(collar_angle)) * collar_length],
    [collar_y, collar_y - np.sin(np.radians(collar_angle)) * collar_length],
    color='#F0F0F0', linewidth=3, zorder=0
)

# Jacket or cardigan suggestion
jacket_top_y = collar_y - 0.01
jacket_width = 0.25
ax.add_patch(Rectangle((face_center_x - jacket_width/2, jacket_top_y - 0.2), jacket_width, 0.2, facecolor='#4682B4', edgecolor='#4A5568', linewidth=1, alpha=0.7, zorder=-1))

# Light pen in jacket pocket
pen_x = face_center_x + 0.07
pen_y = jacket_top_y - 0.05
pen_height = 0.06
plt.plot([pen_x, pen_x], [pen_y, pen_y - pen_height], color='#D4AF37', linewidth=2, alpha=0.7, zorder=0)

# Hand holding a book
hand_x = face_center_x - 0.1
hand_y = jacket_top_y - 0.15
hand_color = '#F5DEB3'

# Simple hand shape
ax.add_patch(Ellipse((hand_x, hand_y), 0.05, 0.08, angle=45, facecolor=hand_color, edgecolor='#DEB887', linewidth=1, zorder=2))

# Book being held
book_width = 0.15
book_height = 0.1
book_x = hand_x - 0.02
book_y = hand_y - 0.02
ax.add_patch(Rectangle((book_x, book_y), book_width, book_height, facecolor='#800000', edgecolor='#000000', linewidth=1, zorder=1))
# Book pages
ax.add_patch(Rectangle((book_x + 0.005, book_y + 0.005), book_width - 0.01, book_height - 0.01, facecolor='#FFFAFA', edgecolor='#A9A9A9', linewidth=0.5, zorder=2))

# Add some text lines to suggest writing in the book
for i in range(5):
    text_y = book_y + 0.02 + i * 0.015
    if text_y < book_y + book_height - 0.01:
        line_length = np.random.uniform(0.05, book_width - 0.03)
        plt.plot([book_x + 0.02, book_x + 0.02 + line_length], [text_y, text_y], color='#000000', linewidth=0.5, alpha=0.6, zorder=3)

# Add title at the top
ax.text(0.5, 0.9, "Dr. Metablog (Vivian de St. Vrain)", 
        horizontalalignment='center', fontsize=18, fontweight='bold', color='#000000')

# Add a subtle signature in the bottom right
ax.text(0.85, 0.05, "Based on his writings\n2025", 
        horizontalalignment='right', fontsize=8, style='italic', color='#696969')

# Remove axes and set limits
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Save the portrait
plt.savefig('output/dr_metablog_portrait.png', dpi=300, bbox_inches='tight')
print("Portrait generated and saved to output/dr_metablog_portrait.png")