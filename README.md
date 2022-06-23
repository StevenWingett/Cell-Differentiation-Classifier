# Cell-Differentiation-Classifier
A logistic regression workflow that takes RNA-seq data to assess the differentiation potential of a cell line.

Project Homepage: https://github.com/StevenWingett/Cell-Differentiation-Classifier

## Repository Data Files
**data_to_download_metadata.tsv** - extensive information of the [HipSci](https://www.hipsci.org/) datasets analysed.

**download_files_list_wget.txt** - use with the wget command to download the HipSci FASTQ data files of interest.

**dataset_summary.tsv** - summary of the datasets, including differentiation scores.

## Repository Scripts (in order of processing)

**Data preparation**
1. convert_to_log2 (all data)
Generates a (log2 TMP) + 1 file

2. select_by_retention_category.ipynb
Extracts data for retention category of interest

3. calc_z_scores.ipynb
Appends z-score for each gene.
Also, creates file of expression average and standard deviation score for each gene 

4. expression_differentiation_efficiency_correlation.ipynb
Determine how well each gene's score correlates with differentiation efficiency.  Creates a separate correlation listing the correlation coefficient for each gene.

**Builing model and classification**
5. classifier.ipnb
Writes out the classifier results
(Also writes out a log of the datasets used to train the classifier)

6. analyse_classifier_results.ipynb

**Using existing model to classify data**
7. predict.ipnb
Makes predictions using expression data, pre-calculated logistic regressions coefficients and pre-calculated gene expression averages and standard deviations

8. assess_predictions.ipnb
Evaluate how good were the predications made by predict.ipnb

## Workflow overview

The FASTQ files should be mapped in paired-end mode (where possible) using the nf-core RNA-seq pipeline nf-core/rnaseq: '3.5' (https://nf-co.re/rnaseq) against Human genome GRCh38 (release 102).

Steven Wingett, The MRC-Laboratory of Molecular Biology, Cambridge, UK
