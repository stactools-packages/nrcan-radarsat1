import os
import unittest
from tempfile import TemporaryDirectory
import pystac
from stactools.nrcan_radarsat1 import stac
from stactools.testing import TestData

test_data = TestData(__file__)


class StacTest(unittest.TestCase):
    def test_create_collection(self):
        with TemporaryDirectory() as tmp_dir:
            json_path = os.path.join(tmp_dir, "test_collection.json")
            collection = stac.create_collection(json_path)

            collection.set_self_href(json_path)

            collection.save_object(dest_href=json_path)

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            collection_path = os.path.join(tmp_dir, jsons[0])

            collection = pystac.read_file(collection_path)

            collection.validate()

    def test_create_item(self):
        with TemporaryDirectory() as tmp_dir:
            test_path = test_data.get_path("data-files")
            # Select a .tif data file
            cog_path = os.path.join(test_path, [
                d for d in os.listdir(test_path) if d.lower().endswith(".tif")
            ][0])

            # Create stac item
            json_path = os.path.join(tmp_dir, "test.json")
            item = stac.create_item(cog_path)
            item.set_self_href(json_path)
            item.save_object(dest_href=json_path)

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            item_path = os.path.join(tmp_dir, jsons[0])
            item = pystac.read_file(item_path)
            item.validate()

    def test_download_asset(self):
        enabled = False
        if enabled:
            with TemporaryDirectory() as tmp_dir:
                cog_href = (
                    "s3://radarsat-r1-l1-cog/2012"
                    "/8/RS1_B0625465_SCWA_20120822_122459_HH_SCW01F.tif")

                # Downloads full cog file. Suggest leaving test disabled unless desired to test
                from stactools.nrcan_radarsat1 import utils
                utils.download_asset(cog_href, tmp_dir)
                cogs = [p for p in os.listdir(tmp_dir) if p.endswith(".tif")]
                self.assertEqual(len(cogs), 1)
        else:
            print(
                "\nCog download test disabled. Re-enable by setting enabled = True "
                "on line 52 in tests/test_stac.py\n")
