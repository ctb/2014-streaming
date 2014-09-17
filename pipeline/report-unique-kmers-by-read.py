#! /usr/bin/env python
import sys
import screed
import khmer
import argparse

def find_first_unique(kh, sequence, cutoff):
    K = kh.ksize()

    start = 0
    end = len(sequence) - K + 1

    # skip over errors at beginning
    while start < end:
        if kh.get(sequence[start:start+K]) > cutoff:
            break
        start += 1

    if start > 0:
        if start < K:         # error in first K
            return [start - 1]

        # multiple errors => unresolvable, probably.
        return [-1]

    # ok, start = 0 & we find first k-mer overlapping an error, if any.
    while start < end:
        kmer = sequence[start:start + K]

        c = kh.get(kmer)
        if c <= cutoff:
            pos = start + K - 1
            return [pos]

        start += 1
        
    return None                         # no errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('table')
    parser.add_argument('sequences')
    parser.add_argument('-C', '--cutoff', default=2, type=int)
    args = parser.parse_args()

    kh = khmer.load_counting_hash(args.table)

    for record in screed.open(args.sequences):
        pos = find_first_unique(kh, record.sequence, args.cutoff)
        if pos is not None and len(pos) >= 0 and pos[0] != -1:
            print record.name, ",".join(map(str, pos))
        else:
            print record.name

if __name__ == '__main__':
   main()
   
