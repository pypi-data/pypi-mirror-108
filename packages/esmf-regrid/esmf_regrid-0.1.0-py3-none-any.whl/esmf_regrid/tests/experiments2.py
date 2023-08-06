#!/usr/bin/env python3
"""
(AW) Regridding LFRic cubed-sphere data to UM-esque rectilinear grid
--------------------------------------------------------------------

Introduction
------------
This script utilizes the (new) `iris_ugrid.regrid` module for
regridding data output on an unstructured mesh, to a regular lat-lon
grid. The data is regridded using first-order conservative regridding.

Helper functions are provided for:
  - reading (the required information) from an LFRic (XIOS) diagnostic
  - deriving a UM-like grid (onto which the diagnostic will be regridded)
  - plotting the raw and regridded results.

The regridding itself is achieved by calling `iris_ugrid.regrid` to:
 1) instantiate the regridder
    (calculates regridding weights based on the geometry of the underlying grids)
 2) perform the regridding
    (interpolates the data from the source mesh, outputting it on the target grid)

A note:
-------
To date, the `iris_ugrid.regrid` interfaces with the
Earth System Modelling Framework (ESMF), which regrids the unstructured
data.  The `iris_ugrid.regrid` is planned to be accessible via `iris`
in the future.


Running the script:
-------------------
For help running the script:   ./regrid_xios_to_um.py -h

See the accompanying wrapper scripts for a demonstration of how
sample orography ("surface_altitude") data is extracted from a test
LFRic output (XIOS) file, and regridded on a (small) global UM-like
lon-lat grid and plotted (to a file), and for how the target grid
can be derived from existing UM data.

Timing information is written at each step, for reference.

It is hoped that the script demonstrates how LFRic data can be
regridded on to a UM like grid, using the new facilities, so that users
can incorporate the functionality into their own code or adapt the
script to meet their current needs.

"""

import sys
sys.path.insert(0, "/home/h01/sworsley/Projects/iris-esmf-regrid/")
sys.path.insert(0, "/home/h01/sworsley/Projects/iris/lib/")

from copy import deepcopy
from datetime import datetime, timedelta
import sys
import argparse
import textwrap
from contextlib import contextmanager

import matplotlib as mpl

# mpl.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.collections import PolyCollection

from netCDF4 import Dataset
import numpy as np

from cartopy.crs import PlateCarree
import iris
import iris.analysis.cartography
from iris.cube import Cube
from iris.coord_systems import GeogCS
from iris.coords import DimCoord
from iris.fileformats.pp import EARTH_RADIUS

from iris.experimental.ugrid import PARSE_UGRID_ON_LOAD
from esmf_regrid.experimental.unstructured_scheme import (
    regrid_unstructured_to_rectilinear, MeshToGridESMFRegridder,
)


def _get_parser():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent("""\
            (AW) Regrid LFRic cubed-sphere data to UM-esque rectilinear grid
            --------------------------------------------------------------------
            """),
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent("""\
            Caveats:  There are a couple of caveats wrt the current code:
             - The regridding scheme is restricted to area-weighted interpolation.
             - Only face-centred cubed sphere data can be correctly processed.
             - Only global (non-rotated) cylindrical lat-lon grids have be tested as the target grid.

            Please see the script docstring for further information regarding intended useage.

            """),
    )

    # LFRic data
    parser.add_argument(
        "-lf", "--lfric_data",
        nargs='+', type=str, required=True,
        help=textwrap.dedent("""\
             The LFRic (XIOS) data to be regridded.
             Provide the LFRic file path and diagnostic name as space separated strings akin to:
              '/full/path/to/the/lfric.nc surface_altitude'.

            """),
    )

    # UM grid information
    parser.add_argument(
        "-g", "--grid",
        nargs='+', type=str, required=True,
        help=textwrap.dedent("""\
            The information for deriving the grid that the data will be regridded onto.
            It is noted that Level 0 UM diagnostics are output on a variety of Arawaka grids,
            are are often regridded to the Level 1 "standard grid".
            Hence, different target grids are likely to be required according to the
            diagnostic being analysed and the type of evaluation being undertaken.
            Therefore, it is desirable to derive the target grid either by:
                a) reading it from an exiting UM diagnostic.
                   - by providing the UM file path and a diagnostic akin to:
                   '/path/to/um_file um_diagnostic_name' (the UM diagnostic name can be a STASH code), 
                   e.g.
                   '/project/avd/ng-vat/data/sprint_0d_20200219/umglaa_pb000-theta.pp air_potential_temperature'

             or b) by specifying the grid.
                   - by listing the number of grid points and the grid bounds akin to:
                   'n_lons, n_lats, western, eastern, southern, northern' bounds
                    e.g. '160 80 -180 180 -90 90'

            """),
    )

    # Set plot file name
    parser.add_argument(
        "-p", "--plot_filename",
        type=str,
        help="The full path and name of the output plot, e.g. ./plots_regrid_xios_to_um.png",
        default='./plots_regrid_xios_to_um.png'
    )

    return parser


