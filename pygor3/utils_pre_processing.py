# pre-processing script for sequence alignment through pyir

import os
import subprocess
import numpy as np
import pandas as pd
from .IgorIO import IgorTask
from .utils import get_fasta_from_dataframe

def from_igor_chain_to_receptor( IgorChainName ) :
    if IgorChainName.startswith("TR") :
        receptor = "TCR"
    elif IgorChainName.startswith("IG") :
        receptor = "Ig"
    else :
        raise Exception( 'Unrecognized Igor chain name: %s' % IgorChainName )
    return receptor

def PreProcessTask( igortask, full_blast_info=False, keep_stop_codon=False, igdata=None, verbose=False ):
        
    '''
    It aligns sequences through IgBlast to return only the relavant for Igor inference.
    
    Parameters :
    ------------
    
    igortask : class IgorTask()
        IgorTask class on which to perform the pre processing.

    full_blast_info : bool
        Keep all IgBlast alignment informations. Default is False.

    keep_stop_codon : bool
        Include inframe vj with stopping codons in the preprocessed file.

    igdata : str, optional
        Path to your custom IGDATA directory.

    verbose : bool
        Provide all passages description.   
    '''        
        
    pr_pr_batchname = f"{igortask.igor_wd}/pre_process/{igortask.igor_batchname}-pr_pr"
    os.makedirs(pr_pr_batchname, exist_ok=True)

    if verbose is True : 
        print ( 'Loading indexed sequences...' )
    get_fasta_from_dataframe( reads_data_frame=igortask.igor_read_seqs, 
                            batchname=pr_pr_batchname )
    if verbose is True : 
        print ( 'Aligning sequences...' )
    
    specie = igortask.igor_species
    receptor = from_igor_chain_to_receptor(igortask.igor_chain)
    Align_Seqs( specie=specie, receptor=receptor, pr_pr_batchname=pr_pr_batchname, igdata=igdata )
    if verbose is True : 
        print ( 'Selecting sequences for Igor inference...' )
        if keep_stop_codon is True :            
            print( 'Out of frame vj and inframe vj with stopping codons are considered.' )
        else :
            print( 'Only out of frame vj are considered.' )
             
    igortask.raw_read_seqs = igortask.read_seqs.copy()
    igortask.read_seqs = Process_Seqs( pr_pr_batchname=pr_pr_batchname, 
                                            full_blast_info=full_blast_info, 
                                            keep_stop_codon=keep_stop_codon )
    if verbose : 
        print( 'Preprocessing completed.\n' )

def Align_Seqs( specie, receptor, pr_pr_batchname, igdata=None ):
    '''
    Call pyir wrap of IgBLAST to perform sequence alignment.
    ''' 

    filein = f"{pr_pr_batchname}.fasta"
    fileout = f"{pr_pr_batchname}-full_blast"

    # define the pre-installed pyir command for alignment
    # WARNING!: pyir must be installed
    args = ["pyir", filein, "-o", fileout, "--outfmt", "tsv", "-r", receptor, "-s", specie]
    if igdata != None :
        if self.verbose :
            print( 'Considering custom igdata at:\n%s' % igdata )
        args.append( ["--igdata", igdata] ) 
    # Run the terminal instruction of pyir within Python
    results = subprocess.run( args, capture_output=True )
    # WARNING!: is there a more elegant way of showing preprocessing error?
    if results.returncode : 
        raise RuntimeError( results.stderr )
    # get rid of the temporary fasta file
    os.remove( filein )     

def Process_Seqs( pr_pr_batchname, full_blast_info=False, keep_stop_codon=False ):
    '''
    It takes PyIR output and translates into a csv working file.
    '''

    filein = f"{pr_pr_batchname}-full_blast.tsv.gz"

    # open temporary igblast alignment file
    aligned = pd.read_csv( filein, sep="\t", compression="gzip", dtype=str, index_col=['sequence_id'] ) 
    keep = ["sequence", "vj_in_frame", "productive"]
    aligned = aligned[ keep ]
    # choose which igblast output to consider
    if keep_stop_codon is True :            
        mask = aligned[ ~ aligned["productive"] ]
    else :
        mask = aligned[ ~ aligned["vj_in_frame"] ]
    processed = aligned[mask].copy()
    del aligned

    # remove temporary igblast alignment file
    if full_blast_info == True : 
        print( )
    else : 
        os.remove( filein )       
   
    processed.to_csv( f'{pr_pr_batchname}.csv.gz', columns=["sequence"], compression="gzip" )     
    return processed