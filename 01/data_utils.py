import re
import random
from collections import defaultdict
import string
import os

# Function to read the UTF-8 text from a file
def read_text_file(file_path):
    """
    Read UTF-8 text from a file.

    Args:
        file_path (str): Path to the text file.

    Returns:
        str: The text content read from the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def split_text_by_sentence(text):
    text = text.replace("\n", "")
    text = re.sub(r'\s+', ' ', text)  
    sentence_endings = r'[.?:]'
    # Split the text into sentences and add sentence markers
    sentences = re.split(sentence_endings, text)
    # trim sentences - whitespace    
    #sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    #print(sentences)
    #print(sentences)
    return sentences

# Function to add sentence markers to the text
def add_sentence_markers(sentences, n):
    """
    Add sentence markers <s> and </s> at the beginning and end of each sentence.

    Args:
        text (str): Input text
        n (int) : n-gram
    Returns:
        str: Text with sentence markers added.
    """
    return [['<s>']*(n-1) + sentence + ['</s>']*(n-1) for sentence in sentences]

 

# Function to replace em-dashes with spaces
def replace_em_dashes(sentences):
    """
    Replace em-dashes with spaces.

    Args:
        text (str): Input text.

    Returns:
        str: Text with em-dashes replaced wit spaces.
    """
    # Replace em-dashes with spaces
    cleaned_text = [sentence.replace('—', ' ') for sentence in sentences]
    return cleaned_text

# Function to convert text to lowe—'r case
def convert_to_lower_case(sentences):
    """
    Convert text to lower case.

    Args:
        text (str): Input text.

    Returns:
        str: Text in lower case.
    """
    # Convert the text to lower case
    lower_case_text = [sentence.lower() for sentence in sentences]
    return lower_case_text

# Function to tokenize and remove special characters
def tokenize_and_remove_special_characters(sentences):
    """
    Tokenize text and remove special characters (except hyphens and apostrophes between letters).

    Args:
        text (str): Input text.

    Returns:
        list: List of cleaned tokens.
    """
    # Define a regular expression pattern to split on whitespace and remove special characters
    token_pattern = r'[^A-Za-z0-9\'-]+'

    # Tokenize the text while preserving hyphens and apostrophes
    tokens = [re.split(token_pattern, sentence) for sentence in sentences]
    return tokens 

def remove_empty_strings(sentences):
    sentences = [[word for word in sentence if word] for sentence in sentences if any(sentence)]
    sentences = [sentence for sentence in sentences if len(sentence)>3]
    return sentences
# Main function to perform data cleanup
def data_cleanup(file_path, n):
    """
    Perform data cleanup on the text from the specified file.

    Args:
        file_path (str): Path to the text file.

    Returns:
        list: List of cleaned tokens.
    """
    # Read the text from the file
    text = read_text_file(file_path)

    text = split_text_by_sentence(text)
 
    # Replace em-dashes
    text = replace_em_dashes(text)

    # Convert to lower case
    text = convert_to_lower_case(text)

    # Tokenize and remove special characters
    cleaned_tokens = tokenize_and_remove_special_characters(text)
    # Add sentence markers
    #print(cleaned_tokens)
    cleaned_tokens = add_sentence_markers(cleaned_tokens, n)
     
    final_tokens = remove_empty_strings(cleaned_tokens) 
    return final_tokens#,#cleaned_tokens