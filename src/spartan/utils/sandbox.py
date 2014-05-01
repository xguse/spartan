from string import Template
from collections import deque
from decimal import Decimal

import pandas as pd

from spartan.utils.errors import *
from spartan.utils.misc import Bunch,fold_seq





def meme_minimal2transfac(meme_path,out_path):
    """
    """
    
    meme_deck = deque(open(meme_path,'rU'))
    #raise Exception
    transfac_out = open(out_path,'w')
    
    
    try:
        while meme_deck:
            motif = Bunch()
            
            try:
                motif.names = get_next_names(meme_deck)
                motif.matrix = get_next_matrix(meme_deck)
                motif.url = get_next_url(meme_deck)
                
                write_next_transfac_motif(motif,transfac_out)
            
            except StopIteration:
                raise
    except Exception as exc:
        if len(meme_deck) == 0:
            pass
        else:
            raise exc
    finally:
        transfac_out.close()



def get_next_names(meme_deck):
    
    while meme_deck:
        line = meme_deck.popleft()
        if line.startswith('MOTIF'):
            return line.strip().split()[1:]
        else:
            # chew through lines until we find the next MOTIF
            pass


def get_next_matrix(meme_deck):
    
    matrix = []
    mat_info = Bunch()
    
    # collect mat_info
    while meme_deck:
        line = meme_deck.popleft()
        if line.startswith('letter-probability matrix:'):
            line = line.strip().replace('letter-probability matrix:','').replace('= ','=').split()
            for attr in line:
                attr = attr.split('=')
                mat_info[attr[0]] = attr[1]
            break
        else:
            # chew through lines until we find the next matrix data
            pass
    
    # collect matrix data
    while meme_deck:
        line = meme_deck.popleft()
        if line.startswith('\n'):
            break
        else:
            position = pd.Series([Decimal(i) for i in line.strip().split()],index=['A','C','G','T'])
            matrix.append(position)
    
    # confirm correct length
    if len(matrix) == int(mat_info.w):
        matrix = pd.DataFrame(matrix)
    else:
        raise SanityCheckError('length of matrix (%s) does not equal "w" attribute (%s) from "letter-probability matrix" line.' 
                               % (len(matrix),mat_info.w))
       
    # convert probabilities into counts
    matrix = (matrix.applymap(lambda x: round(x,5)) * int(mat_info.nsites)).applymap(int)
    
    # confirm all positions sum to the same value
    #if len(set(matrix.sum(1))) == 1:
        #pass
    #else:
        #raise SanityCheckError('all positions in matrix should sum to the same value. Encountered:\n%s' % (str(matrix.sum(1))))
    return matrix

def get_next_url(meme_deck):
    
    while meme_deck:
        line = meme_deck.popleft()
        if line.startswith('URL'):
            return line.strip().split()[-1]
        else:
            # chew through lines till we get to 'URL'
            pass
        
def write_next_transfac_motif(motif,transfac_out):
    """
      AC accession number
      ID any_old_name_for_motif_1
      BF species_name_for_motif_1
      P0      A      C      G      T
      01      1      2      2      0      S
      02      2      1      2      0      R
      03      3      0      1      1      A
      04      0      5      0      0      C
      05      5      0      0      0      A
      06      0      0      4      1      G
      07      0      1      4      0      G
      08      0      0      0      5      T
      09      0      0      5      0      G
      10      0      1      2      2      K
      11      0      2      0      3      Y
      12      1      0      3      1      G
      XX
      //
    """
    
    name = motif.names[1]
    
    ac = '_'.join(motif.names)
    species = 'none_listed' #TODO: handle species field 
    
    #TODO: write a REAL consensus function that uses IUPAC degen code
    
    matrix_line = Template('MA\t$pos\t$A\t$C\t$G\t$T\t$major_nuc\n')
    
    #transfac_out.write('AC %s\n' % (ac))
    #transfac_out.write('XX\n')
    transfac_out.write('NA\t%s\n' % (name))
    #transfac_out.write('XX\n')
    transfac_out.write('BF\t%s\n' % (species))
    #transfac_out.write('P0\tA\tC\tG\tT\n')
    transfac_out.write('XX\n')
    
    for i in list(motif.matrix.index):
        m = motif.matrix
        fields = dict(pos='%02d' % (i+1),
                      A=m.ix[i,'A'],
                      C=m.ix[i,'C'],
                      G=m.ix[i,'G'],
                      T=m.ix[i,'T'],
                      major_nuc=m.ix[i].idxmax())
        
        transfac_out.write(matrix_line.substitute(fields))
    #transfac_out.write('XX\n')
    #transfac_out.write('CC %s\n' % (motif.url))
    transfac_out.write('XX\n//\n')
        
    
    
    
    