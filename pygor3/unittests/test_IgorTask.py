import unittest
from pygor3 import *
import subprocess
import tempfile
import shutil

class MyTestCase(unittest.TestCase):
    null_task = IgorTask()
    # null_task.update_ref_genome()
    # null_task.update_model_filenames()
    # null_task.update_ref_genome()
    # null_task.update_batch_filenames()
    # null_task.update_batchname()

    null_genomes = IgorRefGenome()
    # null_genomes.update_fln_names()


    # Sequences generation
    def test__run_generate(self):
        # _run_generate : IGoR's generating process all files preserved, until _run_clean_batch_generated
        # is executed.
        igor_wd_dirname = "igor_wd_temporario"
        task = IgorTask.default_model("human", "beta", igor_wd=igor_wd_dirname)
        self.assertIsInstance(task.mdl, IgorModel)
        self.assertIsInstance(task.mdl.parms, IgorModel_Parms)

        fln_list = task._run_generate(10)

        df = get_dataframe_from_generated_files(task.igor_fln_generated_seqs_werr)
        print("df.columns: ", df.columns)
        print(df, len(df))
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(len(df) == 10)
        task._run_clean_batch_generate()
        task._run_clean_batch_mdldata()
        subprocess.run("rmdir " +igor_wd_dirname, shell=True)

    def test__run_generate_pass_options(self):
        igor_wd_dirname = "igor_wd_temporario"
        task = IgorTask.default_model("human", "beta", igor_wd=igor_wd_dirname)

        self.assertIsInstance(task.mdl, IgorModel)
        self.assertIsInstance(task.mdl.parms, IgorModel_Parms)
        task.igor_generate_dict_options['--CDR3']['active'] = True
        task.igor_generate_dict_options['--seed']['active'] = True
        task.igor_generate_dict_options['--seed']['value'] = 10
        fln_list = task._run_generate(10)
        df = get_dataframe_from_generated_files(task.igor_fln_generated_seqs_werr)
        print("df.columns: ", df.columns)
        print(df, len(df))

        len_nt_sequence = len(df.loc[0]['nt_sequence'])
        print(len_nt_sequence)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(len(df) == 10)

        task._run_clean_batch_generate()
        task._run_clean_batch_mdldata()
        subprocess.run("rmdir " + igor_wd_dirname, shell=True)

        print(task.igor_generate_dict_options)

    def test__run_generate_from_mdl(self):
        mdl = IgorModel.load_default("human", "tcr_beta")
        task = IgorTask()
        task.mdl = mdl
        task._run_generate(10)
        df = get_dataframe_from_generated_files(task.igor_fln_generated_seqs_werr)
        print("df.columns: ", df.columns)
        print(df)
        task._run_clean_batch_mdldata()
        task._run_clean_batch_generate()

    def test_generate(self):
        """
        generate is a wrapper to _run_generate in IgorTask that delete
        sequences generated files
        """
        Nseqs = 10
        task = IgorTask.default_model("human", "beta", igor_wd="joder")
        df = task.generate(Nseqs)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(len(df)==Nseqs)
        task._update_output_batch_filenames()
        task._update_mdldata_batch_filenames()
        subprocess.run("rmdir joder", shell=True)

    def test_generate_TemporaryDirectory(self):
        with tempfile.TemporaryDirectory(prefix='igor_generating_', dir='.') as tmp_generate_dirname:
            task = IgorTask.default_model("human", "beta", igor_wd=tmp_generate_dirname)
            df = task.generate(10)
            self.assertIsInstance(df, pd.DataFrame)

    def test_pygor3_generate(self):
        Nseqs = 10
        mdl = IgorModel.load_default("human", "tcr_beta")
        self.assertIsInstance(mdl, IgorModel)
        df = generate(Nseqs, mdl)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(len(df) == Nseqs)
        # print(df)
        fln_tmp_input_sequence = 'input_sequences_dfds.csv'
        with open(fln_tmp_input_sequence, 'w') as archivo_temporal:
            write_sequences_to_file(df, archivo_temporal)
        subprocess.run("rm " + fln_tmp_input_sequence, shell=True)

    # def test__run_align(self):
    #     self.null_task.run_align()
    #     self.null_task._run_generate()
    #     self.assertTrue(False)
    #
    # def test_null_mdldata_dir(self):
    #     self.assertIsNone(self.null_task.igor_mdldata_dir)
    #     self.null_task.write_mdldata_dir()
    #     # self.null_task.write_mdldata_dir()

    # infer model
    def test__run_infer(self):
        """Run inference task and use the method to clean only the inference part."""
        igor_wd_dirname = "igor_wd_temporario"
        task = IgorTask.default_model("human", "beta", igor_wd=igor_wd_dirname)
        self.assertIsInstance(task.mdl, IgorModel)
        self.assertIsInstance(task.mdl.parms, IgorModel_Parms)
        print("before: igor_read_seqs : ", task.igor_read_seqs)
        print("before: igor_fln_generated_seqs_werr : ", task.igor_fln_generated_seqs_werr)
        self.assertTrue(task.igor_read_seqs is None)
        self.assertTrue(task.igor_fln_generated_seqs_werr is None)

        task._run_generate(10)

        print("after: igor_read_seqs : ", task.igor_read_seqs)
        print("after: igor_fln_generated_seqs_werr : ", task.igor_fln_generated_seqs_werr)
        self.assertTrue(task.igor_read_seqs is None)
        self.assertFalse(task.igor_fln_generated_seqs_werr is None)

        task.igor_read_seqs = task.igor_fln_generated_seqs_werr


        # Now infer new model with sequences
        # task._update_mdldata_batch_filenames()
        mdl = task._run_infer()

        task._run_clean_batch_infer()
        task._run_clean_batch_aligns()
        self.assertIsInstance(mdl, IgorModel)

        task._run_clean_batch_generate()
        # task.run_clean_batch()
        task._run_clean_batch_mdldata()
        shutil.rmtree(igor_wd_dirname)

    def test_infer(self):
        igor_wd_dirname = "igor_wd_temporario"
        task = IgorTask.default_model("human", "beta", igor_wd=igor_wd_dirname)
        pd_sequences = task.generate(10)
        mdl_new = task.infer(pd_sequences)
        print("task.igor_read_seqs: ", task.igor_read_seqs)
        self.assertIsInstance(mdl_new, IgorModel)
        task._run_clean_batch_infer()
        task._run_clean_batch_aligns()
        task._run_clean_batch_mdldata()
        print("task.igor_read_seqs: ", task.igor_read_seqs)

        self.assertTrue(mdl_new, IgorModel)

    def test_pygor3_infer(self):
        igor_wd_dirname = "igor_wd_temporario"
        mdl = IgorModel.load_default("human", "tcr_beta")
        pd_sequences = generate(10, mdl=mdl)
        mdl_new, df_likelihoods = infer(pd_sequences, mdl=mdl)
        # mdl_new.plot_Bayes_network('archivo.pdf')
        self.assertIsInstance(mdl_new, IgorModel)
        self.assertIsInstance(df_likelihoods, pd.DataFrame)


    def test__run_evaluate(self):
        # TODO: Modify run evaluate as infer and generate.
        igor_wd_dirname = "igor_wd_temporario"

        mdl = IgorModel.load_default("human", "tcr_beta")
        pd_sequences = generate(10, mdl=mdl)

        task = IgorTask(mdl=mdl)
        task._run_evaluate()
        # task.evaluate()
        task.igor_fln_generated_seqs_werr
        # aaa = evaluate(pd_sequences, mdl=mdl)
        # print(aaa)

    def test_null_task(self):
        print(self.null_task.igor_wd)
        self.assertTrue(self.null_task.igor_wd is not None)
        print(self.null_task.to_dict())


    def test_something(self):
        # self.null_task.igor_
        ofile = tempfile.NamedTemporaryFile(mode='w', dir='.')
        original_path = ofile.name
        print(original_path)
        ofile.name = "nombre_temporal.txt"
        ofile.write("jojojo\n")
        ofile.write("abasbgs\n")


    # def test_load_default(self):
    #     """test default task"""
    #     default_task = IgorTask.default_model("human", "beta")
    #     self.assertEqual(type(self.null_task), type(default_task))
    #
    #     # Load from default location explicitaly
    #     path_genomes = IgorRefGenome.load_from_path(default_task.igor_path_ref_genome)
    #     tmp_flag = default_task.genomes.df_genomicVs.equals(path_genomes.df_genomicVs)
    #     self.assertTrue(tmp_flag)
    #     # Now write it in a database
    #     default_task.create_db("hb_genome.db")
    #     print(default_task.igor_fln_db)
    #     default_task.load_db_from_genomes()
    #     default_task.db_export_IgorGenomes("export_genome_from_db")
    #
    #     fromdb_genomes = IgorRefGenome.load_from_path("export_genome_from_db")
    #     tmp_flag = default_task.genomes.df_genomicVs.equals(fromdb_genomes.df_genomicVs)
    #     self.assertTrue(tmp_flag)
    #
    #
    #     subprocess.call("rm -r hb_genome.db", shell=True)
    #     subprocess.call("rm -r export_genome_from_db", shell=True)````


if __name__ == '__main__':
    unittest.main()
