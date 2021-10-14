import gzip

#gtf_file = 'test.gtf.gz'
gtf_file = 'Copy_Homo_sapiens.GRCh38.102.gtf.gz'
outfile = 'parsed_gtf.tsv.gz'

with gzip.open(gtf_file, 'rb') as f, gzip.open(outfile, 'wb') as fout:

    # Write out header line
    header = "target_id\tgene_id\tgene_name\tchromosome\tstart\tend\ttranscript_length\n"
    fout.write(header.encode('utf-8')) 

    for line in f:
        line = line.decode('utf-8').rstrip()

        if(line[0] == '#'):    #Ignore headers
            continue

        line_elements = line.split("\t")
        csome = line_elements[0]
        type_description = line_elements[2]
        start = int(line_elements[3])
        end = int(line_elements[4])
        extra_data_elements = line_elements[8].split(";")

        gene_id = extra_data_elements[0].split()[1].strip('"')
        gene_version = extra_data_elements[1].split()[1].strip('"')
        transcript_id = extra_data_elements[2].split()[1].strip('"')
        transcript_version = extra_data_elements[3].split()[1].strip('"')
        gene_name = extra_data_elements[4].split()[1].strip('"')
        transcript_length = end - start + 1
        # print(type_description)

        #Check this is a transcript
        if(type_description != 'transcript'):
            continue
        
        #Append version number to genes and transcripts
        gene_id = gene_id + '.' + gene_version
        transcript_id = transcript_id + '.' + transcript_version

        line_out = '\t'.join(str(e) for e in [transcript_id, gene_id, gene_name, csome, start, end, transcript_length])
        line_out = line_out + "\n"
        #print(extra_data_elements)
        fout.write(line_out.encode('utf-8'))  

        #print(line)
fout.close()
f.close()
    
print('Done')
