import os
import multiprocessing
import time

# Функція для пошуку ключових слів у файлі
def search_keywords_in_file(file_path, keywords):
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results.append(keyword)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    return (file_path, results)

# Функція для обробки файлів в процесі
def process_files(files, keywords, results_queue):
    for file_path in files:
        file_results = search_keywords_in_file(file_path, keywords)
        results_queue.put(file_results)

# Основна функція для розділення файлів між процесами та обробки
def process_files_multiprocessing(files, keywords, num_processes):
    # Розділити файли між процесами
    chunks = [[] for _ in range(num_processes)]
    for i, file_path in enumerate(files):
        chunks[i % num_processes].append(file_path)
    
    # Створення черги для зберігання результатів
    results_queue = multiprocessing.Queue()

    # Створення та запуск процесів для обробки файлів
    processes = []
    for chunk in chunks:
        process = multiprocessing.Process(target=process_files, args=(chunk, keywords, results_queue))
        processes.append(process)
        process.start()
    
    # Зачекати завершення усіх процесів
    for process in processes:
        process.join()
    
    # Збір результатів з черги
    results = {}
    while not results_queue.empty():
        file_path, found_keywords = results_queue.get()
        if file_path in results:
            results[file_path].extend(found_keywords)
        else:
            results[file_path] = found_keywords
    
    return results

def main():
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']  # Список файлів
    keywords = ['keyword1', 'keyword2']  # Пошукові ключові слова
    num_processes = 2  # Кількість процесів для обробки

    # Виконання обробки файлів з вимірюванням часу
    start_time = time.time()
    results = process_files_multiprocessing(files, keywords, num_processes)
    end_time = time.time()

    # Виведення результатів
    for file_path, found_keywords in results.items():
        print(f"Found keywords {found_keywords} in file {file_path}")

    print(f"Total execution time: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    main()
