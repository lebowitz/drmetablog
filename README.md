# Dr. Metablog Lexical Analysis Project

This document provides a summary of the work performed to analyze lexical patterns in the Dr. Metablog blog posts, using the Google Books Ngram dataset as a reference corpus.

## Project Overview

We began by exploring natural language processing techniques to analyze a collection of blog posts. The primary goals were to:

1. Download and process the Google Books 1-gram dataset
2. Extract text content from blog posts
3. Perform topic modeling using Latent Dirichlet Allocation (LDA)
4. Identify distinctive vocabulary by comparing blog word frequencies with general English

## Part 1: Initial Topic Modeling

### User Prompt
> what about using some ml algo to do topic extraction from the posts

### Implementation
We developed a Python script (`topic_extraction.py`) to implement Latent Dirichlet Allocation (LDA) for topic modeling. The script performs:

1. Text extraction from blog posts
2. Text preprocessing (HTML removal, tokenization)
3. Term frequency vectorization
4. LDA model fitting to identify latent topics
5. Visualization of topic distributions

### Key Results
The LDA model identified 15 topics in the blog posts:

```
Topic 0: novel, read, old, just, like, love, good, time, man, story
Topic 1: quot, english, cornell, writes, february, vivian, just, book, january, read
Topic 2: peace, years, dark, did, going, political, introduction, later, people, unknown
Topic 3: quot, life, october, permalink, december, february, poop, autobiography, jews, jewish
Topic 4: dog, cart, dogs, ball, horse, vehicle, fly, nineteenth, century, just
Topic 5: years, know, just, ve, don, did, new, like, life, time
Topic 6: antres, vast, othello, idle, heads, house, desdemona, touch, men, eat
Topic 7: film, amnesia, movie, memory, films, played, pearlman, plot, movies, murder
Topic 8: shakespeare, word, words, play, language, say, english, like, just, king
Topic 9: universe, joint, stars, billion, numbers, rocks, dark, life, big, years
```

Most common topics:
- Topic 5 (675 documents): Personal reflections, memories
- Topic 0 (298 documents): Literature, novels, reading
- Topic 8 (103 documents): Shakespeare, language, plays
- Topic 7 (52 documents): Films, with focus on amnesia/memory themes

## Part 2: Downloading Google Ngram Data

### Implementation
We created scripts to download the Google Books Ngram dataset:

1. `download_google_1grams.py`: A Python script using urllib to download the entire dataset (40 files)
2. Made the download script idempotent to handle download interruptions gracefully
3. Added command-line options for flexibility

## Part 3: Word Frequency Analysis

### User Prompt
> i want to perform a lexical analysis of the blog post entries. for example Interested in what words he uses that others mostly would not. formulate this and several other interesting analyses you could perform with the 1-gram data

### Implementation Ideas
Several analysis approaches were suggested:

1. **Lexical Distinctiveness Analysis**
   - Compare word frequencies in the blog against general English to identify distinctive vocabulary

2. **Temporal Language Evolution**
   - Check if the author uses older/archaic words more frequently than contemporary writers

3. **Topic-Specific Vocabulary**
   - Identify specialized vocabulary in different topic areas

4. **Readability and Complexity Analysis**
   - Analyze word length and frequency distributions

5. **Stylometric Fingerprinting**
   - Calculate function word usage compared to 1-gram norms

6. **Vocabulary Diversity Analysis**
   - Compare type-token ratio against typical ratios

7. **Neologism and Rare Word Usage**
   - Identify words used by the author that appear below a certain threshold in 1-grams

8. **Semantic Field Analysis**
   - Group words into semantic fields and compare distribution against general norms

### Selected Analysis: Lexical Distinctiveness

We implemented the Lexical Distinctiveness Analysis to identify words that are distinctively frequent in the blog posts compared to general English.

```python
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
```

### Final Result: Most Distinctive Words

The analysis identified the following words as most distinctive to Dr. Metablog's writing:

| Rank | Word       | Distinctiveness Score | Blog Occurrences | Blog Frequency (per million) | General Frequency (per million) |
|------|------------|-----------------------|------------------|------------------------------|--------------------------------|
| 1    | novel      | 79.2x                 | 551              | 871.2                        | 11.0                           |
| 2    | story      | 56.9x                 | 324              | 512.3                        | 9.0                            |
| 3    | poem       | 28.5x                 | 126              | 199.2                        | 7.0                            |
| 4    | literary   | 19.2x                 | 73               | 115.4                        | 6.0                            |
| 5    | fiction    | 19.0x                 | 96               | 151.8                        | 8.0                            |
| 6    | poetry     | 16.6x                 | 105              | 166.0                        | 10.0                           |
| 7    | author     | 15.2x                 | 135              | 213.4                        | 14.0                           |
| 8    | character  | 13.7x                 | 104              | 164.4                        | 12.0                           |
| 9    | reader     | 11.7x                 | 111              | 175.5                        | 15.0                           |
| 10   | text       | 11.4x                 | 94               | 165.2                        | 13.0                           |

## Conclusions

The lexical analysis of Dr. Metablog's writing reveals a strong focus on literary topics. The most distinctive words relate to literature, narrative, and poetry, appearing at much higher frequencies than in general English.

From both the topic modeling and lexical distinctiveness analysis, we can conclude that:

1. The blog has a strong focus on literary criticism and analysis
2. There's significant content about Shakespeare and his works
3. Films, particularly those dealing with amnesia or memory, form a distinct theme
4. The author uses specialized academic vocabulary related to literary analysis

This approach demonstrates how word frequency data from large corpora can reveal distinctive patterns in an individual author's writing style and content focus.

## Files Created
- `topic_extraction.py`: Performs LDA topic modeling
- `analyze_topics.py`: Analyzes topic distribution over time
- `download_google_1grams.py`: Downloads Google Ngram data
- `lexical_distinctiveness_simple.py`: Compares blog vocabulary with general English 
- `rare_word_analysis_strict.py`: Identifies rare words excluding common derivatives
- `truly_rare_words_fixed.py`: Focuses on genuinely rare specialized vocabulary
- `output/distinctive_vocabulary.html`: HTML report of distinctive vocabulary
- `output/distinctive_vocabulary.csv`: CSV data of distinctive vocabulary
- `rare_word_analysis.md`: Analysis of highly unusual vocabulary

## GitHub Pages

This project includes a [GitHub Pages site](https://github.io/USERNAME/drmetablog) with full analysis results.

Key findings from the [rare word analysis](rare_word_analysis.md) include the author's use of extremely uncommon vocabulary like:

1. counterhuman (54 occurrences)
2. blague (49 occurrences) - French for "joke"
3. demotic (12 occurrences)
4. doppelganger (11 occurrences)
5. pandiculation (8 occurrences) - the act of stretching and yawning