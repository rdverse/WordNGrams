import re
import os
import time
import random
import logging
from collections import defaultdict
from itertools import chain, tee, islice

class NGramTextGenerator:
    def __init__(self, cleaned_text="", n=1, laplace_smoothing=True):
        """
        Initialize the NGramTextGenerator with the input text and n-gram size.

        Args:
            text (str): Input text.
            n (int): Size of the n-grams (e.g., 1 for unigrams, 2 for bigrams, tested upto 6grams).
            laplace_smoothing (bool): Whether or not to use Laplace smoothing.
        """
        assert cleaned_text != "", "Input text must be provided."
        assert n > 0, "n must be a positive integer."
        if n>6:
            logging.warning("n>6 is not tested.")
        
        logging.info(f"Initializing NGramTextGenerator with {n}-grams and Laplace smoothing: {laplace_smoothing}")
        
        self.n = n
        self.text = cleaned_text#_preprocess_text(text)
        self.world, self.vocab = self.get_vocab(self.text)
        self.laplace_smoothing = laplace_smoothing
        self.cache_path = f"cache/{n}gram{'_laplace' if laplace_smoothing else ''}.pkl"
        self.ngrams = self._build_ngrams() 

        # if os.path.exists(self.cache_path):
        #     logging.info(f"Loading {n}-gram counts from {self.cache_path}")
        #     self.ngrams = pickle.load(open(self.cache_path, "rb"))
        # else:
        #     self.ngrams = self._build_ngrams() 
        #     logging.info(f"Saving {n}-gram counts to {self.cache_path}")
        #     pickle.dump(self.ngrams, open(self.cache_path, "wb"))   
        
    
    def _build_ngrams(self):
        """
        Build n-grams from the text.
        
        Args:
            text (str): Input text.
            n (int): Size of the n-grams (e.g., 1 for unigrams, 2 for bigrams).
            laplace_smoothing (bool): Whether or not to use Laplace smoothing.
        Returns:
            dict: Dictionary of n-grams and their counts.
        """
    
        start_time = time.time()
        if self.n==1:
            ngrams = defaultdict(int)
            sentences = self.text
            for sentence in sentences:
                for word in sentence:
                    ngrams[word] += 1
        else: 
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
            
        logging.info(f"Built {self.n}-grams in {time.time() - start_time:.2f} seconds.")
        return ngrams


    def get_vocab(self,world):
        start_time = time.time()
        world = list(chain.from_iterable(world))
        vocab = set(world)
        logging.info(f"Built vocab in {time.time() - start_time:.2f} seconds.")
        return world,vocab
        
    def generate_sentence(self, max_length=15):
        """
        Generate a random sentence based on raw n-gram counts.

        Args:
            max_length (int): Maximum length of the generated sentence.

        Returns:
            str: Generated sentence.
        """
        start_time = time.time()
        if self.n==1:
            context = []
            sentence = ["<s>"]
        else:
            context = ["<s>"]*(self.n-1)
            sentence = context 
        
        while sentence[-1] != "</s>" and len(sentence) < max_length:
            logging.debug(f"sentence = {sentence}")
            if self.n==1:
                word_choice = random.choices(list(self.ngrams.keys()),
                                            weights=list(self.ngrams.values()),
                                            k=1)
            
                next_word = word_choice[0]
            else:
                
                context = tuple(sentence[-self.n + 1:])
                # get all the possible words in n-gram given the context
                if self.laplace_smoothing:
                    #Implement lazy loading to speed up the process
                    potential_dict = {word:self.ngrams[context].get(word, 0)+1 for word in self.vocab}
                    next_word = random.choices(list(potential_dict.keys()), weights=potential_dict.values(), k=1)[0]
                    potential_words = self.vocab
                else:    
                    potential_words = self.ngrams.get(context, [])
                    next_word = random.choices(list(potential_words.keys()), weights=list(potential_words.values()) ,k=1)[0]

            sentence.append(next_word) 
            
        def cleaned_sentence(sentence)->str: 
            clean_sentence = " ".join(sentence)
            clean_sentence = re.sub("<s> ","",clean_sentence)
            clean_sentence = re.sub("<s>","",clean_sentence)
            clean_sentence = re.sub("</s>","",clean_sentence)
            return clean_sentence
        
        logging.debug("Time taken to generate sentence: {:.2f} seconds.".format(time.time() - start_time))
        return cleaned_sentence(sentence) # Exclude <s> and </s>



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