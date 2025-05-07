#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

# Directories
OUTPUT_DIR = 'output'

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Define the most distinctive words and their scores
distinctive_words = {
    'novel': 79.2,
    'story': 56.9,
    'poem': 28.5,
    'literary': 19.2,
    'fiction': 19.0,
    'poetry': 16.6,
    'author': 15.2,
    'character': 13.7,
    'reader': 11.7,
    'text': 11.4,
    'language': 10.3,
    'book': 9.2,
    'culture': 9.0,
    'memory': 8.9,
    'idea': 6.5,
    'Shakespeare': 65.3,
    'amnesia': 37.7,
    'sonnet': 31.2,
    'Cornell': 117.9,
    'literature': 6.1,
    'theory': 5.2,
    'context': 5.3,
    'analysis': 3.7,
    'discourse': 4.1
}

# Alternatively, load from CSV if you prefer
# df = pd.read_csv('output/distinctive_vocabulary.csv')
# distinctive_words = dict(zip(df.iloc[:20, 0], df.iloc[:20, 4]))

# Generate word cloud
wordcloud = WordCloud(
    width=1200, 
    height=800,
    background_color='white',
    colormap='viridis',
    max_words=50,
    prefer_horizontal=1.0,
    random_state=42,
    contour_width=1,
    contour_color='steelblue',
    font_path=None,  # Use default font
    relative_scaling=1.0  # Importance of frequency relative to scaling
).generate_from_frequencies(distinctive_words)

# Plot the word cloud
plt.figure(figsize=(16, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Most Distinctive Words in Dr. Metablog", fontsize=24)
plt.tight_layout(pad=0)

# Save the word cloud
output_path = os.path.join(OUTPUT_DIR, 'distinctive_wordcloud.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Word cloud saved to {output_path}")

# Also display the word cloud (if running in an interactive environment)
# plt.show()