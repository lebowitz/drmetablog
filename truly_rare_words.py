import os
import re
import pandas as pd
from collections import Counter, defaultdict
import glob

# Directories
BLOG_DIR = '/Users/cal/drmetablog/www.drmetablog.com'
OUTPUT_DIR = 'output'

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# List of common English words to exclude
with open('/usr/share/dict/words', 'r') as f:
    COMMON_WORDS = set(line.strip().lower() for line in f)

# Focus directly on identifying genuinely unusual words
def extract_and_analyze_blog_text():
    """Extract text from blog posts and identify unusual words."""
    print("Analyzing blog posts for rare words...")
    
    # Find all .txt and .htm files
    text_files = glob.glob(os.path.join(BLOG_DIR, '**/*.txt'), recursive=True)
    htm_files = glob.glob(os.path.join(BLOG_DIR, '**/*.htm'), recursive=True)
    all_files = text_files + htm_files
    
    # Store raw words with their original capitalization
    original_word_forms = {}
    
    # Track article-word relationships
    article_words = defaultdict(list)
    all_words_list = []
    
    processed_files = 0
    
    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Remove HTML tags
                content = re.sub(r'<.*?>', ' ', content)
                # Remove URLs
                content = re.sub(r'https?://\S+', '', content)
                
                # Extract words preserving case
                words = re.findall(r'\b[a-zA-Z][a-zA-Z\'-]*[a-zA-Z]\b', content)
                
                # Store original forms for reference
                for word in words:
                    lower_word = word.lower()
                    original_word_forms[lower_word] = word
                    all_words_list.append(lower_word)
                    
                    # Associate with article
                    filename = os.path.basename(file_path)
                    if lower_word not in article_words[filename]:
                        article_words[filename].append(lower_word)
                
                processed_files += 1
                if processed_files % 100 == 0:
                    print(f"Processed {processed_files} files...")
                
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    print(f"Extracted words from {processed_files} files")
    
    # Count word frequencies
    word_counts = Counter(all_words_list)
    
    return word_counts, original_word_forms, article_words

def find_truly_rare_words(word_counts, original_forms):
    """Identify truly rare, unusual, or specialized words."""
    print("Finding truly rare words...")
    
    # Word categories to help identify truly unusual words
    rare_words = {}
    foreign_words = {}
    specialized_terms = {}
    
    # Keywords for specialized subject areas in the blog
    subject_keywords = {
        'literary': [
            'sonnet', 'metonymy', 'synecdoche', 'kenning', 'sprung', 'stanza', 'caesura', 'heroic', 
            'trochee', 'dactylic', 'iambic', 'assonance', 'villanelle', 'phoneme', 'grapheme'
        ],
        'philosophical': [
            'ontology', 'epistemology', 'phenomenology', 'hermeneutic', 'dialectic', 'teleological', 
            'syllogistic', 'aporia', 'qualia', 'metaphysic', 'semiotic', 'veridical', 'solipsism'
        ],
        'linguistic': [
            'diphthong', 'glottal', 'morpheme', 'allophone', 'lexeme', 'participle', 'deixis', 
            'inflection', 'declension', 'subjunctive', 'morphology', 'ablative', 'phonotactic'
        ]
    }
    
    # Common foreign word roots
    foreign_patterns = {
        'french': ['eux', 'eaux', 'oir', 'oir', 'eau', 'ette', 'eur', 'oir', 'que'],
        'german': ['schaft', 'heit', 'keit', 'lich', 'chen', 'berg', 'burg', 'Mann'],
        'latin': ['ium', 'ius', 'atus', 'ata', 'atum', 'andi', 'endi', 'undo'],
        'greek': ['ikos', 'ismos', 'esis', 'osis', 'oma', 'polis', 'logos', 'ikos']
    }
    
    # Iterate through all words with at least 2 occurrences (filter out typos)
    for word, count in word_counts.items():
        if count < 2:
            continue
            
        # Skip very short words - they're rarely interesting
        if len(word) < 5:
            continue
            
        # Skip words that are in the common dictionary
        if word.lower() in COMMON_WORDS:
            continue
            
        # Check if it's a foreign-looking word
        is_foreign = False
        for lang, patterns in foreign_patterns.items():
            if any(word.endswith(pattern) for pattern in patterns):
                foreign_words[word] = {
                    'count': count, 
                    'original': original_forms.get(word, word),
                    'language': lang
                }
                is_foreign = True
                break
        
        if is_foreign:
            continue
        
        # Check if it's a specialized term
        is_specialized = False
        for subject, keywords in subject_keywords.items():
            for keyword in keywords:
                if keyword in word:
                    specialized_terms[word] = {
                        'count': count, 
                        'original': original_forms.get(word, word),
                        'subject': subject
                    }
                    is_specialized = True
                    break
            if is_specialized:
                break
        
        if is_specialized:
            continue
        
        # If it's not identified as foreign or specialized,
        # add it to the general rare words category
        rare_words[word] = {
            'count': count,
            'original': original_forms.get(word, word)
        }
    
    return rare_words, foreign_words, specialized_terms

