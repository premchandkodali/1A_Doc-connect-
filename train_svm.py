from sentence_transformers import SentenceTransformer
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from joblib import dump
import pandas as pd

# 1. Load the labeled dataset
try:
    df = pd.read_csv("labeled_lines.csv")
except FileNotFoundError:
    print("Error: labeled_lines.csv not found.")
    print("Please run prepare_data.py first to generate the dataset.")
    exit()

# Filter out any rows with missing text
df.dropna(subset=['text'], inplace=True)
print("Loaded labeled dataset. Shape:", df.shape)
print("Label distribution:")
print(df['label'].value_counts())


# 2. Encode text into embeddings using MiniLM
print("\nLoading MiniLM model and encoding text...")
model = SentenceTransformer('all-MiniLM-L6-v2')
# Ensure all text is string type
texts = df['text'].astype(str).tolist()
embeddings = model.encode(texts, show_progress_bar=True)
print("Text encoding complete.")


# 3. Encode labels into numerical format
le = LabelEncoder()
labels = le.fit_transform(df['label'])


# 4. Train the SVM Classifier
print("\nTraining SVM classifier...")
# We use probability=True to get confidence scores later if needed
clf = SVC(kernel='linear', probability=True, class_weight='balanced')
clf.fit(embeddings, labels)
print("SVM training complete.")


# 5. Save the trained model and the label encoder
model_path = "svm_headings.joblib"
dump((clf, le), model_path)
print(f"\nClassifier and label encoder saved to {model_path}")
print("You can now use this model in your main.py script.") 