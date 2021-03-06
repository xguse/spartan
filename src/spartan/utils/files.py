#*****************************************************************************
#  files.py (part of the  package)
#
#  (c) 2013 - Augustine Dunn
#  James Laboratory
#  Department of Biochemistry and Molecular Biology
#  University of California Irvine
#  wadunn83@gmail.com
#
#
#******************************************************************************

"""
####################
files.py
####################

"""

import os
import sys
import collections
import gzip
import shutil
import csv

from spartan.utils.errors import *
from spartan.utils.misc import Bunch


def mv_file_obj(fileObj,newPath='',chmod=False):
    """
    GIVEN:
    1) fileObj: file object to be moved 
    2) newPath: new path (if not abs path, current working dir is used)
       MUST at LEAST include a location for new file.
    3) chmod: string to use for new file permissions (if False: no change).
    
    DO:
    1) fileObj.flush()
    2) use shutil.move(src,dest) to move file location.
    3) change fileObj.location to the new location.
    4) if file is tmpFile, make sure fileObj.delete == False
       (I assume that if you care enough to move the file, you want to keep it)
    5) chmod on new file to set permissions (remember to use octal: 0755 NOT 755)
    
    RETURN:
    1) fileObj
    """
    if not 'file' in str(fileObj):
        raise SanityCheckError("fileObj does not seem to be a file-like object: %s" % (str(fileObj)))

    
    try:
        fileObj.delete = False
    except AttributeError:
        pass
    if not fileObj.closed:
        fileObj.close()
    
    if newPath == '':
        newPath = fileObj.name.split('/')[-1]
    if (not newPath.startswith('/')) and (not newPath.startswith('./')) and (not newPath.startswith('../')):
        newPath = './%s' % (newPath)
        
    shutil.move(fileObj.name,newPath)
    
    fileObj.name = os.path.abspath(newPath)
    if not chmod == False:
        os.chmod(fileObj.name,int(chmod))
        
    return fileObj
    

    
    

