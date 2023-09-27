import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

with open("sw.txt") as f:
    STOPWORDS = f.read()
    STOPWORDS = STOPWORDS.split("\n")

def process_data():
    DO_sentences = load_sentences('corpora/DO/spa-do_web_2015_100K-sentences.txt')
    PE_sentences = load_sentences('corpora/PE/spa-pe_web_2016_100K-sentences.txt')
    CO_sentences = load_sentences('corpora/CO/spa-co_web_2014_100K-sentences.txt')
    MX_sentences = load_sentences('corpora/MX/spa-mx_web_2015_100K-sentences.txt')
    GT_sentences = load_sentences('corpora/GT/spa-gt_web_2014_100K-sentences.txt')

    print_data_stats(DO_sentences)
    print_data_stats(PE_sentences)
    print_data_stats(CO_sentences)
    print_data_stats(MX_sentences)
    print_data_stats(GT_sentences)

    full_dataframe = pd.DataFrame()
    full_dataframe['DO'] = DO_sentences['sentence'].copy()
    full_dataframe['PE'] = PE_sentences['sentence'].copy()
    full_dataframe['CO'] = CO_sentences['sentence'].copy()
    full_dataframe['MX'] = MX_sentences['sentence'].copy()
    full_dataframe['GT'] = GT_sentences['sentence'].copy()

    for col in full_dataframe.columns:
        df = full_dataframe[col].apply(lambda x: re.sub(r'[^\w\s]', '', x))
        df = df.apply(lambda x: x.lower())
        full_dataframe[col] = df

    print(full_dataframe)

    return full_dataframe

def load_sentences(filename):
    df = pd.read_table(filename, sep='\t', header=0)
    sentence_df = df.drop("number", axis='columns')
    return sentence_df

def print_data_stats(df):
    print('Shape = {}'.format(df.shape))
    print('Memory Usage = {:.2f} MB'.format(df.memory_usage().sum() / 1024 ** 2))
    print(df)

def generate_ngrams(text, n_gram=1):
    token = [token for token in text.lower().split(' ') if token != '' if token not in STOPWORDS]
    ngrams = zip(*[token[i:] for i in range(n_gram)])
    return [' '.join(ngram) for ngram in ngrams]

def generate_uni_bi_tri(n, sentences):
    ngrams = defaultdict(int)

    for sentence in sentences:
        for word in generate_ngrams(sentence, n):
            ngrams[word] += 1

    return pd.DataFrame(sorted(ngrams.items(), key=lambda x: x[1])[::-1])


def generate_ngram_stats(data, num_ngrams, country_name):
    fig, axes = plt.subplots(ncols=2, figsize=(18, 50), dpi=100)
    plt.tight_layout()

    sns.barplot(y=data[0].values[:num_ngrams], x=data[1].values[:num_ngrams], ax=axes[0], color='red')

    axes[0].spines['right'].set_visible(False)
    axes[0].set_xlabel('')
    axes[0].set_ylabel('')
    axes[0].tick_params(axis='x', labelsize=13)
    axes[0].tick_params(axis='y', labelsize=13)

    axes[0].set_title(f'Top {num_ngrams} most common unigrams in {country_name}', fontsize=15)


    plt.show()