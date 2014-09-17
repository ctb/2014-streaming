#! /usr/bin/env python
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mutfile')
    parser.add_argument('posfile')

    args = parser.parse_args()

    d = {}
    for line in open(args.mutfile):
        name, pos = line.split()[:2]
        x = d.get(name, [])
        x.append(int(pos))
        d[name] = x

    outfp = open(args.posfile, 'w')
    for k in d:
        posns = map(str, sorted(d[k]))
        outfp.write('%s %s\n' % (k, ",".join(posns)))
    outfp.close()

if __name__ == '__main__':
    main()
