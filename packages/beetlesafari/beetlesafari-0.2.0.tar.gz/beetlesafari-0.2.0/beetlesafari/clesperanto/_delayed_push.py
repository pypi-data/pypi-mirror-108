import pyclesperanto_prototype as cle
import numpy as np
from pyclesperanto_prototype._tier0._pycl import OCLArray


def _push_copy(image : np.ndarray, target : cle.Image, timepoint : int, scale_factor : tuple = None):
    # prevent pushing the same image subsequently
    if _push_copy.last_time_point == timepoint:
        return target
    _push_copy.last_time_point = timepoint

    import time
    start_time = time.time()
    pushed = cle.push_zyx(image)

    if (scale_factor is None):
        target = cle.copy(pushed, target)
    else:
        target = cle.resample(pushed, target, factor_x=scale_factor[2], factor_y=scale_factor[1], factor_z=scale_factor[0])

    print("push took " + str(time.time() - start_time))

    #target.write_array(image)
    return target

_push_copy.last_time_point = -1

def delayed_push(image : np.ndarray, target : cle.Image, zoom = None):
    import dask
    import dask.array as da

    # create dask stack of lazy image readers
    lazy_process_image = dask.delayed(_push_copy)  # lazy reader
    lazy_arrays = [lazy_process_image(image[n], target, n, zoom) for n in range(0, image.shape[0])]
    dask_arrays = [
        da.from_delayed(lazy_array, shape=target.shape, dtype=target.dtype)
        for lazy_array in lazy_arrays
    ]

    # Stack into one large dask.array
    return da.stack(dask_arrays, axis=0)


