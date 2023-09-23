import pandas as pd
import re

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
    print(full_dataframe)

    clean_data(full_dataframe)
    print(full_dataframe)

def load_sentences(filename):
    df = pd.read_table(filename, sep='\t', header=0)
    sentence_df = df.drop("number", axis='columns')
    return sentence_df

def print_data_stats(df):
    print('Shape = {}'.format(df.shape))
    print('Memory Usage = {:.2f} MB'.format(df.memory_usage().sum() / 1024 ** 2))
    print(df)

def clean_data(df):
    for col in df.columns:
        df[col] = df[col].apply(lambda x: re.sub(r'[^\w\s]', '', x))
        df[col] = df[col].apply(lambda x: x.lower())