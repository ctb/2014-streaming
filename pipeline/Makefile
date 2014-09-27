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

simple-genome.fa:
	$(NULLGRAPH)/make-random-genome.py -l 1000 -s 1 > simple-genome.fa

simple-genome-reads.fa: simple-genome.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 simple-genome.fa --mutation-details simple-genome-reads.mut > simple-genome-reads.fa

simple-genome-reads-even.fa: simple-genome.fa
	$(NULLGRAPH)/make-reads.py -S 1 -e .01 -r 100 -C 100 simple-genome.fa --mutation-details simple-genome-reads-even.mut --even > simple-genome-reads-even.fa

simple-genome-perfect.fa: simple-genome.fa
	$(NULLGRAPH)/make-reads.py -S 2 -e 0 -r 100 -C 100 simple-genome.fa > simple-genome-perfect.fa

simple-genome-reads.mut.pos: simple-genome-reads.fa
	./convert-mut-to-pos.py simple-genome-reads.mut simple-genome-reads.mut.pos

simple-genome-reads.dn.kh: simple-genome-reads.fa
	normalize-by-median.py -k 20 -C 20 simple-genome-reads.fa -s simple-genome-reads.dn.kh -x 2e6 -N 4

simple-genome-errors.pos: simple-genome-reads.dn.kh
	./report-errors-by-read.py simple-genome-reads.dn.kh simple-genome-reads.fa > simple-genome-errors.pos

simple-genome-reads.sam: simple-genome-reads.fa
	bowtie-build simple-genome.fa simple-genome > /dev/null
	samtools faidx simple-genome.fa

	bowtie simple-genome -f simple-genome-reads.fa -S simple-genome-reads.sam

simple-genome-reads-even.sam: simple-genome-reads-even.fa
	bowtie-build simple-genome.fa simple-genome > /dev/null
	samtools faidx simple-genome.fa

	bowtie simple-genome -f simple-genome-reads-even.fa -S simple-genome-reads-even.sam

simple-genome-reads-even.sam.errhist: simple-genome-reads-even.sam
	./sam-scan-errhist.py simple-genome.fa simple-genome-reads-even.sam simple-genome-reads-even.fa > simple-genome-reads-even.sam.errhist

simple-genome-reads.sorted.bam: simple-genome-reads.sam
	samtools import simple-genome.fa.fai simple-genome-reads.sam simple-genome-reads.bam
	samtools sort simple-genome-reads.bam simple-genome-reads.sorted
	samtools index simple-genome-reads.sorted.bam

simple-genome-sam-mismatches.pos: simple-genome-reads.sam
	./sam-scan.py simple-genome.fa simple-genome-reads.sam simple-genome-reads.fa > simple-genome-sam-mismatches.pos

simple-genome-reads.fa.abundtrim: simple-genome-reads.fa
	$(KHMER)/sandbox/trim-low-abund.py -k 20 -Z 20 -C 5 simple-genome-reads.fa

simple-genome-abundtrim.sam: simple-genome-reads.fa.abundtrim \
	simple-genome-reads.sam
	bowtie simple-genome -f simple-genome-reads.fa.abundtrim -S simple-genome-abundtrim.sam

simple-genome-abundtrim-sam-mismatches.pos: simple-genome-abundtrim.sam
	./sam-scan.py simple-genome.fa simple-genome-abundtrim.sam simple-genome-reads.fa.abundtrim > simple-genome-abundtrim-sam-mismatches.pos

compare: simple-genome-errors.pos simple-genome-sam-mismatches.pos
	./compare-pos.py simple-genome-errors.pos simple-genome-sam-mismatches.pos simple-genome-reads.fa

compare2: simple-genome-errors.pos simple-genome-reads.mut.pos
	./compare-pos.py simple-genome-errors.pos simple-genome-reads.mut.pos simple-genome-reads.fa

compare3: simple-genome-sam-mismatches.pos simple-genome-reads.mut.pos
	./compare-pos.py simple-genome-sam-mismatches.pos simple-genome-reads.mut.pos simple-genome-reads.fa

simple-genome-stream-mismatches.pos: simple-genome-reads.fa
	./calc-errors-few-pass.py simple-genome-reads.fa > simple-genome-stream-mismatches.pos

