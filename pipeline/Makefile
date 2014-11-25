#TODO - put in spot checks for the trickier scripts!

NULLGRAPH=~/dev/nullgraph
KHMER=~/dev/khmer

all: compare mcompare compare3 mcompare3 rcompare rcompare3 bam \
	compare4 mcompare4 rcompare4 compare5 compare6 \
	simple-genome-reads-even.sam.errhist \
	simple-genome-reads-even.fa.errhist \
	ecoli-report-untrim.txt \
	ecoli-report-trim.txt \
	ecoli-errfree-report.txt \
	simple-genome-kmers.hist \
	simple-genome-dn-kmers.hist

bam: simple-genome-reads.sorted.bam simple-metagenome-reads.sorted.bam \
	mrna-reads.sorted.bam

clean:
	-rm -f simple-genome.fa simple-genome-reads.dn.kh simple-genome-reads.sam
	-rm -f *-reads.fa
	-rm -f *.abundtrim *.ebwt *.fai *.pos *.keep *.bam *.mut *.bai *.sam *.kh

##### simple genome
include makefile.simple-genome

##### simple metagenome
include makefile.simple-metagenome

##### simple mrna molecule with three isoforms (1234, 124, 134)
include makefile.mrna

##### mouse 1m rnaseq data set (real)
include makefile.rseq

ecoli1: ecoli-report.txt

# bowtie index for ecoliMG1655.fa
ecoli.1.ebwt: ecoliMG1655.fa
	bowtie-build ecoliMG1655.fa ecoli
	samtools faidx ecoliMG1655.fa

# ecoli-reads.sam is the bowtie mapping of the reads to the reference genome.
ecoli-reads.sam: ecoli_ref-5m.fastq.gz ecoli.1.ebwt
	gunzip -c ecoli_ref-5m.fastq.gz | bowtie ecoli -q - -S ecoli-reads.sam

# ecoli-reads.sam.pos is the 'pos' file containing the locations of mismatches,
# i.e. errors, determined from mapping.
ecoli-reads.sam.pos: ecoli-reads.sam
	./sam-scan.py ecoliMG1655.fa ecoli-reads.sam ecoli_ref-5m.fastq.gz > ecoli-reads.sam.pos

# ecoli_ref.dn.kh contains the counting table output by digital normalization
# of the raw E. coli reads.
ecoli_ref.dn.kh: ecoli_ref-5m.fastq.gz
	~/dev/khmer/scripts/normalize-by-median.py -x 1e8 -N 4 -k 20 -C 20 -s ecoli_ref.dn.kh ecoli_ref-5m.fastq.gz -R ecoli-dn-report.txt

# ecoli-reads.errors.pos contains the location of errors according to our
# own algorithm.
ecoli-reads.errors.pos: ecoli_ref-5m.fastq.gz ecoli_ref.dn.kh
	./report-errors-by-read.py ecoli_ref.dn.kh ecoli_ref-5m.fastq.gz > ecoli-reads.errors.pos

# ecoli-report.txt: a comparison of the errors found by mapping and 
# those found by our k-mer spectral error detection implementation.
ecoli-report.txt: ecoli-reads.errors.pos ecoli-reads.sam.pos
	./compare-pos.py ecoli-reads.errors.pos ecoli-reads.sam.pos ecoli_ref-5m.fastq.gz > ecoli-report.txt

# ecoli_ref-5m.fastq.gz.abundtrim contains the k-mer abundance trimmed
# reads, produced by trim-low-abund (streaming k-mer abundance trimming)
ecoli_ref-5m.fastq.gz.abundtrim: ecoli_ref-5m.fastq.gz
	$(KHMER)/sandbox/trim-low-abund.py -k 20 -Z 20 -C 5 -x 1e8 -N 4 ecoli_ref-5m.fastq.gz

# ecoli-abundtrim.sam is the mapping of the abundance-trimmed reads to the
# reference genome.
ecoli-abundtrim.sam: ecoli_ref-5m.fastq.gz.abundtrim
	bowtie ecoli -q ecoli_ref-5m.fastq.gz.abundtrim -S ecoli-abundtrim.sam

# ecoli-abundtrim.sam.pos is the 'pos' file containing the locations of
# mismatches to the reference genome in the reads, based on mapping.
ecoli-abundtrim.sam.pos: ecoli-abundtrim.sam
	./sam-scan.py ecoliMG1655.fa ecoli-abundtrim.sam ecoli_ref-5m.fastq.gz.abundtrim > ecoli-abundtrim.sam.pos

# ecoli-report-untrim.txt - a report on the error rate of the untrimmed reads,
# based on mapping to the reference.
ecoli-report-untrim.txt: ecoli-reads.sam.pos ecoli_ref-5m.fastq.gz
	./summarize-pos-file.py ecoli-reads.sam.pos ecoli_ref-5m.fastq.gz > ecoli-report-untrim.txt

# ecoli-report-untrim.txt - a report on the error rate of the k-mer
# abundance trimmed reads, based on mapping to the reference.
ecoli-report-trim.txt: ecoli-abundtrim.sam.pos ecoli_ref-5m.fastq.gz.abundtrim
	./summarize-pos-file.py ecoli-abundtrim.sam.pos ecoli_ref-5m.fastq.gz.abundtrim > ecoli-report-trim.txt

ecoli-errfree-reads.fa: ecoliMG1655.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e 0 -r 100 -C 100 ecoliMG1655.fa > ecoli-errfree-reads.fa

ecoli-errfree-report.txt: ecoli-errfree-reads.fa
	~/dev/khmer/scripts/normalize-by-median.py -x 1e8 -N 4 -k 20 -C 20 ecoli-errfree-reads.fa -R ecoli-errfree-report.txt
