import logging
import click
import os

from stactools.nrcan_radarsat1.stac import create_collection, create_item
from stactools.nrcan_radarsat1.utils import download_asset

logger = logging.getLogger(__name__)


def create_nrcanradarsat1_command(cli):
    """Creates a command line utility for working with Radarsat-1 cogs"""
    @cli.group(
        "nrcanradarsat1",
        short_help=("Commands for working with Radarsat-1 data"),
    )
    def nrcanradarsat1() -> None:
        pass

    @nrcanradarsat1.command(
        "create-collection",
        short_help="Creates a STAC collection from Radarsat-1 metadata",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the STAC Collection json",
    )
    def create_collection_command(destination: str) -> None:
        """Creates a STAC Collection for Radarsat-1 data

        Args:
            destination (str): Directory to create the collection json
        Returns:
            Callable
        """

        output_path = os.path.join(destination, "collection.json")

        collection = create_collection(output_path)
        collection.set_self_href(output_path)
        collection.save_object(dest_href=output_path)

    @nrcanradarsat1.command(
        "create-item",
        short_help="Create a STAC item from a Radarsat-1 COG",
    )
    @click.option(
        "-s",
        "--source",
        required=True,
        help="Path to a Radarsat-1 COG",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the STAC json",
    )
    def create_item_command(source: str, destination: str):
        """Creates a STAC Item from a Radarsat-1 COG

        Args:
            source (str): Path to a Radarsat-1 COG
            destination (str): Directory to create the stac item json
        Returns:
            Callable
        """
        output_path = os.path.join(destination,
                                   os.path.basename(source)[:-4] + ".json")
        item = create_item(source)
        item.set_self_href(output_path)
        item.save_object(dest_href=output_path)

    @nrcanradarsat1.command(
        "download-asset",
        short_help="Downloads a Radarsat-1 COG from AWS link",
    )
    @click.option(
        "-s",
        "--source",
        required=True,
        help="Path to a Radarsat-1 COG",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the COG file",
    )
    def download_asset_command(source: str, destination: str):
        """Downloads a Radarsat-1 COG

        Args:
            source (str): url for Radarsat-1 COG
            destination (str): Directory to download the COG
        Returns:
            Callable
        """
        download_asset(source, destination)
