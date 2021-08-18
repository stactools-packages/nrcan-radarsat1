from pyproj import CRS
import pystac
from pystac.link import Link
from pystac.extensions import sar
from pystac.utils import str_to_datetime
from pystac import Extent, SpatialExtent, TemporalExtent

RADARSAT_ID = "radarsat-r1-l1-cog-aws"
RADARSAT_EPSG = 4326
RADARSAT_CRS = CRS.from_epsg(RADARSAT_EPSG)
RADARSAT_TITLE = "Radarsat-1 COGs on AWS"
RADARSAT_LICENSE = "proprietary"
RADARSAT_LICENSE = "OGL-Canada-2.0"
RADARSAT_LICENSE_LINK = Link(
    rel="license",
    target="https://open.canada.ca/en/open-government-licence-canada",
    title="Open Government Licence - Canada",
)
RADARSAT_PLATFORM = "RADARSAT-1"
RADARSAT_CONSTELLATION = "RADARSAT"
RADARSAT_INSTRUMENTS = ["C-SAR"]
RADARSAT_FREQUENCY_BAND = sar.FrequencyBand.C
RADARSAT_CENTER_FREQUENCY = 5.6
RADARSAT_OBSERVATION_DIRECTION = sar.ObservationDirection.RIGHT
RADARSAT_POLARIZATIONS = [sar.Polarization.HH]

RADARSAT_DATA_PROVIDER = pystac.Provider(
    name="Canadian Space Agency (CSA)",
    roles=["producer", "licensor"],
    url="http://www.asc-csa.gc.ca/eng/satellites/radarsat1/Default.asp")

RADARSAT_PROCESSING_PROVIDER_1 = pystac.Provider(
    name="MDA Geospatial Services International.",
    roles=["processor"],
    url="https://mda.space/en/geo-intelligence/")

RADARSAT_PROCESSING_PROVIDER_2 = pystac.Provider(
    name="Natural Resources Canada",
    roles=["processor", "host"],
    #url="https://nrcan.gc.ca",
    url="https://registry.opendata.aws/radarsat-1/")

RADARSAT_PROCESSING_PROVIDER_3 = pystac.Provider(
    name="Sparkgeo Consulting Inc.",
    roles=["processor"],
    url="https://sparkgeo.com")

RADARSAT_HOST_PROVIDER = pystac.Provider(name="Amazon Web Services",
                                         roles=["host"],
                                         url="https://registry.opendata.aws/")

RADARSAT_DESCRIPTION = (
    "Launched in November 1995, RADARSAT-1 provided Canada and the world with an "
    "operational radar satellite system capable of timely delivery of large amounts of data. "
    "RADARSAT-1 used a synthetic aperture radar (SAR) sensor to image the Earth at a single microwave "
    "frequency of 5.3 GHz, in the C band (wavelength of 5.6 cm). "
    "This was a Canadian-led project involving the Canadian federal government, the Canadian provinces, "
    "the United States, and the private sector. RADARSAT-1 reached end of service on March 29, 2013. "
)

RADARSAT_EXTENT = Extent(
    SpatialExtent([-180.0, -90.0, 180.0, 90.0]),
    TemporalExtent([
        str_to_datetime("1995-11-04T14:22:00Z"),
        str_to_datetime("2013-03-29T00:00:00Z")
    ]))

RADARSAT_PRODUCT_DESCRIPTION = Link(
    rel="about",
    #link="https://www.asc-csa.gc.ca/eng/satellites/radarsat1/components.asp",
    target=
    "https://earth.esa.int/eogateway/catalog/radarsat-1-2-full-archive-and-tasking",
    title="Data Products Specification",
)
