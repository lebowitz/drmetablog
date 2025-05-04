#!/usr/bin/env python3
import os
import re
from bs4 import BeautifulSoup
import glob

def extract_text_from_html(html_file):
    """Extract blog post content from HTML file."""
    with open(html_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Get the title
    title_tag = soup.find('h3', class_='entry-header')
    title = title_tag.get_text().strip() if title_tag else "No Title"
    
    # Get the date
    date_tag = soup.find('h2', class_='date-header')
    date = date_tag.get_text().strip() if date_tag else "No Date"
    
    # Get the main content (the blog post text)
    content_div = soup.find('div', class_='entry-body')
    if content_div:
        # Extract text and preserve paragraph structure
        paragraphs = content_div.find_all('p')
        text_content = "\n\n".join([p.get_text().strip() for p in paragraphs])
    else:
        text_content = "No content found"
    
    return {
        'title': title,
        'date': date,
        'content': text_content
    }

def save_text_to_file(output_dir, relative_path, data):
    """Save extracted text to a txt file."""
    # Create output directory structure
    output_path = os.path.join(output_dir, relative_path.replace('.html', '.txt'))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the extracted content to the file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Title: {data['title']}\n")
        f.write(f"Date: {data['date']}\n\n")
        f.write(data['content'])
    
    return output_path

def concatenate_text_files(output_dir, combined_output_path):
    """Concatenate all extracted text files into a single file."""
    # Find all text files in the output directory
    text_files = glob.glob(f"{output_dir}/**/*.txt", recursive=True)
    
    # Sort the files by date (newest last) - extract date from file content
    def get_file_date(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("Date:"):
                        # Extract and return the date line
                        return line.strip()
            return "Date: Unknown"
        except Exception:
            return "Date: Error"
    
    text_files.sort(key=get_file_date)
    
    # Concatenate all files
    with open(combined_output_path, 'w', encoding='utf-8') as outfile:
        for i, file_path in enumerate(text_files):
            relative_path = os.path.relpath(file_path, output_dir)
            
            # Add separator between entries
            if i > 0:
                outfile.write("\n\n" + "="*80 + "\n\n")
            
            # Add file path as a reference
            outfile.write(f"Source: {relative_path}\n\n")
            
            # Add file content
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
    
    print(f"All text files have been concatenated into {combined_output_path}")
    print(f"Total number of blog posts: {len(text_files)}")

def main():
    base_dir = "/Users/cal/drmetablog/www.drmetablog.com"
    output_dir = "/Users/cal/drmetablog/extracted_text"
    combined_output_path = "/Users/cal/drmetablog/blog.txt"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all HTML files
    html_files = glob.glob(f"{base_dir}/**/*.html", recursive=True)
    
    # Filter out index files and other non-blog pages
    blog_files = [f for f in html_files if not os.path.basename(f).startswith("index")]
    
    print(f"Found {len(blog_files)} blog posts to process")
    
    for html_file in blog_files:
        # Get relative path from the base directory
        relative_path = os.path.relpath(html_file, base_dir)
        
        try:
            # Extract text from HTML
            data = extract_text_from_html(html_file)
            
            # Save to text file
            output_path = save_text_to_file(output_dir, relative_path, data)
            
            print(f"Processed: {relative_path}")
        except Exception as e:
            print(f"Error processing {relative_path}: {str(e)}")
    
    # Concatenate all text files into a single file
    concatenate_text_files(output_dir, combined_output_path)
    
    print("Text extraction complete!")

if __name__ == "__main__":
    main()