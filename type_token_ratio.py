import os
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import re
import math
import random

# Download the 'punkt' resource
nltk.download('punkt')


def calculate_sampled_ttr(text, sample_size=1000, case_sensitive=False):
    if not case_sensitive:
        text = text.lower()
    tokens = word_tokenize(text)

    # Ensure that the sample size does not exceed the total number of tokens
    sample_size = min(sample_size, len(tokens))

    # Randomly sample tokens
    sampled_tokens = random.sample(tokens, sample_size)

    num_types = len(set(sampled_tokens))
    sampled_ttr = num_types / sample_size
    return sampled_ttr


def calculate_normalized_ttr(text, case_sensitive=False):
    if not case_sensitive:
        text = text.lower()
    tokens = word_tokenize(text)
    total_tokens = len(tokens)
    freq_dist = FreqDist(tokens)
    num_types = len(freq_dist)
    normalized_ttr = num_types / math.sqrt(total_tokens)
    return normalized_ttr


def clean_text(text):
    # Use regular expression to remove specific opening and closing tags
    cleaned_text = re.sub(r'<\/?sentence[^>]*>', '', text)
    return cleaned_text


def process_directory(directory_path):
    data = []  # List to store data for each file

    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  # Adjust the file extension as needed
            print(filename)
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                cleaned_text = clean_text(text)
                ttr = calculate_normalized_ttr(cleaned_text)  # You can change this to calculate_ttr if needed
                normalized_ttr = calculate_normalized_ttr(cleaned_text, case_sensitive=True)
                sampled_ttr = calculate_sampled_ttr(cleaned_text, case_sensitive=True)
                data.append({'Filename': filename, 'TTR': ttr, 'Normalized_TTR': normalized_ttr, "Sampled_TTR" : sampled_ttr})

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file (xlsx)
    output_xlsx_path = os.path.join(directory_path, 'ttr_results.xlsx')
    df.to_excel(output_xlsx_path, index=False)
    print(f"Results saved to {output_xlsx_path}")


# Get the directory of the script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Go down one step and into the 'corpus' subdirectory
corpus_dir = os.path.join(script_dir, 'corpus')

# Example usage:
if __name__ == "__main__":
    process_directory(corpus_dir)
