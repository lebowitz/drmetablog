import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import glob
import string
from wordcloud import WordCloud

# Directories
DATA_DIR = 'data'
BLOG_DIR = '/Users/cal/drmetablog/www.drmetablog.com'
OUTPUT_DIR = 'output'

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Load common English words from a dictionary or the 1-gram data
def load_english_vocabulary():
    """
    Load common English vocabulary to filter against rare or novel words.
    """
    print("Loading English vocabulary...")
    
    # Load from Google Ngram total counts file
    total_count_file = os.path.join(DATA_DIR, "googlebooks-eng-all-totalcounts-20120701.txt")
    
    # We'll build our common vocabulary from the a-z files
    common_words = set()
    rare_threshold = 100  # Words appearing fewer than this many times are considered rare
    
    # Get any available 1-gram files (only process a subset for speed)
    files = sorted(glob.glob(os.path.join(DATA_DIR, "googlebooks-eng-all-1gram-20120701-[a-z].gz")))[:5]
    
    if not files:
        print("No 1-gram files found, using built-in English word list")
        # Use nltk's words corpus as a fallback
        try:
            import nltk
            from nltk.corpus import words
            nltk.download('words', quiet=True)
            common_words = set(w.lower() for w in words.words() if len(w) > 1)
            print(f"Loaded {len(common_words)} words from NLTK")
        except:
            # If NLTK isn't available, use a small common word list
            print("NLTK not available, using a simplified common word list")
            with open('/usr/share/dict/words', 'r') as f:
                common_words = set(line.strip().lower() for line in f if len(line.strip()) > 1)
            print(f"Loaded {len(common_words)} words from system dictionary")
    else:
        print(f"Processing {len(files)} 1-gram files to build vocabulary...")
        import gzip
        
        year_range = (1990, 2000)  # Focus on contemporary English
        words_processed = 0
        
        for file_path in files:
            file_name = os.path.basename(file_path)
            print(f"Processing {file_name}...")
            
            try:
                with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f):
                        if i % 5000000 == 0 and i > 0:
                            print(f"  Processed {i:,} lines...")
                        
                        parts = line.strip().split('\t')
                        if len(parts) < 3:
                            continue
                        
                        # Parse the line
                        gram, year, count, _ = parts
                        year, count = int(year), int(count)
                        
                        # Filter by year range and format
                        if year < year_range[0] or year > year_range[1]:
                            continue
                            
                        # Only include words that match lowercase letters
                        if re.match(r'^[a-z]+$', gram) and len(gram) > 1:
                            if count >= rare_threshold:
                                common_words.add(gram)
                            words_processed += 1
                            
                        if words_processed % 1000000 == 0:
                            print(f"  Vocabulary size: {len(common_words):,} words")
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
    
    print(f"Final vocabulary size: {len(common_words):,} common words")
    return common_words

def extract_blog_text():
    """Extract text from all blog posts."""
    print("Extracting text from blog posts...")
    
    # Find all .txt and .htm files
    text_files = glob.glob(os.path.join(BLOG_DIR, '**/*.txt'), recursive=True)
    htm_files = glob.glob(os.path.join(BLOG_DIR, '**/*.htm'), recursive=True)
    all_files = text_files + htm_files
    
    all_text = ""
    file_texts = {}  # Store text by filename for per-article analysis
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
                
                # Store the text indexed by filename for per-article analysis
                filename = os.path.basename(file_path)
                file_texts[filename] = content
                
                processed_files += 1
                
                if processed_files % 100 == 0:
                    print(f"Processed {processed_files} files...")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    print(f"Extracted text from {processed_files} files")
    return all_text, file_texts

def find_rare_and_novel_words(blog_text, common_vocabulary):
    """Find rare and novel words in the blog text."""
    print("Analyzing rare and novel words...")
    
    # Tokenize and clean the blog text
    all_words = re.findall(r'\b[a-z]+\b', blog_text.lower())
    
    # Count word frequencies in the blog
    blog_word_counts = Counter(all_words)
    total_words = len(all_words)
    
    print(f"Found {len(blog_word_counts):,} unique words in the blog out of {total_words:,} total words")
    
    # Identify rare and potentially novel words
    rare_words = {}
    min_blog_count = 3  # Minimum occurrences to avoid typos
    min_word_length = 4  # Minimum characters to be considered interesting
    
    for word, count in blog_word_counts.items():
        # Skip very short words and common words
        if len(word) < min_word_length:
            continue
            
        if count >= min_blog_count and word not in common_vocabulary:
            # Check that it's not a simple plural or common derivative form
            # If a word minus 's', 'ed', 'ing', etc. exists in the vocabulary, it's probably not novel
            stem_checks = [word[:-1], word[:-2], word[:-3]]  # Simple stemming checks
            if not any(stem in common_vocabulary for stem in stem_checks if len(stem) > 3):
                rare_words[word] = count
    
    print(f"Found {len(rare_words)} potentially rare or novel words")
    return rare_words

