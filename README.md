# 🛒 Intelligent E-Commerce FAQ Chatbot

A Natural Language Processing (NLP) chatbot capable of answering customer support queries using Semantic Search (GloVe Embeddings & Cosine Similarity).

## 🚀 Live Demo
[Link to your Streamlit App] (You will add this after deployment)

## 🛠️ Tech Stack
* **Python 3.8+**
* **Streamlit** (Frontend Interface)
* **NLTK** (Text Preprocessing & Tokenization)
* **Scikit-Learn** (Cosine Similarity Math)
* **GloVe Word Embeddings** (100d Vectors)

## 🧠 How It Works
1.  **Preprocessing:** User input is cleaned (lemmatized, stopwords removed) using NLTK.
2.  **Vectorization:** The query is converted into a 100-dimensional vector using pre-trained GloVe embeddings (averaging strategy).
3.  **Semantic Search:** The system calculates the Cosine Similarity between the user's vector and 400+ known question variations.
4.  **Confidence Check:** If the similarity score is below a threshold (0.35), the bot admits ignorance or suggests related topics.

## 📂 Project Structure
* `src/`: Core logic for preprocessing and vectorization.
* `data/`: Augmented dataset with "exploded" question variations.
* `notebooks`: Self checking the codes.
* `models/`: Stores the GloVe embedding model.
* `app.py`: Streamlit application entry point.

## 💿 Setup & Run
1.  Clone the repo.
2.  Install dependencies: `pip install -r requirements.txt`
3.  Run the app: `streamlit run app.py`