import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Custom tokenizer function
def custom_tokenizer(text):
    tokens = re.findall(r'[A-Z][a-z]*|[a-z]+|[0-9]+|_', text)
    return tokens

# Read file names
with open('sliced_names_from_repo2.txt', 'r', encoding='utf-8') as f:
    names = [line.strip() for line in f]

# Split data into chunks
chunk_size = 500  # Adjust this size based on your needs
chunks = [names[i:i + chunk_size] for i in range(0, len(names), chunk_size)]


# Process each chunk
for idx, chunk in enumerate(chunks):
    # Create TF-IDF vectorizer with custom tokenizer
    vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer)
    X = vectorizer.fit_transform(chunk)

    # Determine the optimal number of clusters using the Elbow method
    sse = []
    k_range = range(2, 20)
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        sse.append(kmeans.inertia_)

    # Plot SSE for the Elbow method
    plt.figure(figsize=(7, 6))
    plt.plot(k_range, sse, 'bo-')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Sum of Squared Errors (SSE)')
    plt.title(f'Elbow Method for Optimal K - Chunk {idx + 1}')
    plt.show()



print("Clustering and visualization done for all chunks.")
