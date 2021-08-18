from datetime import datetime
import logging

import pystac
from pystac.collection import Summaries
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.sat import OrbitState, SatExtension
from pystac.extensions.sar import SarExtension
from pystac.extensions.raster import RasterExtension

import constants as c
from utils import Rsat_Metadata

logger = logging.getLogger(__name__)


def create_collection(metadata_url: str) -> pystac.Collection:
    """Creates a STAC Collection for RADARSAT-1

        Args:
        metadata_url (str): Location to save the output STAC Collection json
        
        Returns:
        pystac.Collection: pystac collection object
    """

    summary_dict = {
        'constellation': [c.RADARSAT_CONSTELLATION],
        'platform': c.RADARSAT_PLATFORM,
        'proj:epsg': c.RADARSAT_EPSG,
    }
    collection = pystac.Collection(
        id=c.RADARSAT_ID,
        title=c.RADARSAT_TITLE,
        description=c.RADARSAT_DESCRIPTION,
        license=c.RADARSAT_LICENSE,
        extent=c.RADARSAT_EXTENT,
        catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED,
        stac_extensions=[
            SarExtension.get_schema_uri(),
            SatExtension.get_schema_uri(),
            ProjectionExtension.get_schema_uri(),
            RasterExtension.get_schema_uri(),
        ],
        providers=[
            c.RADARSAT_DATA_PROVIDER, c.RADARSAT_PROCESSING_PROVIDER_1,
            c.RADARSAT_PROCESSING_PROVIDER_2, c.RADARSAT_PROCESSING_PROVIDER_3,
            c.RADARSAT_HOST_PROVIDER
        ],
        summaries=Summaries(summary_dict),
    )

    collection.add_link(c.RADARSAT_LICENSE_LINK)
    collection.add_link(c.RADARSAT_PRODUCT_DESCRIPTION)

    collection.set_self_href(metadata_url)

    collection.save_object()

    return collection


def create_item(metadata_url: str, cog_href: str) -> pystac.Item:
    """Creates a STAC item for a RADARSAT-1 COG image.

    Args:
        metadata_url (str): Output path for the STAC json
        cog_href (str): Location of associated COG asset
        href url should point to radarsat-1 data in s3 storage, e.g. "s3://radarsat-r1-l1-cog/2009/2/RS1_X0597984_F1_20090205_094341_HH_SGF.tif"

    Returns:
        pystac.Item: STAC Item object.
    """

    item_id = cog_href.split('/')[-1][:-4]
    title = item_id

    rsat_metadata = Rsat_Metadata(href=cog_href)

    properties = {
        "title": title,
        "description": rsat_metadata.meta["product_description"],
        "datetime": rsat_metadata.meta["scene_mean_time"],
    }

    # Create item
    item = pystac.Item(
        id=item_id,
        geometry=rsat_metadata.geometry,
        bbox=rsat_metadata.bbox,
        datetime=rsat_metadata.meta["scene_mean_time"],
        properties=properties,
        stac_extensions=[
            SarExtension.get_schema_uri(),
            SatExtension.get_schema_uri(),
            ProjectionExtension.get_schema_uri(),
            RasterExtension.get_schema_uri(),
        ],
    )

    item.common_metadata.constellation = c.RADARSAT_CONSTELLATION
    item.common_metadata.platform = c.RADARSAT_PLATFORM
    item.common_metadata.instruments = c.RADARSAT_INSTRUMENTS
    item.common_metadata.gsd = rsat_metadata.meta["gsd"]

    item.common_metadata.created = datetime.utcnow()

    # --Extensions--
    # SAR https://github.com/stac-extensions/sar
    sar = SarExtension.ext(item, add_if_missing=True)
    sar.frequency_band = c.RADARSAT_FREQUENCY_BAND
    sar.center_frequency = c.RADARSAT_CENTER_FREQUENCY
    sar.observation_direction = c.RADARSAT_OBSERVATION_DIRECTION
    sar.instrument_mode = rsat_metadata.meta["beam_mode"]
    sar.product_type = rsat_metadata.meta["product_type"]
    sar.polarizations = c.RADARSAT_POLARIZATIONS
    sar.pixel_spacing_range = rsat_metadata.pixel_spacing_range
    sar.pixel_spacing_azimuth = rsat_metadata.pixel_spacing_azimuth
    # sar.resolution_range #Can't find this property for Radarsat-1
    # sar.resolution_azimuth = #Can't find this property for Radarsat-1
    # sar.looks_equivalent_number = #Can't find this property for Radarsat-1
    # sar.looks_range = #Can't find this property for Radarsat-1
    # sar.looks_azimuth = #Can't find this property for Radarsat-1

    # SAT https://github.com/stac-extensions/sat
    sat = SatExtension.ext(item, add_if_missing=True)
    sat.orbit_state = OrbitState(rsat_metadata.orbit_state.lower())
    sat.absolute_orbit = rsat_metadata.absolute_orbit  #Not totally sure this one is correct, but I believe it is
    #sat.relative_orbit = rsat_metadata.relative_orbit #Can't find this property for Radarsat-1

    # PROJECTION https://github.com/stac-extensions/projection
    projection = ProjectionExtension.ext(item, add_if_missing=True)
    projection.epsg = rsat_metadata.epsg
    projection.transform = rsat_metadata.meta['transform']
    projection.shape = rsat_metadata.meta['shape']

    item.add_asset(
        "cog",
        pystac.Asset(
            href=cog_href,
            media_type=pystac.MediaType.COG,
            roles=["data"],
            title=title,
        ),
    )

    item.links.append(c.RADARSAT_LICENSE_LINK)
    item.set_self_href(metadata_url)

    item.save_object()

    return item
