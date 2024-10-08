from viz.sys.vm import LibvirtConf, VmHandler


def main() -> None:
    vmHandler = VmHandler(LibvirtConf())

    for domain in vmHandler.list_domains():
        if domain.ID > 0:
            print(f"Domain: {domain.name} State: {domain.state}")

    vmHandler.close()


if __name__ == "__main__":
    main()
