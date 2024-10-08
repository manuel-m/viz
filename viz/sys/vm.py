import libvirt  # type: ignore
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class LibvirtConf(BaseSettings):
    libvirt_user: Optional[str] = None
    hypervisor_host: str = "localhost"

    model_config = SettingsConfigDict(env_prefix="CONF_")


class VmHandler:
    def __init__(self, conf: LibvirtConf) -> None:
        self.conf = conf
        if conf.hypervisor_host == "localhost" or conf.hypervisor_host == "127.0.0.1":
            self.uri = "qemu:///system"
        else:
            self.uri = f"qemu+ssh://{conf.libvirt_user}@{conf.hypervisor_host}/system"

        self.conn = libvirt.openReadOnly(self.uri)
        if self.conn == None:
            print("Failed to open connection to the hypervisor")
            exit(1)

    def list_domains(self) -> list[libvirt.virDomain]:
        domains = self.conn.listAllDomains()
        return domains

    def close(self) -> None:
        if self.conn != None:
            self.conn.close()
