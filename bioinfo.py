#!/usr/bin/python

# codes in "bioinfo" are under the MIT License
# Copyright (c) 2013 Jean-Etienne Morlighem <jem.nvnt@gmail.com>
# https://github.com/jem-gh/bioinfo



from __future__ import division

import re           # for "transcribe" (assertion)
from string import maketrans        # for "complement"



def countNucleotides(seq):
    """ simple nucleotide counting function for DNA or RNA sequences without 
        gap nor nucleotide ambiguity """
    
    if not seq:
        print "countNucleotides: no sequence provided"
        return None
    
    assert isinstance(seq, str)
    
    seq = seq.lower()
    
    a = seq.count('a')
    c = seq.count('c')
    g = seq.count('g')
    t = seq.count('t')
    u = seq.count('u')
    
    if t and u:
        print "countNucleotides: both T and U found in the sequence"
        return False
    
    assert (a + c + g + t == len(seq)) or (a + c + g + u == len(seq))
    
    print "countNucleotides result:"
    print "{:>5} {:>5} {:>5} {:>5} {:>5}".format("A","C","G","T","U")
    print "{:>5} {:>5} {:>5} {:>5} {:>5}".format(a,c,g,t,u)
    
    return a, c, g, t, u



def transcribe(seq):
    """ Transcribed a DNA sequence into its corresponding RNA sequence """
    
    if not seq:
        print "transcribe: no sequence provided"
        return None
    
    assert isinstance(seq, str) and countNucleotides(seq)
    
    seq = seq.lower()
    
    if "u" in seq:
        print "transcribe: U already in the sequence"
        return False
    
    result = seq.replace("t", "u")
    
    assert ([pos.start() for pos in re.finditer("t", seq)] == 
            [pos.start() for pos in re.finditer("u", result)])
    
    print "transcribe result:"
    print result
    
    return result



def GCcontent(seq):
    """ return the GC content in % of a nucleotide sequence """
    
    if not seq:
        print "GCcontent: no sequence provided"
        return None
    
    assert isinstance(seq, str)
    
    try:
        a,c,g,t,u = countNucleotides(seq)
    except TypeError:
        print "GCcontent: sequence not valid"
        return False
    
    result = (c + g) / (a + c + g + t + u) * 100
    
    # due to the Python floating-point approximation issue, assertion is made 
    # by comparing results to an acceptable error margin
    assert abs(result + ((a+t+u)/(a+c+g+t+u)*100) - 100) <= 0.00000000001
    
    print "GCcontent result:"
    print result
    
    return result



def complement(seq):
    """ return the complement of a DNA or RNA sequence """
    
    if not seq:
        print "complement: no sequence provided"
        return None
    
    assert isinstance(seq, str)
    
    try:
        a,c,g,t,u = countNucleotides(seq)
    except TypeError:
        print "complement: sequence not valid"
        return False
    
    in_seq, out_seq  = ("acgu", "ugca") if u else ("acgt", "tgca")
    result = seq.lower().translate(maketrans(in_seq, out_seq))
    
    assert countNucleotides(result) in [(t, g, c, a, u), (u, g, c, t, a)]
    
    print "complement result:"
    print result
    
    return result



def reverse_complement(seq):
    """ return the reverse complement of a DNA or RNA sequence """
    
    if not seq:
        print "reverse_complement: no sequence provided"
        return None
    
    assert isinstance(seq, str)
    
    result_c = complement(seq)
    if result_c:
        result_rc = result_c[::-1]
    else:
        print "reverse_complement: sequence not valid"
        return False
    
    assert complement(result_rc)[::-1] == seq.lower()
    
    print "reverse_complement result:"
    print result_rc
    
    return result_rc