@contextmanager
def report_time(times):
    """
    maintain state within a simple context manager
    """
    start = datetime.now()
    try:
        yield
    finally:
        time_value = datetime.now() - start
        times.append(time_value)
        print(f"Time elapsed: {time_value}\n")


def create_um_cube(n_lon, min_lon, max_lon, n_lat, min_lat, max_lat):
    """
    Create longitude and latitude grid information akin to the global UM
    rectilinear grid.
    n_lon and n_lat are the numbers of grid points in the E-W and N-S
    directions respectively.
    The max and min values refer to the extents the grid bounds (not the
    values of the grid points themselves)
    """
    # Setup grid latitude and longitudes
    step = (max_lon - min_lon) / (n_lon)
    longitudes = np.linspace(min_lon + 0.5 * step, max_lon - 0.5 * step, n_lon)
    step = (max_lat - min_lat) / (n_lat)
    latitudes = np.linspace(min_lat + 0.5 * step, max_lat - 0.5 * step, n_lat)
    # Create latitude and longitude coordinates
    cs = GeogCS(EARTH_RADIUS)
    lon_coord = iris.coords.DimCoord(longitudes, "longitude", units="degrees", coord_system=cs, )
    lat_coord = iris.coords.DimCoord(latitudes, "latitude", units="degrees", coord_system=cs, )
    lon_coord.guess_bounds()
    lat_coord.guess_bounds()
    # Create the cube
    cube = iris.cube.Cube(np.zeros((n_lats, n_lons)))
    cube.add_dim_coord(lat_coord, 0)
    cube.add_dim_coord(lon_coord, 1)
    return cube


