

def benjHochFDR(pVals,pValColumn=1):
    """
    pVals      = 2D list(hypothesis,p-value) hypothesis could = geneName tested for enrichment
    pValColumn = integer of column index containing the p-value.
    
    returns _ALL_ items passed to it with no filtering at the moment.
    """
    assert type(pValColumn) == type(1),\
           "ERROR: pValColumn must be int type!"
    # Sort pVals from highest to lowest after converting them all to floats.
    for i in range(len(pVals)):
        pVals[i][pValColumn] = float(pVals[i][pValColumn])
    pVals.sort(key=lambda x: x[pValColumn])
    pVals.reverse()
    
    n = len(pVals)
    
    lastPval = pVals[0][pValColumn]
    for i in range(len(pVals)):
        p    = pVals[i][pValColumn]
        adj  = (float(n)/(n-i))
        adjP = p*adj
        miN  = min(adjP,lastPval)
        pVals[i].append(miN)
        lastPval = pVals[i][-1]
    
    pVals.reverse()
    return pVals