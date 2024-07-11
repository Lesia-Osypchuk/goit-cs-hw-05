import os
import threading
import time

def search_keywords_in_files(files, keywords):
    results = {}
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                for keyword in keywords:
                    if keyword in content:
                        if keyword not in results:
                            results[keyword] = []
                        results[keyword].append(file_path)
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
    return results

def process_files(files, keywords, num_threads):
    chunks = [[] for _ in range(num_threads)]
    for i, file_path in enumerate(files):
        chunks[i % num_threads].append(file_path)
    
    threads = []
    results_lock = threading.Lock()
    results = {}
    
    def process_chunk(chunk, results_lock):
        nonlocal results
        chunk_results = search_keywords_in_files(chunk, keywords)
        with results_lock:
            for keyword, file_list in chunk_results.items():
                if keyword not in results:
                    results[keyword] = []
                results[keyword].extend(file_list)
    
    start_time = time.time()
    
    for chunk in chunks:
        thread = threading.Thread(target=process_chunk, args=(chunk, results_lock))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time} seconds")
    
    return results

def main():
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt']
    keywords = ['keyword1', 'keyword2']
    num_threads = 2
    
    results = process_files(files, keywords, num_threads)
    
    for keyword, file_list in results.items():
        print(f"Keyword '{keyword}' found in files: {', '.join(file_list)}")

if __name__ == "__main__":
    main()
