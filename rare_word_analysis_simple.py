import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import glob
import string

# Directories
BLOG_DIR = '/Users/cal/drmetablog/www.drmetablog.com'
OUTPUT_DIR = 'output'

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def load_system_dictionary():
    """Load a dictionary of common English words from the system."""
    print("Loading system dictionary...")
    
    try:
        # Try system dictionary first
        with open('/usr/share/dict/words', 'r') as f:
            common_words = set(line.strip().lower() for line in f if len(line.strip()) > 1)
        print(f"Loaded {len(common_words)} words from system dictionary")
        return common_words
    except:
        # Fallback to a basic common words list
        print("System dictionary not available, using a basic common words set")
        with open('common_words.txt', 'w') as f:
            f.write("\n".join([
                "the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "it", "for", "not", "on", "with", 
                "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", 
                "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", 
                "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", 
                "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", "them", "see", 
                "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", 
                "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because",
                "any", "these", "give", "day", "most", "us", "is", "am", "are", "was", "were", "has", "had", "does",
                "did", "doing", "done", "should", "would", "should", "much", "many", "more", "most", "such", "very",
                "too", "little", "same", "different", "kind", "still", "high", "every", "each", "follow", "own",
                "around", "find", "long", "both", "might", "while", "begin", "end", "next", "last", "never", "few",
                "often", "always", "those", "through", "part", "place", "where", "after", "back", "little",
                "only", "round", "man", "year", "came", "show", "every", "good", "me", "give", "our", "under",
                "name", "very", "through", "just", "form", "sentence", "great", "think", "tell", "help", "ask", "line",
                "much", "before", "right", "too", "mean", "old", "move", "same", "tell", "boy", "following",
                "came", "want", "show", "also", "point", "four", "group", "always", "together", "talk", "until",
                "children", "side", "feet", "car", "mile", "night", "service", "river", "word", "walk", "pattern",
                "letter", "turn", "leave", "simple", "build", "call", "girl", "number", "paint", "picture",
                "person", "place", "room", "set", "sound", "spell", "tell", "thing", "walk", "watch", "water",
                "wave", "whole", "wind", "wonder", "world", "write", "answer", "found", "learn", "order", "possible",
                "red", "blue", "green", "yellow", "white", "black", "best", "kind", "house", "page", "father",
                "mother", "brother", "sister", "family", "face", "inch", "minute", "quick", "several", "vowel",
                "wait", "love", "money", "serve", "appear", "close", "road", "map", "rain", "rule",
                "govern", "pull", "cold", "notice", "voice", "energy", "hunt", "probable", "bed", "direct",
                "dog", "cat", "protect", "noon", "crop", "element", "hit", "planet", "size", "current", "check",
                "doctor", "please", "middle", "moment", "scale", "spring", "observe", "child", "straight", "consonant",
                "nation", "speed", "organ", "gold", "king", "queen", "count", "base", "cell", "happy", "basic", "smell",
                "century", "consider", "coast", "copy", "free", "chair", "danger", "fruit", "rich", "soldier", "travel",
                "week", "machine", "human", "people", "length", "distance", "condition", "listen", "morning", "evening",
                "night", "river", "single", "east", "west", "north", "south", "east", "paragraph", "scientist", 
                "temperature", "finger", "industry", "value", "fight", "lie", "beat", "excite", "natural", "view", 
                "sense", "capital", "chair", "danger", "fruit", "rich", "soldier", "travel", "coast", "forest", 
                "shore", "shell", "desert", "suit", "rise", "wonder", "laugh", "thousand", "ago", "ran", "game", 
                "shape", "equate", "often", "though", "record", "hat", "warm", "singular", "winter", "box", "noun",
                "field", "surprise", "symbol", "paint", "separate", "language", "swim", "trade"
            ]))
            
            # Load the created file
            with open('common_words.txt', 'r') as f:
                common_words = set(line.strip().lower() for line in f if len(line.strip()) > 1)
            print(f"Created and loaded {len(common_words)} basic common words")
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
            if not any(stem in common_vocabulary for stem in stem_checks if len(stem) > 2):
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
    article_densities = {}
    for filename, words in article_rare_words.items():
        density = 0
        for item in words:
            if isinstance(item, tuple) and item[0] == '_density_':
                density = item[1]
                break
        article_densities[filename] = density
    
    top_articles = sorted(article_densities.items(), key=lambda x: x[1], reverse=True)[:20]
    
    return article_rare_words, top_articles

def generate_report(rare_words, article_analysis, top_articles, output_csv, output_html):
    """Generate a report of rare word usage."""
    print("Generating rare word report...")
    
    # Convert to DataFrame for the CSV export
    df = pd.DataFrame(sorted(rare_words.items(), key=lambda x: x[1], reverse=True), 
                     columns=['word', 'count'])
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
    for i, (word, count) in enumerate(sorted(rare_words.items(), key=lambda x: x[1], reverse=True)[:100]):
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
        article_rare_words = []
        for item in article_analysis[filename]:
            if isinstance(item, tuple) and item[0] == '_density_':
                continue
            else:
                article_rare_words.append(item)
        
        # Keep only unique words for display
        unique_examples = list(set(article_rare_words))[:5]  # Show up to 5 examples
        
        html += f"""
        <tr>
            <td>{i+1}</td>
            <td>{filename}</td>
            <td>{density:.2f}</td>
            <td>{', '.join(unique_examples)}</td>
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

def main():
    # Load common English vocabulary
    common_vocabulary = load_system_dictionary()
    
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
    
    # Print top rare words
    print("\nTop 20 potentially rare or novel words:")
    for i, (word, count) in enumerate(sorted(rare_words.items(), key=lambda x: x[1], reverse=True)[:20]):
        print(f"{i+1:2d}. {word:15s}: {count} occurrences")

if __name__ == "__main__":
    main()