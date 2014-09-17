NULLGRAPH=~/dev/nullgraph
KHMER=~/dev/khmer

all: simple-genome-reads.dn.kh simple-genome-errors.hist

clean:
	-rm -f simple-genome.fa simple-genome-reads.dn.kh simple-genome-reads.sam

simple-genome.fa:
	$(NULLGRAPH)/make-random-genome.py -l 1000 -s 1 > simple-genome.fa

simple-genome-reads.fa: simple-genome.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 simple-genome.fa --mutation-details simple-genome-reads.mut > simple-genome-reads.fa

simple-genome-reads.mut.pos: simple-genome-reads.fa
	./convert-mut-to-pos.py simple-genome-reads.mut simple-genome-reads.mut.pos

simple-genome-reads.dn.kh: simple-genome-reads.fa
	normalize-by-median.py -k 20 -C 20 simple-genome-reads.fa -s simple-genome-reads.dn.kh -x 2e6 -N 4

simple-genome-errors.hist: simple-genome-reads.dn.kh
	report-unique-kmers-by-position.py simple-genome-reads.dn.kh simple-genome-reads.fa > simple-genome-errors.hist

simple-genome-errors.pos: simple-genome-reads.dn.kh
	./report-unique-kmers-by-read.py simple-genome-reads.dn.kh simple-genome-reads.fa > simple-genome-errors.pos

simple-genome-reads.sam: simple-genome-reads.fa
	bowtie-build simple-genome.fa simple-genome > /dev/null
	samtools faidx simple-genome.fa

	bowtie simple-genome -f simple-genome-reads.fa -S simple-genome-reads.sam

simple-genome-reads.bam: simple-genome-reads.sam
	samtools import simple-genome.fa.fai simple-genome-reads.sam simple-genome-reads.bam
	samtools sort simple-genome-reads.bam simple-genome-reads.sorted
	samtools index simple-genome-reads.sorted.bam

simple-genome-sam-mismatches.pos: simple-genome-reads.sam
	./sam-scan.py simple-genome.fa simple-genome-reads.sam simple-genome-reads.fa > simple-genome-sam-mismatches.pos

compare: simple-genome-errors.pos simple-genome-sam-mismatches.pos
	./compare-pos.py simple-genome-errors.pos simple-genome-sam-mismatches.pos

compare2: simple-genome-errors.pos simple-genome-reads.mut.pos
	./compare-pos.py simple-genome-errors.pos simple-genome-reads.mut.pos

compare3: simple-genome-sam-mismatches.pos simple-genome-reads.mut.pos
	./compare-pos.py simple-genome-sam-mismatches.pos simple-genome-reads.mut.pos

