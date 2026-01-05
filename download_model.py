import os
import urllib.request
import zipfile
import shutil

def check_and_download_model():
    """
    Checks if GloVe embeddings exist. If not, downloads and extracts them.
    Returns True if successful.
    """
    # Define paths relative to this script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR = os.path.join(BASE_DIR, "models", "glove")
    ZIP_PATH = os.path.join(MODEL_DIR, "glove.6B.zip")
    TXT_PATH = os.path.join(MODEL_DIR, "glove.6B.100d.txt")

    # 1. Check if the specific model file exists
    if os.path.exists(TXT_PATH):
        print("✅ GloVe model found.")
        return

    # 2. Create directory if missing
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    # 3. Download
    print("⚠️ Model missing. Downloading GloVe (822MB)... This will take time.")
    url = "https://nlp.stanford.edu/data/glove.6B.zip"
    
    # Progress hook (optional, keeps logs alive)
    def progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if downloaded % (10 * 1024 * 1024) == 0: # Print every 10MB
            print(f"Downloaded: {downloaded / (1024*1024):.0f} MB")

    try:
        urllib.request.urlretrieve(url, ZIP_PATH, progress)
        print("Download complete. Unzipping...")
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return

    # 4. Unzip
    try:
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            # Only extract the file we need to save space/time
            zip_ref.extract("glove.6B.100d.txt", MODEL_DIR)
        print("Unzip complete.")
        
        # 5. Cleanup (Delete the zip and other sizes if extracted)
        os.remove(ZIP_PATH)
        print("Cleanup complete. Model ready!")
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")

if __name__ == "__main__":
    check_and_download_model()