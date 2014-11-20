#! /usr/bin/env python
import sys
import argparse
import screed

def ignore_at(iter):
    for item in iter:
        if item.startswith('@'):
            continue
        yield item

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('genome')
    parser.add_argument('samfile')
    parser.add_argument('readfile')
    args = parser.parse_args()

    genome_dict = dict([ (record.name, record.sequence) for record in \
                        screed.open(args.genome) ])

    n = 0
    for samline in ignore_at(open(args.samfile)):
        n += 1
        if n % 10000 == 0:
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
                errors.append(pos)

        print readname, ",".join(map(str, errors))

if __name__ == '__main__':
    main()
