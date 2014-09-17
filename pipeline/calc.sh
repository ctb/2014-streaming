X=$(samtools view mrna-reads.sorted.bam mrna14:250 | wc -l)
echo $X
X=$(samtools view mrna-reads.sorted.bam mrna14:251 | wc -l)
echo $X
