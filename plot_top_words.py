import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import matplotlib.pyplot as plt
import requests


def fetch_text(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def map_function(text):
    words = re.findall(r'\b\w+\b', text.lower())  # Розділяємо текст на слова
    return [(word, 1) for word in words]


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(shuffled_values):
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced


def map_reduce(text):
    with ThreadPoolExecutor() as executor:
        # Крок 1: Мапінг
        mapped_values = list(executor.map(map_function, [text]))

        # Об'єднання всіх промаплених значень у один список
        combined_mapped_values = [item for sublist in mapped_values for item in sublist]

        # Крок 2: Shuffle
        shuffled_values = shuffle_function(combined_mapped_values)

        # Крок 3: Редукція
        reduced_values = reduce_function(shuffled_values)

    return reduced_values


def visualize_top_words(word_counts, top_n=10):
    top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]

    words, counts = zip(*top_words)

    plt.figure(figsize=(12, 8))
    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Counts')
    plt.title('Top Words by Frequency')
    plt.show()


if __name__ == '__main__':
    url = "https://www.gutenberg.org/files/2600/2600-0.txt"
    text = fetch_text(url)

    result = map_reduce(text)
    print("Результат підрахунку слів:", result)

    visualize_top_words(result)
