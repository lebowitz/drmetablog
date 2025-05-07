import os
import re
import gzip
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import glob
import math
from wordcloud import WordCloud
import string

# Directories
DATA_DIR = 'data'
BLOG_DIR = 'www.drmetablog.com'
OUTPUT_DIR = 'output'

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def load_general_english_frequencies(year_range=(1990, 2000), min_count=100):
    """Load word frequencies from Google Books 1-gram data."""
    print("Loading general English word frequencies...")
    
    # Get available 1-gram files
    files = glob.glob(os.path.join(DATA_DIR, "googlebooks-eng-all-1gram-*.gz"))
    
    # Get total word count from the totalcounts file
    total_count_file = os.path.join(DATA_DIR, "googlebooks-eng-all-totalcounts-20120701.txt")
    total_words_in_corpus = 0
    
    if os.path.exists(total_count_file):
        with open(total_count_file, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 2 and parts[0] == 'TOTAL_WORDS':
                    total_words_in_corpus = int(parts[1])
                    break
    
    print(f"Total words in Google Books corpus: {total_words_in_corpus:,}")
    
    # Initialize word frequency dictionary
    word_freq = Counter()
    processed_files = 0
    
    # Process a subset of files to make it manageable
    # Prioritize files with letters, not numbers
    letter_files = [f for f in files if 'googlebooks-eng-all-1gram-20120701-' in f and f[-5] in 'abcdefghijklmnopqrstuvwxyz']
    subset_files = letter_files[:5]  # Using first 5 letter files
    
    for file_path in subset_files:
        file_name = os.path.basename(file_path)
        
        # Skip non-standard files
        if any(special in file_name for special in ['pos', 'punctuation', 'other']):
            continue
            
        print(f"Processing {file_name}...")
        
        with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                if i % 5000000 == 0 and i > 0:
                    print(f"  Processed {i:,} lines...")
                
                parts = line.strip().split('\t')
                if len(parts) < 3:
                    continue
                
                # Parse the line
                gram, year, count, volume_count = parts
                year, count = int(year), int(count)
                
                # Filter by year range
                if year < year_range[0] or year > year_range[1]:
                    continue
                
                # Only include words that match this pattern (lowercase words)
                if not re.match(r'^[a-z]+$', gram):
                    continue
                
                # Update the word count
                word_freq[gram] += count
        
        processed_files += 1
        print(f"Found {len(word_freq):,} unique words so far across {processed_files} files")
    
    # Filter by minimum frequency
    word_freq = {word: count for word, count in word_freq.items() if count >= min_count}
    
    # Calculate normalized frequencies (per million words)
    if total_words_in_corpus > 0:
        normalized_freq = {word: (count / total_words_in_corpus) * 1000000 
                          for word, count in word_freq.items()}
    else:
        # If we don't have the total count, estimate based on the sum of our counts
        total_processed = sum(word_freq.values())
        normalized_freq = {word: (count / total_processed) * 1000000 
                          for word, count in word_freq.items()}
    
    print(f"Loaded {len(normalized_freq):,} general English words with normalized frequencies")
    return normalized_freq

def extract_blog_text():
    """Extract text from all blog posts."""
    print("Extracting text from blog posts...")
    
    # Find all .txt and .htm files
    text_files = glob.glob(os.path.join(BLOG_DIR, '**/*.txt'), recursive=True)
    htm_files = glob.glob(os.path.join(BLOG_DIR, '**/*.htm'), recursive=True)
    all_files = text_files + htm_files
    
    all_text = ""
    processed_files = 0
    
    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Remove HTML tags
                content = re.sub(r'<.*?>', ' ', content)
                
                # Remove URLs
                content = re.sub(r'https?://\S+', '', content)
                
                all_text += content + " "
                processed_files += 1
                
                if processed_files % 100 == 0:
                    print(f"Processed {processed_files} files...")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    print(f"Extracted text from {processed_files} files")
    return all_text

def analyze_blog_vocabulary(blog_text, general_freq):
    """Analyze vocabulary distinctiveness in blog posts."""
    print("Analyzing blog vocabulary...")
    
    # Tokenize and clean the blog text
    words = re.findall(r'\b[a-z]+\b', blog_text.lower())
    
    # Count word frequencies in the blog
    blog_word_counts = Counter(words)
    total_words = len(words)
    
    print(f"Found {len(blog_word_counts):,} unique words in the blog out of {total_words:,} total words")
    
    # Calculate normalized frequencies (per million words)
    blog_freq = {word: (count / total_words) * 1000000 for word, count in blog_word_counts.items()}
    
    # Calculate distinctiveness scores (blog frequency / general frequency)
    distinctiveness = {}
    min_blog_count = 5  # Minimum occurrences in blog to be considered
    
    for word, blog_count in blog_word_counts.items():
        if blog_count >= min_blog_count and word in general_freq and len(word) > 2:
            # Skip very common words (top 100)
            if general_freq[word] > 10000:  # Very common words
                continue
                
            # Calculate distinctiveness score
            score = blog_freq[word] / general_freq[word]
            distinctiveness[word] = {
                'blog_count': blog_count,
                'blog_freq_per_million': blog_freq[word],
                'general_freq_per_million': general_freq[word],
                'distinctiveness': score
            }
    
    print(f"Calculated distinctiveness scores for {len(distinctiveness):,} words")
    return distinctiveness

def generate_distinctiveness_report(distinctiveness, output_csv, output_html):
    """Generate a report of the most distinctive words."""
    print("Generating distinctiveness report...")
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame.from_dict(distinctiveness, orient='index')
    
    # Sort by distinctiveness score (descending)
    df.sort_values('distinctiveness', ascending=False, inplace=True)
    
    # Add rank column
    df['rank'] = range(1, len(df) + 1)
    
    # Save to CSV
    df.to_csv(output_csv)
    print(f"Saved distinctiveness data to {output_csv}")
    
    # Create HTML report with more detailed styling
    html = """
    <html>
    <head>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333366; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th { background-color: #333366; color: white; text-align: left; padding: 8px; }
        td { border: 1px solid #ddd; padding: 8px; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .highlight { background-color: #ffffcc; }
        .score-high { color: #cc0000; font-weight: bold; }
        .score-med { color: #ff6600; }
    </style>
    </head>
    <body>
    <h1>Dr. Metablog Distinctive Vocabulary Analysis</h1>
    <p>This report identifies words that appear much more frequently in Dr. Metablog's writing 
    compared to general English usage. A distinctiveness score of 10 means the word appears 10 times 
    more frequently in the blog than in general English.</p>
    
    <table>
    <tr>
        <th>Rank</th>
        <th>Word</th>
        <th>Distinctiveness Score</th>
        <th>Blog Occurrences</th>
        <th>Blog Frequency (per million)</th>
        <th>General Frequency (per million)</th>
    </tr>
    """
    
    # Add top 500 most distinctive words
    for i, (word, row) in enumerate(df.head(500).iterrows()):
        score_class = "score-high" if row['distinctiveness'] > 20 else "score-med"
        highlight = " class='highlight'" if i % 2 == 0 else ""
        
        html += f"""
        <tr{highlight}>
            <td>{row['rank']}</td>
            <td><strong>{word}</strong></td>
            <td class='{score_class}'>{row['distinctiveness']:.1f}x</td>
            <td>{row['blog_count']}</td>
            <td>{row['blog_freq_per_million']:.1f}</td>
            <td>{row['general_freq_per_million']:.1f}</td>
        </tr>
        """
    
    html += """
    </table>
    </body>
    </html>
    """
    
    with open(output_html, 'w') as f:
        f.write(html)
    
    print(f"Saved HTML report to {output_html}")
    return df

def visualize_distinctive_words(distinctiveness_df, output_path):
    """Create visualizations for distinctive words."""
    print("Creating visualizations...")
    
    # Create a word cloud of distinctive words
    top_words = distinctiveness_df.head(200)
    
    # Create a dictionary with words and their distinctiveness scores
    word_dict = {idx: row['distinctiveness'] for idx, row in top_words.iterrows()}
    
    # Generate the wordcloud
    wordcloud = WordCloud(
        width=1200, 
        height=800, 
        background_color='white',
        max_words=100,
        colormap='viridis',
        random_state=42
    ).generate_from_frequencies(word_dict)
    
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("Most Distinctive Words in Dr. Metablog's Writing", fontsize=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Saved word cloud to {output_path}")

def main():
    # Load general English word frequencies
    general_freq = load_general_english_frequencies()
    
    # Extract text from blog posts
    blog_text = extract_blog_text()
    
    # Analyze blog vocabulary distinctiveness
    distinctiveness = analyze_blog_vocabulary(blog_text, general_freq)
    
    # Generate distinctiveness report
    output_csv = os.path.join(OUTPUT_DIR, "distinctive_vocabulary.csv")
    output_html = os.path.join(OUTPUT_DIR, "distinctive_vocabulary.html")
    df = generate_distinctiveness_report(distinctiveness, output_csv, output_html)
    
    # Visualize distinctive words
    output_vis = os.path.join(OUTPUT_DIR, "distinctive_wordcloud.png")
    visualize_distinctive_words(df, output_vis)
    
    # Print top 20 most distinctive words
    print("\nTop 20 most distinctive words in Dr. Metablog's writing:")
    for i, (word, row) in enumerate(df.head(20).iterrows()):
        print(f"{i+1:2d}. {word:15s}: {row['distinctiveness']:.1f}x more frequent " +
              f"({row['blog_count']} occurrences)")

if __name__ == "__main__":
    main()