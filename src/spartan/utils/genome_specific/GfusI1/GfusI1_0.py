# GfusI1.0.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 11/19/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
GfusI1_0.py
=================================================
Purpose:

"""
__author__ = 'Gus Dunn'

from spartan.utils.fastas import ParseFastA
import re


#### ----- Rename VCF file's chrom names to `ScaffoldX` where needed  <BEGIN> ----- ####
def get_name_map_from_fasta_headers(fasta_path):
    """
    Use fasta headers to learn which names need to be re-mapped and make the map.
    :param fasta_path:
    :return: Dictionary of name mappings

    """

    name_map = {}

    scaffold = "genomic scaffold Scaffold"

    fasta_recs = ParseFastA(fasta_path, key=lambda x: x[1:]).to_dict()

    headers = list(fasta_recs.keys())

    for header in headers:
        if scaffold in header:
            header = header.split()
            name1 = header[0]
            name2 = header[7].rstrip(',')

            name_map[name1] = name2

        else:
            header = header.split()
            name1 = header[0]
            name_map[name1] = name1

    return name_map


def is_vcf_chrom_header(line):
    """
    Returns ``True`` if ``line`` is a VCF chrom-definition header line, ``False`` otherwise.

    :param line: line from VCF file
    :return: ``bool``
    """

    if line.startswith('##contig='):
        return True
    else:
        return False


def is_vcf_call_line(line):
    """
    Returns ``True`` if ``line`` is a VCF SNP call line, ``False`` otherwise.

    :param line: line from VCF file
    :return: ``bool``
    """

    if line.startswith('##contig='):
        return True
    else:
        return False


def replace_chrom_name_in_header(line, name_map):
    """
    Replaces the Chrom name from header.
    Returns new header.

    :param line: line from VCF
    :param name_map: name-mapping dict
    :return: new header line
    """


    old_name = re.split('=|,', line)[2]

    return line.replace(old_name, name_map[old_name])


def replace_chrom_name_in_call_line(line, name_map):
    """
    Replaces the Chrom name from call line.
    Returns new call line.

    :param line: line from VCF
    :param name_map: name-mapping dict
    :return: new call line
    """

    # split on whitespace THEN ':',
    # bc not all VCF will have the source_file:Chrom_Name structure
    old_name = line.split()[0].split(':')[-1]
    fields_not_first = line.split()[1:]
    new_name = name_map[old_name]
    new_line = "%s\t%s\n" % (new_name, '\t'.join(fields_not_first))

    return new_line


def change_vcf_chrom_names(in_path, out_path, name_map):
    """
    Writes new VCF file as it changes the chrom names based on ``name_map``.

    :param in_path: path to in file
    :param out_path: path to out file
    :param name_map: name_map to use
    :return: ``None``
    """
    in_file = open(in_path,'rU')
    out_file = open(out_path, 'w')

    for line in in_file:

        if line.startswith('#'):
            if is_vcf_chrom_header(line):
                out_file.write(replace_chrom_name_in_header(line, name_map))
            else:
                out_file.write(line)

        else:
            out_file.write(replace_chrom_name_in_call_line(line, name_map))

    in_file.close()
    out_file.close()

#### ----- Rename VCF file's chrom names to `ScaffoldX` where needed  <END> ----- ####