def filter_PEfastQs(filterFunc,fwdMatePath,revMatePath,matchedPassPath1,matchedPassPath2,singlePassPath,nonPassPath):
    """
    Takes the paths to mated PE fastq files with coordinated read-ordering.
    Tests whether paired reads satisfy the provided filterFunc.
    :param filterFunc:
    :param fwdMatePath:
    :param revMatePath:
    :param matchedPassPath1:
    :param matchedPassPath2:
    :param singlePassPath:
    :param nonPassPath:
    For example fastQs from hudsonAlpha should have either "Y" or "N" flag in their header:
    
    @HWI-ST619:70:B0BMTABXX:3:1102:9652:78621 1:N:0:TAGCTT
    GAATGCGATAGTCACAAGGCATGCCGTTGAATATTCGCAACTGAGCTTCG
    +
    @@@?DAD;DADAD:EGAGH=CFEEHB?GIEBFBGI@CFGD@FG>>@GGGH
    
    The fastQ parsers represent each read as a 4 member list with each line's data as an index.

    
    The filterFunc for this case might be:
    lambda x: x[0].split(' ')[-1].split(':')[1] == "N"
    
    If both mates satisfy the filter, the fwd mate is written to matchedPassPath1 and rev mate to matchedPassPath2.
    If only one mate satisfies the filter, it is written to singlePassPath regardles of fwd/rev.
    All reads that do not satisfy the filter are written to nonPassPath.
    
    Notes:
    * The filterFunc does not have to be a simple lambda, but even something like "testMeanQualScore()",
      as long as it returns a True/False with True meaning that the read should be KEPT.
    * Write-files are overwritten if they exist, created otherwise.
    """
    
    
    fwdMates = ParseFastQ(fwdMatePath)
    revMates = ParseFastQ(revMatePath)
    mPassF_file = open(matchedPassPath1, 'w')
    mPassR_file = open(matchedPassPath2, 'w')
    sPass_file  = open(singlePassPath, 'w')
    nPass_file  = open(nonPassPath, 'w')
    
    outFiles = [mPassF_file,
                mPassR_file,
                sPass_file,
                nPass_file]
    
    counts = Bunch({'pairs_passed':0,
                  'fwd_passed_as_single':0,
                  'rev_passed_as_single':0,
                  'fwd_failed':0,
                  'rev_failed':0,
                  'total':0})
    
    while 1:
        # get next fastq Records or set mates to None
        try:
            fwdMate = fwdMates.next()
            counts.total += 1
        except StopIteration:
            fwdMate = None
        
        try:
            revMate = revMates.next()
            counts.total += 1
        except StopIteration:
            revMate = None
        
        # break out if both files are empty 
        if (fwdMate == None) and (revMate == None):
            break

        # set up logical switches to guide the outWriting/counting
        if fwdMate == None:
            keepFwd = None
        else:
            keepFwd = filterFunc(fwdMate)
        if revMate == None:
            keepRev = None
        else:
            keepRev = filterFunc(revMate)
            
        #print "fwdMate %s\nkeepFwd %s\nrevMate %s\nkeepRev %s" % (fwdMate[0],keepFwd,revMate[0],keepRev)
        #break
            
        # write fwd and rev to appropriate files and += respective counts
        if keepFwd and keepRev:
            mPassF_file.write('%s\n' % ('\n'.join(fwdMate)))
            mPassR_file.write('%s\n' % ('\n'.join(revMate)))
            counts.pairs_passed += 1
        if keepFwd and not keepRev:
            sPass_file.write('%s\n' % ('\n'.join(fwdMate)))
            nPass_file.write('%s\n' % ('\n'.join(revMate)))
            counts.fwd_passed_as_single += 1
            counts.rev_failed += 1
        if not keepFwd and keepRev:
            nPass_file.write('%s\n' % ('\n'.join(fwdMate)))
            sPass_file.write('%s\n' % ('\n'.join(revMate)))
            counts.fwd_failed += 1
            counts.rev_passed_as_single += 1
        if not keepFwd and not keepRev:
            nPass_file.write('%s\n' % ('\n'.join(fwdMate)))
            nPass_file.write('%s\n' % ('\n'.join(revMate)))
            counts.fwd_failed += 1
            counts.rev_failed += 1
    
    for f in outFiles:
        f.close()
    
    reportTxt = '''================
Filtered your files using the supplied filter function:
fwdMatePath:\t\t%s
revMatePath:\t\t%s
matchedPassPath1:\t%s
matchedPassPath2:\t%s
singlePassPath:\t\t%s
nonPassPath:\t\t%s\n----\n''' % (fwdMatePath,revMatePath,matchedPassPath1,matchedPassPath2,singlePassPath,nonPassPath)
    sanityCount = (counts.pairs_passed * 2) + counts.fwd_passed_as_single + counts.rev_passed_as_single + counts.fwd_failed + counts.rev_failed
    if not sanityCount == counts.total:
        reportTxt += "WARNING: sanityCount (%s) does not equal counts.total (%s)\n" % (sanityCount, counts.total)
    reportTxt += "PairsPassed:\t\t%s\nFwdSinglePassed:\t%s\nRevSinglePassed:\t%s\nFwdFailed:\t\t%s\nRevFailed:\t\t%s\n" % (counts.pairs_passed,
                                                                                                                           counts.fwd_passed_as_single,
                                                                                                                           counts.rev_passed_as_single,
                                                                                                                           counts.fwd_failed,
                                                                                                                           counts.rev_failed)
    sys.stderr.write("%s\n" % (reportTxt))
    

#def strip_str_of_comments(string,commentStr='#'):
    #"""
    #Take string and return everything to the right of the first
    #comment string found, unless it is quoted or escaped: '#' or "#" or \#.
    #"""
    #qComStr = """'%s'""" % (commentStr)
    #qqComStr = '''"%s"''' % (commentStr)
    #esqComStr = '\%s' % (commentStr)
    #if """'%s'""" % (commentStr) in string:
        
    #return string.rstrip('/n').split(commentStr)[0]

    
