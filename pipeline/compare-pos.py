#! /usr/bin/env python
import argparse

def read_pos_file(filename):
    for line in open(filename):
        line = line.strip()
        try:
            read, posns = line.split(' ', 2)
            posns = map(int, posns.split(','))
        except ValueError:
            continue
#            read = line
#            posns = []
            
        yield read, posns

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pos_a')
    parser.add_argument('pos_b')
    args = parser.parse_args()

    a = dict(read_pos_file(args.pos_a))
    b = dict(read_pos_file(args.pos_b))

    n = 0
    m = 0
    unexplained = 0
    for k, va in a.iteritems():
        n += 1
        vb = b.get(k)
        if vb:
            if va[0] in vb:
                m += 1
            elif 100 - va[0] - 1 in vb:
                m += 1
            elif min(vb) < 20 or max(vb) > 80:
                pass
            else:
                print k, va, vb
                unexplained += 1

    o = 0
    for k, vb in b.iteritems():
        if len(vb):
            o += 1

    print m, n, o, unexplained
    print args.pos_a, len(a), n
    print args.pos_b, len(b), o

if __name__ == '__main__':
    main()
