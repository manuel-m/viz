import libvirt  # type: ignore
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pydantic import BaseModel

import sys


class LibvirtConf(BaseSettings):
    libvirt_user: Optional[str] = None
    hypervisor_host: str = "localhost"

    model_config = SettingsConfigDict(env_prefix="CONF_")


class VmDomain(BaseModel):
    ID: int
    name: str
    state: int
    UUID: str


class VmHandler:
    def __init__(self, conf: LibvirtConf) -> None:
        self.conf = conf
        if conf.hypervisor_host == "localhost" or conf.hypervisor_host == "127.0.0.1":
            self.uri = "qemu:///system"
        else:
            self.uri = f"qemu+ssh://{conf.libvirt_user}@{conf.hypervisor_host}/system"

        self.conn = None

        try:
            self.conn = libvirt.openReadOnly(self.uri)
        except libvirt.libvirtError as e:
            print("Failed to open connection to the hypervisor", file=sys.stderr)
            print(repr(e), file=sys.stderr)

    def list_domains(self) -> list[VmDomain]:
        if self.conn is None:
            return []

        domains = self.conn.listAllDomains()
        return [
            VmDomain(
                name=domain.name(),
                ID=domain.ID(),
                UUID=domain.UUIDString(),
                state=domain.state()[1],
            )
            for domain in domains
        ]

    def close(self) -> None:
        if self.conn is not None:
            self.conn.close()
