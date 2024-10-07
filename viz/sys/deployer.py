from dataclasses import dataclass, field

from datetime import datetime
from viz.sys.packages.retriever import Retriever
from viz.sys.packages.package import PackageItem


@dataclass
class Deployer:
    retriever: Retriever
    last_retrieved: int = 0

    # [!] prevent packages being shared between instances
    packages: list[PackageItem] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.retriever, Retriever):
            raise ValueError("Field 'retriever' must be of Retriever type")
        if not isinstance(self.last_retrieved, int):
            raise ValueError("Field 'last_retrieved' must be of int type")

        if not isinstance(self.packages, list):
            raise ValueError("Field 'packages' must be of list type")

        for package in self.packages:
            if not isinstance(package, PackageItem):
                raise ValueError(
                    "All elements in 'packages' must be of PackageItem type"
                )

    def getPackages(self) -> list[PackageItem]:

        if self.last_retrieved == 0:
            self.packages = self.retriever.scan()
            self.last_retrieved = int(datetime.now().timestamp())

        return self.packages
