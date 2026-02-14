## 1. System Architecture Overview

Astro-Clarity operates as a decentralized microservice suite, utilizing **Python** for its heavy NLP/scraping capabilities and **Go** for its high-concurrency API and data orchestration.

- **Data Tier:** PostgreSQL (Structured Meta), Redis (Hot Transit Cache), Pinecone (Semantic Embeddings).
    
- **Service Tier:** Python Scraper (PRAW), Go API Gateway, Astro-Acharya Logic Engine.
    
- **Presentation Tier:** Next.js (Dashboard), Tailwind CSS, Framer Motion (Visualizations).
    

---

## 2. Python Scraper Service (The "Collector")

This service runs as a background worker, continuously pooling data from specific subreddits (e.g., `r/vedicastrology`, `r/spirituality`).

### Technical Logic (PRAW Implementation)

- **Asynchronous Polling:** Uses a `SubmissionStream` to capture real-time posts and comments.
    
- **NLP Pipeline:**
    
    - **Preprocessing:** Tokenization and lemmatization using `spaCy`.
        
    - **Sentiment Extraction:** Leverages `VADER` or a fine-tuned `RoBERTa` model for nuanced emotional scoring (Valence, Arousal, Dominance).
        
    - **Keyword Extraction:** Identifies astrological terms (e.g., "Sade Sati," "Jupiter Retrograde").
        

Python

```
# Conceptual Snippet: Python NLP Worker
import praw
from transformers import pipeline

class RedditAstroScraper:
    def __init__(self):
        self.reddit = praw.Reddit(client_id="...", client_secret="...", user_agent="AstroClarity")
        self.sentiment_model = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

    def monitor_subreddits(self, subreddit_list):
        subreddit = self.reddit.subreddit("+".join(subreddit_list))
        for submission in subreddit.stream.submissions():
            sentiment = self.sentiment_model(submission.title[:512])
            # Push to Go API via gRPC or Webhook
            self.dispatch_to_motherboard(submission.id, sentiment, submission.created_utc)
```

---

## 3. Go API Architecture (Motherboard Core)

The Go service acts as the central brain, handling the high volume of incoming data from the scraper and serving the Next.js frontend.

- **Concurrency Model:** Uses **Goroutines** to process incoming sentiment scores and map them against the current Ephemeris data (planetary positions).
    
- **Transit Mapping Logic:**
    
    - The service queries the **Astro-Acharya Engine** (a library/service calculating planetary degrees).
        
    - It creates a "Correlation Key": `[Planet]_[Transit_Sign]_[Timestamp_Bucket]`.
        
- **Endpoints:**
    
    - `GET /api/v1/sentiment/heatmap`: Returns aggregated sentiment data by planetary transit.
        
    - `GET /api/v1/search/semantic`: Proxies requests to the Vector Database.
        

---

## 4. Astro-Acharya Engine: Transit-Sentiment Mapping

This is the unique logic layer that gives the app "Astro Clarity."

- **Mapping Mechanism:**
    
    1. **Sentiment Peak Detection:** Identify a statistically significant surge in "Anxiety" sentiment on Reddit.
        
    2. **Transit Overlay:** Check if a malefic planet (e.g., Mars or Saturn) is currently in a difficult _Nakshatra_ or aspecting the Moon.
        
    3. **Clarity Output:** Generate a correlation score. If Anxiety correlates with a specific Mars transit, it flags this as a **"Collective Transit Response."**
        

---

## 5. Next.js Frontend UI Components

The frontend focuses on making abstract astrological data scannable and intuitive.

### Component A: Transit-Sentiment Heatmap

- **Visual:** A grid where the X-axis represents planets (Sun to Rahu) and the Y-axis represents current Signs.
    
- **Interaction:** Cells are color-coded based on the average sentiment score of Reddit posts created while a planet was in that position. Red = Intense/Negative, Blue = Calm/Positive.
    

### Component B: Semantic Astro-Search

- **Logic:** Uses a vector search (via Pinecone) to find posts that are _conceptually_ related to an astrological query, even if the keywords don't match.
    
- **UI:** A search bar that suggests terms like "Saturn Returns" or "Rahu Dasha Impact" and highlights relevant Reddit threads with an "Astro-Significance" score.