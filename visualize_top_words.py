import requests
import matplotlib.pyplot as plt
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import re

# Функція для завантаження тексту з URL
def fetch_text(url):
    response = requests.get(url)
    return response.text

# Функція для розбиття тексту на слова
def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

# Функція map для парадигми MapReduce
def map_func(chunk):
    counter = Counter(chunk)
    return counter

# Функція reduce для парадигми MapReduce
def reduce_func(counters):
    total_counter = Counter()
    for counter in counters:
        total_counter.update(counter)
    return total_counter

# Функція для візуалізації результатів
def visualize_top_words(word_counts, top_n=10):
    common_words = word_counts.most_common(top_n)
    words, counts = zip(*common_words)

    plt.figure(figsize=(10, 8))
    plt.bar(words, counts, color='blue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Words by Frequency')
    plt.show()

# Основна функція для обробки тексту за допомогою MapReduce
def mapreduce(text, num_workers=4):
    words = tokenize(text)
    chunk_size = len(words) // num_workers
    chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        mapped = list(executor.map(map_func, chunks))

    word_counts = reduce_func(mapped)
    return word_counts

def main():
    url = "http://www.gutenberg.org/files/11/11-0.txt"  #  Приклад URL з текстом "Alice's Adventures in Wonderland"
    text = fetch_text(url)
    word_counts = mapreduce(text)
    visualize_top_words(word_counts)

if __name__ == "__main__":
    main()