def manual_inspection_filter(rare_words):
    """Apply manual curation to filter for truly rare/interesting words."""
    
    # Set of words to exclude - these aren't as interesting
    exclude_words = {
        # Regular plurals and common derivatives
        'became', 'began', 'families', 'abilities', 'copies', 'varieties', 
        'entries', 'boxes', 'theories', 'accompanied', 'occurred', 'earliest',
        'scattered', 'offered', 'chosen', 'spoken', 'forgotten', 'chosen',
        'occasionally', 'reminded', 'remembered', 'discovered', 'visited',
        'belonged', 'matched', 'watched', 'allowed', 'carried', 'noticed',
        'helped', 'managed', 'delivered', 'remembered', 'wondered', 'admitted',
        
        # Technical/code terms 
        'getelementsbytagname', 'onreadystatechange', 'createelement', 'typeof',
        'innerhtml', 'doctype', 'onclick', 'substr', 'parseInt', 'parseint',
        
        # Common but just not in dictionary
        'signified', 'comedies', 'tragedies', 'galaxies', 'signifies', 'operas',
        'theatres', 'adjectives', 'pronoun', 'verbs', 'adverb', 'underlined',
        'underlining', 'unmarked', 'nouns', 'worded', 'reworded', 'rewords'
    }
    
    # Filter the rare words
    filtered_words = {}
    for word, data in rare_words.items():
        if word not in exclude_words:
            filtered_words[word] = data
    
    return filtered_words

def find_article_examples(article_words, target_words):
    """Find example articles containing rare words."""
    word_to_articles = defaultdict(list)
    
    for filename, words in article_words.items():
        for word in words:
            if word in target_words:
                if filename not in word_to_articles[word]:
                    word_to_articles[word].append(filename)
    
    return word_to_articles

