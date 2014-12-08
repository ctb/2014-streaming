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
    
    all_reads = 0
    sum_bp = 0

    print 'reading sequences...'
    for n, record in enumerate(screed.open(args.reads)):
        if n % 100000 == 0:
            print >>sys.stderr, '...', n
        all_reads += 1
        sum_bp += len(record.sequence)

    print 'done!'

    n = 0
    m = 0
    for k, v in posdict.iteritems():
        if not v:
            continue

        n += 1
        m += len(v)

    print 'posfile %s: %d mutated reads of %d; %d mutations total' % \
          (args.posfile, n, all_reads, m)
    print '%d bp total' % (sum_bp,)
    print 'overall error rate: %f%%' % (100. * m / float(sum_bp))

    
if __name__ == '__main__':
    main()


