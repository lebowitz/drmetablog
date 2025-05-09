#!/usr/bin/env python3

import re
import os

# Create directory to store split files
os.makedirs('split_blogs_decade', exist_ok=True)

# Dictionary to store content by decade
decade_content = {}

# Read the blog.txt file
with open('blog.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Split the content into individual blog entries
entries = re.split(r'={80,}\n+', content)

# Process each entry
for entry in entries:
    if not entry.strip():
        continue
    
    # Extract the year from the source line
    source_match = re.search(r'Source: (\d{4})/', entry)
    if source_match:
        year = source_match.group(1)
        decade = year[:3] + "0s"  # Convert year to decade (e.g., 2005 -> 2000s)
        
        # Add entry to the appropriate decade's content
        if decade not in decade_content:
            decade_content[decade] = []
        
        decade_content[decade].append(entry.strip())

# Write each decade's content to a separate file
for decade, entries in sorted(decade_content.items()):
    with open(f'split_blogs_decade/blog_{decade}.txt', 'w', encoding='utf-8') as decade_file:
        decade_file.write('\n\n' + '='*80 + '\n\n'.join(entries))
    
    print(f"Created blog_{decade}.txt with {len(entries)} entries")

print("Blog splitting by decade complete!")