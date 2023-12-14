import re
import time
import logging

class TextProcessor:
    def __init__(self, file_path, n):
        self.file_path = file_path
        self.n = n

    def process_text(self)->list:
        """ 
        Main function to process text.
         Args:
                file_path (str): Path to the text file.
                n (int): n-gram
        Returns:
                list: List of cleaned tokens.
        """ 
        text = self.read_text_file()
        functions = [self.split_text_by_sentence,
                     self.replace_em_dashes, 
                     self.convert_to_lower_case,
                     self.tokenize_and_remove_special_characters,
                     self.add_sentence_markers, 
                     self.remove_empty_strings]
        
        for function in functions:
            start_time = time.time()
            logging.debug(f"Running function {function.__name__}")
            text = function(text)
            logging.info(f"Completed running function {function.__name__} in {time.time() - start_time} seconds")
        return text

    def read_text_file(self)->str:
        """
        Read text file.
        Args:
            file_path (str): Path to the text file.
        Returns:
            str: Text read from the file.
        """
        start_time = time.time()
        logging.debug(f"Reading file {self.file_path}")
        with open(self.file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        logging.info(f"Completed reading file in {time.time() - start_time} seconds")
        return text
    
    def split_text_by_sentence(self, text)->list:
        
        text = text.replace("\n", "")
        text = re.sub(r'\s+', ' ', text)  
        sentence_endings = r'[.?:]'
        # Split the text into sentences and add sentence markers
        sentences = re.split(sentence_endings, text)
        logging.info(f"Split text into {len(sentences)} sentences")
        return sentences
    
    def replace_em_dashes(self, sentences)->list:
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
    
    def convert_to_lower_case(self, sentences)->list:
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

    def tokenize_and_remove_special_characters(self, sentences)->list:
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
    
    def add_sentence_markers(self, sentences)->list:
        """
        Add sentence markers <s> and </s> at the beginning and end of each sentence.

        Args:
            text (str): Input text
            n (int) : n-gram
        Returns:
            str: Text with sentence markers added.
        """
        return [['<s>']*(self.n-1) + sentence + ['</s>']*(self.n-1) for sentence in sentences]
    
    def remove_empty_strings(self, sentences)->list:
        sentences = [[word for word in sentence if word] for sentence in sentences if any(sentence)]
        sentences = [sentence for sentence in sentences if len(sentence)>3]
        return sentences