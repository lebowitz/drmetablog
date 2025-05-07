import os
import urllib.request
import time
import sys
import concurrent.futures
import argparse

# Create data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# All available 1-gram files
base_url = "http://storage.googleapis.com/books/ngrams/books/"
all_1gram_files = [f"googlebooks-eng-all-1gram-20120701-{char}.gz" for char in 
                '0123456789abcdefghijklmnopqrstuvwxyz']

# Add special files
special_files = [
    "googlebooks-eng-all-totalcounts-20120701.txt",
    "googlebooks-eng-all-1gram-20120701-other.gz",
    "googlebooks-eng-all-1gram-20120701-pos.gz",
    "googlebooks-eng-all-1gram-20120701-punctuation.gz"
]

all_files = special_files + all_1gram_files

# Check which files already exist and which need to be downloaded
files_to_download = []
for file_name in all_files:
    if not os.path.exists(os.path.join('data', file_name)):
        files_to_download.append(file_name)

def download_file(file_name, force=False):
    """Download a single file"""
    file_url = base_url + file_name
    output_path = os.path.join('data', file_name)
    
    if os.path.exists(output_path) and not force:
        print(f"File {output_path} already exists, skipping download.")
        return True
    
    print(f"Downloading {file_url} to {output_path}...")
    
    try:
        # Set a custom user agent to avoid being blocked
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        req = urllib.request.Request(file_url, headers=headers)
        
        with urllib.request.urlopen(req) as response, open(output_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        
        print(f"Downloaded {file_name} successfully.")
        return True
    
    except Exception as e:
        print(f"Error downloading {file_name}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Download Google Books 1-gram files')
    parser.add_argument('--force', action='store_true', help='Force download even if file exists')
    parser.add_argument('--max-workers', type=int, default=1, 
                        help='Maximum number of concurrent downloads (default: 1)')
    parser.add_argument('--list-missing', action='store_true', 
                        help='Only list missing files without downloading')
    args = parser.parse_args()
    
    # If force option is used, download all files
    if args.force:
        download_list = all_files
    else:
        download_list = files_to_download
    
    print(f"Found {len(all_files)} total files")
    print(f"Already downloaded: {len(all_files) - len(files_to_download)} files")
    print(f"Missing: {len(files_to_download)} files")
    
    if args.list_missing:
        if files_to_download:
            print("\nMissing files:")
            for file in files_to_download:
                print(f"  - {file}")
        return
    
    if not download_list:
        print("All files are already downloaded. Use --force to re-download.")
        return
    
    print(f"\nPreparing to download {len(download_list)} files with {args.max_workers} workers...")
    if len(download_list) <= 5:  # Only show all files if there are just a few
        print(f"Files to download: {', '.join(download_list)}")
    
    if args.max_workers > 1:
        # Parallel download with ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
            futures = {executor.submit(download_file, file, args.force): file 
                      for file in download_list}
            
            success = 0
            for future in concurrent.futures.as_completed(futures):
                file = futures[future]
                if future.result():
                    success += 1
                    
            print(f"Downloaded {success} out of {len(download_list)} files successfully.")
    else:
        # Sequential download
        success = 0
        for file_name in download_list:
            if download_file(file_name, args.force):
                success += 1
            # Be nice to the server
            if file_name != download_list[-1]:
                print("Waiting 3 seconds before next download...")
                time.sleep(3)
        
        print(f"Downloaded {success} out of {len(download_list)} files successfully.")

if __name__ == "__main__":
    main()