def open_wo_comments(filePath,commentStr):
    """
    Return a generator that acts like fileObj.next() but removes
    both commented lines and in-line comments. 
    
    Preserves line numbers.
    """
    inFile = open(filePath,'rU')
    for line in inFile:
        line = strip_str_of_comments(line)
        yield '%s\n' % (line) # replace \n to preserve the behavior of fileObj.next()



def unSoftMask(inFastaPath,outFastaPath):
    # TODO: replace unSoftMask() with mask_converter() that provides multiple options for changing the masking of sequences
    """
    UPPERcases any lowercased nucs in the fasta recs.
    Writes new file.
    """
    inFasta  = open(inFastaPath, 'rU')
    outFasta = open(outFastaPath, 'w')
    for line in inFasta:
        if line.startswith('>'):
            outFasta.write(line)
        else:
            outFasta.write(line.upper())
    inFasta.close()
    outFasta.close()
    
    
def tableFile2namedTuple(tablePath, sep='\t', headers=None):
    """Returns namedTuple from table file using first row fields as
    col headers or a list supplied by user."""

    reader = csv.reader(open(tablePath, 'rU'), delimiter=sep)
    if not headers:
        headers = [h.lower() for h in reader.next()]
    Table = collections.namedtuple('Table', headers)
    # wrap Table.__getattribute__() for less typing

    def get(self, colName):
        return self.__getattribute__(colName)
    Table.get = get
    
    data = [Table._make(x) for x in reader if x != []]  # reader kept feeding an empty list at the end that botched
    # everything!  wtf?!
    return data


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

    def _open_gzip_or_not(filename):
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
        
def onlyInA(fileA,fileB,outFile):
    """Takes two files. Writes a third file with the lines that are unique to
    fileA.  NOTE: Can be Memory intensive for large files."""
    
    fileA = open(fileA,'rU')
    fileB = open(fileB,'rU')
    
    lineDict = {}
    
    # Get line info
    for line in fileA:
        line = line.strip('\n')
        if line in lineDict:
            lineDict[line][0] += 1
        else:
            lineDict[line] = [1,0]
    
    for line in fileB:
        line = line.strip('\n')
        if line in lineDict:
            lineDict[line][1] += 1
        else:
            lineDict[line] = [0,1]
    
    # write lines unique to fileA
    outFile = open(outFile,'w')
    rLines = 0
    for item in lineDict.iteritems():
        line   = item[0]
        counts = item[1]
        if counts[1] == 0:
            if counts[0] == 1:
                outFile.write('%s\n' % (line))
            elif counts[0] > 1:
                rLines += 1
                outFile.write('%s\n' % (line))
            elif counts[0] == 0:
                raise UnexpectedValueError('It looks like line "%s" does not occur in either file!!\n"lineDict" may have been corrupted.' % \
                                           (line))
        else:
            continue    
    if rLines:
        sys.stderr.write('WARNING: %s lines written to %s occured more than once in %s, but %s is now non-redundant.' %\
                         (rLines,outFile.name,fileA.name,outFile.name))
    outFile.close()
        


    
def renameChrom_in_SAM(path):
    """
    """
    import fileinput
    path = os.path.abspath(path)
    bkExt = ".zap_me.backup"
    bkPath = path + bkExt
    
    try:
        for line in fileinput.input(files=path, inplace=1, backup=bkExt,
                                    bufsize=0,mode="r", openhook=None):
            if line.startswith('@SQ'):
                line = line.split('\t')
                chrm = "SN:%s" % (line[1].split(':')[3])
                line[1] = chrm
                sys.stdout.write('\t'.join(line))
            elif line.startswith('HWI'):
                line = line.split('\t')
                chrm = line[2].split(':')[2]
                line[2] = chrm
                sys.stdout.write('\t'.join(line))
            else:
                sys.stdout.write(line)
    except:
        raise



