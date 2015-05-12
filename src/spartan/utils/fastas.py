# fastas.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 5/2/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
fastas.py
=================================================
Purpose:

"""
import collections
import gzip
import os
import sys
import tempfile
import math
from spartan.utils.errors import InvalidFileFormatError, SanityCheckError
from spartan.utils.externals import run_external_app
from spartan.utils.misc import fold_seq

__author__ = 'Gus Dunn'


class ParseFastA(object):
    """Returns a record-by-record fastA parser analogous to file.readline()."""
    def __init__(self, filePath, joinWith='', key=None):
        """Returns a record-by-record fastA parser analogous to file.readline().
        Exmpl: parser.next()
        Its ALSO an iterator so "for rec in parser" works too!

        <joinWith> is string to use to join rec lines with.
        joinWith='' results in a single line with no breaks (usually what you want!)

        <key> is func used to parse the recName from HeaderInfo.
        """

        if filePath.endswith('.gz'):
            self._file = gzip.open(filePath)
        else:
            self._file = open(filePath, 'rU')

        if key:
            self._key = key
        else:
            self._key = lambda x:x[1:].split()[0]
        self.bufferLine = None   # stores next headerLine between records.
        self.joinWith = joinWith
        self._stop = False

    def __iter__(self):
        return self

    def __next__(self):
        """Reads in next element, parses, and does minimal verification.
        Returns: tuple: (seqName,seqStr)"""
        if not self._stop:
            pass
        else:
            raise StopIteration
        # ++++ Get A Record ++++
        recHead = ''
        recData = []
        # ++++ Check to see if we already have a headerLine ++++
        if self.bufferLine:
            recHead = self.bufferLine
        else:
        # ++++ If not, seek one ++++
            while 1:
                try:
                    line = next(self._file)
                except StopIteration:
                    self._stop = True
                    break
                if line.startswith('>'):
                    recHead = line
                    break
                elif not line:
                    raise InvalidFileFormatError("CheckFastaFile: Encountered EOF before any data.")
                elif line == '\n':
                    continue
                else:
                    raise InvalidFileFormatError('CheckFastaFile: The first line containing text does not start with ">".')
        # ++++ Collect recData ++++
        while 1:
            try:
                line = next(self._file)
            except StopIteration:
                self._stop = True
                break
            if line.startswith('>'):
                self.bufferLine = line.strip('\n')
                break
            elif not line.startswith('>'):
                recData.append(line.strip('\n'))

        # ++++ Minor Seq Validation ++++
        ## AddHere
        # ++++ Format Rec For Return ++++
        if not recData:
            recHead = self._key(recHead)
            return (recHead,'')
        else:
            recHead = self._key(recHead)
            return (recHead,self.joinWith.join(recData))

    def to_dict(self):
        """Returns a single Dict populated with the fastaRecs
        contained in self._file."""
        fasDict = {}
        while 1:
            try:
                fasRec = next(self)
            except StopIteration:
                break
            if fasRec:
                if not fasRec[0] in fasDict:
                    fasDict[fasRec[0]] = fasRec[1]
                else:
                    raise InvalidFileFormatError("DuplicateFastaRec: %s occurs in your file more than once.")
            else:
                break
        return fasDict

    def rewrite_headers(self, outPath, lineLen=70, delim=' ', order=[], ow=False, chmod=755):
        """
        PURPOSE
        * reorganize the headers of a fasta file:
          >supercontig:CpipQ1:supercont3.1:1:3873040:1 supercontig supercont3.1
          to
          >supercont3.1 supercontig:CpipQ1:supercont3.1:1:3873040:1 supercontig

        NOTES
        1) If ow, ignores outPath
        2) delim is what to spilt on
        3) order is a list of index numbers from the original header, reorganized for the new header.
           Exp: delim=' ',order=[2,0,1]  would produce what is seen above.
        4) chmod= set new file with this mode (exp: 755)
        5) lineLen sets fastaSeq line length in new file.
        """

        if ow:
            outPath = tempfile.NamedTemporaryFile(suffix='.renamed.fas')
        else:
            outPath = open(outPath, 'w')

        while 1:
            try:
                f = next(self)
            except StopIteration:
                break
            fSplit  = f[0].lstrip('>').rstrip('\n').split(delim)
            newHead = delim.join([fSplit[x] for x in order])
            outPath.write('>%s\n%s\n' % (newHead, '\n'.join(fold_seq(f[1], lineLen))))

        self._file.close()

        absPath = os.path.abspath
        if ow:
            outPath.flush()
            outPath.delete = False
            os.rename(absPath(outPath.name), absPath(self._file.name))

            try:
                chmodResult = run_external_app('chmod', '%s %s' % (chmod, absPath(self._file.name)))
            except ExternalError as err:
                sys.stderr.write('%s\n' % (err))
        else:
            try:
                outPath.close()
                chmodResult = run_external_app('chmod', '%s %s' % (chmod, absPath(outPath.name)))
            except ExternalError as err:
                sys.stderr.write('%s\n' % (err))


def rename_fasta_headers(in_path, out_path, header_func):
    """



    :param in_path: path to original fasta file
    :param out_path: path to future altered fasta file
    :param header_func: function to take a header line and return an altered string version of it

    :returns: `None`


    GIVEN:
        - in_path
        - out_path
        - header_func
    DOES:
        - Reads in in_path file one line at a time
        - If the line is a fasta header (starts with '>')
          uses header_func logic to rearrange the header and
          writes out the changed line to out_path.
        - If not a header, writes same line out to out_path.
        - Closes both file objects.
    RETURNS:
        - None
    """

    in_file = open(in_path,'rU')
    out_file = open(out_path,'w')

    for line in in_file:
        if line.startswith('>'):
            line = header_func(line)
            # Handle and ensure that each modified line has one and only one \n
            line = line.rstrip('\n') + '\n'
        else:
            pass

        out_file.write(line)

    in_file.close()
    out_file.close()


def fastaRec_length_indexer(fastaFiles):
    """
    GIVEN:
    1) fastaFiles: list of fasta files or dirs containing fasta files

    DO:
    1) iterate through all fasta files recording recName and length to a dict

    RETURN:
    1) dict with recName and lengths

    NOTES:
    1) will complain if it sees more than one fastaRec with the same name ONLY
       if one of the length values disagrees with those already seen.
    """
    recDict = {}
    seqDict = {}
    tmpDict = collections.defaultdict(list)

    for each in fastaFiles:
        try:
            # if each is a directory, measure all recs in all fasta files in that dir (ignore subdirs)
            paths = os.listdir(each)
            for p in paths:
                try:
                    p = ParseFastA(p)
                    for name,seq in p:
                        tmpDict[name].append(len(seq))
                        seqDict[name] = seq
                except IOError:
                    # most likely p was a dir, ignore
                    ## TODO: logging code here to inform when this happens
                    pass
                except InvalidFileFormatError:
                    # most likely p did not have valid fasta format, ignore
                    ## TODO: logging code here to inform when this happens
                    pass

        except OSError as errTxt:
            if not ('Not a directory' in errTxt):
                raise
            else:
                # if each is a file, measure all recs in file
                try:
                    p = ParseFastA(each)
                    for name,seq in p:
                        tmpDict[name].append(len(seq))
                        seqDict[name] = seq
                except InvalidFileFormatError:
                    # most likely p did not have valid fasta format, ignore
                    ## TODO: logging code here to inform when this happens
                    pass


    for rec,lengths in tmpDict.items():
        if not (len(set(lengths)) == 1):
            # SANITY_CHECK: make sure that any duplicate fastaRecs gave the same length, if not: complain and die
            raise SanityCheckError("Encountered fastaRec with lengths that do not agree: %s:%s" % (rec,lengths))
        else:
            # consolodate the lengths lists to a single number
            recDict[rec] = lengths[0]

    return (recDict,seqDict)


def count_fasta_recs_in_file(fasta_path):
    """
    Returns number of records contained in a fasta file.

    :param fasta_path: Path to fasta file
    """
    return len(list(ParseFastA(fasta_path).to_dict().keys()))


def divide_fasta_file(fasta_path, divide_by=2, out_path_base=None):
    """
    Returns tuple of paths to resulting files.
    Splits and writes out records in ``fasta_path`` to new files.
    Default ``out_path_base`` derived from ``fasta_path``.

    :param fasta_path: Path to fasta file
    :param divide_by: Number of files to divide the fasta records into
    :param out_path_base: Base path for resulting fasta files

    """
    assert isinstance(divide_by, int)

    num_fastas = count_fasta_recs_in_file(fasta_path)
    recs_per_file = math.ceil(num_fastas/divide_by)

    out_paths = []

    ext = '.fas'
    if out_path_base is None:
        out_path_base, ext = os.path.splitext(fasta_path)

    out_path_template = "{out_base}.{file_num}{ext}"
    fasta_seq_template = ">{header}\n{seq_lines}\n"

    for index, (header, seq) in enumerate(ParseFastA(fasta_path).to_dict().items()):

        # create a switch after every `recs_per_file` records that opens a new file for writing
        if index % recs_per_file == 0:
            current_out_path = out_path_template.format(out_base=out_path_base,
                                                        file_num=index,
                                                        ext=ext)
            # Record out_path
            out_paths.append(current_out_path)

            # Close current file if it exists
            try:
                out_file.close()
            except NameError:
                pass

            # create new out_file with current path
            out_file = open(current_out_path, 'w')

        # with this fasta dict item,
        # fold seqs into '\n' delimited string
        # append to new header
        # write to file

        seq_lines = fold_seq(seq, lineLen=100)

        fasta_record = fasta_seq_template.format(header=header,
                                                 seq_lines='\n'.join(seq_lines))
        out_file.write(fasta_record)

    return out_paths




