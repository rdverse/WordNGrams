from data_utils import *
import os
import re
from itertools import chain, tee, islice
class NGramTextGenerator:
    def __init__(self, cleaned_text, n, laplace_smoothing=True):
        """
        Initialize the NGramTextGenerator with the input text and n-gram size.

        Args:
            text (str): Input text.
            n (int): Size of the n-grams (e.g., 1 for unigrams, 2 for bigrams).
        """
        self.n = n
        self.text = cleaned_text#_preprocess_text(text)
        self.world, self.vocab = self.get_vocab(self.text)
        self.ngrams = self._build_ngrams()
        self.laplace_smoothing = laplace_smoothing
    # def _preprocess_text(self, text):
    #     # Data cleanup as per your instructions
    #     # text = text.replace("—", " ")  # Replace em-dashes with spaces
    #     # text = text.lower()  # Convert to lowercase
    #     # text = re.sub(r"[^a-z0-9\s'-]", "", text)  # Remove special characters
    #     cleaned_tokens = self.text#data_cleanup(self.file_path)
    #     #print(cleaned_tokens)
    #     return cleaned_tokens 

    # def _build_ngrams(self):
    #     from itertools import tee, islice
    #     ngrams = defaultdict(int)
    #     for sentence in self.text:
    #         # Add sentence start and end markers
    #         sentence = ['<s>'] * (self.n - 1) + sentence + ['</s>']
            
    #         # Create n iterators for the sentence
    #         sentence_iters = tee(sentence, self.n)
            
    #         # Offset each iterator by an increasing number
    #         for i in range(1, self.n):
    #             sentence_iters[i] = islice(sentence_iters[i], i, None)
            
    #         # Zip the iterators to get n-grams and count them
    #         for ngram in zip(*sentence_iters):
    #             ngrams[ngram] += 1

    #     return ngrams
    

    # def _build_ngrams(self):
    #     from collections import defaultdict
    #     from itertools import tee, islice
    #     ngrams = defaultdict(int)
    #     for sentence in self.text:
    #         # Add sentence start and end markers
    #         sentence = ['<s>'] * (self.n - 1) + sentence + ['</s>']
            
    #         # Create n iterators for the sentence and convert them to a list
    #         sentence_iters = list(tee(sentence, self.n))
            
    #         # Offset each iterator by an increasing number
    #         for i in range(1, self.n):
    #             sentence_iters[i] = islice(sentence_iters[i], i, None)
            
    #         # Zip the iterators to get n-grams and count them
    #         for ngram in zip(*sentence_iters):
    #             ngrams[ngram] += 1
    #     print(ngrams)
    #     return ngrams
    
    def _build_ngrams(self):
        # adapted from https://github.com/nltk/nltk/blob/develop/nltk/util.py
        ngrams = defaultdict(lambda: defaultdict(int))
        for sentence in self.text:
            # Add sentence start and end markers
            sentence = ['<s>'] * (self.n - 1) + sentence + ['</s>']
            
            # Create n iterators for the sentence and convert them to a list
            sentence_iters = list(tee(sentence, self.n))
            
            # Offset each iterator by an increasing number
            for i in range(1, self.n):
                sentence_iters[i] = islice(sentence_iters[i], i, None)
            
            # Zip the iterators to get n-grams and count them
            for ngram in zip(*sentence_iters):
                context, target = tuple(ngram[:-1]), ngram[-1]
                ngrams[context][target] += 1
        # too slow        
        # if laplace_smoothing:
        #     # Add 1 to all n-gram counts
        #     import tqdm
        #     for context in tqdm.tqdm(ngrams):
        #         for token in self.vocab:
        #             ngrams[context][token] += 1
                    
        #print(ngrams)
        return ngrams

    # def _build_ngrams(self):
    #     ngrams = defaultdict(int)
    #     #print(self.text)
    #     #words = self.text.split()
    #     sentences = self.text
    #     # for i in range(len(words) - self.n + 1):
    #     #     print(words[i:i + self.n])
    #     #     ngram = tuple(words[i:i + self.n])
    #     #     ngrams[ngram[:-1]].append(ngram[-1])
    #     #vocab = []
    #     from itertools import tee
    #     for sentence in sentences:
    #         sentence = tee(sentence,self.n)
    #         for i, sentence_iter in enumerate(sentence):
    #             for _ in range(i):
    #                 next(sentence_iter, None)
    #             #print(sentence)
    #                 print(sentence_iter)
                    
    #             print(list(zip(*sentence)))
    #     #print(sentences)
    #             #ngrams[word] += 1
    #     #print(ngrams)
    #     return ngrams

    def get_nested_value(data, key_path):
        """
        Extracts a value from a nested dictionary given a list of keys.
        
        :param data: The nested dictionary to search.
        :param key_path: A list of keys representing the path to the desired value.
        :return: The extracted value, or None if the path is invalid.
        """
        try:
            for key in key_path:
                data = data[key]
            return data
        except KeyError:
            return None
        
    def get_vocab(self,world):
        world = list(chain.from_iterable(world))
        vocab = set(world)
        return world,vocab
        
    def generate_sentence(self, max_length=15):
        """
        Generate a random sentence based on raw n-gram counts.

        Args:
            max_length (int): Maximum length of the generated sentence.

        Returns:
            str: Generated sentence.
        """
        
        context = ["<s>"]*(self.n-1)
        sentence = context 
        #print(sentence)
        while sentence[-1] != "</s>" and len(sentence) < max_length:
            #if n!==1:
                #world = self.ngrams.get(tuple(sentence[-self.n + 1:]), [])
             #   world = self.ngrams.items()
            #word_frequency = list(chain.from_iterable([[key]*value for key, value in world]))
            if self.n==1:
                word_choice = random.choices(list(self.ngrams.keys()),
                                            weights=list(self.ngrams.values()),
                                            k=1)
            
                next_word = word_choice[0]
            else:
                
                context = tuple(sentence[-self.n + 1:])
                # get all the possible words in n-gram given the context
                print(sentence)
                if self.laplace_smoothing:
                    #Implement lazy loading to speed up the process
                    potential_dict = {word:self.ngrams[context].get(word, 0)+1 for word in self.vocab}
                    next_word = random.choices(list(potential_dict.keys()), weights=potential_dict.values(), k=1)[0]
                    potential_words = self.vocab
                else:    
                    potential_words = self.ngrams.get(context, [])
                    # sort them based on frequency
                    #print(potential_words)
                    #sorted_words = sorted(potential_words, key= potential_words.get, reverse=True)
                    #print(sorted_words)
                    # select next word and context word  
                    #next_word = random.choices(sorted_words.keys(), weights=[self.ngrams[(tuple(sentence[-self.n + 1:]), x)] for x in sorted_words[:10]], k=1)[0]
                    next_word = random.choices(list(potential_words.keys()), weights=list(potential_words.values()) ,k=1)[0]

            sentence.append(next_word) 
            #print(choice)
            #words_choice = [word for word, count in self.ngrams.items() if count == choice[0]]
            #choice = random.sample(list(self.ngrams.keys()))
            #next_word = random.sample(words_choice, 1)
                        # current_ngram = tuple(sentence[-self.n + 1:])
            # #print(current_ngram)
            # #print(current_ngram)
            # next_word_options = self.ngrams.get(current_ngram, [])
            # if next_word_options:
            #     next_word = random.choice(next_word_options)
            #     sentence.append(next_word)
            # else:
            #     break
        #print(sentence)
        #sentence = " ".join(sentence)
        #print(sentence)
        clean_sentence = " ".join(sentence)
        clean_sentence = re.sub("<s> ","",clean_sentence)
        clean_sentence = re.sub("<s>","",clean_sentence)
        clean_sentence = re.sub("</s>","",clean_sentence)
        #print(clean_sentence)
        return clean_sentence # Exclude <s> and </s>

def generate_text_with_ngrams(text, n):
    """
    Generate text using n-grams.

    Args:
        text (str): Input text.
        n (int): Size of the n-grams (e.g., 1 for unigrams, 2 for bigrams).

    Returns:
        str: Generated text.
    """
    generator = NGramTextGenerator(text, n)
    generated_text = generator.generate_sentence()
    print(generated_text)
    return generated_text

# def main_generate(input_text):
#     # Task 1: Random sentence generation with raw n-gram counts
#     random_sentence = generate_text_with_ngrams(input_text, 1)  # Unigram
#     print("Random Sentence (Unigram):")
    
    #print(random_sentence)

    # Task 2: Generate text with n-grams up to n = 6
    # for n in range(1):
    #     generated_text = generate_text_with_ngrams(input_text, n)
    #     print(f"\nGenerated Text (n={n}):")
    #     print(generated_text)
    # Task 3: Repeat step 2 using add-1 smoothing (not implemented here)
    # Task 4: Write up your findings (not implemented here)