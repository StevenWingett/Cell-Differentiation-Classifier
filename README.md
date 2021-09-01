# Cell-Differentiation-Classifier
A machine learning workflow that takes RNA-seq data to assess the differentiation potential of a cell line

## Repository Data Files
data_to_download_metadata.tsv - extensive information of the HipSci datasets

download_files_list_wget.txt - file that may be used with wget to download the data

dataset_summary.tsv - summary file of the datasets that includes differentiation scores

## Repository Scripts
create_classifier_datafile.py - collates the Kallisto data into one file


## Processing RNA-seq datasets
Map only the forward read of paired-end data or use single end data.  

### Trimming
Pre-trim to 50nt reads. This allows for consistent processing for all future datasets.

    nf_trim_galore *.fastq.gz --single_end -bg

    nf_trim_galore --trim_galore_args="--hardtrim5 50" test.fastq.gz -bg

Used trim_galore version 0.6.3_dev (update: 02 07 2019) powered by Cutadapt version 2.4

### Mapping
kallisto, version 0.46.1
GRCh38 (v102)
Homo_sapiens.GRCh38.cdna.all.fa.gz

    for F in *.fq.gz; do nohup kallisto quant -i Homo_sapiens.GRCh38_102_kallisto_index -o $F.kallisto --single -l 200 -s 20 -t 20 $F > $F.kallisto.log; done
