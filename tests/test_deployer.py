# tests/test_deployer.py

from unittest.mock import MagicMock

import pytest

from viz.conf import Conf
from viz.sys.deployer import Deployer
from viz.sys.packages.package import PackageItem
from viz.sys.packages.retriever import Retriever


def test_get_packages():
    retrieverMock = MagicMock(spec=Retriever)
    retrieverMock.scan.return_value = [
        PackageItem(package_path=f"file{i}") for i in range(1, 3)
    ]
    deployer = Deployer(retrieverMock)

    packages0 = deployer.getPackages()
    assert packages0 == [PackageItem(package_path=f"file{i}") for i in range(1, 3)]
    retrieverMock.scan.assert_called_once()

    # retriever returns only 2 files to check deployer cache feature
    retrieverMock.scan.return_value = [
        PackageItem(package_path=f"file{i}") for i in range(1, 2)
    ]
    packages1 = deployer.getPackages()
    assert packages1 == [PackageItem(package_path=f"file{i}") for i in range(1, 3)]
    retrieverMock.scan.assert_called_once()


def test_deployer_required_default_values():
    with pytest.raises(TypeError):
        Deployer()


def test_deployer_required_values():
    # Test that Deployer raises an error if conf is empty
    confMock = MagicMock(spec=Conf)
    retrieverMock = MagicMock(spec=Retriever)
    with pytest.raises(ValueError):
        Deployer(None, retrieverMock)

    # Test that Deployer raises an error if retriever is empty
    with pytest.raises(ValueError):
        Deployer(confMock, None)
