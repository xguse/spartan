from collections import defaultdict

import pandas as pd

import networkx as nx



def get_uniprot2gene_map(dataframe):
    """
    assumes: dataframe = dataframe.fillna('empty')
    """
    my_columns = dataframe[['Gene','UniProt']]
    
    u2g_map = defaultdict(set)
    
    for row in my_columns.itertuples():
        idx,gene,uniprot = row
        
        u2g_map[uniprot].add(gene)
        
    for u,g in u2g_map.items():
        u2g_map[u] = sorted(list(g))
        
    return dict(u2g_map)
    
    
def get_gene2uniprot_map(dataframe):
    """
    assumes: dataframe = dataframe.fillna('empty')
    """
    my_columns = dataframe[['Gene','UniProt']]
    
    g2u_map = defaultdict(set)
    
    for row in my_columns.itertuples():
        idx,gene,uniprot = row
        
        g2u_map[gene].add(uniprot)
        
    for g,u in g2u_map.items():
        g2u_map[g] = sorted(list(u))
        
    return dict(g2u_map)