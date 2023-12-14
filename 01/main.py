from data_utils import *
from ngrams import *

if __name__=="__main__":
    file_path = 'pg74.txt'  # Replace with the path to your text file
    n=2
    cleaned_tokens = data_cleanup(file_path, n)
    #print(cleaned_tokens)
    corpus = []
    for tokens in cleaned_tokens:
        corpus.extend(tokens)    
    generator = NGramTextGenerator(cleaned_tokens, n)
    generated_text = generator.generate_sentence()
    print(generated_text)