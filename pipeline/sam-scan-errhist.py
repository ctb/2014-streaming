#! /usr/bin/env python
import sys
import argparse
import screed


MAX_SEQ_LEN = 5000


def ignore_at(iter):
    for item in iter:
        if item.startswith('@'):
            continue
        yield item

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('genome')
    parser.add_argument('samfile')
    args = parser.parse_args()

    genome_dict = dict([ (record.name, record.sequence) for record in \
                        screed.open(args.genome) ])

    positions = [0] * MAX_SEQ_LEN
    lengths = []

    n = 0
    for samline in ignore_at(open(args.samfile)):
        n += 1
        if n % 100000 == 0:
            print >>sys.stderr, '...', n

        readname, _, refname, refpos, _, _, _, _, _, seq = samline.split()[:10]
        if refname == '*' or refpos == '*':
            continue
        
        refpos = int(refpos)

        #assert record.name == readname, (record.name, readname)
        ref = genome_dict[refname][refpos-1:refpos+len(seq) - 1]
        #print ref
        #print seq

        errors = []
        for pos, (a, b) in enumerate(zip(ref, seq)):
            if a != b:
                if readname.endswith('r'):
                    pos = len(seq) - pos - 1
                positions[pos] += 1
        lengths.append(len(seq))

    # normalize for length
    lengths.sort()
    max_length = lengths[-1]

    length_count = [0]*max_length
    for j in range(max_length):
        length_count[j] = sum([1 for i in lengths if i >= j])

    # write!
    for n, i in enumerate(positions[:max_length]):
        print n, i, float(i) / float(length_count[n])

    print >>sys.stderr, "error rate: %.2f%%" % \
          (100.0 * sum(positions) / float(sum(lengths)))

if __name__ == '__main__':
    main()