def analyze_rare_words_by_article(file_texts, rare_words):
    """Analyze the distribution of rare words across articles."""
    print("Analyzing rare word distribution by article...")
    
    # Track rare word occurrences by article
    article_rare_words = defaultdict(list)
    article_rare_word_counts = defaultdict(int)
    
    for filename, text in file_texts.items():
        # Find words in this article
        article_words = re.findall(r'\b[a-z]+\b', text.lower())
        total_article_words = len(article_words)
        
        # Count rare words in this article
        for word in article_words:
            if word in rare_words:
                article_rare_words[filename].append(word)
                article_rare_word_counts[filename] += 1
        
        # Calculate rare word density (rare words per 1000 words)
        if total_article_words > 0:
            article_rare_words[filename].append(
                ('_density_', article_rare_word_counts[filename] / total_article_words * 1000)
            )
    
    # Find articles with the highest density of rare words
    article_densities = {
        filename: next(value for word, value in words if word == '_density_')
        for filename, words in article_rare_words.items()
        if any(word == '_density_' for word, _ in words)
    }
    
    top_articles = sorted(article_densities.items(), key=lambda x: x[1], reverse=True)[:20]
    
    return article_rare_words, top_articles

def generate_report(rare_words, article_analysis, top_articles, output_csv, output_html):
    """Generate a report of rare word usage."""
    print("Generating rare word report...")
    
    # Convert to DataFrame for the CSV export
    df = pd.DataFrame(rare_words.items(), columns=['word', 'count'])
    df.sort_values('count', ascending=False, inplace=True)
    df.to_csv(output_csv, index=False)
    print(f"Saved rare word data to {output_csv}")
    
    # Create HTML report
    html = """
    <html>
    <head>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1, h2 { color: #333366; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th { background-color: #333366; color: white; text-align: left; padding: 8px; }
        td { border: 1px solid #ddd; padding: 8px; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .highlight { background-color: #ffffcc; }
        .article-section { margin-top: 30px; border-top: 1px solid #ddd; padding-top: 20px; }
    </style>
    </head>
    <body>
    <h1>Dr. Metablog Rare and Novel Word Analysis</h1>
    <p>This report identifies words that appear in the blog but are not found in common English 
    vocabularies. These may include specialized terminology, neologisms, or obscure/archaic words.</p>
    
    <h2>Top Rare Words by Frequency</h2>
    <table>
    <tr>
        <th>Rank</th>
        <th>Word</th>
        <th>Occurrences in Blog</th>
    </tr>
    """
    
    # Add top 100 rare words
    for i, (word, count) in enumerate(rare_words.items()):
        if i >= 100:
            break
        html += f"""
        <tr>
            <td>{i+1}</td>
            <td><strong>{word}</strong></td>
            <td>{count}</td>
        </tr>
        """
    
    html += """
    </table>
    
    <div class="article-section">
    <h2>Articles with Highest Density of Rare Words</h2>
    <p>These articles contain the highest concentration of rare or specialized vocabulary.</p>
    <table>
    <tr>
        <th>Rank</th>
        <th>Article</th>
        <th>Rare Word Density<br>(per 1000 words)</th>
        <th>Example Rare Words</th>
    </tr>
    """
    
    # Add articles with highest rare word density
    for i, (filename, density) in enumerate(top_articles):
        # Get some example rare words from this article
        article_rare_words = [word for word, _ in article_analysis[filename] if word != '_density_']
        example_words = article_rare_words[:5]  # Show up to 5 examples
        
        html += f"""
        <tr>
            <td>{i+1}</td>
            <td>{filename}</td>
            <td>{density:.2f}</td>
            <td>{', '.join(example_words)}</td>
        </tr>
        """
    
    html += """
    </table>
    </div>
    </body>
    </html>
    """
    
    with open(output_html, 'w') as f:
        f.write(html)
    
    print(f"Saved HTML report to {output_html}")
    return df

def visualize_rare_words(rare_words, output_path):
    """Create a word cloud of rare words."""
    print("Creating rare word visualization...")
    
    # Create a word cloud
    wordcloud = WordCloud(
        width=1200, 
        height=800, 
        background_color='white',
        max_words=200,
        colormap='plasma',
        random_state=42
    ).generate_from_frequencies(rare_words)
    
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("Rare and Potentially Novel Words in Dr. Metablog's Writing", fontsize=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Saved rare word cloud to {output_path}")

def main():
    # Load common English vocabulary
    common_vocabulary = load_english_vocabulary()
    
    # Extract text from blog posts
    blog_text, file_texts = extract_blog_text()
    
    # Find rare and novel words
    rare_words = find_rare_and_novel_words(blog_text, common_vocabulary)
    
    if not rare_words:
        print("No rare words found.")
        return
    
    # Analyze distribution by article
    article_analysis, top_articles = analyze_rare_words_by_article(file_texts, rare_words)
    
    # Generate reports and visualizations
    output_csv = os.path.join(OUTPUT_DIR, "rare_words.csv")
    output_html = os.path.join(OUTPUT_DIR, "rare_words.html")
    df = generate_report(rare_words, article_analysis, top_articles, output_csv, output_html)
    
    # Create visualization
    output_vis = os.path.join(OUTPUT_DIR, "rare_wordcloud.png")
    visualize_rare_words(rare_words, output_vis)
    
    # Print top rare words
    print("\nTop 20 potentially rare or novel words:")
    for i, (word, count) in enumerate(sorted(rare_words.items(), key=lambda x: x[1], reverse=True)[:20]):
        print(f"{i+1:2d}. {word:15s}: {count} occurrences")

if __name__ == "__main__":
    main()