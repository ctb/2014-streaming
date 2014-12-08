#! /usr/bin/env python
import sys
import argparse
import screed
import cPickle

def ignore_at(iter):
    for item in iter:
        if item.startswith('@'):
            continue
        yield item

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('genome')
    parser.add_argument('samfile')
    parser.add_argument('coverage_d_pickle')
    parser.add_argument('covhist')
    args = parser.parse_args()

    coords_d = {}
    for record in screed.open(args.genome):
        coords_d[record.name] = [0]*len(record.sequence)
        
    n = 0
    n_skipped = 0

    for samline in ignore_at(open(args.samfile)):
        n += 1
        if n % 10000 == 0:
            print >>sys.stderr, '...', n

        readname, _, refname, refpos, _, _, _, _, _, seq = samline.split()[:10]
        if refname == '*' or refpos == '*':
            # (don't count these as skipped.)
            continue
        
        refpos = int(refpos)
        try:
            coord = coords_d[refname]
            for pos in range(len(seq)):
                coord[refpos - 1 + pos] += 1
        except KeyError:
            print >>sys.stderr, "unknown refname: %s; ignoring (read %s)" % (refname, readname)
            n_skipped += 1
            continue

    if n_skipped / float(n) > .01:
        raise Exception, "Error: too many reads ignored! %d of %d" % \
              (n_skipped, n)

    # now, calculate coverage per read!
    coverage_d = {}
    total = 0.
    n = 0
    for samline in ignore_at(open(args.samfile)):
        readname, _, refname, refpos, _, _, _, _, _, seq = samline.split()[:10]
        if refname == '*' or refpos == '*':
            # (don't count these as skipped.)
            continue
        
        refpos = int(refpos)
        try:
            coord = coords_d[refname]
        except KeyError:
            continue

        slice = list(coord[refpos - 1:refpos - 1 + len(seq)])
        slice = sorted(slice)
        coverage = slice[len(slice)/2]  # median

        assert readname not in coverage_d, readname
        coverage_d[readname] = coverage
        total += coverage
        n += 1
        if n % 10000 == 0:
            print >>sys.stderr, '...', n

    print 'average of the median mapping coverage', total / float(n)
    print 'min coverage by read', min(coverage_d.values())
    print 'max coverage by read', max(coverage_d.values())

    covhist_d = {}
    sofar = 0
    for v in coverage_d.values():
        v = int(v + 0.5)
        covhist_d[v] = covhist_d.get(v, 0) + 1

    fp = open(args.covhist, 'w')

    total = sum(covhist_d.values())
    sofar = 0
    for k in range(0, max(covhist_d.keys()) + 1):
        v = covhist_d.get(k, 0)
        sofar += v
        print >>fp, k, v, sofar, sofar / float(total)
        
    fp.close()

    fp = open(args.coverage_d_pickle, 'w')
    cPickle.dump(coverage_d, fp)
    fp.close()

if __name__ == '__main__':
    main()