def plot_raw_and_regridded_results(node_coords, face_nodes, node_start_index, lfric_data,
                                   regridded_result, longitudes, latitudes, lon_bounds, lat_bounds, plot_file):
    def cubed_sphere_fix(vertices):
        """
        Credit Paul Earnshaw
        https://www.yammer.com/metoffice.gov.uk/#/Threads/show?threadId=424429100425216
        """

        n_face, n_npf, _ = vertices.shape
        for i in range(n_face):
            for j in range(n_npf):
                # If north or south pole then it needs an appropriate
                #  "drawing" longitude
                if vertices[i, j, 1] in (-90, 90):
                    vertices[i, j, 0] = vertices[i, j - 2, 0]
                # If zero meridian and other points are on west side, then set
                #  to 360 instead of 0
                if vertices[i, j, 0] == 0.0:
                    if any(vertices[i, :, 0] > 180):
                        vertices[i, j, 0] = 360.0
        return vertices

    face_coords = node_coords[face_nodes - node_start_index]
    face_coords = cubed_sphere_fix(face_coords)
    coll = PolyCollection(face_coords,
                          array=lfric_data,
                          transform=PlateCarree(),
                          edgecolors="face")

    fig = plt.figure(figsize=(10, 10))
    grid_spec = fig.add_gridspec(2, 3)

    def global_plot(row, data_array, area_weights=None):
        meanval = np.average(data_array, weights=area_weights)
        diffs = data_array - meanval
        stdval = np.sqrt(np.average(diffs * diffs, weights=area_weights))
        metrics_dict = {
            "min": np.min(data_array),
            "max": np.max(data_array),
            "mean": meanval,
            "st-dev": stdval,
            "count": np.size(data_array)
        }
        metrics_string = "\n".join([f"{metric}: {round(value, 2)}" for
                                    metric, value in metrics_dict.items()])

        new_plot = fig.add_subplot(grid_spec[row, :2], projection=PlateCarree())
        new_plot.set_global()
        new_plot.text(-175, -50, metrics_string, color="white")
        new_plot.coastlines()
        return new_plot

    def zoomed_plot(row):
        new_plot = fig.add_subplot(grid_spec[row, 2], projection=PlateCarree())
        new_plot.set_title("<-- zoomed (McMurdo Sound)")
        new_plot.set_extent([163.7, 164.7, -75.9, -76.9])
        return new_plot

    lfric_global = global_plot(row=0, data_array=lfric_data)
    lfric_global.set_title("LFRic cubesphere data")
    lfric_zoom = zoomed_plot(row=0)
    for subplot in (lfric_global, lfric_zoom):
        subplot.add_collection(deepcopy(coll))

    # Calculate cell areas for the UM latlon grid
    # Create a dummy grid cube so we can use Iris
    um_cube = Cube(np.zeros((len(latitudes), len(longitudes))))

    def coord_bounds_from_contiguous(bounds):
        n_pts = len(bounds) - 1
        coord_bounds = np.zeros((n_pts, 2))
        coord_bounds[..., 0] = bounds[:-1]
        coord_bounds[..., 1] = bounds[1:]
        return coord_bounds

    um_cube.add_dim_coord(
        DimCoord(latitudes,
                 # bounds=lat_bounds,
                 bounds=coord_bounds_from_contiguous(lat_bounds),
                 standard_name='latitude', units='degrees',
                 coord_system=GeogCS(EARTH_RADIUS)),
        0)

    um_cube.add_dim_coord(
        DimCoord(longitudes,
                 # bounds=lon_bounds,
                 bounds=coord_bounds_from_contiguous(lon_bounds),
                 standard_name='longitude', units='degrees',
                 coord_system=GeogCS(EARTH_RADIUS)),  # this just avoids a warning
        1)

    # Use Iris to calculate the cell areas. Note we are transposing the weights so the array is
    # in the same order as the regridded_result (which has inherited the order from ESMF)
    # um_area_weights = np.transpose(iris.analysis.cartography.area_weights(um_cube, normalize=True))
    um_area_weights = iris.analysis.cartography.area_weights(um_cube, normalize=True).T
    print(um_area_weights.shape)
    print(regridded_result.shape)

    um_global = global_plot(row=1, data_array=regridded_result,
                            area_weights=um_area_weights)
    um_global.set_title("LFRic cubesphere data regridded to UM lon-lat grid")
    um_zoom = zoomed_plot(row=1)
    for subplot in (um_global, um_zoom):
        subplot.pcolormesh(lon_bounds, lat_bounds,
                           regridded_result.data.T
                           # np.transpose(regridded_result)
                           )

    # plt.savefig(plot_file)
    plt.show()


