# Custom tokenizer function
import re

from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer


def custom_tokenizer(text):
    tokens = re.findall(r'[A-Z][a-z]*|[a-z]+|[0-9]+|_', text)
    return tokens

# Read file names
with open('sliced_names_from_repo2.txt', 'r', encoding='utf-8') as f:
    names = [line.strip() for line in f]

# Split data into chunks
chunk_size = 500  # Adjust this size based on your needs
chunks = [names[i:i + chunk_size] for i in range(0, len(names), chunk_size)]

with open('elbow-points.txt', 'r') as file:
    elbow_points = [int(line.strip()) for line in file]


# Process each chunk
for idx, chunk in enumerate(chunks):
    # Create TF-IDF vectorizer with custom tokenizer
    vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer)
    X = vectorizer.fit_transform(chunk)

    # Assuming the optimal K is determined from the plot
    optimal_k = elbow_points[idx]  # Replace this with the elbow point determined from the plot
    kmeans = KMeans(n_clusters=optimal_k, random_state=42)
    kmeans.fit(X)

    # Reduce dimensions for visualization
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X.toarray())

    # Visualize the clusters with cluster centers
    plt.figure(figsize=(7, 6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=kmeans.labels_, cmap='viridis', marker='o', edgecolor='k', s=20)
    centers = kmeans.cluster_centers_
    centers_pca = pca.transform(centers)
    plt.scatter(centers_pca[:, 0], centers_pca[:, 1], c='red', marker='X', s=200, label='Centers')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.title(f'K-means Clustering - Chunk {idx + 1} (K={optimal_k})')
    plt.legend()
    plt.show()

    # Save clustered names to a file for each chunk
    with open('clustered_class_names.txt', 'a', encoding='utf-8') as file:
        for i, name in enumerate(chunk):
            file.write(f"{name}: Cluster {kmeans.labels_[i]}\n")