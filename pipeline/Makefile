#TODO - put in spot checks for the trickier scripts!

NULLGRAPH=~/dev/nullgraph
KHMER=~/dev/khmer
QUAKE=../Quake
JELLYFISH=/usr/local/bin/jellyfish

all: compare mcompare compare3 mcompare3 rcompare rcompare3 bam \
	compare4 mcompare4 rcompare4 compare5 compare6 \
	simple-genome-reads-even.sam.errhist \
	simple-genome-reads-even.fa.errhist \
	ecoli1 \
	ecoli-report-untrim.txt \
	ecoli-report-trim.txt \
	ecoli-errfree-report.txt \
	simple-genome-kmers.hist \
	simple-genome-dn-kmers.hist \

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

ecoli1: ecoli-report.txt ecoli-report-nodn.txt

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

# ecoli_ref.kh contains the counting table of k-mers in the raw read data set.
ecoli_ref.kh: ecoli_ref-5m.fastq.gz
	load-into-counting.py ecoli_ref.kh -k 20 -x 2e8 -N 4 ecoli_ref-5m.fastq.gz --report-total-kmers

ecoli-reads-nodn.errors.pos: ecoli_ref.kh
	./report-errors-by-read.py -C 15 ecoli_ref.kh ecoli_ref-5m.fastq.gz > ecoli-reads-nodn.errors.pos

ecoli-report-nodn.txt: ecoli-reads-nodn.errors.pos
	./compare-pos.py ecoli-reads-nodn.errors.pos ecoli-reads.sam.pos ecoli_ref-5m.fastq.gz > ecoli-report-nodn.txt

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

#####

repeat-10.fa:
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 1 > repeat-1.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 2 > repeat-2.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 3 > repeat-3.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 4 > repeat-4.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 5 > repeat-5.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 6 > repeat-6.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 7 > repeat-7.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 8 > repeat-8.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 9 > repeat-9.fa
	$(NULLGRAPH)/make-repeats.py -l 1000 -e .01 -s 3 -n 10 > repeat-10.fa

repgenome-10.fa: repeat-10.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-1.fa > repgenome-1.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-2.fa > repgenome-2.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-3.fa > repgenome-3.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-4.fa > repgenome-4.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-5.fa > repgenome-5.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-6.fa > repgenome-6.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-7.fa > repgenome-7.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-8.fa > repgenome-8.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-9.fa > repgenome-9.fa
	$(NULLGRAPH)/mix-into-genome.py repeat-10.fa > repgenome-10.fa

repgenome-10-reads.fa: repgenome-10.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-1.fa --mutation-details repgenome-1-reads.mut > repgenome-1-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-2.fa --mutation-details repgenome-2-reads.mut > repgenome-2-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-3.fa --mutation-details repgenome-3-reads.mut > repgenome-3-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-4.fa --mutation-details repgenome-4-reads.mut > repgenome-4-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-5.fa --mutation-details repgenome-5-reads.mut > repgenome-5-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-6.fa --mutation-details repgenome-6-reads.mut > repgenome-6-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-7.fa --mutation-details repgenome-7-reads.mut > repgenome-7-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-8.fa --mutation-details repgenome-8-reads.mut > repgenome-8-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-9.fa --mutation-details repgenome-9-reads.mut > repgenome-9-reads.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 repgenome-10.fa --mutation-details repgenome-10-reads.mut > repgenome-10-reads.fa

repgenome-10-reads.mut.pos: repgenome-10-reads.mut repgenome-10.fa
	./convert-mut-to-pos.py repgenome-1-reads.mut repgenome-1-reads.mut.pos
	./convert-mut-to-pos.py repgenome-2-reads.mut repgenome-2-reads.mut.pos
	./convert-mut-to-pos.py repgenome-3-reads.mut repgenome-3-reads.mut.pos
	./convert-mut-to-pos.py repgenome-4-reads.mut repgenome-4-reads.mut.pos
	./convert-mut-to-pos.py repgenome-5-reads.mut repgenome-5-reads.mut.pos
	./convert-mut-to-pos.py repgenome-6-reads.mut repgenome-6-reads.mut.pos
	./convert-mut-to-pos.py repgenome-7-reads.mut repgenome-7-reads.mut.pos
	./convert-mut-to-pos.py repgenome-8-reads.mut repgenome-8-reads.mut.pos
	./convert-mut-to-pos.py repgenome-9-reads.mut repgenome-9-reads.mut.pos
	./convert-mut-to-pos.py repgenome-10-reads.mut repgenome-10-reads.mut.pos

