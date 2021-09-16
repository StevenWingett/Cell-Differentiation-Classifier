#Trim files
echo "Trimming FASTQ Files"

#Standard Trimming
for F in *.fastq.gz; do trim_galore --gzip $F; done

#Trim to 50 bps to allow consistent processing of different input files
for F in *_trimmed.fq.gz; do trim_galore --hardtrim5 50 --gzip --fastqc $F; done 

#FastQC on input and Final output files
echo "Producing FastQC Reports"
for F in *.fastq.gz; do fastqc $F; done
for F in *.50bp_5prime.fq.gz; do fastqc $F; done

#Kallisto Mapping ($1 is Kallisto index file argument)
echo "Kallisto Mapping"
for F in *.50bp_5prime.fq.gz; do kallisto quant -i $1 -o $F.kallisto --single -l 200 -s 20 -t 20 $F &> ${F}_kallisto.log; done

#Create links to Kallisto output for ease of analysis
for F in *.50bp_5prime.fq.gz; do ln -s $F.kallisto/abundance.tsv $F.abundance.tsv; done
rename -e s/\.50bp_5prime\.fq\.gz\.abundance\.tsv/.abundance.tsv/ *.abundance.tsv

#MultiQC
echo "Producing Multi QC Report"
multiqc --ignore cell_diff_class_map* .
