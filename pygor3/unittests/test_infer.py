import unittest
from pygor3 import IgorTask
from pygor3 import IgorModel
from pygor3 import IgorRefGenome
from pygor3 import generate
from pygor3 import infer
from pygor3 import evaluate_pgen
import pandas as pd
from pygor3 import v_genLabel



str_mock_VDJ_fln_genomicVs = \
""">TRBV1*01
GATACTGGAATTACCCAGACACCAAAATACCTGGTCACAGCAATGGGGAGTAAAAGGACA
ATGAAACGTGAGCATCTGGGACATGATTCTATGTATTGGTACAGACAGAAAGCTAAGAAA
TCCCTGGAGTTCATGTTTTACTACAACTGTAAGGAATTCATTGAAAACAAGACTGTGCCA
AATCACTTCACACCTGAATGCCCTGACAGCTCTCGCTTATACCTTCATGTGGTCGCACTG
CAGCAAGAAGACTCAGCTGCGTATCTCTGCACCAGCAGCCAAGA
>TRBV2*01
GAACCTGAAGTCACCCAGACTCCCAGCCATCAGGTCACACAGATGGGACAGGAAGTGATC
TTGCGCTGTGTCCCCATCTCTAATCACTTATACTTCTATTGGTACAGACAAATCTTGGGG
CAGAAAGTCGAGTTTCTGGTTTCCTTTTATAATAATGAAATCTCAGAGAAGTCTGAAATA
TTCGATGATCAATTCTCAGTTGAAAGGCCTGATGGATCAAATTTCACTCTGAAGATCCGG
TCCACAAAGCTGGAGGACTCAGCCATGTACTTCTGTGCCAGCAGTGAAGC
>TRBV2*02
GAACCTGAAGTCACCCAGACTCCCAGCCATCAGGTCACACAGATGGGACAGGAAGTGATC
TTGCACTGTGTCCCCATCTCTAATCACTTATACTTCTATTGGTACAGACAAATCTTGGGG
CAGAAAGTCGAGTTTCTGGTTTCCTTTTATAATAATGAAATCTCAGAGAAGTCTGAAATA
TTCGATGATCAATTCTCAGTTGAAAGGCCTGATGGATCAAATTTCACTCTGAAGATCCGG
TCCACAAAGCTGGAGGACTCAGCCATGTACTTCTGTGCCAGCAGT
>TRBV2*03
GAACCTGAAGTCACCCAGACTCCCAGCCATCAGGTCACACAGATGGGACAGGAAGTGATC
TTGCGCTGTGTCCCCATCTCTAATCACTTATACTTCTATTGGTACAGACAAATCTTGGGG
CAGAAAGTCGAGTTTCTGGTTTCCTTTTATAATAATGAAATCTCAGAGAAGTCTGAAATA
TTCGATGATCAATTCTCAGTTGAGAGGCCTGATGGATCAAATTTCACTCTGAAGATCCGG
TCCACAAAGCTGGAGGACTCAGCCATGTACTTCTGTGCCAGCAGTGAA
>TRBV3-1*01
GACACAGCTGTTTCCCAGACTCCAAAATACCTGGTCACACAGATGGGAAACGACAAGTCC
ATTAAATGTGAACAAAATCTGGGCCATGATACTATGTATTGGTATAAACAGGACTCTAAG
AAATTTCTGAAGATAATGTTTAGCTACAATAATAAGGAGCTCATTATAAATGAAACAGTT
CCAAATCGCTTCTCACCTAAATCTCCAGACAAAGCTCACTTAAATCTTCACATCAATTCC
CTGGAGCTTGGTGACTCTGCTGTGTATTTCTGTGCCAGCAGCCAAGA
>TRBV3-1*02
GACACAGCTGTTTCCCAGACTCCAAAATACCTGGTCACACAGATGGGAAACGACAAGTCC
ATTAAATGTGAACAAAATCTGGGCCATGATACTATGTATTGGTATAAACAGGACTCTAAG
AAATTTCTGAAGATAATGTTTAGCTACAATAACAAGGAGATCATTATAAATGAAACAGTT
CCAAATCGATTCTCACCTAAATCTCCAGACAAAGCTAAATTAAATCTTCACATCAATTCC
CTGGAGCTTGGTGACTCTGCTGTGTATTTCTGTGCCAGC
>TRBV3-2*01
GACACAGCCGTTTCCCAGACTCCAAAATACCTGGTCACACAGATGGGAAAAAAGGAGTCT
CTTAAATGAGAACAAAATCTGGGCCATAATGCTATGTATTGGTATAAACAGGACTCTAAG
AAATTTCTGAAGACAATGTTTATCTACAGTAACAAGGAGCCAATTTTAAATGAAACAGTT
CCAAATCGCTTCTCACCTGACTCTCCAGACAAAGCTCATTTAAATCTTCACATCAATTCC
CTGGAGCTTGGTGACTCTGCTGTGTATTTCTGTGCCAGCAGCCAAGA
>TRBV3-2*02
GACACAGCCGTTTCCCAGACTCCAAAATACCTGGTCACACAGATGGGAAAAAAGGAGTCT
CTTAAATGAGAACAAAATCTGGGCCATAATGCTATGTATTGGTATAAACAGGACTCTAAG
AAATTTCTGAAGACAATGTTTATCTACAGTAACAAGGAGCCAATTTTAAATGAAACAGTT
CCAAATCGCTTCTCACCTGACTCTCCAGACAAAGTTCATTTAAATCTTCACATCAATTCC
CTGGAGCTTGGTGACTCTGCTGTGTATTTCTGTGCCAGCAGCCAAGA
>TRBV3-2*03
GACACAGCCGTTTCCCAGACTCCAAAATACCTGGTCACACAGACGGGAAAAAAGGAGTCT
CTTAAATGAGAACAAAATCTGGGCCATAATGCTATGTATTGGTATAAACAGGACTCTAAG
AAATTTCTGAAGACAATGTTTATCTACAGTAACAAGGAGCCAATTTTAAATGAAACAGTT
CCAAATCGCTTCTCACCTGACTCTCCAGACAAAGTTCATTTAAATCTTCACATCAATTCC
CTGGAGCTTGGTGACTCTGCTGTGTATTTCTGTGCCAGCAGCCAAG
>TRBV4-1*02
CACCTGGTCATGGGAATGACAAATAAGAAGTCTTTGAAATGTGAACAACATATGGGGCAC
AGGGCAATGTATTGGTACAAGCAGAAAGCTAAGAAGCCACCGGAGCTCATGTTTGTCTAC
AGCTATGAGAAACTCTCTATAAATGAAAGTGTGCCAAGTCGCTTCTCACCTGAATGCCCC
AACAGCTCTCTCTTAAACCTTCACCTACACGCCCTGCAGCCAGAAGACTCAGCCCTGTAT
CTCTGCGCCAGCAGCCAAG
>TRBV4-2*01
GAAACGGGAGTTACGCAGACACCAAGACACCTGGTCATGGGAATGACAAATAAGAAGTCT
TTGAAATGTGAACAACATCTGGGGCATAACGCTATGTATTGGTACAAGCAAAGTGCTAAG
AAGCCACTGGAGCTCATGTTTGTCTACAACTTTAAAGAACAGACTGAAAACAACAGTGTG
CCAAGTCGCTTCTCACCTGAATGCCCCAACAGCTCTCACTTATTCCTTCACCTACACACC
CTGCAGCCAGAAGACTCGGCCCTGTATCTCTGTGCCAGCAGCCAAGA
>TRBV4-2*02
GAAACGGGAGTTACGCAGACACCAAGACACCTGGTCATGGGAATGACAAATAAGAAGTCT
TTGAAATGTGAACAACATCTGGGGCATAACGCTATGTATTGGTACAAGCAAAGTGCTAAG
AAGCCACTGGAGCTCATGTTTGTCTACAACTTTAAAGAACAGACTGAAAACAACAGTGTG
CCAAGTCGCTTCTCACCTGAATGCCCCAACAGCTCTCACTTATGCCTTCACCTACACACC
CTGCAGCCAGAAGACTCGGCCCTGTATCTCTGTGCCAGCACC
>TRBV4-3*01
GAAACGGGAGTTACGCAGACACCAAGACACCTGGTCATGGGAATGACAAATAAGAAGTCT
TTGAAATGTGAACAACATCTGGGTCATAACGCTATGTATTGGTACAAGCAAAGTGCTAAG
AAGCCACTGGAGCTCATGTTTGTCTACAGTCTTGAAGAACGGGTTGAAAACAACAGTGTG
CCAAGTCGCTTCTCACCTGAATGCCCCAACAGCTCTCACTTATTCCTTCACCTACACACC
CTGCAGCCAGAAGACTCGGCCCTGTATCTCTGCGCCAGCAGCCAAGA
>TRBV4-3*02
GAAACGGGAGTTACGCAGACACCAAGACACCTGGTCATGGGAATGACAAATAAGAAGTCT
TTGAAATGTGAACAACATCTGGGTCATAACGCTATGTATTGGTACAAGCAAAGTGCTAAG
AAGCCACTGGAGCTCATGTTTGTCTACAGTCTTGAAGAACGGGTTGAAAACAACAGTGTG
CCAAGTCGCTTCTCACCTGAATGCCCCAACAGCTCTCACTTATCCCTTCACCTACACACC
CTGCAGCCAGAAGACTCGGCCCTGTATCTCTGCGCCAGCAGC
>TRBV4-3*03
GAAACGGGAGTTACGCAGACACCAAGACACCTGGTCATGGGAATGACAAATAAGAAGTCT
TTGAAATGTGAACAACATCTGGGTCATAACGCTATGTATTGGTACAAGCAAAGTGCTAAG
AAGCCACTGGAGCTCATGTTTGTCTACAGTCTTGAAGAACGTGTTGAAAACAACAGTGTG
CCAAGTCGCTTCTCACCTGAATGCCCCAACAGCTCTCACTTATTCCTTCACCTACACACC
CTGCAGCCAGAAGACTCGGCCCTGTATCTCTGCGCCAGCAGC
>TRBV4-3*04
AAGAAGTCTTTGAAATGTGAACAACATCTGGGGCATAACGCTATGTATTGGTACAAGCAA
AGTGCTAAGAAGCCACTGGAGCTCATGTTTGTCTACAGTCTTGAAGAACGGGTTGAAAAC
AACAGTGTGCCAAGTCGCTTCTCACCTGAATGCCCCAACAGCTCTCACTTATTCCTTCAC
CTACACACCCTGCAGCCAGAAGACTCGGCCCTGTATCTCTGCGCCAGCAGC
>TRBV5-1*01
AAGGCTGGAGTCACTCAAACTCCAAGATATCTGATCAAAACGAGAGGACAGCAAGTGACA
CTGAGCTGCTCCCCTATCTCTGGGCATAGGAGTGTATCCTGGTACCAACAGACCCCAGGA
CAGGGCCTTCAGTTCCTCTTTGAATACTTCAGTGAGACACAGAGAAACAAAGGAAACTTC
CCTGGTCGATTCTCAGGGCGCCAGTTCTCTAACTCTCGCTCTGAGATGAATGTGAGCACC
TTGGAGCTGGGGGACTCGGCCCTTTATCTTTGCGCCAGCAGCTTGG
>TRBV5-1*02
AGGGCTGGGGTCACTCAAACTCCAAGACATCTGATCAAAACGAGAGGACAGCAAGTGACA
CTGGGCTGCTCCCCTATCTCTGGGCATAGGAGTGTATCCTGGTACCAACAGACCCTAGGA
CAGGGCCTTCAGTTCCTCTTTGAATACTTCAGTGAGACACAGAGAAACAAAGGAAACTTC
CTTGGTCGATTCTCAGGGCGCCAGTTCTCTAACTCTCGCTCTGAGATGAATGTGAGCACC
TTGGAGCTGGGGGACTCGGCCCTTTATCTTTGCGCCAGC
>TRBV5-2*01
GAGGCTGGAATCACCCAAGCTCCAAGACACCTGATCAAAACAAGAGACCAGCAAGTGACA
CTGAGATGCTCCCCTGCCTCTGGGCATAACTGTGTGTCCTGGTACCTACGAACTCCAAGT
CAGCCCCTCTAGTTATTGTTACAATATTGTAATAGGTTACAAAGAGCAAAAGGAAACTTG
CCTAATTGATTCTCAGCTCACCACGTCCATAACTATTACTGAGTCAAACACGGAGCTAGG
GGACTCAGCCCTGTATCTCTGTGCCAGCAACTTGATG
>TRBV5-3*01
GAGGCTGGAGTCACCCAAAGTCCCACACACCTGATCAAAACGAGAGGACAGCAAGTGACT
CTGAGATGCTCTCCTATCTCTGGGCACAGCAGTGTGTCCTGGTACCAACAGGCCCCGGGT
CAGGGGCCCCAGTTTATCTTTGAATATGCTAATGAGTTAAGGAGATCAGAAGGAAACTTC
CCTAATCGATTCTCAGGGCGCCAGTTCCATGACTGTTGCTCTGAGATGAATGTGAGTGCC
TTGGAGCTGGGGGACTCGGCCCTGTATCTCTGTGCCAGAAGCTTGG
>TRBV5-3*02
GAGGCTGGAGTCACCCAAAGTCCCACACACCTGATCAAAACGAGAGGACAGCAAGTGACT
CTGAGATGCTCTCCTATCTCTGGGCACAGCAGTGTGTCCTGGTACCAACAGGCCCCGGGT
CAGGGGCCCCAGTTTATCTTTGAATATGCTAATGAGTTAAGGAGATCAGAAGGAAACTTC
CCTAATCGATTCTCAGGGCGCCAGTTCCATGACTATTGCTCTGAGATGAATGTGAGTGCC
TTGGAGCTGGGGGACTCGGCCCTGTATCTCTGTGCCAGAAGCTTGG
>TRBV5-4*01
GAGACTGGAGTCACCCAAAGTCCCACACACCTGATCAAAACGAGAGGACAGCAAGTGACT
CTGAGATGCTCTTCTCAGTCTGGGCACAACACTGTGTCCTGGTACCAACAGGCCCTGGGT
CAGGGGCCCCAGTTTATCTTTCAGTATTATAGGGAGGAAGAGAATGGCAGAGGAAACTTC
CCTCCTAGATTCTCAGGTCTCCAGTTCCCTAATTATAGCTCTGAGCTGAATGTGAACGCC
TTGGAGCTGGACGACTCGGCCCTGTATCTCTGTGCCAGCAGCTTGG
>TRBV5-4*02
GAGACTGGAGTCACCCAAAGTCCCACACACCTGATCAAAACGAGAGGACAGCAAGTGACT
CTGAGATGCTCTTCTCAGTCTGGGCACAACACTGTGTCCTGGTACCAACAGGCCCTGGGT
CAGGGGCCCCAGTTTATCTTTCAGTATTATAGGGAGGAAGAGAATGGCAGAGGAAACTTC
CCTCCTAGATTCTCAGGTCTCCAGTTCCCTAATTATAACTCTGAGCTGAATGTGAACGCC
TTGGAGCTGGACGACTCGGCCCTGTATCTCTGTGCCAGCAGC
>TRBV5-4*03
CAGCAAGTGACACTGAGATGCTCTTCTCAGTCTGGGCACAACACTGTGTCCTGGTACCAA
CAGGCCCTGGGTCAGGGGCCCCAGTTTATCTTTCAGTATTATAGGGAGGAAGAGAATGGC
AGAGGAAACTTCCCTCCTAGATTCTCAGGTCTCCAGTTCCCTAATTATAGCTCTGAGCTG
AATGTGAACGCCTTGGAGCTGGACGACTCGGCCCTGTATCTCTGTGCCAGCAGC
>TRBV5-4*04
ACTGTGTCCTGGTACCAACAGGCCCTGGGTCAGGGGCCCCAGTTTATCTTTCAGTATTAT
AGGGAGGAAGAGAATGGCAGAGGAAACTCCCCTCCTAGATTCTCAGGTCTCCAGTTCCCT
AATTATAGCTCTGAGCTGAATGTGAACGCCTTGGAGCTGGACGACTCGGCCCTGTATCTC
TGTGCCAGCAGC
>TRBV5-5*01
GACGCTGGAGTCACCCAAAGTCCCACACACCTGATCAAAACGAGAGGACAGCAAGTGACT
CTGAGATGCTCTCCTATCTCTGGGCACAAGAGTGTGTCCTGGTACCAACAGGTCCTGGGT
CAGGGGCCCCAGTTTATCTTTCAGTATTATGAGAAAGAAGAGAGAGGAAGAGGAAACTTC
CCTGATCGATTCTCAGCTCGCCAGTTCCCTAACTATAGCTCTGAGCTGAATGTGAACGCC
TTGTTGCTGGGGGACTCGGCCCTGTATCTCTGTGCCAGCAGCTTGG
>TRBV5-5*02
GACGCTGGAGTCACCCAAAGTCCCACACACCTGATCAAAACGAGAGGACAGCACGTGACT
CTGAGATGCTCTCCTATCTCTGGGCACAAGAGTGTGTCCTGGTACCAACAGGTCCTGGGT
CAGGGGCCCCAGTTTATCTTTCAGTATTATGAGAAAGAAGAGAGAGGAAGAGGAAACTTC
CCTGATCGATTCTCAGCTCGCCAGTTCCCTAACTATAGCTCTGAGCTGAATGTGAACGCC
TTGTTGCTGGGGGACTCGGCCCTGTATCTCTGTGCCAGCAGC
>TRBV5-5*03
GACGCTGGAGTCACCCAAAGTCCCACACACCTGATCAAAACGAGAGGACAGCAAGTGACT
CTGAGATGCTCTCCTATCTCTGAGCACAAGAGTGTGTCCTGGTACCAACAGGTCCTGGGT
CAGGGGCCCCAGTTTATCTTTCAGTATTATGAGAAAGAAGAGAGAGGAAGAGGAAACTTC
CCTGATCGATTCTCAGCTCGCCAGTTCCCTAACTATAGCTCTGAGCTGAATGTGAACGCC
TTGTTGCTGGGGGACTCGGCCCTGTATCTCTGTGCCAGCAGC
>TRBV5-6*01
GACGCTGGAGTCACCCAAAGTCCCACACACCTGATCAAAACGAGAGGACAGCAAGTGACT
CTGAGATGCTCTCCTAAGTCTGGGCATGACACTGTGTCCTGGTACCAACAGGCCCTGGGT
CAGGGGCCCCAGTTTATCTTTCAGTATTATGAGGAGGAAGAGAGACAGAGAGGCAACTTC
CCTGATCGATTCTCAGGTCACCAGTTCCCTAACTATAGCTCTGAGCTGAATGTGAACGCC
TTGTTGCTGGGGGACTCGGCCCTCTATCTCTGTGCCAGCAGCTTGG
>TRBV5-7*01
GACGCTGGAGTCACCCAAAGTCCCACACACCTGATCAAAACGAGAGGACAGCACGTGACT
CTGAGATGCTCTCCTATCTCTGGGCACACCAGTGTGTCCTCGTACCAACAGGCCCTGGGT
CAGGGGCCCCAGTTTATCTTTCAGTATTATGAGAAAGAAGAGAGAGGAAGAGGAAACTTC
CCTGATCAATTCTCAGGTCACCAGTTCCCTAACTATAGCTCTGAGCTGAATGTGAACGCC
TTGTTGCTAGGGGACTCGGCCCTCTATCTCTGTGCCAGCAGCTTGG
>TRBV5-8*01
GAGGCTGGAGTCACACAAAGTCCCACACACCTGATCAAAACGAGAGGACAGCAAGCGACT
CTGAGATGCTCTCCTATCTCTGGGCACACCAGTGTGTACTGGTACCAACAGGCCCTGGGT
CTGGGCCTCCAGTTCCTCCTTTGGTATGACGAGGGTGAAGAGAGAAACAGAGGAAACTTC
CCTCCTAGATTTTCAGGTCGCCAGTTCCCTAATTATAGCTCTGAGCTGAATGTGAACGCC
TTGGAGCTGGAGGACTCGGCCCTGTATCTCTGTGCCAGCAGCTTGG
>TRBV5-8*02
AGGACAGCAAGCGACTCTGAGATGCTCTCCTATCTCTGGGCACACCAGTGTGTACTGGTA
CCAACAGGCCCTGGGTCTGGGCCTCCAGCTCCTCCTTTGGTATGACGAGGGTGAAGAGAG
AAACAGAGGAAACTTCCCTCCTAGATTTTCAGGTCGCCAGTTCCCTAATTATAGCTCTGA
GCTGAATGTGAACGCCTTGGAGCTGGAGGACTCGGCCCTGTATCTCTGTGCCAGCAGC
"""
str_mock_VDJ_fln_genomicDs = \
""">TRBD1*01
GGGACAGGGGGC
>TRBD2*01
GGGACTAGCGGGGGGG
>TRBD2*02
GGGACTAGCGGGAGGG
"""
str_mock_VDJ_fln_genomicJs = \
""">TRBJ1-1*01
TGAACACTGAAGCTTTCTTTGGACAAGGCACCAGACTCACAGTTGTAG
>TRBJ1-2*01
CTAACTATGGCTACACCTTCGGTTCGGGGACCAGGTTAACCGTTGTAG
>TRBJ1-3*01
CTCTGGAAACACCATATATTTTGGAGAGGGAAGTTGGCTCACTGTTGTAG
>TRBJ1-4*01
CAACTAATGAAAAACTGTTTTTTGGCAGTGGAACCCAGCTCTCTGTCTTGG
>TRBJ1-5*01
TAGCAATCAGCCCCAGCATTTTGGTGATGGGACTCGACTCTCCATCCTAG
>TRBJ1-6*01
CTCCTATAATTCACCCCTCCACTTTGGGAATGGGACCAGGCTCACTGTGACAG
>TRBJ1-6*02
CTCCTATAATTCACCCCTCCACTTTGGGAACGGGACCAGGCTCACTGTGACAG
>TRBJ2-1*01
CTCCTACAATGAGCAGTTCTTCGGGCCAGGGACACGGCTCACCGTGCTAG
>TRBJ2-2*01
CGAACACCGGGGAGCTGTTTTTTGGAGAAGGCTCTAGGCTGACCGTACTGG
>TRBJ2-2P*01
CTGAGAGGCGCTGCTGGGCGTCTGGGCGGAGGACTCCTGGTTCTGG
>TRBJ2-3*01
AGCACAGATACGCAGTATTTTGGCCCAGGCACCCGGCTGACAGTGCTCG
>TRBJ2-4*01
AGCCAAAAACATTCAGTACTTCGGCGCCGGGACCCGGCTCTCAGTGCTGG
>TRBJ2-5*01
ACCAAGAGACCCAGTACTTCGGGCCAGGCACGCGGCTCCTGGTGCTCG
>TRBJ2-6*01
CTCTGGGGCCAACGTCCTGACTTTCGGGGCCGGCAGCAGGCTGACCGTGCTGG
>TRBJ2-7*01
CTCCTACGAGCAGTACTTCGGGCCGGGCACCAGGCTCACGGTCACAG
>TRBJ2-7*02
CTCCTACGAGCAGTACGTCGGGCCGGGCACCAGGCTCACGGTCACAG
"""
str_mock_VDJ_fln_V_gene_CDR3_anchors = \
"""gene;anchor_index;gfunction
TRBV1*01;267;P
TRBV2*01;273;F
TRBV2*02;273;(F)
TRBV2*03;273;(F)
TRBV3-1*01;270;F
TRBV3-1*02;270;(F)
TRBV3-2*01;270;P
TRBV3-2*02;270;P
TRBV3-2*03;270;(P)
TRBV4-1*01;270;F
TRBV4-1*02;243;(F)
TRBV4-2*01;270;F
TRBV4-2*02;270;(F)
TRBV4-3*01;270;F
TRBV4-3*02;270;(F)
TRBV4-3*03;270;(F)
TRBV4-3*04;219;(F)
TRBV5-1*01;270;F
TRBV5-1*02;270;(F)
TRBV5-2*01;259;P
TRBV5-3*01;270;ORF
TRBV5-3*02;270;ORF
TRBV5-4*01;270;F
TRBV5-4*02;270;(F)
TRBV5-4*03;222;(F)
TRBV5-4*04;180;(F)
TRBV5-5*01;270;F
TRBV5-5*02;270;(F)
TRBV5-5*03;270;(F)
TRBV5-6*01;270;F
TRBV5-7*01;270;ORF
TRBV5-8*01;270;F
TRBV5-8*02;226;(F)
"""
str_mock_VDJ_fln_J_gene_CDR3_anchors = \
"""gene;anchor_index;function
TRBJ1-1*01;17;F
TRBJ1-2*01;17;F
TRBJ1-3*01;19;F
TRBJ1-4*01;20;F
TRBJ1-5*01;19;F
TRBJ1-6*01;22;F
TRBJ1-6*02;22;F
TRBJ2-1*01;19;F
TRBJ2-2*01;20;F
TRBJ2-3*01;18;F
TRBJ2-4*01;19;F
TRBJ2-5*01;17;F
TRBJ2-6*01;22;F
TRBJ2-7*01;16;F
"""

