import re
from collections import Counter

# Custom tokenizer function
def custom_tokenizer(text):
    tokens = re.findall(r'[A-Z][a-z]*|[a-z]+|[0-9]+|_', text)
    return tokens

# Read file names
with open('sliced_names_from_repo2.txt', 'r', encoding='utf-8') as f:
    names = [line.strip() for line in f]

# Tokenize names
all_tokens = []
for name in names:
    tokens = custom_tokenizer(name)
    all_tokens.extend(tokens)

# Count word frequencies
word_counts = Counter(all_tokens)

# Sort by frequency
sorted_word_counts = word_counts.most_common()

# Save to a file
with open('word_popularity_ranking2.txt', 'w', encoding='utf-8') as file:
    for word, count in sorted_word_counts:
        file.write(f"{word}: {count}\n")

print(f"Word popularity ranking saved to word_popularity_ranking.txt")
