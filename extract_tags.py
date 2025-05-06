#!/usr/bin/env python3
import os
import re
import csv
from bs4 import BeautifulSoup
import urllib.parse

def extract_tags_from_html(html_file):
    """Extract post filename and tags from an HTML file."""
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all entry divs
    entries = soup.find_all('div', class_=re.compile(r'entry-category-'))
    
    results = []
    for entry in entries:
        # Extract permalink
        permalink_tag = entry.find('a', class_='permalink')
        if not permalink_tag:
            continue
        
        permalink = permalink_tag.get('href', '')
        if not permalink:
            continue
        
        # Format the filename like www.drmetablog.com/2008/04/crockery.txt
        try:
            # Parse the URL to extract path components
            parsed_url = urllib.parse.urlparse(permalink)
            path_parts = parsed_url.path.strip('/').split('/')
            
            if len(path_parts) >= 3 and path_parts[0].isdigit() and path_parts[1].isdigit():
                year = path_parts[0]
                month = path_parts[1]
                basename = path_parts[2].replace('.html', '.txt')
                formatted_filename = f"www.drmetablog.com/{year}/{month}/{basename}"
            else:
                # Fallback if URL structure is unexpected
                basename = os.path.basename(permalink).replace('.html', '.txt')
                formatted_filename = basename
        except Exception as e:
            print(f"Error parsing permalink {permalink}: {e}")
            continue
        
        # Extract tags from class attribute
        class_attr = entry.get('class', [])
        tags = []
        for cls in class_attr:
            if cls.startswith('entry-category-') and cls != 'entry-category-':
                tag = cls.replace('entry-category-', '')
                if tag and tag != 'autobiography_brooklyn_in_the_1950s': # Skip compound tags
                    tags.append(tag)
        
        # Also try to extract tags from footer links
        footer_info = entry.find('p', class_='entry-footer-info')
        if footer_info:
            footer_links = footer_info.find_all('a')
            for link in footer_links:
                href = link.get('href', '')
                if 'drmetablog.com/' in href and href.endswith('/'):
                    tag = href.rstrip('/').split('/')[-1]
                    if tag and tag not in tags:
                        tags.append(tag)
        
        for tag in tags:
            results.append((formatted_filename, tag))
    
    return results

def main():
    csv_path = 'post_tags.csv'
    all_results = []
    seen_entries = set()  # To avoid duplicates
    
    # Process .html files in scrape directory and its subdirectories
    for root, _, files in os.walk('scrape'):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    results = extract_tags_from_html(file_path)
                    for result in results:
                        entry = (result[0], result[1])
                        if entry not in seen_entries:
                            all_results.append(result)
                            seen_entries.add(entry)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    # Write results to CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['post_file', 'tag'])
        writer.writerows(all_results)
    
    print(f"Extracted {len(all_results)} post-tag associations to {csv_path}")

if __name__ == "__main__":
    main()