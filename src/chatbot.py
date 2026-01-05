import json
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import clean_text

class SimpleChatbot:
    def __init__(self, data_path, embedding_engine):
        self.data_path = data_path
        self.engine = embedding_engine
        self.df = None
        self.question_matrix = None 
        
        # Load and process data immediately upon initialization
        self._load_and_vectorize()
        
    def _load_and_vectorize(self):
        """
        Loads JSON, expands variations into a flat list, cleans text, 
        and pre-calculates vectors for every variation.
        """
        print(f"Loading FAQ database from {self.data_path}...")
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find data file at {self.data_path}. Did you run generate_variations.py?")

        # --- KEY UPGRADE: Flatten the Data ---
        # We transform the nested JSON into a long list of (question_text, answer_text) pairs.
        # This allows the bot to search "variations" exactly like "main questions".
        expanded_data = []
        
        for entry in data['questions']:
            # 1. Add the main question
            expanded_data.append({
                'search_key': entry['question'],  # The text we will vectorise
                'answer': entry['answer'],        # The answer we return
                'original_question': entry['question'], # For debugging
                'type': 'main'
            })
            
            # 2. Add variations (if they exist in the augmented file)
            if 'variations' in entry:
                for variation in entry['variations']:
                    expanded_data.append({
                        'search_key': variation,
                        'answer': entry['answer'],
                        'original_question': entry['question'],
                        'type': 'variation'
                    })
        
        # Create DataFrame from the expanded list
        self.df = pd.DataFrame(expanded_data)
        
        # DEBUG PRINT: Verify we loaded the augmented data
        print(f"DEBUG: Successfully loaded {len(self.df)} search keys (Questions + Variations).")
        
        # 1. Clean the Search Keys
        print("Preprocessing and Vectorizing database...")
        self.df['clean_tokens'] = self.df['search_key'].apply(clean_text)
        
        # 2. Vectorize the Questions
        vectors = self.df['clean_tokens'].apply(self.engine.get_sentence_vector).tolist()
        
        # 3. Store as a Matrix
        self.question_matrix = np.array(vectors)
        print(f"Database ready! Matrix Shape: {self.question_matrix.shape}")

    def get_response(self, user_query, threshold=0.3):
        """
        The main search function.
        """
        # 1. Process User Query
        user_tokens = clean_text(user_query)
        
        # Handle empty/garbage input
        if not user_tokens:
            return {"answer": "I didn't catch that. Could you rephrase?", "score": 0.0, "matched_question": "None"}
            
        user_vector = self.engine.get_sentence_vector(user_tokens)
        
        # 2. Reshape user vector for sklearn (1D -> 2D)
        user_vector = user_vector.reshape(1, -1)
        
        # 3. Calculate Cosine Similarity against ALL variations
        similarities = cosine_similarity(user_vector, self.question_matrix)
        
        # 4. Find the Best Match
        best_index = np.argmax(similarities) # Index of the highest score
        best_score = similarities[0][best_index] # The actual score value
        
        # 5. Return Answer
        # We return the answer associated with the best matching variation
        matched_row = self.df.iloc[best_index]
        
        if best_score < threshold:
            return {
                "answer": "I'm sorry, I don't have information on that topic.",
                "score": float(best_score),
                "matched_question": None
            }
        
        return {
            "answer": matched_row['answer'],
            "score": float(best_score),
            "matched_question": matched_row['search_key'] # Show exactly which variation matched
        }