str_mock_VDJ_fln_dict = dict()
str_mock_VDJ_fln_dict['fln_genomicVs'] = str_mock_VDJ_fln_genomicVs
str_mock_VDJ_fln_dict['fln_genomicDs'] = str_mock_VDJ_fln_genomicDs
str_mock_VDJ_fln_dict['fln_genomicJs'] = str_mock_VDJ_fln_genomicJs
str_mock_VDJ_fln_dict['fln_V_gene_CDR3_anchors'] = str_mock_VDJ_fln_V_gene_CDR3_anchors
str_mock_VDJ_fln_dict['fln_J_gene_CDR3_anchors'] = str_mock_VDJ_fln_J_gene_CDR3_anchors



class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.species = "human"
        self.chain = "tcr_beta"
        self.mdl = IgorModel.load_default(self.species, self.chain)
        # mdl = IgorTask.run_generate(return_df=True)
        self.pd_sequences = generate(10, self.mdl)


    def test_infer_VDJ(self):
        # 0. Get your input sequences, in this case generated sequences
        print(self.pd_sequences)
        self.assertIsInstance(self.pd_sequences, pd.DataFrame)

        # 1. Get an IgorRefGenome from imgt website
        hb_ref_genome = IgorRefGenome.load_VDJ_from_IMGT_website("Homo+sapiens", "TRB")
        hb_ref_genome.clean_empty_anchors()
        self.assertIsInstance(hb_ref_genome, IgorRefGenome)

        # 2. Create a Model from a recently downloaded imgt models
        hb_mdl_ini = IgorModel.make_default_model_from_IgorRefGenome(hb_ref_genome)
        self.assertIsInstance(hb_mdl_ini, IgorModel)

        # 3. infer a new model using the initial model.
        new_mdl, df_likelihoods = infer(self.pd_sequences, hb_mdl_ini)
        print(df_likelihoods)
        self.assertIsInstance(df_likelihoods, pd.DataFrame)
        self.assertIsInstance(new_mdl, IgorModel)

    def test_infer_VJ(self):
        # 0. Get your input sequences, in this case generated sequences
        print(self.pd_sequences)
        self.assertIsInstance(self.pd_sequences, pd.DataFrame)

        # 1. Get an IgorRefGenome from imgt website
        hb_ref_genome = IgorRefGenome.load_VJ_from_IMGT_website("Homo+sapiens", "TRB")
        hb_ref_genome.clean_empty_anchors()
        self.assertIsInstance(hb_ref_genome, IgorRefGenome)

        # 2. Create a Model from a recently downloaded imgt models
        hb_mdl_ini = IgorModel.make_default_model_from_IgorRefGenome(hb_ref_genome)
        self.assertIsInstance(hb_mdl_ini, IgorModel)

        # 3. infer a new model using the initial model.
        new_mdl = infer(self.pd_sequences, hb_mdl_ini, batch_clean=False)
        self.assertIsInstance(new_mdl, IgorModel)


    def test_infer_command(self):
        mdl_ini = IgorModel.load_default("human", "tcr_beta")
        print("%"*50)
        mdl_new, df_likelihood = infer(self.pd_sequences, mdl_ini)

    # def tearDown(self) -> None:
    #     self.tmp_dir.cleanup()

    def test_IgorTask_infer(self):
        # TODO: FINISH ME
        task = IgorTask.default_model("human", "tcr_beta")
        task.infer(self.pd_sequences)





if __name__ == '__main__':
    unittest.main()
