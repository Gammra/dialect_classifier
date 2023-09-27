import data_processes

def main():
    data = data_processes.process_data()
    for col in data.columns:
        for n in range(1, 4):
            ngrams = data_processes.generate_uni_bi_tri(n, data[col])
            data_processes.generate_ngram_stats(ngrams, 100, col)

if __name__ == "__main__":
    main()
