for pos in 100 250 251 350
do
    X=$(samtools view mrna-reads.sorted.bam mrna14:${pos} | wc -l)
    echo mrna14 pos $pos count $X
done

for pos in 100 250 251 350
do
    X=$(samtools view mrna-reads.sorted.bam mrna134:${pos} | wc -l)
    echo mrna134 pos $pos count $X
done

for pos in 100 350 500 501 650
do
    X=$(samtools view mrna-reads.sorted.bam mrna124:${pos} | wc -l)
    echo mrna124 pos $pos count $X
done
