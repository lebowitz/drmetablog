#!/usr/bin/env python3
import os
import glob
import subprocess
import re

def format_with_par(text, width=80):
    """Format text using the par command."""
    # Split the text into paragraphs
    paragraphs = re.split(r'\n\n+', text)
    
    formatted_paragraphs = []
    for paragraph in paragraphs:
        # Skip empty paragraphs
        if not paragraph.strip():
            continue
        
        # Preserve title, date lines, and source lines without reformatting
        if (paragraph.startswith("Title:") or 
            paragraph.startswith("Date:") or 
            paragraph.startswith("Source:")):
            formatted_paragraphs.append(paragraph)
            continue
            
        # Preserve section dividers
        if paragraph.strip() == "=" * 80:
            formatted_paragraphs.append(paragraph)
            continue
            
        # Check if paragraph looks like a list or formatted text
        if (re.match(r'(\s*[•\-\*\d]+\.?\s+)', paragraph) or 
            paragraph.startswith("[") or 
            "|" in paragraph):
            formatted_paragraphs.append(paragraph)
            continue
        
        # For regular paragraphs, use par to reformat
        try:
            # Run par command
            result = subprocess.run(
                ["par", f"{width}"],
                input=paragraph.encode(),
                capture_output=True,
                check=True
            )
            formatted = result.stdout.decode().strip()
            formatted_paragraphs.append(formatted)
        except subprocess.CalledProcessError:
            # If par fails, keep the original paragraph
            formatted_paragraphs.append(paragraph)
    
    # Join paragraphs with a single blank line between each
    return "\n\n".join(formatted_paragraphs)

def process_files(pattern, width=80):
    """Process all files matching the pattern."""
    files = glob.glob(pattern, recursive=True)
    print(f"Found {len(files)} files to process")
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Format the text using par
            formatted_content = format_with_par(content, width)
            
            # Write the formatted text back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted_content)
            
            print(f"Processed: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

def main():
    """Main function."""
    # Process individual text files
    process_files("/Users/cal/drmetablog/www.drmetablog.com/**/*.txt", width=80)
    
    # Process the combined blog.txt file
    blog_file = "/Users/cal/drmetablog/blog.txt"
    try:
        with open(blog_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Format the combined text file
        formatted_content = format_with_par(content, width=80)
        
        # Write the formatted text back to the file
        with open(blog_file, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        print(f"Processed: {blog_file}")
    except Exception as e:
        print(f"Error processing {blog_file}: {e}")
    
    print("Text formatting with par complete!")

if __name__ == "__main__":
    main()