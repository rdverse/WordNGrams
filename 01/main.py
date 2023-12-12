from data_utils import *
from ngrams import *

if __name__=="__main__":
    file_path = 'pg74.txt'  # Replace with the path to your text file
    cleaned_tokens = data_cleanup(file_path)
    #print(cleaned_tokens)
    corpus = []
    for tokens in cleaned_tokens:
        corpus.extend(tokens)    
    n=1
    generator = NGramTextGenerator(file_path,cleaned_tokens, n)
    generated_text = generator.generate_sentence()