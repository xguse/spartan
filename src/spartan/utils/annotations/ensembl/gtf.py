from collections import OrderedDict

from spartan.utils.misc import Bunch

def parse_ensembl_gtf_attributes_string(attribute_string):
    """
    """
    
    attributes = attribute_string.rstrip().rstrip(';').split(';')
    
    attrib_dict = OrderedDict()
    
    for attrib in attributes:

        attrib = attrib.rstrip().rstrip('"').split('"')
        key = attrib[0].strip()
        val = attrib[1]
        attrib_dict[key] = val
        
    return attrib_dict

def write_ensembl_gtf_attributes_string(attrib_dict):
    """
    """
    attrib_string = []
    
    for key,value in attrib_dict.items():
        attrib_string.append('''%s "%s";''' % (key,value))
    
    return ' '.join(attrib_string)

def no_common_names_in_ensembl_gtf(gtf_in,gtf_out):
    """
    replace 'gene_id' value with 'nearest_ref' (wo the isoform tags) in the GTF file
    so that we can only have to know the AAEL, AGAP, CPIJ IDs to get our genes.
    Writes new file.
    """
    
    gtf_in = open(gtf_in,'rU')
    gtf_out = open(gtf_out,'w')
    
    for line in gtf_in:
        line = line.strip('\n').split('\t')
        
        # get atrribute string
        attrib_string = line[-1]
        
        # parse into an ordered dict and replace gene_id with accession type ID from nearest_ref field
        attrib_dict = parse_ensembl_gtf_attributes_string(attrib_string)
        attrib_dict['gene_id'] = attrib_dict['nearest_ref'].split('-')[0]
        
        # convert back to attribute string and replace the original attributes field in `line`
        attrib_string = write_ensembl_gtf_attributes_string(attrib_dict)
        line[-1] = attrib_string
        
        # make it string again and write the line out to the new gtf file
        line = '\t'.join(line)
        gtf_out.write('%s\n' % (line))
        
    gtf_in.close()
    gtf_out.close()
        