compare4: simple-genome-stream-mismatches.pos simple-genome-reads.mut.pos
	./compare-pos.py simple-genome-stream-mismatches.pos simple-genome-reads.mut.pos simple-genome-reads.fa

compare5: simple-genome-sam-mismatches.pos simple-genome-abundtrim-sam-mismatches.pos
	./summarize-pos-file.py simple-genome-sam-mismatches.pos simple-genome-reads.fa
	./summarize-pos-file.py simple-genome-abundtrim-sam-mismatches.pos simple-genome-reads.fa.abundtrim

simple-genome-reads-even.fa.errhist: simple-genome-reads-even.fa
	-$(KHMER)/sandbox/calc-error-profile.py simple-genome-reads-even.fa simple-genome-reads-even.fa

##### simple metagenome

simple-metagenome-reads.fa: simple-metagenome.fa
	$(NULLGRAPH)/make-biased-reads.py -S 1 -e .01 -r 100 -C 10 simple-metagenome.fa --mutation-details simple-metagenome-reads.mut > simple-metagenome-reads.fa

simple-metagenome-reads.mut.pos: simple-metagenome-reads.fa
	./convert-mut-to-pos.py simple-metagenome-reads.mut simple-metagenome-reads.mut.pos

simple-metagenome-reads.dn.kh: simple-metagenome-reads.fa
	normalize-by-median.py -k 20 -C 20 simple-metagenome-reads.fa -s simple-metagenome-reads.dn.kh -x 2e6 -N 4

simple-metagenome-errors.pos: simple-metagenome-reads.dn.kh
	./report-errors-by-read.py -V --coverage 20 simple-metagenome-reads.dn.kh simple-metagenome-reads.fa > simple-metagenome-errors.pos

simple-metagenome-reads.sam: simple-metagenome-reads.fa
	bowtie-build simple-metagenome.fa simple-metagenome > /dev/null
	samtools faidx simple-metagenome.fa

	bowtie simple-metagenome -f simple-metagenome-reads.fa -S simple-metagenome-reads.sam

simple-metagenome-reads.sorted.bam: simple-metagenome-reads.sam
	samtools import simple-metagenome.fa.fai simple-metagenome-reads.sam simple-metagenome-reads.bam
	samtools sort simple-metagenome-reads.bam simple-metagenome-reads.sorted
	samtools index simple-metagenome-reads.sorted.bam

simple-metagenome-sam-mismatches.pos: simple-metagenome-reads.sam
	./sam-scan.py simple-metagenome.fa simple-metagenome-reads.sam simple-metagenome-reads.fa > simple-metagenome-sam-mismatches.pos

simple-metagenome-reads.fa.abundtrim: simple-metagenome-reads.fa
	$(KHMER)/sandbox/trim-low-abund.py -V -k 20 -Z 20 -C 5 simple-metagenome-reads.fa

simple-metagenome-abundtrim.sam: simple-metagenome-reads.fa.abundtrim \
	simple-metagenome-reads.sam
	bowtie simple-metagenome -f simple-metagenome-reads.fa.abundtrim -S simple-metagenome-abundtrim.sam

simple-metagenome-abundtrim-sam-mismatches.pos: simple-metagenome-abundtrim.sam
	./sam-scan.py simple-metagenome.fa simple-metagenome-abundtrim.sam simple-metagenome-reads.fa.abundtrim > simple-metagenome-abundtrim-sam-mismatches.pos

mcompare: simple-metagenome-errors.pos simple-metagenome-sam-mismatches.pos
	./compare-pos.py simple-metagenome-errors.pos simple-metagenome-sam-mismatches.pos simple-metagenome-reads.fa

mcompare2: simple-metagenome-errors.pos simple-metagenome-reads.mut.pos
	./compare-pos.py simple-metagenome-errors.pos simple-metagenome-reads.mut.pos simple-metagenome-reads.fa

mcompare3: simple-metagenome-sam-mismatches.pos simple-metagenome-reads.mut.pos
	./compare-pos.py simple-metagenome-sam-mismatches.pos simple-metagenome-reads.mut.pos simple-metagenome-reads.fa

