import os
import yaml
from appdirs import AppDirs
from argparse import ArgumentParser

CONF_API_ID = "api_id"
CONF_API_HASH = "api_hash"
CONF_BOT_TOKEN = "bot_token"


def get_config_path():
    """Set the config path."""
    return AppDirs("telegram_simulation_bot").user_config_dir + ".yaml"


def safe_config(config):
    """Safe the config file."""
    with open(get_config_path(), "w") as f:
        yaml.dump(config, f, Dumper=yaml.Dumper)


def read_config():
    """Read the config file."""
    if not os.path.isfile(get_config_path()):
        raise FileNotFoundError("We did not find a config for telegram_simulation_bot.")

    with open(os.path.join(get_config_path())) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def delete_config():
    """Delete the config file."""
    print("deleting the configuration.")
    os.remove(get_config_path())


def setup(args):
    """Carry out the configuration."""

    if args.delete:
        delete_config()
        quit()

    if args.config or not os.path.isfile(get_config_path()):
        config = {}
        print("-- telegram_simulation_bot --")
        print("starting the configuration.\n")
        print("Start a chat with the BotFather (https://telegram.me/BotFather) and create your bot.\n")
        config[CONF_BOT_TOKEN] = str(input("Input a bot token:\n>"))
        print("\nGet an api_id and api_hash from https://my.telegram.org, under API Development.\n"
              "More info: https://docs.telethon.dev/en/latest/basic/signing-in.html\n")
        config[CONF_API_ID] = int(input("Input an api id:\n>"))
        config[CONF_API_HASH] = str(input("Input an api hash:\n>"))

        safe_config(config)
        print("\nFinished the configuration.")


class ClusterStatusArgparser(ArgumentParser):
    """Class that deals with arguments for the telegram_simulation_bot"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_argument(
            "-c",
            "--config",
            action='store_true',
            help="start the config",
        )
        self.add_argument(
            "-d",
            "--delete",
            action='store_true',
            help="remove your config",
        )
        self.add_argument(
            "-t",
            "--type",
            default="MITgcm",
            help="specify which type of simulation you want to monitor",
        )
