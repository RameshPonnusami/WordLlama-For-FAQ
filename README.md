# FAQ System with WordLlama Integration

This project implements an FAQ system that uses **WordLlama** to provide semantic similarity-based search capabilities. The script loads a WordLlama model, stores sample FAQ data in an SQLite database, and allows users to search for the most relevant FAQs based on a query. The results are ranked by their similarity score to the query.

## Features

- **WordLlama-based Search**: The script uses WordLlama for semantic similarity to find the most relevant FAQs.
- **SQLite Database**: FAQ data is stored in a local SQLite database.
- **Model Loading with Diagnostics**: Includes detailed diagnostics when loading the WordLlama model to ensure proper configuration and file paths.
- **Sample FAQ Data**: Automatically loads sample FAQ data into the SQLite database.
- **Search Functionality**: Allows querying the FAQ system and returns top matching FAQs based on semantic similarity.

## Requirements

- >=Python 3.8
- `wordllama` package (make sure it's installed)
- SQLite (which is part of the Python standard library)
- JSON configuration files for WordLlama model

## Installation

### 1. Clone the Repository
Clone this repository to your local machine using:

```bash
git clone <repository_url>
cd <repository_directory>
