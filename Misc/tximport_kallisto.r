#if (!requireNamespace("BiocManager", quietly = TRUE))
#    install.packages("BiocManager")

#BiocManager::install("tximportData")
#BiocManager::install("TxDb.Hsapiens.UCSC.hg19.knownGene")
library(tximport)
library(tidyverse)

rm(list=ls())

#Setup
transcript_gene_lookupfile <- 'parsed_gtf.tsv.gz'
input_files_list_file <- 'input_files_list.tsv' #2-column file #SampleName FileName
outfile <- "gene_level_TPM_matrix.tsv"


#Create gene-transcript lookup
lookup_data <- read.delim(transcript_gene_lookupfile,
                                    stringsAsFactors = FALSE)
tran_gene_lookup <- lookup_data[, 1:2]
files <- read.delim(input_files_list_file, stringsAsFactors=FALSE) #named vector of filenames
sample_names <- files[, 1]
files <- files[, 2]
names(files) <- sample_names

if(!all(file.exists(files))){
    print("Not all input files found!")
    stop()
}

#Create object conversion
txi.data_object <- tximport(files, type = "kallisto", tx2gene = tran_gene_lookup, ignoreAfterBar = TRUE)
#head(txi.data_object$counts)

#Relate gene name to gene id
gene_tmps <- as_tibble(txi.data_object$abundance)
gene_names <- tibble(rownames(txi.data_object$abundance))

gene_tmps %>%
    add_column(gene_names, .before=1) -> gene_tmps

colnames(gene_tmps)[1] <- "gene_id"
 
lookup_data <- tibble(lookup_data)
lookup_data <- lookup_data[,1:3]
lookup_data %>%
    select('gene_id', 'gene_name') %>%
    distinct() -> lookup_data

gene_tmps <- right_join(lookup_data, gene_tmps, by="gene_id")

#Write out results
print(paste("Writing to", outfile))
write_tsv(x=gene_tmps, file=outfile)

#Write out results of log10 quantitation
outfile <- paste0("log10_", outfile)
log10_gene_tmps <- log10((gene_tmps[, c(-1, -2)]) + 1)
log10_gene_tmps <- tibble(cbind(gene_tmps[, 1:2], log10_gene_tmps))
print(paste("Writing to log10(TMP+1) data to", outfile))
write_tsv(x=log10_gene_tmps, file=outfile)

print("Done")
