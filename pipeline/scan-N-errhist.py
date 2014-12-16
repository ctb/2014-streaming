#! /usr/bin/env python
import sys
import screed
import argparse

MAX_SEQ_LEN = 5000


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('readsfile')
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'),
                        default=sys.stdout)
    
    args = parser.parse_args()

    lengths = []
    positions = [0] * MAX_SEQ_LEN

    for n, record in enumerate(screed.open(args.readsfile)):
        if n % 100000 == 0:
            print >>sys.stderr, '...', n
        seq = record.sequence.upper()
        pos = seq.find('N')
        while pos >= 0:
            positions[pos] += 1
            pos = seq.find('N', pos + 1)
        lengths.append(len(seq))

    # normalize for length
    lengths.sort()
    max_length = lengths[-1]

    length_count = [0]*max_length
    for j in range(max_length):
        length_count[j] = sum([1 for i in lengths if i >= j])
        
    # write!
    for n, i in enumerate(positions[:max_length]):
        print >>args.outfile, n, i, float(i) / float(length_count[n])

if __name__ == '__main__':
    main()
