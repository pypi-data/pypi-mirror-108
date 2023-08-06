"""deploy modules helps for the deployement of application on deepchain"""
import configparser
import os
import shutil
from argparse import ArgumentParser

import pkg_resources
import requests
from deepchain.cli import BaseCLICommand
from deepchain.cli.apps_utils import save_app


def download_command_factory(args):
    return DownloadCommmand(args.app_name, args.app_dir)


class DownloadCommmand(BaseCLICommand):
    def __init__(self, app_name: str, app_dir: str):
        self.app_name = app_name
        self.app_dir = app_dir

    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        download_parser = parser.add_parser(  # type: ignore
            name="download", help="download public app from deepchain  hub"
        )

        download_parser.add_argument(
            "app_name",
            action="store",
            type=str,
            help="app name in the format creatorEmail:appName",
        )
        download_parser.add_argument(
            "app_dir",
            action="store",
            type=str,
            help="destination folder",
        )

        download_parser.set_defaults(func=download_command_factory)

    def run(self):
        """
        Download public app
        """
        config = configparser.ConfigParser()
        config.read(pkg_resources.resource_filename("deepchain", "cli/config.ini"))
        url = config["APP"]["DEEP_CHAIN_URL"]
        if os.path.exists(f"{self.app_dir}") and len(os.listdir((f"{self.app_dir}"))) > 0:
            print("destination folder is not empty, exiting.")
            return
        os.mkdir(f"{self.app_dir}")
        self.unpack(self.download_tar(url))
        [self.unpack(f"{self.app_dir}/{f}") for f in os.listdir(self.app_dir)]
        save_app(self.app_name, self.app_dir)

    def download_tar(self, url):
        req = requests.get(f"{url}/public-apps/{self.app_name}")
        if req.status_code != 200:
            print(f"api returning {req.status_code}, exiting.")
            exit(1)
        with open(f"{self.app_dir}/tmp.tar", "wb") as file:
            file.write(req.content)
        return f"{self.app_dir}/tmp.tar"

    def unpack(self, file):
        dest = self.app_dir
        if file.endswith("_checkpoints.tar"):
            dest = os.path.join(self.app_dir, "checkpoint")
        elif file.endswith("code.tar"):
            dest = os.path.join(self.app_dir, "src")
        shutil.unpack_archive(file, dest)
        os.remove(file)
