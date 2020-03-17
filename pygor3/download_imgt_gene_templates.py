#!/usr/bin/env python3

# get data from IMGT and generate a model
# options.type   = "VDJ"
# options.gene   = "TRB"
# options.species = "Mus+musculus"
import pygor3 as p3

def main():
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options] ")
    parser.add_option("-t", "--type",   dest="type",   help="VJ or VDJ")
    parser.add_option("-c", "--chain",   dest="gene",   help="Type of chain like TRB")
    parser.add_option("-s", "--species", dest="species", help="Type of species")

    (options, args) = parser.parse_args()

    species_list = p3.imgt.get_species_list()
    species_list.remove('')

    if options.species is None:
        print("species is a mandatory option. Please select one species from list:")
        print(species_list)
    else:
        if not (options.species in species_list):
            print("Species not recognized. Please select one species from list:")
            print(species_list)
            exit()

    if options.type == "VDJ":
        flnVGenome = p3.imgt.download_gene_template(options.species, options.chain + 'V')
        flnDGenome = p3.imgt.download_gene_template(options.species, options.chain + 'D')
        flnJGenome = p3.imgt.download_gene_template(options.species, options.chain + 'J')
        # write anchors
        p3.imgt.download_genes_anchors(options.species, options.chain, flnVGenome, flnJGenome)
    elif options.type == "VJ":
        flnVGenome = p3.imgt.download_gene_template(options.species, options.chain + 'V')
        flnJGenome = p3.imgt.download_gene_template(options.species, options.chain + 'J')
        # write anchors
        p3.imgt.download_genes_anchors(options.species, options.chain, flnVGenome, flnJGenome)
        # Now construct the models from a dictionary.

    else:
        print("type not recognized. Please choose VDJ or VJ.")




    # igor_species="human"
    # igor_chain="tcr_beta"
    # mdl = p3.IgorModel.load_default(igor_species, igor_chain)
    #
    # mdl.parms.plot_Graph()
    # mdl.get_events_nicknames_list()
    # mdl.plot_Event_Marginal('v_3_del')
    # mdl.plot_Event_Marginal('v_choice')
    #
    # mdl.xdata['v_choice']


if __name__ == "__main__":
    main()

#mdl.plot_Event_Marginal('v_choice')
# From the loaded model I want a list of event_types


"""
mdl.xdata['d_gene']
mdl.xdata['j_choice']

mdl.xdata['d_gene'].dot( mdl.xdata['j_choice'] )

mdl.xdata['d_3_del'].shape
mdl.xdata['d_3_del'].coords
mdl.xdata['d_3_del'].dims
mdl.xdata['d_3_del']*mdl.xdata['d_5_del']
(mdl.xdata['d_3_del'].dot(mdl.xdata['d_5_del'])).dims
mdl.parms.G['d_3_del']

elist = mdl.parms.Event_list
print(str(elist[0]))
nelist = sorted(elist, key=lambda x:x.priority, reverse=False)

mdl.parms.dictNicknameName.keys()
#0 Define the templates and define model.
# p3.imgt.download_gene(specie, gene)


#0.1 Get templates from IMGT from a list of available templates.
#1 Choose an specie and chain, this means define a model.

iseq = p3.IgorIndexedSequence(10,'ATCTGAGCT')
print(iseq)


mdl = p3.IgorModel.load_default("mouse", "tcr_beta")


#2 Input a sequence
#3 Align the sequence given the model, show the alignment
#3 Give me the pgen of the sequence probability of this sequence.


bs = p3.IgorBestScenariosVDJ()
print(bs)

bs.
"""
