#TODO - put in spot checks for the trickier scripts!

NULLGRAPH=~/dev/nullgraph
KHMER=~/dev/khmer

all: compare mcompare compare3 mcompare3 rcompare rcompare3 bam \
	compare4 mcompare4 rcompare4 \
	simple-genome-reads-even.sam.errhist \
	simple-genome-reads-even.fa.errhist

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

#####

ecoli1: ecoli-reads.errors.pos ecoli-reads.sam.pos
	./compare-pos.py ecoli-reads.errors.pos ecoli-reads.sam.pos ecoli_ref-5m.fastq.gz

ecoli.1.ebwt: ecoliMG1655.fa
	bowtie-build ecoliMG1655.fa ecoli
	samtools faidx ecoliMG1655.fa

ecoli-reads.sam: ecoli_ref-5m.fastq.gz ecoli.1.ebwt
	gunzip -c ecoli_ref-5m.fastq.gz | bowtie ecoli -q - -S ecoli-reads.sam

ecoli-reads.sam.pos: ecoli-reads.sam
	./sam-scan.py ecoliMG1655.fa ecoli-reads.sam ecoli_ref-5m.fastq.gz > ecoli-reads.sam.pos

ecoli_ref.dn.kh: ecoli_ref-5m.fastq.gz
	normalize-by-median.py -x 1e7 -N 4 -k 20 -s ecoli_ref.dn.kh ecoli_ref-5m.fastq.gz

ecoli-reads.errors.pos: ecoli_ref-5m.fastq.gz ecoli_ref.dn.kh
	./report-errors-by-read.py ecoli_ref.dn.kh ecoli_ref-5m.fastq.gz > ecoli-reads.errors.pos