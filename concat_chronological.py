#!/usr/bin/env python3
import os
import glob
import re
from datetime import datetime

def parse_date(file_path):
    """Extract date from file content and convert to datetime for sorting."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Extract date from content
        date_match = re.search(r'Date: (.+)$', content, re.MULTILINE)
        if date_match:
            date_str = date_match.group(1).strip()
            # Try multiple date formats
            for fmt in ['%B %d, %Y', '%b %d, %Y', '%d %B %Y', '%d %b %Y']:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
        
        # If date extraction fails, try to use folder structure (yyyy/mm)
        parts = file_path.split('/')
        if len(parts) >= 3:
            try:
                year = int(parts[-3])
                month = int(parts[-2])
                # Use middle of month as default date
                return datetime(year, month, 15)
            except (ValueError, IndexError):
                pass
        
        # Default to epoch (oldest)
        return datetime(1970, 1, 1)
    except Exception as e:
        print(f"Error parsing date from {file_path}: {e}")
        return datetime(1970, 1, 1)

def main():
    """Concatenate all .txt files in chronological order."""
    base_dir = "/Users/cal/drmetablog/www.drmetablog.com"
    output_file = "/Users/cal/drmetablog/blog.txt"
    
    # Find all .txt files
    txt_files = glob.glob(f"{base_dir}/**/*.txt", recursive=True)
    
    print(f"Found {len(txt_files)} text files to concatenate")
    
    # Get date and path for each file
    file_info = []
    for file_path in txt_files:
        date = parse_date(file_path)
        file_info.append((date, file_path))
    
    # Sort by date (oldest first)
    file_info.sort(key=lambda x: x[0])
    
    # Concatenate files
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, (date, file_path) in enumerate(file_info):
            rel_path = os.path.relpath(file_path, base_dir)
            
            # Add separator for all but the first entry
            if i > 0:
                outfile.write('\n\n' + '=' * 80 + '\n\n')
            
            # Add source information
            outfile.write(f"Source: {rel_path.replace('.txt', '')}\n\n")
            
            # Add file content
            with open(file_path, 'r', encoding='utf-8', errors='replace') as infile:
                outfile.write(infile.read())
    
    print(f"All text files have been concatenated into {output_file} in chronological order")

if __name__ == "__main__":
    main()