import mdtraj as mdt
from extasycoco import complement
import pytest
import os

rootdir = os.path.dirname(os.path.abspath('__file__'))
dcdfile = os.path.join(rootdir, 'test/1cfc.dcd')
pdbfile = os.path.join(rootdir, 'test/1cfc.pdb')

@pytest.fixture(scope="module")
def traj():
    return  mdt.load(dcdfile, top=pdbfile)

def test_complement(traj):
    t_comp_crude = complement(traj, selection='mass > 2', npoints=10, refine=False)

def test_complement_refined(traj):
    t_comp_refined = complement(traj, selection='mass > 2', npoints=10, refine=True)
