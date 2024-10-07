from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict
from dataclasses import dataclass
from viz.sys.packages.retriever import Retriever
from viz.sys.packages.package import PackageItem


import os as builtin_os
import re

"""
FolderRetrieverConf defines configuration for FolderRetriever.
It specifies the directory where packages are stored and a pattern to filter package files.
"""


class FolderRetrieverConf(BaseSettings):
    packages_dir: str = "dist"
    pattern: str = r"^[a-zA-Z]+\.bundle\.\d+\.\d+\.\d+\.tar\.gz$"

    model_config = SettingsConfigDict(env_prefix="CONF_")


"""
FolderRetriever retrieves a list of package files from a specified directory.

The class inherits from the Retriever class and implements the scan method to 
read the directory, filter the files based on a specific pattern, and return a 
list of files that match the pattern.
"""


@dataclass
class FolderRetriever(Retriever):
    conf: FolderRetrieverConf
    os: Any = builtin_os

    def __post_init__(self) -> None:
        # [!] self.conf shall not be equal to None
        if not isinstance(self.conf, FolderRetrieverConf):
            raise ValueError("Field 'conf' must be of FolderRetrieverConf type")

    def scan(self) -> list[PackageItem]:
        """
        Scans the packages directory and returns a list of files that match the pattern defined in the configuration.

        Raises:
            PermissionError: If the directory is not readable.

        Returns:
            list[str]: A list of file names that match the pattern.
        """
        os = self.os
        packages_dir = self.conf.packages_dir
        if not os.access(packages_dir, os.R_OK):
            raise PermissionError(f"Unable to read directory: {packages_dir}")

        print(self.conf)

        files = [
            f
            for f in os.listdir(packages_dir)
            if os.path.isfile(os.path.join(packages_dir, f))
        ]

        filtered_files = [f for f in files if re.match(self.conf.pattern, f)]

        package_items = [PackageItem(package_path=f) for f in filtered_files]

        return package_items
