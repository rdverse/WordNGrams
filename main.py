from data_utils import *
from ngrams import *

if __name__=="__main__":
    
    print("#"*100)
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(level=logging.INFO, 
                        filename='logs\logs.log',
                        filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    file_path = 'data/pg74.txt'  # Replace with the path to your text file
    print(f"Reading file : {file_path}") 
    
    
    for n in range(1, 7):
        for laplace in [True, False]:
            print("\n\nAdd-1 Smoothing enabled" if laplace else "\n\nNo Smoothing")        
            TextPreProcess = TextProcessor(file_path=file_path, n=n)
            cleaned_tokens = TextPreProcess.process_text()

            print(f"\nGenerating {n}-grams")
            generator = NGramTextGenerator(cleaned_tokens, 
                                               n, 
                                               laplace_smoothing=laplace)

            for sent_no in range(10):
                generated_text = generator.generate_sentence()
                print(f"Generating sentence {sent_no+1} of length {len(generated_text.split())} : {generated_text}") 
        print("#"*100)
        print("\n\n")