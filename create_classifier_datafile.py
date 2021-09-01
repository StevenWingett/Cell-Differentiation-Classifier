# Python script to generate a datafile that can
# subsequently be used by the cell classifier
# returns the collated results

import argparse
import sys
import re
import pandas as pd
import numpy as np

help_text = '''Python script to collate Kallisto results files.
Takes Kallisto output (TSV files) as input and
returns the collated results'''
parser = argparse.ArgumentParser(description=help_text)

parser.add_argument("-m", "--metadata", action="store", type=str, 
                    default='dataset_summary.tsv',
                    help="specify the metadata file \n[default: [dataset_summary.tsv]",
                    metavar='')
args = parser.parse_known_args()    #Use parse_known_arg to differentiate between arguments pre-specified and those that are not


#options = args[0]   # Get the 2 arrays of known/unknown arguments from the tuple
files = args[1]
outfile_collated = 'collated_kallisto.tsv'
outfile_processed = 'classifier_input.tsv.gz'

# Checks
if(len(files) == 0):
    print("Please specify input Kallisto files.")
    sys.exit()



#Make sure no input file named collated_kallisto.tsv
for file in files:
    if(file == outfile_collated):
        print("Input files cannot be named " + outfile_collated)
        sys.exit()
    elif(file == outfile_processed):
        print("Input files cannot be named " + outfile_processed)
        sys.exit()


# Read in metadata using Pandas
# Do this before processing kallisto files in case of problems at this
# stage
metadata_file = args[0].metadata
print("Reading in " + metadata_file)
df_meta = pd.read_csv(metadata_file, sep='\t')


#Collate all Kallisto files
include_header = True

with open(outfile_collated, 'w') as out_collated:

    for file in files:
        accession = (re.split('\s|_|\.', file))[0]
        try:
            with open(file, 'r') as f:
                print(f'Processing {file}')
                header = f.readline()
                header = 'Accession\t' + header
                if(include_header):
                    out_collated.writelines(header)
                    include_header = False

                for line in f:
                    outline = accession + "\t" + line 
                    out_collated.writelines(outline)
        except(FileNotFoundError):
            print(f'Could not find file {file}')
            sys.exit()
        except:
            print(f'Error processing file {file}')
            sys.exit()

f.close()
out_collated.close()

print("Collated results written to " + outfile_collated)

# Process the collated file
print("Now reading in " + outfile_collated)
df_kallisto = pd.read_csv(outfile_collated, sep='\t')

print("Merging with metadata file")
df_merged_data = pd.merge(df_kallisto, df_meta, how='inner', on='Accession')

#Summarise input
unique_accession_metadata_count = (df_meta['Accession']
                                    .drop_duplicates()
                                    .size
                                  )
print("Unique accessions (cell lines) in metadata: " + str(unique_accession_metadata_count))

unique_accession_kallisto_count = (df_kallisto['Accession']
                                    .drop_duplicates()
                                    .size
                                  )
print("Unique accessions (cell lines) in collated Kallisto data: " + str(unique_accession_kallisto_count))

unique_accession_merged_count = (df_merged_data['Accession']
                                    .drop_duplicates()
                                    .size
                                  )
print("Unique accessions (cell lines) after merging Kallisto data with metadata: " + str(unique_accession_merged_count))

#Delete large data objects
#del(df_kallisto)
#del(df_meta)

# Calculate log10 values (convert 0 to 0.0001 to prevent division by zero errors)
df_merged_data['log10_tpm'] = df_merged_data['tpm'] + 1
df_merged_data['log10_tpm'] = np.log10(df_merged_data['log10_tpm'])

#Calculate transcript z-scores and on transcript-wise basis
target_means = (
    df_merged_data
        .groupby(by='target_id')
        .mean()
        .filter(items=['target_id', 'log10_tpm'])
        .rename(columns={'log10_tpm': 'target_mean_log10_tpm'})
        .reset_index()
    )

target_stdevs = (
    df_merged_data
        .groupby(by='target_id')
        .std()
        .filter(items=['target_id', 'log10_tpm'])
        .rename(columns={'log10_tpm': 'target_StdDev_log10_tpm'})
        .reset_index()
    )


df_merged_data = pd.merge(df_merged_data, target_means, how='inner', on='target_id') 
df_merged_data = pd.merge(df_merged_data, target_stdevs, how='inner', on='target_id')
df_merged_data['z_score'] = (df_merged_data['log10_tpm'] - df_merged_data['target_mean_log10_tpm']) / df_merged_data['target_StdDev_log10_tpm']

#Write out the result
print("Writing results to: " + outfile_processed)
df_merged_data.to_csv(outfile_processed, index=False, compression='gzip', sep="\t") 

print("Done")
