NULLGRAPH=~/dev/nullgraph
KHMER=~/dev/khmer

all: simple-genome-reads.dn.kh simple-genome-errors.hist

simple-genome.fa:
	$(NULLGRAPH)/make-random-genome.py -l 1000 -s 1 > simple-genome.fa

simple-genome-reads.fa: simple-genome.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 simple-genome.fa > simple-genome-reads.fa

simple-genome-reads.dn.kh: simple-genome-reads.fa
	normalize-by-median.py -k 20 -C 20 simple-genome-reads.fa -s simple-genome-reads.dn.kh -x 2e6 -N 4

simple-genome-errors.hist: simple-genome-reads.dn.kh
	report-unique-kmers-by-position.py simple-genome-reads.dn.kh simple-genome-reads.fa.keep > simple-genome-errors.hist

