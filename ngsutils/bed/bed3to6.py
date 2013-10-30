#!/usr/bin/env python
## category Conversion
## desc Convert a BED3 file to a BED6 file
'''
Convert a BED3 file to a BED6 file with constant name, score, and strand.
(This can also be used to replace values in a BED6 file)
'''

import os
import sys
from ngsutils.bed import BedFile


def usage():
    print __doc__
    print """\
Usage: bedutils bed3to6 {-name val} {-score val} {-strand val} bedfile

"""
    sys.exit(1)


def bed_bed3to6(bed, name=None, score=None, strand=None, out=sys.stdout):
    for region in bed:
        region.name = name if name else '%s:%s-%s' % (region.chrom, region.start, region.end)
        region.score = score if score else ''
        region.strand = strand if strand else ''
        region.write(out)

if __name__ == '__main__':
    fname = None
    name = None
    score = None
    strand = None

    last = None

    for arg in sys.argv[1:]:
        if arg == '-h':
            usage()
        if last == '-name':
            name = arg
            last = None
        elif last == '-score':
            score = arg
            last = None
        elif last == '-strand':
            strand = arg
            last = None
        elif arg in ['-name', '-score', '-strand']:
            last = arg
        elif not fname and (os.path.exists(arg) or arg == '-'):
            fname = arg
        else:
            print "Unknown option: %s" % arg
            usage()

    if not fname:
        usage()

    bed_bed3to6(BedFile(fname), name=name, score=score, strand=strand)
