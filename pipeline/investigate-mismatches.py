#! /usr/bin/env python
import sys
import argparse
import khmer
import screed

C=20
CUTOFF=3


def add_n_posns(posns, sequence):
    loc = sequence.find('N')
    p = set(posns)

    while loc > -1:
        p.add(loc)
        loc = sequence.find('N', loc + 1)

    return list(sorted(p))


# read in list of error positions per read
def read_pos_file(filename, ignore_set):
    for line in open(filename):
        line = line.strip()
        try:
            read, posns = line.split(' ', 2)
        except ValueError:
            read = line
            posns = []

        if read in ignore_set:
            posns = []
        elif posns:
            if posns is 'V':            # ignore variable coverage foo
                ignore_set.add(read)
                posns = []
            else:
                posns = list(sorted(map(int, posns.split(','))))

        yield read, posns


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('readsfile')
    parser.add_argument('samposfile')
    parser.add_argument('khfile')
    parser.add_argument('-V', '--variable', default=False, action='store_true')
    
    args = parser.parse_args()

    print >>sys.stderr, 'loading posdict'
    ignore_set = set()
    posdict = dict(read_pos_file(args.samposfile, ignore_set))

    print >>sys.stderr, 'loading kh'
    kh = khmer.load_counting_hash(args.khfile)
    K = kh.ksize()

    count = 0
    for record in screed.open(args.readsfile):
        if record.name in posdict:
            posns2 = posdict[record.name]
            
            seq = record.sequence.replace('N', 'A')
            posns1 = kh.find_spectral_error_positions(seq, CUTOFF)
            posns1 = add_n_posns(posns1, record.sequence)

            if posns1 != posns2:
                count += 1
                
                print record.name, posns1, posns2

                sys.stdout.write(record.sequence)
                sys.stdout.write('\n')
                for i in range(len(seq)):
                    if i in posns1:
                        sys.stdout.write('X')
                    else:
                        sys.stdout.write(' ')
                sys.stdout.write('\n')
                    
                for i in range(len(seq)):
                    if i in posns2:
                        sys.stdout.write('Z')
                    else:
                        sys.stdout.write(' ')
                sys.stdout.write('\n')
                    
                for i in range(len(seq) - K + 1):
                    if kh.get(seq[i:i+K]) < CUTOFF:
                        sys.stdout.write('*')
                    else:
                        sys.stdout.write(' ')
                sys.stdout.write('\n')
                print ''
                
        if count > 1000:
            break


if __name__ == '__main__':
    main()
