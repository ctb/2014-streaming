#! /usr/bin/env python
import sys
import screed
import khmer
import argparse

MAX_SEQ_LEN = 5000


def add_n_posns(posns, sequence):
    loc = sequence.find('N')
    p = set(posns)

    while loc > -1:
        p.add(loc)
        loc = sequence.find('N', loc + 1)
            
    return list(sorted(p))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('table')
    parser.add_argument('sequences')
    parser.add_argument('-C', '--cutoff', default=3, type=int)
    parser.add_argument('--coverage', default=20, type=int)
    parser.add_argument('-V', '--variable', default=False, action='store_true')
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'),
                        default=sys.stdout)

    args = parser.parse_args()

    kh = khmer.load_counting_hash(args.table)
    n_skipped_variable = 0
    n_total = 0

    positions = [0] * MAX_SEQ_LEN
    lengths = []

    print >>sys.stderr, "K:", kh.ksize()
    print >>sys.stderr, "CUTOFF:", args.cutoff
    if args.variable:
        print >>sys.stderr, "variable coverage flag set;"
        print >>sys.stderr, "NORMALIZE_LIMIT:", args.coverage
    else:
        print >>sys.stderr, "assuming even coverage - no -V"

    for n, record in enumerate(screed.open(args.sequences)):
        if n % 100000 == 0:
            print >>sys.stderr, '...', n
        seq = record.sequence.replace('N', 'A')

        n_total += 1

        varskip = False
        if args.variable:
            med, _, _ = kh.get_median_count(seq)
            if med < args.coverage:
                varskip = True
                n_skipped_variable += 1
            
        if not varskip:
            posns = kh.find_spectral_error_positions(seq, args.cutoff)
            for p in posns:
                positions[p] += 1
            lengths.append(len(seq))

    if args.variable:
        sys.stderr.write('Skipped %d reads of %d total due to -V\n' % \
                         (n_skipped_variable, n_total))

    # normalize for length
    lengths.sort()
    max_length = lengths[-1]

    length_count = [0]*max_length
    for j in range(max_length):
        length_count[j] = sum([1 for i in lengths if i >= j])

    # write!
    args.outfile.write('position error_count error_fraction\n')
    for n, i in enumerate(positions[:max_length]):
        print >>args.outfile, n, i, float(i) / float(length_count[n])
        

if __name__ == '__main__':
   main()
   
