#!/usr/bin/env python

# count_oligos_at_slice_of_seq.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 2/25/15.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
count_oligos_at_slice_of_seq.py
=================================================
Purpose:

"""
__author__ = 'Gus Dunn'

import sys
import os
import gzip

from collections import defaultdict

import argparse


class ParseFastQ(object):
    """Returns a read-by-read fastQ parser analogous to file.readline()"""
    def __init__(self,filePath,headerSymbols=['@','+']):
        """Returns a read-by-read fastQ parser analogous to file.readline().
        Exmpl: parser.next()
        -OR-
        Its an iterator so you can do:
        for rec in parser:
            ... do something with rec ...

        rec is tuple: (seqHeader,seqStr,qualHeader,qualStr)
        """
        if filePath.endswith('.gz'):
            self._file = self._open_gzip_or_not(filePath)
        else:
            self._file = open(filePath, 'rU')
        self._currentLineNumber = 0
        self._hdSyms = headerSymbols
        
    def __iter__(self):
        return self

    def _open_gzip_or_not(self, filename):
        f = open(filename,'rb')
        if (f.read(2) == '\x1f\x8b'):
            f.seek(0)
            return gzip.GzipFile(fileobj=f)
        else:
            f.seek(0)
            return f

    def next(self):
        """Reads in next element, parses, and does minimal verification.
        Returns: tuple: (seqHeader,seqStr,qualHeader,qualStr)"""
        # ++++ Get Next Four Lines ++++
        elemList = []
        for i in range(4):
            line = self._file.readline()
            self._currentLineNumber += 1 ## increment file position
            if line:
                elemList.append(line.strip('\n'))
            else: 
                elemList.append(None)
        
        # ++++ Check Lines For Expected Form ++++
        trues = [bool(x) for x in elemList].count(True)
        nones = elemList.count(None)
        # -- Check for acceptable end of file --
        if nones == 4:
            raise StopIteration
        # -- Make sure we got 4 full lines of data --
        assert trues == 4,\
               "** ERROR: It looks like I encountered a premature EOF or empty line.\n\
               Please check FastQ file near line number %s (plus or minus ~4 lines) and try again**" % (self._currentLineNumber)
        # -- Make sure we are in the correct "register" --
        assert elemList[0].startswith(self._hdSyms[0]),\
               "** ERROR: The 1st line in fastq element does not start with '%s'.\n\
               Please check FastQ file near line number %s (plus or minus ~4 lines) and try again**" % (self._hdSyms[0],self._currentLineNumber) 
        assert elemList[2].startswith(self._hdSyms[1]),\
               "** ERROR: The 3rd line in fastq element does not start with '%s'.\n\
               Please check FastQ file near line number %s (plus or minus ~4 lines) and try again**" % (self._hdSyms[1],self._currentLineNumber) 
        # -- Make sure the seq line and qual line have equal lengths --
        assert len(elemList[1]) == len(elemList[3]), "** ERROR: The length of Sequence data and Quality data of the last record aren't equal.\n\
               Please check FastQ file near line number %s (plus or minus ~4 lines) and try again**" % (self._currentLineNumber) 
        
        # ++++ Return fatsQ data as tuple ++++
        return tuple(elemList)
    
    def get_next_readSeq(self):
        """Convenience method: calls self.next and returns only the readSeq."""
        try:
            record = self.next()
            return record[1]
        except StopIteration:
            return None
        
    def filter_SEfastQ_headings(self,filteredPath,key=None):
        """
        Iterates through a single-end fastQ file and writes only those recs
        that satisfy the <key> lambda func to <filteredPath>.
        """
        fastqLen = 0
        filteredLen = 0
        
        if key == None:
            key = lambda x: x
        filtered = open(filteredPath, 'w')
        
        while 1:
            try:
                qRec = self.next()
                fastqLen += 1
            except StopIteration:
                break
            
            if key(qRec[0]) == True:
                for line in qRec:
                    filtered.write('%s\n' % (line))
                    filteredLen += 1
            elif key(qRec[0]) == False:
                pass
            else:
                raise UnexpectedValueError("ERROR: in ParseFastQ.filter_fastQ_headings() 'key' returned a non-T/F value.")
        
        filtered.flush()
        filtered.close()
        
        return Bag({"path":os.path.abspath(filtered.name),
                "original":fastqLen,
                "filtered":filteredLen})




def count_oligo_slices(fastq_path, first=0, last=-1):

    records = ParseFastQ(fastq_path)

    oligo_count = defaultdict(int)

    for rec in records:
        oligo = rec[1][first:last]
        oligo_count[oligo] += 1

    return oligo_count




def write_table(oligos, out_path):
    template = "{oligo}\t{count}\n"
    
    with open(out_path,'w') as out:
        for oligo, count in oligos.iteritems():
            
            out.write(template.format(oligo=oligo, count=count))


def get_files(dir_path):
    fastq_names = []
    for name in os.listdir(dir_path):
        if name.upper().endswith(".FASTQ") or name.upper().endswith(".FASTQ.GZ"):
            fastq_names.append(name)

    return fastq_names





def main():
    """
    The main loop.  Lets ROCK!
    """

    desc = """This script takes a directory and slice coordinates for fastq reads as arguments.
    It loops through each *.fastq or *.fastq.gz file in that directory, counts all oligos it finds at
    the slice coords and writes the results to a file named "ORIGINAL_FILE_NAME.start_end_count.tsv". """

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-s', '--start', type=int, default=0, 
                        help="""Slice start coordinate (NOTE: uses python slicing logic). (default: %(default)s)""")

    parser.add_argument('-e', '--end', type=int, default=-1, 
                        help="""Slice end coordinate (NOTE: uses python slicing logic). (default: %(default)s)""")

    
    parser.add_argument('-d','--dir', type=str, default=".",
                        help="""Path to a directory that hopefully contains at least one fastq file. (default: %(default)s)""")
    


    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    args = parser.parse_args()

    fastq_names = get_files(args.dir)

    count_name_template = "{fastq_name}.{start}_{end}_count.tsv"

    for fastq in fastq_names:
        count_name = count_name_template.format(fastq_name=fastq, 
                                                start=args.start, 
                                                end=args.end
                                                )
        # assemble in and out paths
        fastq_path = os.path.join(args.dir,fastq)
        out_path = os.path.join(args.dir,count_name)

        # do the counting
        try:
            oligo_counts = count_oligo_slices(fastq_path=fastq_path, 
                                              first=args.start, 
                                              last=args.end
                                              )
        except IOError:
            print "-!- WARNING: file ({file}) was not processed because it is not actually a gzipped file.".format(file=fastq_path)
            continue
        except AssertionError:
            print "-!- WARNING: file ({file}) was not able to be processed; it may be corrupted.".format(file=fastq_path)

        # write the outfile
        write_table(oligos=oligo_counts, out_path=out_path)

        # Comfort you that things are happening
        print "Completed file: {file}".format(file=out_path)





if __name__ == '__main__':
    main()