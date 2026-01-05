import os
import sys

# Setup paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from embeddings import EmbeddingEngine
from chatbot import SimpleChatbot

def main():
    # 1. Configuration
    DATA_PATH = 'data/raw/Ecommerce_FAQ_Chatbot_dataset_augmented.json'
    GLOVE_PATH = 'models/glove/glove.6B.100d.txt'
    
    # 2. Initialize Engine
    print("--- Initializing E-Commerce Chatbot ---")
    embedding_engine = EmbeddingEngine(GLOVE_PATH)
    embedding_engine.load_model()
    
    # 3. Initialize Chatbot (This loads the DB)
    bot = SimpleChatbot(DATA_PATH, embedding_engine)
     
    print("\n" + "="*50)
    print("Chatbot is Ready! Type 'exit' to quit.")
    print("="*50)
    
    # 4. The Chat Loop
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Bot: Goodbye! Happy Shopping!")
                break
            
            response = bot.get_response(user_input)
            
            print(f"Bot: {response['answer']}")
            
            # Optional: Print debug info to see how confident the bot is
            print(f"    (Debug: Matched '{response.get('matched_question')}' with score {response['score']:.2f})")
            
        except KeyboardInterrupt:
            print("\nBot: Exiting...")
            break

if __name__ == "__main__":
    main()