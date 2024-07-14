import requests
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import matplotlib.pyplot as plt


def get_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    except requests.RequestException:
        raise Exception(f'Error downloading file {url}')


def map_func(word):
    return word, 1


def shuffle(values):
    res = defaultdict(list)

    for key, value in values:
        res[key].append(value)

    return res.items()


def reduce_func(values):
    key, value = values
    return key, len(value)


def map_reduce(text):
    words = text.split()

    with ThreadPoolExecutor() as executor:
        mapped_words = list(executor.map(map_func, words))

    shuffled_values = shuffle(mapped_words)

    with ThreadPoolExecutor() as executor:
        reduced_values = executor.map(reduce_func, shuffled_values)

    return dict(reduced_values)


def visualize_top_words(top_words):
    names = []
    values = []

    for key, value in top_words:
        names.append(key)
        values.append(value)

    ax = plt.subplot()
    plt.figure(figsize=(9, 4))
    plt.barh(names, values)

    for i in range(len(values)):
        plt.text(values[i] // 2, names[i], values[i], va='center', color='white')

    plt.xlabel('Frequency')
    plt.ylabel('Word')
    plt.title('Top 10 most frequent words')
    plt.show()


if __name__ == "__main__":
    url = 'https://www.gutenberg.org/ebooks/1965.txt.utf-81'
    try:
        text = get_file(url)
        result = map_reduce(text)

        sort = sorted(result.items(), key=lambda x: x[1])

        visualize_top_words(sort[-10:])
    except Exception as e:
        print(e)
        print('Exit with error')
