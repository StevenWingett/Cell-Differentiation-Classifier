# Cell-Differentiation-Classifier
A logistic regression workflow that takes RNA-seq data to assess the differentiation potential of a cell line.

Project Homepage: https://github.com/StevenWingett/Cell-Differentiation-Classifier

## Repository Data Files
**data_to_download_metadata.tsv** - extensive information of the [HipSci](https://www.hipsci.org/) datasets analysed.

**download_files_list_wget.txt** - use with the wget command to download the HipSci FASTQ data files of interest.

**dataset_summary.tsv** - summary of the datasets, including differentiation scores.

## Repository Scripts
**cell_diff_class_map.def** - Definitions file to build a (Singularity)[https://sylabs.io/singularity/] container for consistent QC/trimming/mapping of RNA-seq FASTQ files.

**create_classifier_datafile.py** - Python3 script that collates the Kallisto mapping results into one file. The script also determines the log10(tpm + 1) value for each transcript in each cell line (or more accurately accession, since one cell line may encompass multiple accessions).  In addition, the script returns the mean log10(tpm + 1) and standard deviation log10(tpm + 1) for each transcript across all accessions.  Then, to compare transcript levels between different accessions, the script determines the z-score for each transcript (i.e. it compares the expression of a transcript in a given accession against that same transcript in different accessions.)

This script takes as input the *.abundance.tsv files generated by Kallisto and a metadata file, which by default will be named 'dataset_summary.tsv'.

    python3 create_classifier_datafile.py -m [metadata file] [Kallisto abundance files]

This project's GitHub repository contains the metadata file 'dataset_summary.tsv' used for processing the selected HipSci datasets, which should also be used as a template for processing additional datasets.  If constructing your own metadata file, you will need to include 'Accession', 'Cell_line', 'Diff_efficiency' and 'Retention_group' columns.  (The Retention_group is simply a way of filtering which accessions are analysed by logistic regression.  The unedited Jupyter notebook (logistic_regression_classifier.ipynb) will only process accessions in Retention_group==0.)

**logistic_regression_classifier.ipynb** - Jupyter notebook that runs the logistic regression classifier.  Takes as input the data file generated by the create_classifier_datafile.py script.

**map_fastq_file.sh** - Bash script for QC/trimming/mapping of RNA-seq FASTQ files.  The script processes all files with extension *.fastq.gz in the current working directory.  The Kallisto transcriptome reference file should be passed as an argument.

    map_fastq_file.sh [Kallisto transcriptome reference file] 

## Workflow overview
To improve consistency between samples (and any future samples), map only the forward read of paired-end data, or use single-end data.  This choice was made because unknown future samples may be single-ended, but if we have mapped against paired-end data originally to build our classification model, it will therefore not be possible to process all the data uniformly (i.e. since obviously single-end data cannot be mapped as paired-end data). 

Below gives more detail on the QC, trimming and mapping processes.

### QC
Quality control is performed with (FastQC v0.11.9)[https://www.bioinformatics.babraham.ac.uk/projects/fastqc/] and (MultiQC v1.11QC)[https://multiqc.info/].

### Trimming
Uses (TrimGalore! v0.6.3)[https://www.bioinformatics.babraham.ac.uk/projects/trim_galore/], powered by (Cutadapt version 3.1)[http://journal.embnet.org/index.php/embnetjournal/article/view/200].

Reads are trimmed with standard parameters, and then re-trimmed to a length of 50nt (TrimGalore! parameter --hardtrim5 50)

### Mapping
Mapping uses (Kallisto, v0.46.1)[https://pachterlab.github.io/kallisto/]:

    kallisto quant -i [Kallisto index] -o $F.kallisto --single -l 200 -s 20 -t 20 [FASTQ FILE] 

The Homo sapiens GRCh38 (v102) cDNA genome was downloaded from [Ensembl](http://www.ensembl.org/) to make the Kallisto index.

## Processing data
We recommend using the Singularity container for QC/trimming/mapping.  Run the command below to build the container using the definitions file.  (The --bind $PWD:/mnt argument makes your current working directory ($PWD) visible to the container inside the container's /mnt folder).  

    sudo singularity build --bind $PWD:/mnt cell_diff_class_map.sif cell_diff_class_map.def

To perform the QC/trimming/mapping, run the command:

    singularity run --bind $PWD:/mnt cell_diff_class_map.sif [Kallisto index]

**Note:**  This command requires the metadata file dataset_summary.tsv to be in your current working directory.  The FASTQ files for processing and the Kallisto index should also be in your current working directory.  FASTQ files with the extension *.fastq.gz will be processed.

Should you wish to enter the Singularity container (e.g. for using Kallisto to generate a Kaillisto transcriptome index), run the command:

    singularity shell --bind $PWD:/mnt cell_diff_class_map.sif

Steven Wingett, The MRC-Laboratory of Molecular Biology, Cambridge, UK