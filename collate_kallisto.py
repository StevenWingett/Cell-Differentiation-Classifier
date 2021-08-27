# Python script to collate Kallisto results files
# Takes Kallisto output (TSV files) as input and
# returns the collated results

import argparse

help_text = '''Python script to collate Kallisto results files.
Takes Kallisto output (TSV files) as input and
returns the collated results'''
parser = argparse.ArgumentParser(description=help_text)

#parser.add_argument("-w", "--width", action="store", type=int, default=50,
#                    help="specify the width in characters of the formatted text",
#                    metavar='')
args = parser.parse_known_args()    #Use parse_known_arg to differentiate between arguments pre-specified and those that are not

#options = args[0]   # Get the 2 arrays of known/unknown arguments from the tuple
files = args[1]

#Process all files
include_header = True

outfile = 'collated_kallisto.tsv'
with open(outfile, 'w') as out:

    for file in files:
        try:
            with open(file, 'r') as f:
                print(f'Processing {file}')
                header = f.readline()
                if(include_header):
                    out.writelines(header)
                    include_header = False

                for line in f:
                    out.writelines(line)
        except(FileNotFoundError):
            print(f'Could not find file {file}')
            exit() 
        except:
            print(f'Error processing file {file}') 

print("Done")
