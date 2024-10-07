import libvirt  # type: ignore
from pydantic_settings import BaseSettings, SettingsConfigDict


class LibvirtConf(BaseSettings):
    libvirt_user: str
    hypervisor_host: str

    model_config = SettingsConfigDict(env_prefix="CONF_")


def main() -> None:
    conf = LibvirtConf()
    uri = f"qemu+ssh://{conf.libvirt_user}@{conf.hypervisor_host}/system"

    conn = libvirt.openReadOnly(uri)

    if conn == None:
        print("Failed to open connection to the hypervisor")
        exit(1)

    domains = conn.listAllDomains()

    for domain in domains:
        if domain.ID() > 0:
            print(f"Domain: {domain.name()} State: {domain.state()[1]}")

    conn.close()


if __name__ == "__main__":
    main()
