from __future__ import print_function
import unittest
from pytraj.base import *
from pytraj import adict
from pytraj import io as io
from pytraj.utils import eq, aa_eq
from pytraj.decorators import no_test, test_if_having, test_if_path_exists
from pytraj.testing import cpptraj_test_dir
import pytraj.common_actions as pyca
from pytraj.externals.six import PY2

class Test(unittest.TestCase):
    def test_0(self):
        traj = io.iterload("./data/md1_prod.Tc5b.x", "./data/Tc5b.top")
        mydict = traj.search_hbonds(dtype='dict')

        # pickle
        pk_fname = "./output/test_dict_pickle.pk"
        io.to_pickle(mydict, pk_fname)

        new_dict = io.read_pickle(pk_fname)
        for key in mydict.keys():
            aa_eq(mydict[key], new_dict[key])

        # json
        js_name = "./output/my_json.js"
        # TODO : PY3 complains
        # "TypeError: 'str' does not support the buffer interface"
        if PY2:
            for key in mydict.keys():
                    mydict[key] = mydict.pop(key)
            io.to_json(mydict, js_name)
            new_dict2 = io.read_json(js_name)
            for key in mydict.keys():
                aa_eq(mydict[key], new_dict2[key])

if __name__ == "__main__":
    unittest.main()