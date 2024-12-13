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
```

# WordLlama FAQ System Setup Guide

This guide provides step-by-step instructions for setting up the WordLlama FAQ System, including installing dependencies, placing model files, and using the system effectively.

## 1. Install Dependencies

To begin, create a virtual environment and install the required Python packages. You can do this by running the following command in your terminal:

```pip install -r requirements.txt```

Ensure that you have the necessary WordLlama model and configuration files located in the `wordlama_models` directory.

## 2. Place Your Model Files

You need to have the following files in the `wordlama_models` directory for WordLlama to function properly:

- **l2_supercat_256.safetensors**: This is the weights file.
- **l2_supercat_tokenizer_config.json**: This file contains the configuration settings.

Make sure these files are correctly placed to allow WordLlama to load the model without issues.

## 3. Usage

### Initialize the FAQ System

To initialize the FAQ system, you will need to load a WordLlama model and provide paths to your model weights and configuration files when creating the `FAQSystem` object.

### Search for FAQs

You can search for FAQs using the `search_faqs` method. Here’s an example of how to implement this:

```python
queries = "password reset"
results = faq_system.search_faqs(queries)
```

### Output
The search results will be returned as a list of dictionaries containing the question, answer, and similarity score. An example output might look like this:
```json
[
  {
    "question": "How do I reset my password?",
    "answer": "You can reset your password by clicking 'Forgot Password' on the login page.",
    "similarity_score": 0.95
  }
] ```

