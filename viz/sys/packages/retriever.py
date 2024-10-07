from abc import ABC, abstractmethod
from viz.sys.packages.package import PackageItem


class Retriever(ABC):
    @abstractmethod
    def scan(self) -> list[PackageItem]:
        """
        Returns a list of files that match the pattern defined in the configuration
        """
