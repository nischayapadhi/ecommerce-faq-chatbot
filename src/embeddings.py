import numpy as np
from gensim.models import KeyedVectors
import os

class EmbeddingEngine:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.vector_size = 0
        
    def load_model(self):
        """
        Loads the GloVe vectors using Gensim.
        This might take 1-2 minutes the first time.
        """
        print(f"Loading GloVe model from {self.model_path}...")
        
        # We need to convert the GloVe text format to a format Gensim likes
        # But Gensim has a handy function 'load_word2vec_format' that works for GloVe
        # providing we set no_header=True because standard GloVe txt files have no header.
        try:
            self.model = KeyedVectors.load_word2vec_format(
                self.model_path, 
                binary=False, 
                no_header=True
            )
            self.vector_size = self.model.vector_size
            print("Model loaded successfully!")
        except FileNotFoundError:
            print(f"Error: Model file not found at {self.model_path}")
            
    def get_sentence_vector(self, clean_tokens):
        """
        Calculates the average vector for a list of tokens.
        
        Args:
            clean_tokens (list): A list of strings e.g. ['track', 'order']
            
        Returns:
            np.array: A 1D numpy array representing the sentence vector.
        """
        if not self.model:
            raise ValueError("Model is not loaded. Call load_model() first.")
            
        if not clean_tokens:
            # Return a vector of zeros if the list is empty
            return np.zeros(self.vector_size)
        
        # 1. Get vectors for each word (if the word exists in our GloVe dictionary)
        word_vectors = []
        for word in clean_tokens:
            if word in self.model:
                word_vectors.append(self.model[word])
            else:
                # Optional: Log unknown words? For now, we just skip them.
                pass
        
        # 2. If no words were found in the dictionary, return zeros
        if not word_vectors:
            return np.zeros(self.vector_size)
        
        # 3. Calculate the Average (Mean) Vector
        # axis=0 means we average vertically (column by column)
        sentence_vector = np.mean(word_vectors, axis=0)
        
        return sentence_vector