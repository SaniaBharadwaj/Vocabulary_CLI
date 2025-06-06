# Practice_with python

# Word Meaning Fetcher

A simple command-line tool to fetch and store word meanings from a public dictionary API. Enter any sentence, and the script highlights a word and shows its meaning. If a word's meaning is not already stored, it's fetched from the web and saved locally for future use.

## 🌟 Features

- Highlights a random or known word in your sentence
- Fetches up to 3 meanings for each word
- Stores results in `data.json` to avoid redundant API calls
- Recovers from corrupted JSON files automatically
- Works offline after enough data is gathered

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Internet connection for first-time word fetches

### Installation

```bash
git clone https://github.com/SaniaBharadwaj/Vocabulary_CLI.git
cd Vocabulary_CLI
pip install -r requirements.txt
