"""Main CLI tool for adding, managing, and viewing prefect accounts."""
import fire
import toml
import yaml
import os
from pathlib import Path
from typing import Dict, Optional
import subprocess

PM_PATH = f"{str(Path.home())}/.prefect-manager"

def get_accounts():

    with open(f"{PM_PATH}/accounts.yml", 'r') as f:
        accounts = yaml.safe_load(f)
    return accounts

def get_config(name: str):
    with open(f"{PM_PATH}/{name}.toml", "r") as f:
        config = toml.load(f)

    return config

def write_prefect_config(config: Dict):
    with open(f"{str(Path.home())}/.prefect/config.toml", "w+") as f:
        toml.dump(config, f)

class PrefectCloudManager:
    """CLI Tool for managing multiple Prefect accounts"""
    def __init__(self):
        if not os.path.exists(f"{PM_PATH}"):
            os.mkdir(f"{PM_PATH}")

            with open(f"{PM_PATH}/accounts.yml", "w") as f:
                yaml.dump({"accounts": {}}, f)

            with open(f"{PM_PATH}/default_config.toml", "w") as f:
                toml.dump({"cloud": {"agent": {}}}, f)

    def add_account(self):
        """Add a new account to prefect-manager."""
        account_name = ""
        while account_name == "":
            account_name = input("Name of Account: ")
        access_token = ""
        while access_token == "":
            access_token = input("Access Token: ")

        accounts = get_accounts()

        accounts["accounts"].update({account_name: access_token})
        with open(f"{PM_PATH}/accounts.yml", "w+") as f:
            yaml.dump(accounts, f)

    def list_accounts(self):
        """List all the accounts tracked by prefect-manager."""
        accounts = get_accounts()
        print("Accounts")
        print ("-"* 15)
        for account in accounts["accounts"]:
            print(account)

    def activate(self, account_name: str, config_name: str="default_config"):
        """Switch prefect accounts and login.

        This sets the cloud agent token in the config file to the one provided for this
        account and also logs in using that same token.

        Args:
            account_name: Name of account (see list-accounts for options)
            config_name: Name of config to use (see list-configs for options).
                         See add-config or edit-config commands to change the other options
                         provided to the prefect config. Default is default_config.
        """
        config = get_config(config_name)
        accounts = get_accounts()
        token = accounts["accounts"][account_name]
        config["cloud"]["agent"] = token
        write_prefect_config(config)
        subprocess.run(["prefect", "auth", "login", "--token", f"{token}"])

    def add_config(self, config_name: str, config_path: str=f"{str(Path.home())}/.prefect/config.toml"):
        """Add a new config setup to the tracked config files from an already created config.

        This takes a config that has been created and adds it with a name to the list of files. If
        you want to write a new config using the command line, use the edit-config command.

        Args:
            config_name: Name to give the config.
            config_path: Path to the config to import. Defaults to the current prefect config.toml file.
        """
        with open(config_path, "r") as f:
            config_template = toml.load(f)

        with open(f"{PM_PATH}/{config_name}.toml", "w+") as f:
            toml.dump(config_template, f)

    def list_configs(self):
        """List all the configurations available for use."""
        configs = os.listdir(PM_PATH)
        print("Configs")
        print("-" * 15)
        for config in configs:
            if "toml" in config:
                print(config.split(".")[0])

    def edit_config(self, config_name: str="default_config"):
        """Edit an existing configuration or write a new one from the command line."""
        subprocess.run(["nano", f"{PM_PATH}/{config_name}.toml"])


def main():
    fire.Fire(PrefectCloudManager)


if __name__ == '__main__':
    main()