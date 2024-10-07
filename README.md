
## VIZ for VM

[!] **WIP! not for production**

## Overview

This project is designed to **explore the deployment of complex applications** in hypervisors that are **disconnected from the internet**. The deployment process is fully **automated, simple, and reproducible**, utilizing a combination of modern tools and technologies including **Linux**, **libvirt**, **Python**, **Pydantic**, **Ansible**, **QEMU**, and others. The project aims to streamline application management and deployment in isolated environments using Python scripts and command-line tools.

## Features

- **Automated Deployment**: Deploy complex applications efficiently without manual intervention using Python scripts and Ansible playbooks.
- **Offline Environment**: Designed specifically for hypervisors that do not have internet access.
- **Reproducibility**: Ensures that each deployment is consistent and repeatable, reducing the likelihood of discrepancies between environments.
- **Centralized Control**: All actions are managed from a **development machine** and executed using a **Makefile**, providing a unified interface for managing deployments.

## Technologies Used

The project utilizes a wide array of tools and technologies to accomplish its goals:

- **Linux**: Operating system and environment for development and deployment.
- **Libvirt & QEMU**: Virtualization tools for managing and interacting with hypervisors.
- **Python**: Main scripting language for automation and deployment logic.
- **Pydantic**: Data validation and settings management for Python scripts.
- **Ansible**: Configuration management and automation tool for managing deployments.
- **Poetry**: Python dependency management and packaging tool for managing project dependencies.
- **Devpi**: Python package server for managing dependencies offline.
- **Cockpit**: Web-based interface for managing Linux servers and virtual machines.
- **Mypy**: Type checker for Python, ensuring type safety in the codebase.
- **Linting tools**: Code quality and style enforcement to maintain clean and readable code.

## Installation

### Development workflow

To set up the development environment and dependencies, make sure you have **Python**, **Poetry**.

**dev setup**

```bash
pyenv local 3.11.2
poetry install
poetry shell
```

**dev prerequisites** (debian)

```bash
#pyenv
sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev libvirt-dev

curl https://pyenv.run | bash

pyenv install 3.11.2


#poetry
curl -sSL https://install.python-poetry.org | python3 -
```

### Hypervisor setup

You will need to ssh into 
- the hypervisor as ANSIBLE_USER from workstation
- the target VM as ANSIBLE_USER from hypervisor

**KVM host setup**

```bash
apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager cpu-checker python3-pip python3-venv pipx software-properties-common -y
systemctl status libvirtd
virsh net-start default
virsh net-autostart default

pipx ensurepath
```

**KVM build guest setup**
```bash
apt sudo install python3-pip python3-venv rsync libvirt-dev python3-pip python3-venv pipx qemu-guest-agent  -y
systemctl enable qemu-guest-agent
systemctl start qemu-guest-agent

```