if __name__ == '__main__':

    # Check module version
    print("Iris environment", iris.__file__)
    print("Iris version", iris.__version__)

    times_list = []

    # INPUTS ######################################################################

    parser = _get_parser()
    args = parser.parse_args()

    lfric_path, lfric_diagnostic = args.lfric_data
    grid_specification = args.grid
    plotfile_path = args.plot_filename

    # LFRIC #######################################################################

    print("Loading LFRic data ...")
    with report_time(times_list):
        with PARSE_UGRID_ON_LOAD.context():
            src_cube = iris.load_cube(lfric_path, lfric_diagnostic)

    # UM ##########################################################################

    print("Getting latlon grid")
    with report_time(times_list):
        if len(grid_specification) == 2:
            print("Derive grid from an existing UM diagnostic.  Loading UM grid ...")
            um_path, um_diagnostic = grid_specification
            tgt_cube = iris.load_cube(um_path, um_diagnostic)
            tgt_cube.coord("longitude").guess_bounds()
            tgt_cube.coord("latitude").guess_bounds()


        elif len(grid_specification) == 6:
            print("Creating UM-esque rectilinear grid ...")
            grid_specification = list(map(int, grid_specification))
            n_lons, n_lats, western, eastern, southern, northern = grid_specification
            tgt_cube = (
                create_um_cube(n_lons, western, eastern, n_lats, southern, northern)
            )

        else:
            print("Target grid specifications are incorrect. Aborting")
            sys.exit(1)

    # REGRID ######################################################################

    print("Regridding LFRic data using first-order conservative regridding... ")
    # with report_time(times_list):
    #    regridded_result = regrid_unstructured_to_rectilinear(src_cube, tgt_cube)

    # Regridder: Prepare the regridding.
    # Includes the calculation of the regrid weights.
    print("Instantiating Regridder ...")
    with report_time(times_list):
        rg = MeshToGridESMFRegridder(src_cube, tgt_cube)

    # Now regrid LFRic data from its mesh to UM grid.
    # The regridded_result is a numpy array.
    print("Performing regridding ...")
    with report_time(times_list):
        regridded_result = rg(src_cube)

    time_sum = sum(times_list, timedelta())
    print(f"Sum of times: {time_sum}")

    # PLOT ########################################################################
    # from iris.experimental.ugrid.plot import plot as uplot
    #
    # # see the iris.experimental.ugrid.plot doc-string for further details
    # plotter = uplot(src_cube, projection="moll", resolution="110m")
    # # plotter.show()
    #
    # import cartopy.crs as ccrs
    # import iris.quickplot as qplt
    # import matplotlib.pyplot as plt
    #
    # fig = plt.figure(figsize=[16, 8])
    # ax = plt.axes(projection=ccrs.Mollweide())
    # qplt.pcolor(regridded_result, cmap="twilight_shifted")
    # ax.coastlines()
    # #    plt.show()
    # plot_file = plotfile_path
    # plt.savefig(plot_file)

    # Extract information from source cube mesh.
    face_nodes = src_cube.mesh.face_node_connectivity.indices
    node_start_index = src_cube.mesh.face_node_connectivity.start_index
    node_xs = src_cube.mesh.coord(axis="x", include_nodes=True).points  # typically in degrees_east
    node_ys = src_cube.mesh.coord(axis="y", include_nodes=True).points  # typically in degrees_north
    face_nodes = src_cube.mesh.face_node_connectivity.indices
    node_coords = np.stack((node_xs, node_ys), axis=1)
    lfric_data = src_cube.data

    # Extract reformatted lat/lon information from target cube.
    longitudes = tgt_cube.coord("longitude").points
    lon_bounds = np.empty(len(tgt_cube.coord("longitude").points) + 1)
    lon_bounds[:-1] = tgt_cube.coord("longitude").bounds[:, 0]
    lon_bounds[-1:] = tgt_cube.coord("longitude").bounds[-1:, 1]
    latitudes = tgt_cube.coord("latitude").points
    lat_bounds = np.empty(len(tgt_cube.coord("latitude").points) + 1)
    lat_bounds[:-1] = tgt_cube.coord("latitude").bounds[:, 0]
    lat_bounds[-1:] = tgt_cube.coord("latitude").bounds[-1:, 1]

    print("Plotting results ...")
    plot_info = (node_coords, face_nodes, node_start_index, lfric_data,
                 regridded_result.data.T, longitudes, latitudes, lon_bounds, lat_bounds, plotfile_path)
    plot_raw_and_regridded_results(*plot_info)
    print(f'... done :  Plotted results are in the file "{plotfile_path}".')


    # FINISHED #####################################################################

    print(f"Finished running {__file__}")