simple-metagenome-stream-mismatches.pos: simple-metagenome-reads.fa
	./calc-errors-few-pass.py simple-metagenome-reads.fa > simple-metagenome-stream-mismatches.pos

mcompare4: simple-metagenome-stream-mismatches.pos simple-metagenome-reads.mut.pos
	./compare-pos.py simple-metagenome-stream-mismatches.pos simple-metagenome-reads.mut.pos simple-metagenome-reads.fa

mcompare5: simple-metagenome-sam-mismatches.pos simple-metagenome-abundtrim-sam-mismatches.pos
	./summarize-pos-file.py simple-metagenome-sam-mismatches.pos simple-metagenome-reads.fa
	./summarize-pos-file.py simple-metagenome-abundtrim-sam-mismatches.pos simple-metagenome-reads.fa.abundtrim

##### simple mrna molecule with three isoforms (1234, 124, 134)

mrna-reads.fa: mrna.fa
	$(NULLGRAPH)/make-biased-reads.py -S 1 -e .01 -r 100 -C 100 mrna.fa --mutation-details mrna-reads.mut > mrna-reads.fa

mrna-reads.mut.pos: mrna-reads.fa
	./convert-mut-to-pos.py mrna-reads.mut mrna-reads.mut.pos

mrna-reads.dn.kh: mrna-reads.fa
	normalize-by-median.py -k 20 -C 20 mrna-reads.fa -s mrna-reads.dn.kh -x 2e6 -N 4

mrna-errors.pos: mrna-reads.dn.kh
	./report-errors-by-read.py -V --coverage 20 mrna-reads.dn.kh mrna-reads.fa > mrna-errors.pos

mrna-reads.sam: mrna-reads.fa
	bowtie-build mrna.fa mrna > /dev/null
	samtools faidx mrna.fa

	bowtie mrna -f mrna-reads.fa -S mrna-reads.sam

mrna-reads.sorted.bam: mrna-reads.sam
	samtools import mrna.fa.fai mrna-reads.sam mrna-reads.bam
	samtools sort mrna-reads.bam mrna-reads.sorted
	samtools index mrna-reads.sorted.bam

mrna-sam-mismatches.pos: mrna-reads.sam
	./sam-scan.py mrna.fa mrna-reads.sam mrna-reads.fa > mrna-sam-mismatches.pos

mrna-reads.fa.abundtrim: mrna-reads.fa
	$(KHMER)/sandbox/trim-low-abund.py -V -k 20 -Z 20 -C 5 mrna-reads.fa

mrna-abundtrim.sam: mrna-reads.fa.abundtrim \
	mrna-reads.sam
	bowtie mrna -f mrna-reads.fa.abundtrim -S mrna-abundtrim.sam

mrna-abundtrim-sam-mismatches.pos: mrna-abundtrim.sam
	./sam-scan.py mrna.fa mrna-abundtrim.sam mrna-reads.fa.abundtrim > mrna-abundtrim-sam-mismatches.pos

rcompare: mrna-errors.pos mrna-sam-mismatches.pos
	./compare-pos.py mrna-errors.pos mrna-sam-mismatches.pos mrna-reads.fa

rcompare2: mrna-errors.pos mrna-reads.mut.pos
	./compare-pos.py mrna-errors.pos mrna-reads.mut.pos mrna-reads.fa

rcompare3: mrna-sam-mismatches.pos mrna-reads.mut.pos
	./compare-pos.py mrna-sam-mismatches.pos mrna-reads.mut.pos mrna-reads.fa

mrna-stream-mismatches.pos: mrna-reads.fa
	./calc-errors-few-pass.py mrna-reads.fa > mrna-stream-mismatches.pos

rcompare4: mrna-stream-mismatches.pos mrna-reads.mut.pos
	./compare-pos.py mrna-stream-mismatches.pos mrna-reads.mut.pos mrna-reads.fa

rcompare5: mrna-sam-mismatches.pos mrna-abundtrim-sam-mismatches.pos
	./summarize-pos-file.py mrna-sam-mismatches.pos mrna-reads.fa
	./summarize-pos-file.py mrna-abundtrim-sam-mismatches.pos mrna-reads.fa.abundtrim
