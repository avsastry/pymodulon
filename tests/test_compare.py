import pymodulon.compare as cmp
from pymodulon.core import IcaData
from pymodulon.example_data import load_example_bbh, load_staph_data
import os
import shutil
import pytest



@pytest.fixture
def staph_obj():
    return load_staph_data()

@pytest.fixture
def example_bbh():
    return load_example_bbh()

def test_convert_gene_index(staph_obj, example_bbh, ecoli_obj):
    ten_genes = IcaData(
        ecoli_obj.M.iloc[:10, :10],
        ecoli_obj.A.iloc[:10, :10],
        gene_table=ecoli_obj.gene_table.iloc[:10],
        sample_table=ecoli_obj.sample_table.iloc[:10],
        imodulon_table=ecoli_obj.imodulon_table.iloc[:10],
    )

    # Test conforming M matrix from same organism
    M1, M2 = cmp.convert_gene_index(ecoli_obj.M, ten_genes.M)
    assert (M1.index == M2.index).all()
    assert len(M1.index) == 10

    # Test conforming M matrix from different organisms
    orgM1, orgM2 = cmp.convert_gene_index(ecoli_obj.M, staph_obj.M,
                                          ortho_file=example_bbh)
    assert (orgM1.index == orgM2.index).all()
    assert len(orgM1) > 10

    # Test conforming gene info data between organisms
    org_table1, org_table2 = cmp.convert_gene_index(
        ecoli_obj.gene_table,
        staph_obj.gene_table,
        ortho_file=example_bbh,
    )

    assert (org_table1.index == org_table2.index).all()
    assert (org_table1.index == orgM1.index).all()

def test_make_prots_faout(tmp_path):
    gbk = '../src/pymodulon/data/ecoli/genome.gb'
    fa_out = tmp_path / 'test.fa'
    fa_out.touch()

    cmp.make_prots(gbk, fa_out)

    with open(fa_out) as fa:
        line = fa.readline().strip()
        assert line == '>b0001'

    # def test_compare_ica():
    #     S2 = pd.read_csv("data/mtb_S.csv", index_col=0)
    #     S1 = pd.read_csv("data/ecoli_S.csv", index_col=0)
    #     ortho_dir = (
    #         "/home/sbrg/Desktop/modulome/data/organism_compare/"
    #         "bbh_csv/eColi_full_protein_vs"
    #         "_mTuberculosis_full_protein_parsed.csv"
    #     )
    #     dot, links = compare_ica(S1, S2, ortho_file=ortho_dir)
