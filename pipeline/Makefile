#TODO - put in spot checks for the trickier scripts!

NULLGRAPH=~/dev/nullgraph
KHMER=~/dev/khmer
QUAKE=../Quake
JELLYFISH=/usr/local/bin/jellyfish

all: compare mcompare compare3 mcompare3 rcompare rcompare3 bam \
	compare4 mcompare4 rcompare4 compare5 compare6 \
	simple-genome-reads-even.sam.errhist \
	simple-genome-reads-even.fa.errhist \
	simple-genome-kmers.hist \
	simple-genome-dn-kmers.hist \
	ecoli \
	ecoli-errfree-report.txt \
	rseq podar ecoli_corr

# delete the targets of rules on an error
.DELETE_ON_ERROR:

bam: simple-genome-reads.sorted.bam simple-metagenome-reads.sorted.bam \
	simple-mrna-reads.sorted.bam

clean:
	-rm -f simple-genome.fa simple-genome-reads.dn.kh simple-genome-reads.sam
	-rm -f *-reads.fa
	-rm -f rseq_compare*.txt
	-rm -f *.abundtrim *.ebwt *.fai *.pos *.keep *.bam *.mut *.bai *.sam *.kh
	-rm -f *.errhist *.abundfilt *.hicov.fq *.lowcov.fq *.report
	-rm -f *.txt repgenome* repeat* *.out *.cov
	-rm -f *.bt2 *.hist *.info *.dict *.covhist *.covdict

##### simple genome
include makefile.simple-genome

##### simple metagenome
include makefile.simple-metagenome

##### simple mrna molecule with three isoforms (1234, 124, 134)
include makefile.simple-mrna

##### mouse 1m rnaseq data set (real)
include makefile.rseq

##### E. coli genome data set (real)
include makefile.ecoli

##### shotgun metagenome data set (real)
include makefile.podar

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
