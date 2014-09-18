#! /usr/bin/env python
import khmer
import argparse
import screed

COV=20


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('readfile')
    args = parser.parse_args()

    kh = khmer.new_counting_hash(20, 1e6, 4)

    kept = 0
    discard = 0
    total = 0
    for record in screed.open(args.readfile):
        total += 1
        med, _, _ = kh.get_median_count(record.sequence)
        if med < COV:
            kh.consume(record.sequence)
            kept += 1
        else:
            discard += 1

        print total, kept, discard

if __name__ == '__main__':
    main()
