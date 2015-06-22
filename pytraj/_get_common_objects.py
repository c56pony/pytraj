from __future__ import absolute_import
from .externals.six import string_types
from .Topology import Topology
from .ArgList import ArgList
from .utils import _import
from .utils.check_and_assert import is_frame_iter, is_chunk_iter
from .datasetlist import DataSetList as DSL

def _get_top(traj, top):
    if isinstance(top, string_types):
        _top = Topology(top)
    elif top is None: 
       if hasattr(traj, 'top'):
           _top = traj.top 
       elif is_frame_iter(traj) or is_chunk_iter(traj):
           _top = None
       else:
            # list, tuple of traj objects 
            try:
                for tmp in traj:
                    if hasattr(tmp, 'top'):
                        _top = tmp.top 
                        break
            except:
                #print("Topology is None")
                _top = None
    else:
        _top = top
    return _top

def _get_arglist(arg):
    if isinstance(arg, ArgList):
        return arg
    else:
        return ArgList(arg)

def _get_data_from_dtype(d0, dtype='dataset'):
    from pytraj.datasets.DataSet import DataSet
    if dtype is None or dtype == 'dataset':
        if hasattr(d0, 'set_py_free_mem'):
            d0.set_py_free_mem(False)
        elif hasattr(d0, 'py_free_mem'):
            d0.py_free_mem = False
    if dtype is None:
        return DSL(d0)
    elif not isinstance(dtype, string_types):
        raise ValueError("dtype must a None or a string")
    else:
        dtype = dtype.lower()
        if dtype == 'dataset':
            if isinstance(d0, DataSet):
                return d0
            else:
                return DSL(d0)
        elif dtype == 'list':
            return d0.tolist()
        elif dtype == 'ndarray':
            return d0.to_ndarray()
        elif dtype == 'pyarray':
            return d0.to_pyarray()
        elif dtype == 'dict':
            try:
                import numpy
                return d0.to_dict(use_numpy=True)
            except ImportError:
                return d0.to_dict(use_numpy=False)
        elif dtype == 'dataframe':
            return d0.to_dataframe()
        else:
            raise NotImplenmentedError()

def _get_list_of_commands(mask_or_commands):
    if isinstance(mask_or_commands, string_types):
        return [mask_or_commands,]
    elif isinstance(mask_or_commands, (list, tuple)):
        return mask_or_commands
    else:
        raise ValueError("must be string or list/tuple of strings")