def generate_report(rare_words, foreign_words, specialized_terms, word_articles):
    """Generate a report of the truly rare words."""
    print("Generating rare word report...")
    
    # Convert to DataFrame
    rare_df = pd.DataFrame([
        {
            'word': data['original'], 
            'count': data['count'],
            'articles': ", ".join(word_articles.get(word, [])[:3])
        }
        for word, data in rare_words.items()
    ])
    rare_df = rare_df.sort_values('count', ascending=False)
    
    foreign_df = pd.DataFrame([
        {
            'word': data['original'], 
            'count': data['count'],
            'language': data['language'],
            'articles': ", ".join(word_articles.get(word, [])[:3])
        }
        for word, data in foreign_words.items()
    ])
    foreign_df = foreign_df.sort_values('count', ascending=False)
    
    specialized_df = pd.DataFrame([
        {
            'word': data['original'], 
            'count': data['count'],
            'subject': data['subject'],
            'articles': ", ".join(word_articles.get(word, [])[:3])
        }
        for word, data in specialized_terms.items()
    ])
    specialized_df = specialized_df.sort_values('count', ascending=False)
    
    # Save to CSV
    rare_df.to_csv(os.path.join(OUTPUT_DIR, 'truly_rare_words.csv'), index=False)
    foreign_df.to_csv(os.path.join(OUTPUT_DIR, 'foreign_words.csv'), index=False)
    specialized_df.to_csv(os.path.join(OUTPUT_DIR, 'specialized_terms.csv'), index=False)
    
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
        .section { margin-top: 30px; }
    </style>
    </head>
    <body>
    <h1>Dr. Metablog Rare and Unusual Word Analysis</h1>
    <p>This report identifies truly rare, unusual, or specialized words from the blog that reveal
    the author's distinctive vocabulary and subject expertise.</p>
    
    <div class="section">
    <h2>Truly Rare and Unusual Words</h2>
    <table>
    <tr>
        <th>Rank</th>
        <th>Word</th>
        <th>Occurrences</th>
        <th>Example Articles</th>
    </tr>
    """
    
    # Add rare words
    for i, row in rare_df.head(50).iterrows():
        html += f"""
        <tr>
            <td>{i+1}</td>
            <td><strong>{row['word']}</strong></td>
            <td>{row['count']}</td>
            <td>{row['articles']}</td>
        </tr>
        """
    
    html += """
    </table>
    </div>
    
    <div class="section">
    <h2>Foreign Words and Terms</h2>
    <table>
    <tr>
        <th>Rank</th>
        <th>Word</th>
        <th>Occurrences</th>
        <th>Language</th>
        <th>Example Articles</th>
    </tr>
    """
    
    # Add foreign words
    for i, row in foreign_df.head(50).iterrows():
        html += f"""
        <tr>
            <td>{i+1}</td>
            <td><strong>{row['word']}</strong></td>
            <td>{row['count']}</td>
            <td>{row['language']}</td>
            <td>{row['articles']}</td>
        </tr>
        """
    
    html += """
    </table>
    </div>
    
    <div class="section">
    <h2>Specialized Academic and Literary Terms</h2>
    <table>
    <tr>
        <th>Rank</th>
        <th>Word</th>
        <th>Occurrences</th>
        <th>Subject Area</th>
        <th>Example Articles</th>
    </tr>
    """
    
    # Add specialized terms
    for i, row in specialized_df.head(50).iterrows():
        html += f"""
        <tr>
            <td>{i+1}</td>
            <td><strong>{row['word']}</strong></td>
            <td>{row['count']}</td>
            <td>{row['subject']}</td>
            <td>{row['articles']}</td>
        </tr>
        """
    
    html += """
    </table>
    </div>
    </body>
    </html>
    """
    
    with open(os.path.join(OUTPUT_DIR, 'truly_rare_words.html'), 'w') as f:
        f.write(html)
    
    print("Report generated successfully.")
    
    # Return DataFrames for display
    return rare_df, foreign_df, specialized_df

def main():
    # Extract and analyze all words
    word_counts, original_forms, article_words = extract_and_analyze_blog_text()
    
    # Find rare, foreign, and specialized words
    rare_words, foreign_words, specialized_terms = find_truly_rare_words(word_counts, original_forms)
    
    # Apply manual curation to get truly rare/interesting words
    rare_words = manual_inspection_filter(rare_words)
    
    # Find articles containing these words
    all_target_words = list(rare_words.keys()) + list(foreign_words.keys()) + list(specialized_terms.keys())
    word_articles = find_article_examples(article_words, all_target_words)
    
    # Generate report
    rare_df, foreign_df, specialized_df = generate_report(
        rare_words, foreign_words, specialized_terms, word_articles
    )
    
    # Print most interesting truly rare words
    print("\nTop Truly Rare and Unusual Words:")
    for i, row in rare_df.head(20).iterrows():
        print(f"{i+1:2d}. {row['word']:15s}: {row['count']} occurrences")
        
    print("\nTop Foreign Words:")
    for i, row in foreign_df.head(10).iterrows():
        print(f"{i+1:2d}. {row['word']:15s}: {row['count']} occurrences ({row['language']})")
        
    print("\nTop Specialized Academic Terms:")
    for i, row in specialized_df.head(10).iterrows():
        print(f"{i+1:2d}. {row['word']:15s}: {row['count']} occurrences ({row['subject']})")

if __name__ == "__main__":
    main()