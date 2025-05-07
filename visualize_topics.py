#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import os

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

# Topic distribution data from topic_analysis_report.md
topics = [
    ('Topic 5 (Life Experiences)', 55.8),
    ('Topic 0 (Literature & Reading)', 24.6),
    ('Topic 8 (Shakespeare Studies)', 8.5),
    ('Topic 7 (Film Analysis)', 4.3),
    ('Topic 1 (Academic & Cornell)', 1.8),
    ('Topic 3 (Personal Reflections)', 1.8)
]

# Create an "Other" category for the smallest topics (less than 1%)
other_topics = [
    ('Topic 10 (American Politics)', 0.9),
    ('Topic 4 (Animals & Historical)', 0.7),
    ('Topic 13 (Poetry Analysis)', 0.5),
    ('Topic 9 (Astronomy & Science)', 0.3),
    ('Topic 6 (Shakespeare\'s Othello)', 0.2),
    ('Topic 12 (Poetry & Music)', 0.2),
    ('Topic 11 (Travel Experiences)', 0.1),
    ('Topic 14 (Nature Observations)', 0.1)
]

# Add "Other" category to the topics list
other_percentage = sum(percentage for _, percentage in other_topics)
topics.append(('Other Topics', other_percentage))

# Extract labels and values
labels = [topic[0] for topic in topics]
values = [topic[1] for topic in topics]

# Create color map
colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(topics)))

# Create figure and axis
plt.figure(figsize=(12, 8))

# Create pie chart
wedges, texts, autotexts = plt.pie(
    values, 
    labels=None,  # We'll add custom labels later
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    pctdistance=0.85,
    explode=[0.05 if i < 3 else 0 for i in range(len(topics))]  # Explode the top 3 topics
)

# Customize text properties
plt.setp(autotexts, size=10, weight='bold')

# Add a legend
plt.legend(
    wedges, 
    [f"{label} ({value}%)" for label, value in zip(labels, values)],
    title="Topics",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1)
)

# Add title
plt.title('Topic Distribution in Dr. Metablog Posts', size=14, weight='bold')

# Save the figure
plt.tight_layout()
plt.savefig('output/lda_topics.png', dpi=300, bbox_inches='tight')

print("Visualization complete. Image saved to output/lda_topics.png")