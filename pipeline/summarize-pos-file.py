#! /usr/bin/env python
import sys
import argparse
import screed

def read_pos_file(filename):
    for line in open(filename):
        line = line.strip()
        try:
            read, posns = line.split(' ', 2)
            posns = map(int, posns.split(','))
        except ValueError:
            read = line
            posns = []
            
        yield read, posns

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('posfile')
    parser.add_argument('reads')
    args = parser.parse_args()

    print 'reading files...', args.posfile, args.reads
    posdict = dict(read_pos_file(args.posfile))
    all_reads = set([ record.name for record in screed.open(args.reads) ])
    sum_bp = sum([ len(record.sequence) for record in screed.open(args.reads) ])

    n = 0
    m = 0
    for k, v in posdict.iteritems():
        if not v:
            continue

        n += 1
        m += len(v)

    print 'posfile %s: %d mutated reads of %d; %d mutations total' % \
          (args.posfile, n, len(all_reads), m)
    print '%d bp total' % (sum_bp,)
    print 'overall error rate: %f%%' % (100. * m / float(sum_bp))

    
if __name__ == '__main__':
    main()


