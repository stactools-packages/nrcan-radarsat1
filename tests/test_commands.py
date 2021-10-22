import os.path
from tempfile import TemporaryDirectory

import pystac
from stactools.nrcan_radarsat1.commands import create_nrcanradarsat1_command
from stactools.testing import CliTestCase
from stactools.testing import TestData

test_data = TestData(__file__)


class CommandsTest(CliTestCase):
    def create_subcommand_functions(self):
        return [create_nrcanradarsat1_command]

    def test_create_collection(self):
        with TemporaryDirectory() as tmp_dir:
            result = self.run_command(
                ["nrcanradarsat1", "create-collection", "-d", tmp_dir])

            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            collection = pystac.read_file(os.path.join(tmp_dir, jsons[0]))
            # self.assertEqual(collection.id, "my-collection-id")
            # self.assertEqual(item.other_attr...

            collection.validate()

    def test_create_item(self):
        with TemporaryDirectory() as tmp_dir:

            test_path = test_data.get_path("data-files")
            # Select a .tif data file
            cog_path = os.path.join(test_path, [
                d for d in os.listdir(test_path) if d.lower().endswith(".tif")
            ][0])

            result = self.run_command([
                "nrcanradarsat1",
                "create-item",
                "-s",
                cog_path,
                "-d",
                tmp_dir,
            ])
            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            item_path = os.path.join(tmp_dir, jsons[0])
            item = pystac.read_file(item_path)

            item.validate()

    # Downloads full cog file. Suggest leaving commented unless desired to test
    def test_download_asset(self):
        enabled = False
        if enabled:
            with TemporaryDirectory() as tmp_dir:
                cog_href = (
                    "s3://radarsat-r1-l1-cog/2012"
                    "/8/RS1_B0625465_SCWA_20120822_122459_HH_SCW01F.tif")

            result = self.run_command([
                "nrcanradarsat1",
                "download-asset",
                "-s",
                cog_href,
                "-d",
                tmp_dir,
            ])

            self.assertEqual(result.exit_code,
                             0,
                             msg="\n{}".format(result.output))

            cogs = [p for p in os.listdir(tmp_dir) if p.endswith(".tif")]
            self.assertEqual(len(cogs), 1)
        else:
            print(
                "\nCog download test disabled. Re-enable by setting enabled = True "
                "on line 65 in tests/test_commands.py\n")
