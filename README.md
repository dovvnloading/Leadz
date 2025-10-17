<img width="838" height="415" alt="Leadz_Banner_001" src="https://github.com/user-attachments/assets/4486556c-e908-46bf-aaf8-38418e31c10b" />

# Leadz

[![Repo Status](https://img.shields.io/badge/repo%20status-active-brightgreen.svg)](https://github.com/dovvnloading/Leadz)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/Framework-PySide6-249e47.svg)](https://www.qt.io/qt-for-python)
[![AI Backend](https://img.shields.io/badge/AI_Backend-Ollama-lightgrey.svg)](https://ollama.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![GitHub stars](https://img.shields.io/github/stars/dovvnloading/Leadz?style=social)](https://github.com/dovvnloading/Leadz/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/dovvnloading/Leadz?style=social)](https://github.com/dovvnloading/Leadz/network/members)
[![GitHub issues](https://img.shields.io/github/issues/dovvnloading/Leadz)](https://github.com/dovvnloading/Leadz/issues)

Leadz is an intelligent, AI-powered desktop application designed to automate and enhance your job search. By leveraging local Large Language Models (LLMs) via Ollama, Leadz transforms a simple query into a curated list of relevant job opportunities, complete with summaries, key skills, and direct links to the listings.

<p align="center">
  <img width="900" height="750" alt="Leadz Application Screenshot" src="https://github.com/user-attachments/assets/779fb2a6-190f-4bde-a90c-bbd8f269025f">
</p>

## Key Features

-   **AI-Powered Search:** Generates intelligent, context-aware search queries from your input to find the best results.
-   **Autonomous Web Scraping:** Scans the web for job listings across multiple platforms and career pages.
-   **Content Analysis & Ranking:** Uses an embedding model and an LLM to rank pages for relevance and extract structured job data.
-   **Clean, Modern UI:** A sleek and intuitive interface built with PySide6, featuring both light and dark themes.
-   **Local & Private:** All AI processing is done locally via Ollama, ensuring your search data remains completely private.
-   **Structured Results:** Presents findings in easy-to-read job cards with essential details like title, company, location, skills, and summary.

## ⚙️ How It Works

Leadz follows a sophisticated multi-step process to find and deliver high-quality job leads:

1.  **Query Generation:** You enter a job description (e.g., "Senior Python Developer, Remote"). Leadz uses a local LLM to generate a set of diverse, high-quality search engine queries.
2.  **Web Search:** It performs a web search using the generated queries, prioritizing known job boards and career pages.
3.  **Content Scraping & Cleaning:** Relevant pages are scraped, and extraneous content (like headers, footers, and scripts) is stripped away, leaving only the core text.
4.  **Relevance Ranking:** The cleaned text from each page is compared against your original query using a sentence-transformer embedding model to calculate cosine similarity. The most relevant pages are prioritized.
5.  **Data Extraction:** The top-ranked pages are passed to the LLM, which analyzes the text to determine if it's a valid job posting and extracts key information (Job Title, Company, Skills, etc.) into a structured format.
6.  **Display:** The structured data is presented in the UI as interactive job cards.

## 🛠️ Tech Stack

| Component             | Technology                                                                                                   |
| --------------------- | ------------------------------------------------------------------------------------------------------------ |
| **GUI Framework**     | [PySide6](https://www.qt.io/qt-for-python) (Qt for Python)                                                     |
| **AI/LLM Backend**    | [Ollama](https://ollama.com/) (running a model like `qwen3:8b`)                                                |
| **Semantic Search**   | [Sentence Transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`)                                           |
| **Web Search**        | [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) (`ddgs`)                                      |
| **Web Scraping**      | [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), [Requests](https://docs.python-requests.org/en/latest/) |

## Getting Started

Follow these instructions to get Leadz running on your local machine.

### Prerequisites

-   Python 3.9+
-   [Ollama](https://ollama.com/) installed and running.
-   An Ollama model pulled for text generation (the default is `qwen3:8b`).

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/dovvnloading/Leadz.git
    cd Leadz
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    venv\Scripts\activate
    ```
    
    > **Note:** You will need to create a `requirements.txt` file by running:
    > `pip freeze > requirements.txt`
    > Then, you can install the dependencies in a new environment with `pip install -r requirements.txt`.


3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up Ollama:**
    -   Ensure the Ollama application or service is running in the background.
    -   Pull the required LLM model via your terminal:
        ```sh
        ollama pull qwen3:8b
        ```

5.  **Configure the application (optional):**
    -   Open `config.py`.
    -   You can change the `LLM_MODEL` and `EMBEDDING_MODEL` variables to match your preferred setup.

### Usage

Once the setup is complete, run the application with the following command:

```sh
python Leadz.py
```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more information.

> **Note:** Remember to create a `LICENSE` file in your repository containing the MIT License text.
