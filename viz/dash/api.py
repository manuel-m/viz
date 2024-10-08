import libvirt  # type: ignore

from fastapi import FastAPI

from pydantic_settings import BaseSettings, SettingsConfigDict

from viz.sys.packages.folderRetriever import FolderRetriever, FolderRetrieverConf

from viz.sys.utils import dump_environment_variables
from viz.sys.packages.package import PackageItem
from viz.sys.vm import LibvirtConf, VmHandler, VmDomain


from pydantic import BaseModel


class PackagesResponse(BaseModel):
    packages: list[PackageItem]


class AppConf(BaseSettings):
    run_mode: str = "production"
    model_config = SettingsConfigDict(env_prefix="CONF_")


def create_app(appConf: AppConf) -> FastAPI:
    retrieverConf = FolderRetrieverConf()
    folder_retriever = FolderRetriever(retrieverConf)

    dump_environment_variables()

    if appConf.run_mode == "dev":
        app = FastAPI()
    else:
        app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    @app.get("/packages")
    def packages() -> PackagesResponse:
        """
        Returns a list of packages in the packages directory.
        """
        package_items = folder_retriever.scan()
        return PackagesResponse(packages=package_items)

    @app.get("/domains")
    def domains() -> list[VmDomain]:
        # [!] recreate handler each time
        vmHandler = VmHandler(LibvirtConf())
        result = vmHandler.list_domains()
        vmHandler.close()
        return result

    return app


# Created FastAPI app instance
app = create_app(AppConf())
