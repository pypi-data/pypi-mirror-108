import sys
sys.path.insert(0, "/home/h01/sworsley/Projects/iris-esmf-regrid/")
sys.path.insert(0, "/home/h01/sworsley/Projects/iris/lib/")

import os
import iris
# from iris.experimental.ugrid import PARSE_UGRID_ON_LOAD
#
# from pathlib import Path
# import esmf_regrid
#
# from iris.coords import AuxCoord, DimCoord
# import numpy as np
#
# from esmf_regrid.experimental.unstructured_scheme import (
#     regrid_unstructured_to_rectilinear, MeshToGridESMFRegridder,
# )
# from esmf_regrid.tests.unit.experimental.unstructured_scheme.test__cube_to_GridInfo import (
#     _grid_cube,
# )
# from esmf_regrid.tests.unit.experimental.unstructured_scheme.test__regrid_unstructured_to_rectilinear__prepare import (
#     _flat_mesh_cube,
# )
# from time import time
#
#
# # path_original = Path("/project") / "avd" / "ng-vat" / "data" / "r25376_lfric_atm_files" / "lfric_averages.nc"
# # new_name = path_original.stem + "_fixed_edges"
# # path_copy = (Path().home() / "Desktop" / new_name).with_suffix(path_original.suffix)
# # copy(path_original, path_copy)
#
# fname ="/project/avd/ng-vat/data/poc-03/real/qrclim.sst.ugrid.nc"
#
# with PARSE_UGRID_ON_LOAD.context():
#     cubes = iris.load(fname)
#
# src = cubes[0]
# # print(cubes)
# # print(cubes[0])
# # print(cubes[0].mesh)
#
# n_lons = 200
# n_lats = 100
# lon_bounds = (-180, 180)
# lat_bounds = (-90, 90)
# tgt = _grid_cube(n_lons, n_lats, lon_bounds, lat_bounds, circular=True)
#
# t = time()
# result = regrid_unstructured_to_rectilinear(src, tgt)
# print(time()-t)
#
# print(src)
# print(result)
#
# t = time()
# rg = MeshToGridESMFRegridder(src[0], tgt)
# print(time()-t)
# t = time()
# result2 = rg(src)
# print(time()-t)
# t = time()
# result2 = rg(src)
# print(time()-t)
#
# print(result == result2)

# import iris.quickplot as qplt
# import matplotlib.pyplot as plt
#
# qplt.pcolor(result[0])
# plt.show()
#
#
# e_grid = Cube(np.ones([2, 4]))
# e_lat = DimCoord([-45, 45], bounds=[[-90, 0], [0, 90]])

# from esmf_regrid.experimental.unstructured_scheme import (
#     regrid_rectilinear_to_unstructured
# )
# 
# back = regrid_rectilinear_to_unstructured(result, src)
# 
# print(back)
# 
# print(src.data.max())
# print(src.data.min())
# print(back.data.max())
# print(back.data.min())
# print((src.data-back.data).max())
# print((src.data-back.data).min())

from esmf_regrid.schemes import regrid_rectilinear_to_rectilinear

# test_data_dir = iris.config.TEST_DATA_DIR
test_data_dir = "/home/h01/sworsley/Repos/iris-test-data-2.2/test_data"

# Load target grid cube.
tgt_fn = os.path.join(
    test_data_dir, "NetCDF", "global", "xyt", "SMALL_hires_wind_u_for_ipcc4.nc"
)
tgt = iris.load_cube(tgt_fn)

sim = regrid_rectilinear_to_rectilinear(tgt, tgt)

print(sim)
