from data_utils import *
import os
 
class NGramTextGenerator:
    def __init__(self, file_path, text, n):
        """
        Initialize the NGramTextGenerator with the input text and n-gram size.

        Args:
            text (str): Input text.
            n (int): Size of the n-grams (e.g., 1 for unigrams, 2 for bigrams).
        """
        self.file_path = file_path
        self.n = n
        self.text = self._preprocess_text(text)
        self.ngrams = self._build_ngrams()

    def _preprocess_text(self, text):
        # Data cleanup as per your instructions
        # text = text.replace("—", " ")  # Replace em-dashes with spaces
        # text = text.lower()  # Convert to lowercase
        # text = re.sub(r"[^a-z0-9\s'-]", "", text)  # Remove special characters
        cleaned_tokens = data_cleanup(self.file_path)
        #print(cleaned_tokens)
        return cleaned_tokens 

    def _build_ngrams(self):
        # source : https://github.com/nltk/nltk/blob/develop/nltk/util.py
        ngrams = defaultdict(int)
        #print(self.text)
        #words = self.text.split()
        sentences = self.text
        # for i in range(len(words) - self.n + 1):
        #     print(words[i:i + self.n])
        #     ngram = tuple(words[i:i + self.n])
        #     ngrams[ngram[:-1]].append(ngram[-1])
        for sentence in sentences:
            for word in sentence:
                ngrams[word] += 1
        #print(ngrams)
        return ngrams

    def generate_sentence(self, max_length=10000):
        """
        Generate a random sentence based on raw n-gram counts.

        Args:
            max_length (int): Maximum length of the generated sentence.

        Returns:
            str: Generated sentence.
        """
        sentence = ["<s>"]
        #print(sentence)
        while sentence[-1] != "</s>" and len(sentence) < max_length:
            choice = random.sample(list(self.ngrams.values()),1)   
            words_choice = [word for word, count in self.ngrams.items() if count == choice[0]]
            next_word = random.sample(words_choice, 1)
            sentence.append(next_word[0])
            # current_ngram = tuple(sentence[-self.n + 1:])
            # #print(current_ngram)
            # #print(current_ngram)
            # next_word_options = self.ngrams.get(current_ngram, [])
            # if next_word_options:
            #     next_word = random.choice(next_word_options)
            #     sentence.append(next_word)
            # else:
            #     break
        print(len(sentence))
        #sentence = " ".join(sentence)
        #print(sentence)
        return sentence # Exclude <s> and </s>

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
