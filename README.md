# Dr. Metablog Analysis

## Text Analysis of Blog Content

This repository contains analysis of the Dr. Metablog content, including:

- **[Topic Modeling](topic_analysis_report.md)** - LDA topic analysis of blog content
- **[Rare Word Analysis](rare_word_analysis.md)** - Analysis of unusual and sophisticated vocabulary
- **[Lexical Distinctiveness](distinctive_vocabulary.md)** - Words used more frequently than in general English

Each analysis provides a different perspective on the author's writing style and interests:

- The [topic analysis](topic_analysis_report.md) reveals key themes like literature (24.6%), Shakespeare studies (8.5%), and film analysis (4.3%) alongside personal reflections (55.8%).

- The [rare word analysis](rare_word_analysis.md) uncovers the author's use of extremely uncommon vocabulary like "counterhuman" (54 occurrences), "blague" (49), and "pandiculation" (8).

- The [lexical distinctiveness analysis](distinctive_vocabulary.md) shows the author uses literary terms at dramatically higher rates than general English (e.g., "novel" appears 79.2× more frequently).

## Google Ngram Data

The analysis uses Google Books Ngram data for comparison with general English usage.

## Repository Contents

- `topic_extraction.py` - LDA topic modeling script
- `analyze_topics.py` - Topic distribution analysis
- `lexical_distinctiveness_simple.py` - Compares blog vocabulary with standard English
- `rare_word_analysis_strict.py` - Identifies rare words excluding common derivatives
- `truly_rare_words_fixed.py` - Focuses on genuinely rare specialized vocabulary
- `download_google_1grams.py` - Script for downloading Google Ngram data

## Topic Model Results

The LDA model identified 15 topics in the blog posts:

```
Topic 0: novel, read, old, just, like, love, good, time, man, story
Topic 1: quot, english, cornell, writes, february, vivian, just, book, january, read
Topic 5: years, know, just, ve, don, did, new, like, life, time
Topic 7: film, amnesia, movie, memory, films, played, pearlman, plot, movies, murder
Topic 8: shakespeare, word, words, play, language, say, english, like, just, king
```

## Most Distinctive Words

These words appear much more frequently in the blog than in general English:

1. novel (79.2× more frequent)
2. story (56.9× more frequent)
3. poem (28.5× more frequent)
4. literary (19.2× more frequent)
5. fiction (19.0× more frequent)

## Genuinely Rare Words

The most unusual words used in the blog include:

1. counterhuman (54 occurrences)
2. blague (49 occurrences) - French for "joke"
3. demotic (12 occurrences)
4. doppelganger (11 occurrences)
5. pandiculation (8 occurrences) - the act of stretching and yawning