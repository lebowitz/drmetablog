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

# Hardcoded list of actually rare words to look for
INTERESTING_RARE_WORDS = {
    # Literary/philosophical terms
    'blague', 'counterhuman', 'crepuscular', 'crepitant', 'eidolon', 'diegetic', 
    'ekphrastic', 'ersatz', 'exegetical', 'flâneur', 'lacuna', 'liminal', 'ludic', 
    'magisterial', 'mimetic', 'noumenal', 'palimpsest', 'paronomasia', 'patina', 
    'phantasmagoria', 'phatic', 'phlogiston', 'plangent', 'prelapsarian', 'prestidigitation',
    'prosaic', 'rhizome', 'semiotics', 'simulacra', 'skeuomorph', 'spectrality', 
    'stochastic', 'sublation', 'subaltern', 'syntagmatic', 'thanatos', 'threnody',
    'uncanny', 'xenia', 'zetetic',
    
    # Rare/archaic English words
    'abecedarian', 'absquatulate', 'adumbrate', 'anagnorisis', 'anent', 'anfractuous',
    'antediluvian', 'apricity', 'argute', 'ataraxia', 'autochthonous', 'blandishment',
    'borborygmus', 'cacoethes', 'callipygian', 'canorous', 'catafalque', 'chatoyant',
    'chthonic', 'clerisy', 'cloying', 'concinnity', 'crapulent', 'cynosure', 'defenestrate',
    'deliquescent', 'demotic', 'denouement', 'dithyramb', 'elision', 'eldritch',
    'embrocation', 'eructation', 'esurient', 'etiolate', 'eudaemonic', 'exsanguinate',
    'febrile', 'frangible', 'fuscous', 'fuliginous', 'gasconade', 'gelid', 'gormless',
    'gyrfalcon', 'horripilation', 'impignorate', 'imprecation', 'inchoate', 'inspissate',
    'juxtapose', 'kakistocracy', 'limerence', 'lucubration', 'macerate', 'mephitic',
    'moiety', 'mulligrubs', 'nascent', 'nescience', 'nidificate', 'noctivagant',
    'obfuscate', 'obstreperous', 'omphaloskepsis', 'oneiric', 'orotund', 'osculate',
    'palaver', 'pandiculation', 'parapraxis', 'parsimonious', 'pejorative', 'perspicacious',
    'petrichor', 'philter', 'pogonotrophy', 'pulchritudinous', 'pyrrhic', 'quiddity',
    'raconteur', 'recondite', 'regnant', 'riparian', 'ruelle', 'sangfroid', 'satori',
    'schadenfreude', 'sesquipedalian', 'sinecure', 'soporific', 'sphygmomanometer',
    'susurration', 'tatterdemalion', 'tenebrous', 'tergiversate', 'triskaidekaphobia',
    'tenebrific', 'velleity', 'virago', 'welkin', 'woolgathering', 'zeugma', 'zugzwang',
    
    # Foreign words
    'aporia', 'anomie', 'bricolage', 'dasein', 'doppelganger', 'flâneur', 'gesamtkunstwerk',
    'habitus', 'jouissance', 'kairos', 'lacunae', 'ostranenie', 'pharmakon', 'différance',
    'eidolon', 'koan', 'labarum', 'mauvaise', 'praxis', 'qualia', 'simulacrum', 'sprezzatura',
    'weltanschauung', 'zeitgeist', 'zoetrope'
}

def extract_and_analyze_blog_text():
    """Extract text from blog posts and identify unusual words."""
    print("Analyzing blog posts for genuinely rare words...")
    
    # Find all .txt and .htm files
    text_files = glob.glob(os.path.join(BLOG_DIR, '**/*.txt'), recursive=True)
    htm_files = glob.glob(os.path.join(BLOG_DIR, '**/*.htm'), recursive=True)
    all_files = text_files + htm_files
    
    # Track word occurrences and article information
    rare_word_counts = Counter()
    word_to_articles = defaultdict(list)
    
    processed_files = 0
    
    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Remove HTML tags
                content = re.sub(r'<.*?>', ' ', content)
                # Remove URLs
                content = re.sub(r'https?://\S+', '', content)
                
                filename = os.path.basename(file_path)
                
                # Look for each rare word
                for rare_word in INTERESTING_RARE_WORDS:
                    # Pattern to match the word with word boundaries
                    pattern = r'\b' + re.escape(rare_word) + r'\b'
                    
                    # Case insensitive search
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    
                    # If found, record it
                    if matches:
                        count = len(matches)
                        rare_word_counts[rare_word] += count
                        
                        # Record this article as containing the word
                        if filename not in word_to_articles[rare_word]:
                            word_to_articles[rare_word].append(filename)
                
                processed_files += 1
                if processed_files % 100 == 0:
                    print(f"Processed {processed_files} files...")
                    
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    print(f"Extracted words from {processed_files} files")
    print(f"Found {len([w for w, c in rare_word_counts.items() if c > 0])} genuinely rare words")
    
    return rare_word_counts, word_to_articles

def generate_report(rare_word_counts, word_to_articles):
    """Generate a report of the truly rare words."""
    print("Generating rare word report...")
    
    # Convert to DataFrame
    data = []
    for word, count in rare_word_counts.items():
        if count > 0:
            data.append({
                'word': word, 
                'count': count,
                'articles': ", ".join(word_to_articles[word][:3])
            })
    
    df = pd.DataFrame(data)
    df = df.sort_values('count', ascending=False)
    
    # Save to CSV
    df.to_csv(os.path.join(OUTPUT_DIR, 'genuinely_rare_words.csv'), index=False)
    
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
    </style>
    </head>
    <body>
    <h1>Dr. Metablog Genuinely Rare Words</h1>
    <p>This report identifies truly rare, unusual, or specialized words from the blog that would generally 
    only be familiar to specialists in literary theory, philosophy, or those with an exceptionally large vocabulary.</p>
    
    <h2>Genuinely Rare and Unusual Words</h2>
    <table>
    <tr>
        <th>Rank</th>
        <th>Word</th>
        <th>Occurrences</th>
        <th>Example Articles</th>
    </tr>
    """
    
    # Add rare words
    for i, row in df.iterrows():
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
    </body>
    </html>
    """
    
    with open(os.path.join(OUTPUT_DIR, 'genuinely_rare_words.html'), 'w') as f:
        f.write(html)
    
    print("Report generated successfully.")
    
    return df

def main():
    # Extract and analyze all words
    rare_word_counts, word_to_articles = extract_and_analyze_blog_text()
    
    # Generate report
    df = generate_report(rare_word_counts, word_to_articles)
    
    # Print most interesting truly rare words
    print("\nTop 20 Genuinely Rare and Unusual Words:")
    for i, row in df.head(20).iterrows():
        print(f"{i+1:2d}. {row['word']:15s}: {row['count']} occurrences")

if __name__ == "__main__":
    main()