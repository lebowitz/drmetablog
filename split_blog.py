#!/usr/bin/env python3

import re
import os

# Create directory to store split files
os.makedirs('split_blogs', exist_ok=True)

# Dictionary to store content by year
year_content = {}

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
        
        # Add entry to the appropriate year's content
        if year not in year_content:
            year_content[year] = []
        
        year_content[year].append(entry.strip())

# Write each year's content to a separate file
for year, entries in sorted(year_content.items()):
    with open(f'split_blogs/blog_{year}.txt', 'w', encoding='utf-8') as year_file:
        year_file.write('\n\n' + '='*80 + '\n\n'.join(entries))
    
    print(f"Created blog_{year}.txt with {len(entries)} entries")

print("Blog splitting complete!")