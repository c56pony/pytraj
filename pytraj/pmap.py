from functools import partial

def worker(rank, n_cores=None, func=None, filelist=None,
           top=None,
           args=None,
           kwd=None):
    from pytraj import iterload
    local_traj = iterload(filelist, top=top)
    return (rank, func(
            local_traj.split_iterators(n_cores, rank=rank),
            top=local_traj.top, *args, **kwd))

def pmap(n_cores=2, func=None, traj=None, *args, **kwd):
    print(traj)
    from multiprocessing import Pool

    p = Pool(n_cores)
    pfuncs = partial(worker,
                     n_cores=n_cores,
                     func=func,
                     filelist=traj.filelist,
                     top=traj.top.filename,
                     args=args, kwd=kwd)
    result = p.map(pfuncs, [rank for rank in range(n_cores)])
    return result
