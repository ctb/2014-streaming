#! /usr/bin/env python
import sys
import screed
import khmer
import argparse

def find_first_unique(kh, sequence, cutoff):
    K = kh.ksize()

    start = 0
    end = len(sequence) - K + 1
    posns = []

    # skip over errors at beginning
    while start < end:
        if kh.get(sequence[start:start+K]) > cutoff:
            break
        start += 1

    if start > 0:
        if start >= K:
            # multiple errors => unresolvable
            return [-1]
        else:          # error in first K
            posns.append(start - 1)

    # ok, now find next k-mer overlapping an error, if any.
    while start < end:
        kmer = sequence[start:start + K]

        c = kh.get(kmer)
        print start, c
        if c <= cutoff:
            pos = start + K - 1
            posns.append(pos)
            
            while start < end:
                if kh.get(sequence[start:start+K]) > cutoff:
                    break
                start += 1
        else:
            start += 1

    if not posns:
        return None
        
    return posns

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('table')
    parser.add_argument('sequences')
    parser.add_argument('-C', '--cutoff', default=2, type=int)
    args = parser.parse_args()

    kh = khmer.load_counting_hash(args.table)

    for record in screed.open(args.sequences):
        #if record.name != 'read573':
        #    continue
        posns = find_first_unique(kh, record.sequence, args.cutoff)
        if posns is not None and len(posns) > 0 and posns[0] != -1:
            print record.name, ",".join(map(str, posns))
        else:
            print record.name

if __name__ == '__main__':
   main()
   
