# tests/test_folder_retriever.py

import os
from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from viz.sys.packages.folderRetriever import FolderRetriever, FolderRetrieverConf
from viz.sys.packages.package import PackageItem


def test_folder_retriever_init():
    conf_mock = MagicMock(spec=FolderRetrieverConf)
    # [!] to prevent dataclasses.field from raising an error
    conf_mock.packages_dir = "/some/directory"
    conf_mock.pattern = r"^[a-zA-Z]+\.bundle\.\d+\.\d+\.\d+\.tar\.gz$"

    retriever = FolderRetriever(conf_mock)
    assert retriever.conf == conf_mock
    assert retriever.conf.packages_dir == "/some/directory"
    assert retriever.conf.pattern == conf_mock.pattern


def test_folder_retriever_init_required_values():

    with pytest.raises(
        ValueError, match="Field 'conf' must be of FolderRetrieverConf type"
    ):
        FolderRetriever(None)

    with pytest.raises(TypeError):
        FolderRetriever()

    with pytest.raises(ValidationError):
        FolderRetrieverConf(packages_dir=2123)


def test_folder_retriever_scan():
    os_mock = MagicMock(spec=os)
    os_mock.listdir.return_value = [
        "file.tar.gz",
        "file.bundle.1.2.3.tar.gz",
        "file.txt",
    ]
    os_mock.path.isfile.return_value = True
    os_mock.access.return_value = True
    retriever = FolderRetriever(
        conf=FolderRetrieverConf(packages_dir="/some/directory"), os=os_mock
    )
    files = retriever.scan()
    assert files == [PackageItem(package_path="file.bundle.1.2.3.tar.gz")]
    os_mock.listdir.assert_called_once_with("/some/directory")


def test_folder_retriever_not_access():
    conf = FolderRetrieverConf(packages_dir="/a/folder/that/is/not/avaible")
    retriever = FolderRetriever(conf)
    with pytest.raises(PermissionError):
        retriever.scan()
