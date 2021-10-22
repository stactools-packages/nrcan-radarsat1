from stactools.nrcan_radarsat1 import sat_properties
import os
import datetime
from typing import Optional
import logging
import numpy as np
import rasterio
import rasterio.features
from rasterio import Affine as A
from rasterio.warp import transform_geom
from shapely.geometry import mapping, shape
import utm
import boto3
from botocore import UNSIGNED
from botocore.config import Config

logger = logging.getLogger(__name__)


class Rsat_Metadata():
    """
    Metadata class for Radarsat-1
    """
    def __init__(self, href):
        """
        Args:
        href: path to cog file. Can be aws link or path to local file.
        """
        self.href = href

        def _load_metadata_from_asset():
            """
            Retrieve metadata from COG asset
            """

            with rasterio.Env(AWS_NO_SIGN_REQUEST='YES',
                              GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR'):
                with rasterio.open(href) as src:
                    # Retrieve metadata stored in COG file
                    metadata = src.profile
                    metadata.update(src.tags())
                    metadata['shape'] = src.shape

                    # Retrieve COG CRS. Note: these COGs do not appear to have CRS info that can be
                    # accessed via the .crs method. If this occurs assume it is in WGS84.
                    # All COGs in AWS appear to be projected in WGS84.
                    if src.crs is None:
                        metadata['crs'] = rasterio.crs.CRS.from_epsg(4326)
                    else:
                        metadata['crs'] = src.crs

                    # Compute bounding box, image footprint, and gsd
                    bbox, footprint, metadata = _get_geometries(src, metadata)

                # Derive some additional metadata from the filename
                fname = os.path.basename(href)
                metadata = _parse_filename(fname, metadata)

            return metadata, bbox, footprint

        def _get_geometries(src, metadata, scale=2, precision=5):
            """
            Retrieve geometric information (bounding box, footprint, and gsd) from COG file

            Args:
            src: COG file opened as Rasterio object
            metadata: dictionary containing COG metadata
            scale: option to subsample image when computing footprint
            (better performance, worse accuracy).
                   scale can be 1,2,4,8,16. scale=1 creates most precise footprint
                   at the expense of reading all pixel values. scale=2 reads 1/4 amount
                   of data be overestimates footprint by at least 1pixel (20 meters).
            precision: number of decimals to store for bounding box coordinates
            """

            # Get bounding box for raster in Lat/Long
            with rasterio.vrt.WarpedVRT(src, crs='EPSG:4326') as vrt:
                bbox = [np.round(x, decimals=precision) for x in vrt.bounds]
                metadata['transform'] = vrt.transform

            # Get GSD in meters. Requires conversion to UTM. Appropriate UTM zone determined
            # based on bbox centroid.
            # Note: UTM may not always be appropriate for this sensor? (high/low latitudes?)
            mid_lat = bbox[1] + ((bbox[3] - bbox[1]) / 2)
            mid_long = bbox[0] + ((bbox[2] - bbox[0]) / 2)
            utm_zone = utm.latlon_to_zone_number(mid_lat, mid_long)
            south = True if mid_lat < 0.0 else False
            utm_crs = rasterio.crs.CRS.from_dict({
                'proj': 'utm',
                'zone': utm_zone,
                'south': south
            })
            utm_epsg = utm_crs.to_authority()[1]

            with rasterio.vrt.WarpedVRT(
                    src, crs='EPSG:{}'.format(utm_epsg)) as utm_vrt:
                gsd = utm_vrt.transform[0]
                metadata['gsd'] = round(gsd, 2)

            # Get polygon covering entire valid data region.
            # This might be a bit heavy of an operation. Could just use the bounds for geometry
            arr = src.read(1,
                           out_shape=(src.height // scale, src.width // scale))
            arr[np.where(arr != 0)] = 1
            transform = src.transform * A.scale(scale)

            rioshapes = rasterio.features.shapes(arr, transform=transform)
            max_perimeter = 0
            max_geometry = None
            for geom, val in rioshapes:
                if val == 1:
                    geometry = shape(geom)
                    if geometry.length > max_perimeter:
                        max_perimeter = geometry.length
                        max_geometry = geometry

            valid_geom = mapping(max_geometry.convex_hull)

            footprint = transform_geom("EPSG:4326",
                                       "EPSG:{}".format(
                                           metadata['crs'].to_epsg()),
                                       valid_geom,
                                       precision=precision)

            return bbox, footprint, metadata

        def _parse_filename(filename, metadata):
            """
            Parse metadata from the SAR cog filename

            Args:
            filename: name of cog file
            metadata: dict of metadata

            Returns:
            metadata: updated metadata dictionary
            """

            file_noext = os.path.splitext(filename)[0]
            fname = file_noext.split("_")

            metadata["scene_id"] = fname[1]
            metadata[
                "beam_mode"] = sat_properties.radarsat_product_characteristics[
                    fname[2]]
            metadata["product_type"] = fname[-1]
            try:
                metadata[
                    "product_description"] = sat_properties.radarsat_1_data_products[
                        fname[-1][:3]]['description']
            except Exception:
                metadata["product_description"] = ""

            metadata["scene_mean_time"] = datetime.datetime.strptime(
                fname[3] + fname[4], "%Y%m%d%H%M%S")

            return metadata

        self.meta, self.bbox, self.geometry = _load_metadata_from_asset()

    @property
    def epsg(self) -> Optional[int]:
        '''returns image epsg code'''
        return self.meta['crs'].to_epsg()

    @property
    def orbit_state(self) -> Optional[str]:
        '''returns satellite orbit state'''
        return self.meta['CEOS_ASC_DES'].strip().lower()

    @property
    def absolute_orbit(self) -> Optional[int]:
        '''returns satellite absolute orbit number'''
        return int(self.meta['CEOS_ORBIT_NUMBER'].strip())

    @property
    def pixel_spacing_range(self) -> Optional[float]:
        '''returns range pixel spacing in meters'''
        return round(float(self.meta['CEOS_PIXEL_SPACING_METERS'].strip()), 2)

    @property
    def pixel_spacing_azimuth(self) -> Optional[float]:
        '''returns azimuth pixel spacing in meters'''
        return round(float(self.meta['CEOS_LINE_SPACING_METERS'].strip()), 2)


def download_asset(cog_href: str, outpath: str) -> Optional[str]:
    """
    Download COG asset

    Args:
        cog_href (str): Location of associated COG asset
        href url should point to radarsat-1 data in s3 storage,
        e.g. "s3://radarsat-r1-l1-cog/2009/2/RS1_X0597984_F1_20090205_094341_HH_SGF.tif"
        outpath (str): Directory for outfile.

    Returns:
        path to file
    """

    import warnings
    warnings.simplefilter("ignore", ResourceWarning)

    bucket_name = "radarsat-r1-l1-cog"

    if not os.path.exists(outpath):
        os.makedirs(outpath)

    s3_fpath = cog_href.split(bucket_name)[1][1:]
    fname = os.path.basename(cog_href)

    out_file = os.path.join(outpath, fname)

    s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))

    with open(out_file, 'wb') as f:
        s3.download_fileobj(bucket_name, s3_fpath, f)

    return out_file