repgenome-10-reads.dn.kh: repgenome-10-reads.fa
	normalize-by-median.py -k 20 -C 20 repgenome-1-reads.fa -s repgenome-1-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-2-reads.fa -s repgenome-2-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-3-reads.fa -s repgenome-3-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-4-reads.fa -s repgenome-4-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-5-reads.fa -s repgenome-5-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-6-reads.fa -s repgenome-6-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-7-reads.fa -s repgenome-7-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-8-reads.fa -s repgenome-8-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-9-reads.fa -s repgenome-9-reads.dn.kh -x 2e6 -N 4
	normalize-by-median.py -k 20 -C 20 repgenome-10-reads.fa -s repgenome-10-reads.dn.kh -x 2e6 -N 4

repgenome-10-reads.calc.pos: repgenome-10-reads.dn.kh
	./report-errors-by-read.py repgenome-1-reads.dn.kh repgenome-1-reads.fa > repgenome-1-reads.calc.pos
	./report-errors-by-read.py repgenome-2-reads.dn.kh repgenome-2-reads.fa > repgenome-2-reads.calc.pos
	./report-errors-by-read.py repgenome-3-reads.dn.kh repgenome-3-reads.fa > repgenome-3-reads.calc.pos
	./report-errors-by-read.py repgenome-4-reads.dn.kh repgenome-4-reads.fa > repgenome-4-reads.calc.pos
	./report-errors-by-read.py repgenome-5-reads.dn.kh repgenome-5-reads.fa > repgenome-5-reads.calc.pos
	./report-errors-by-read.py repgenome-6-reads.dn.kh repgenome-6-reads.fa > repgenome-6-reads.calc.pos
	./report-errors-by-read.py repgenome-7-reads.dn.kh repgenome-7-reads.fa > repgenome-7-reads.calc.pos
	./report-errors-by-read.py repgenome-8-reads.dn.kh repgenome-8-reads.fa > repgenome-8-reads.calc.pos
	./report-errors-by-read.py repgenome-9-reads.dn.kh repgenome-9-reads.fa > repgenome-9-reads.calc.pos
	./report-errors-by-read.py repgenome-10-reads.dn.kh repgenome-10-reads.fa > repgenome-10-reads.calc.pos

repgenome-compare.txt: repgenome-10-reads.calc.pos repgenome-10-reads.mut.pos
	./compare-pos-2.py 1 repgenome-1-reads.mut.pos repgenome-1-reads.calc.pos repgenome-1-reads.fa > repgenome-compare.txt
	./compare-pos-2.py 2 repgenome-2-reads.mut.pos repgenome-2-reads.calc.pos repgenome-2-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 3 repgenome-3-reads.mut.pos repgenome-3-reads.calc.pos repgenome-3-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 4 repgenome-4-reads.mut.pos repgenome-4-reads.calc.pos repgenome-4-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 5 repgenome-5-reads.mut.pos repgenome-5-reads.calc.pos repgenome-5-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 6 repgenome-6-reads.mut.pos repgenome-6-reads.calc.pos repgenome-6-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 7 repgenome-7-reads.mut.pos repgenome-7-reads.calc.pos repgenome-7-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 8 repgenome-8-reads.mut.pos repgenome-8-reads.calc.pos repgenome-8-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 9 repgenome-9-reads.mut.pos repgenome-9-reads.calc.pos repgenome-9-reads.fa >> repgenome-compare.txt
	./compare-pos-2.py 10 repgenome-10-reads.mut.pos repgenome-10-reads.calc.pos repgenome-10-reads.fa >> repgenome-compare.txt

####

ecoli_corr: ecoli_ref-5m.dn.cor.fastq.gz ecoli_ref-5m.raw.cor.fastq.gz

ecoli_ref-5m.dn.cor.fastq.gz:
	echo ecoli_ref-5m.fastq.gz > quake_list.txt
	ln -fs /usr/local/bin/jellyfish .
	#cat ecoli_ref-5m.fastq.gz.keep | $(QUAKE)/bin/count-qmers -q 33 -k 14 > ecoli_dn_counts.out
	$(QUAKE)/bin/cov_model.py ecoli_dn_counts.out > ecoli_dn_counts.cov
	$(QUAKE)/bin/correct -f quake_list.txt -p 4 -k 14 -q 33 -c 7.94 -z -m ecoli_dn_counts.out
	mv ecoli_ref-5m.cor.fastq.gz ecoli_ref-5m.dn.cor.fastq.gz

ecoli_ref-5m.raw.cor.fastq.gz:
	echo ecoli_ref-5m.fastq.gz > quake_list.txt
	ln -fs /usr/local/bin/jellyfish .
	gunzip -c ecoli_ref-5m.fastq.gz | $(QUAKE)/bin/count-qmers -q 33 -k 14 > ecoli_raw_counts.out
	$(QUAKE)/bin/cov_model.py ecoli_raw_counts.out
	$(QUAKE)/bin/correct -f quake_list.txt -p 4 -k 14 -q 33 -c 7.2 -z -m ecoli_raw_counts.out
	mv ecoli_ref-5m.cor.fastq.gz ecoli_ref-5m.raw.cor.fastq.gz

