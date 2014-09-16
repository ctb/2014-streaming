#! /usr/bin/env python
import sys
import screed
import khmer
import argparse

def find_first_unique(kh, sequence):
    K = kh.ksize()

    if kh.get(sequence[:K]) == 1:
        return None               # ignore errors in first K
    
    for start in range(len(sequence) - K + 1):
        kmer = sequence[start:start + K]

        c = kh.get(kmer)
        if c == 1:
            pos = start + K - 1
            return pos

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('table')
    parser.add_argument('sequences')
    args = parser.parse_args()

    kh = khmer.load_counting_hash(args.table)

    hist = [0] * 1000
    for record in screed.open(args.sequences):
        pos = find_first_unique(kh, record.sequence)
        if pos is not None:
            hist[pos] += 1

    for n, i in enumerate(hist):
        print n, i

if __name__ == '__main__':
   main()
   
