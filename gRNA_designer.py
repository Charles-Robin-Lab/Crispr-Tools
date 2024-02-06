# Hodge podge of chatgpt code
# 

import argparse
import pandas as pd
import json
# Function to read and process the files
def process_files(chopchop_tsv_path, crisprdirect_json_paths, output_path):
    # Read the TSV files into pandas DataFrames
    df1 = pd.read_csv(chopchop_tsv_path, delimiter='\t')

    # Read JSON data from the file
    results_array = list()
    for file2_prepath in crisprdirect_json_paths:
        for file2_path in file2_prepath.split(", "):    
            with open(file2_path, 'r') as file:
                data = json.load(file)
            # Extract the array under the 'results' key
            results_array += data.get('results', [])


    # Convert the array to a pandas DataFrame
    df2 = pd.DataFrame(results_array)
    df2['sequence'] = df2.apply(lambda r : reverse_complement_if_backwards(r), axis=1)

    result_df = pd.merge(df1, df2, left_on='Target sequence', right_on='sequence', how='left')
    result_df = result_df.dropna(subset=['sequence'])
    result_df = result_df.drop('sequence', axis=1)
    result_df = result_df.drop('gc', axis=1)
    specific_df = result_df[(result_df['hit_20mer'].astype(int) <= 1) & (result_df['hit_12mer'].astype(int) <= 1)]
    specific_df = specific_df.drop('hit_12mer', axis=1)
    specific_df = specific_df.drop('hit_20mer', axis=1)
    specific_df = specific_df[['Rank','Target sequence','Efficiency','Genomic location','start','end','Strand','strand','MM0','MM1','MM2','MM3','hit_8mer','GC content (%)','Self-complementarity','resite','tm','tttt']]


    # Sort df1 based on efficiency (assuming there is a column named 'efficiency')
    df1_sorted = specific_df.sort_values(by='Efficiency', ascending=False)
    # Save the result to a new CSV file
    print(df1_sorted)
    df1_sorted.to_csv(output_path, sep=',', index=False)

def reverse_complement(dna_sequence):
    complement_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    reverse_comp_seq = ''.join(complement_dict[base] for base in reversed(dna_sequence))
    return reverse_comp_seq

def reverse_complement_if_backwards(row):
    if row['strand'] == '-':
        return reverse_complement(row['sequence'])
    else:
        return row['sequence']



if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', None)
    # pd.set_option('display.length', None)
    pd.set_option('display.max_rows', None)

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--chop', type=str, required=True)
    parser.add_argument('--crisprdirect', nargs='+', type=str, required=True)
    parser.add_argument('--out', type=str, required=True)
    args = parser.parse_args()

    process_files(args.chop, args.crisprdirect, args.out)