# ecoli-reads.dn.cor.sam is the bowtie mapping of the DN-Quake-corrected reads to the reference genome.
ecoli-reads.dn.cor.sam: ecoli_ref-5m.dn.cor.fastq.gz ecoli.1.ebwt
	gunzip -c ecoli_ref-5m.dn.cor.fastq.gz | bowtie ecoli -q - -S ecoli-reads.dn.cor.sam

# ecoli-reads.dn.cor.sam.pos is the 'pos' file containing the locations
# of mismatches from the dn quake-corrected reads.
ecoli-reads.dn.cor.sam.pos: ecoli-reads.dn.cor.sam
	./sam-scan.py ecoliMG1655.fa ecoli-reads.dn.cor.sam ecoli_ref-5m.dn.cor.fastq.gz > ecoli-reads.dn.cor.sam.pos

quake-ecoli-dn-cor.txt: ecoli-reads.dn.cor.sam.pos
	./summarize-pos-file.py ecoli-reads.dn.cor.sam.pos ecoli_ref-5m.dn.cor.fastq.gz > quake-ecoli-dn-cor.txt

# ecoli-reads.raw.cor.sam is the bowtie mapping of the Quake-corrected reads to the reference genome.
ecoli-reads.raw.cor.sam: ecoli_ref-5m.raw.cor.fastq.gz ecoli.1.ebwt
	gunzip -c ecoli_ref-5m.raw.cor.fastq.gz | bowtie ecoli -q - -S ecoli-reads.raw.cor.sam

# ecoli-reads.raw.cor.sam.pos is the 'pos' file containing the locations
# of mismatches from the raw quake-corrected reads.
ecoli-reads.raw.cor.sam.pos: ecoli-reads.raw.cor.sam
	./sam-scan.py ecoliMG1655.fa ecoli-reads.raw.cor.sam ecoli_ref-5m.raw.cor.fastq.gz > ecoli-reads.raw.cor.sam.pos

quake-ecoli-raw-cor.txt: ecoli-reads.raw.cor.sam.pos
	./summarize-pos-file.py ecoli-reads.raw.cor.sam.pos ecoli_ref-5m.raw.cor.fastq.gz > quake-ecoli-raw-cor.txt

###

podar:  podar.1.ebwt \
	podar-reads.sam \
	podar-reads.sam.pos \
	podar.dn.kh \
	podar-reads.erros.pos \
	podar.fastq.gz.abundtrim \
	podar-abundtrim.sam \
	podar-abundtrim.sam.pos \
	podar-report-untrim.txt \
	podar-report-trim.txt \
	podar-report.txt \
	podar1

podar1: podar-report.txt podar-report-trim.txt podar-report-untrim.txt

podar-report.txt: podar-reads.errors.pos podar-reads.sam.pos
	./compare-pos.py podar-reads.errors.pos podar-reads.sam.pos podar-1.fastq.gz >podar-report.txt

podar.1.ebwt: podar-ref.fa
	bowtie-build podar-ref.fa podar
	samtools faidx podar-ref.fa

podar-reads.sam: podar-1.fastq.gz podar.1.ebwt
	gunzip -c podar-1.fastq.gz | bowtie podar -q - -S podar-reads.sam

podar-reads.sam.pos: podar-reads.sam
	./sam-scan.py podar-ref.fa podar-reads.sam podar-1.fastq.gz > podar-reads.sam.pos

podar.dn.kh: podar-1.fastq.gz
	 normalize-by-median.py -x 1e8 -N 4 -k 20 -C 10 -s podar.dn.kh podar-1.fastq.gz -R podar-dn-report.txt

podar-reads.errors.pos: podar-1.fastq.gz podar.dn.kh
	 ./report-errors-by-read.py -V --coverage 10 podar.dn.kh podar-1.fastq.gz > podar-reads.errors.pos 	

podar-1.fastq.gz.abundtrim: podar-1.fastq.gz
	$(KHMER)/sandbox/trim-low-abund.py -k 20 -Z 10 -C 5 -x 1e9 -N 4 podar-1.fastq.gz

podar-abundtrim.sam: podar-1.fastq.gz.abundtrim
	bowtie podar -q podar-1.fastq.gz.abundtrim -S podar-abundtrim.sam

podar-abundtrim.sam.pos: podar-abundtrim.sam
	./sam-scan.py podar-ref.fa podar-abundtrim.sam podar-1.fastq.gz.abundtrim > podar-abundtrim.sam.pos

podar-report-untrim.txt:podar-reads.sam.pos podar-1.fastq.gz
	./summarize-pos-file.py podar-reads.sam.pos podar-1.fastq.gz > podar-report-untrim.txt

podar-report-trim.txt: podar-abundtrim.sam.pos podar-1.fastq.gz.abundtrim
	./summarize-pos-file.py podar-abundtrim.sam.pos podar-1.fastq.gz.abundtrim > podar-report-trim.txt
