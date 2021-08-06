import stactools.core
from stactools.nrcan_radarsat1.stac import create_collection, create_item

__all__ = ['create_collection', 'create_item']

stactools.core.use_fsspec()


def register_plugin(registry):
    from stactools.nrcan_radarsat1 import commands
    registry.register_subcommand(commands.create_nrcanradarsat1_command)


__version__ = "0.1.0"
