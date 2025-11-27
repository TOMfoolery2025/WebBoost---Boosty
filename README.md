# Django Website Analyzer

A powerful Python-based tool that analyzes websites (and Medium profiles) to provide actionable insights on Content, SEO, Visual Design, and Sentiment.

## Features

*   **Advanced Analysis**: Scores your blog (0-100) based on SEO, Content Quality, and Visual Design.
*   **Topic Detection**: Automatically detects if your blog is about **Food, Music, Travel, Sport, or Art**.
*   **Sentiment Engine**: Uses VADER (Valence Aware Dictionary and sEntiment Reasoner) to analyze the tone of your writing and suggest improvements.
*   **Medium Profile Support**: Enter a profile URL (e.g., `medium.com/@user`) and it automatically finds and analyzes the latest article.
*   **Benchmarking**: Compares your metrics against top-performing blogs in your category.
*   **Author & Socials**: Detects author names and social media links to help you grow your audience.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd django_backend
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: If `requirements.txt` is missing, install manually:*
    ```bash
    pip install django requests beautifulsoup4 textblob nltk
    ```

4.  **Download NLP Data**:
    ```bash
    python -m textblob.download_corpora
    python -m nltk.downloader vader_lexicon
    ```

## Usage

1.  **Start the server**:
    ```bash
    python manage.py runserver 8001
    ```

2.  **Open your browser**:
    Go to `http://127.0.0.1:8001`.

3.  **Analyze**:
    *   Enter a blog URL (e.g., `https://pinchofyum.com/`).
    *   OR enter a Medium profile (e.g., `https://medium.com/@username`).

## Project Structure

*   `analyzer_app/`: Main Django app.
    *   `logic.py`: Core analysis engine (Scraping, NLP, Scoring).
    *   `topic_trainer.py`: Script to train the topic classification model.
    *   `medium_trainer.py`: Script to generate general benchmarks.
    *   `views.py`: Handles web requests.
*   `website_analyzer/`: Django project settings.
*   `benchmarks.json`: Generated benchmark data.
*   `topic_models.json`: Generated topic profiles.

## Technologies

*   **Backend**: Django, Python
*   **NLP**: NLTK (VADER), TextBlob
*   **Scraping**: BeautifulSoup4, Requests
*   **Frontend**: Tailwind CSS
