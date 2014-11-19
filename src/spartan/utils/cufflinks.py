import csv

from collections import defaultdict

from spartan.utils.annotations.ensembl import gtf


def get_ensembl_from_gene_name(gene_names_path,cuffmerge_gtf_path,out_file_path):
    """
    See also: the gtf.py
    """
    
    gene_names = [ line.strip('\n') for line in open(gene_names_path,'rU')]
    
    reader = csv.reader(open(cuffmerge_gtf_path,'rU'),delimiter='\t',quotechar='"')
    
    name_maps = {}
    
    # ensembl location seems to be 'oId' and 'nearest_ref' in attributes field
    # gene nam/symbol/short_name/etc seems to be 'gene_name'
    # extract attribute key/value pairs
    
    for rec in reader:
        attributes = gtf.parse_attributes(rec[-1])

        gene_name   = attributes['gene_name']
        oId         = attributes['oId']
        nearest_ref = attributes['nearest_ref']

            
        name_maps[gene_name] = '%s\t%s' % (oId,nearest_ref)
    
    # query name_maps with provided gene_names and write results to file
    out_file = open(out_file_path,'w')
    for name in gene_names:
        
        try:
            out_line = '%s\t%s\n' % (name,name_maps[name])
        except KeyError:
            out_line = '%s\tNot Found\n' % (name)
        
        out_file.write(out_line)
        
def get_XLOC_to_nearest_ref_map(merged_gtf,kind='gene'):
    """
    kind ~ ['gene','full']
    """
    
    merged_gtf = open(merged_gtf,'rU')
    
    name_maps = defaultdict(set)
    
    for line in merged_gtf:
        line = line.strip('\n').split('\t')
        
        # get atrribute dict
        attrib_string = line[-1]
        attrib_dict = gtf.parse_ensembl_gtf_attributes_string(attrib_string)
        
        xloc = attrib_dict['gene_id']
        
        if kind == 'gene':
            nearest = attrib_dict['nearest_ref'].split('-')[0]
        elif kind == 'full':
            nearest = attrib_dict['nearest_ref']
            
        name_maps[xloc].add(nearest)
        name_maps[nearest].add(xloc)
    
    # we dont want the final data type to be sets
    for xloc,nearest_set in name_maps.iteritems():
        name_maps[xloc] = ','.join(sorted(list(nearest_set)))
    
    return XLOCmapping(dict(name_maps))

class XLOCmapping(dict):
    """
    """
    def __init__(self,arg={}):
        dict.__init__(self,arg)
    
    def __getitem__(self,key):
        """
        define custom getter to allow handeling certain snafus like KeyError
        """
        try:
            return dict.__getitem__(self,key)
        except (KeyError,):
            return key     
    
