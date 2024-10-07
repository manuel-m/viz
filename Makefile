include utils.mk

APP_ID := $(call extract_value, app_id)


OPS_WORKING_DIR := /home/$(ANSIBLE_USER)/w/opt/$(APP_ID)
ANSIBLE_PATH := /home/$(ANSIBLE_USER)/.local/bin

DASH_PORT := $(call extract_value, dash_port)

PYTHON_VERSION := $(shell cat pyproject.toml | grep "^python = " | cut -d '"' -f2)

PACKAGE_VERSION := $(shell poetry version | cut -d ' ' -f2-)
DIST_D := dist/$(PACKAGE_VERSION)
VERSION_YML := ./ops/ansible/vars/version.yml

ifdef PYTHON_VERSION
    $(info PYTHON_VERSION:$(PYTHON_VERSION))
else
    $(error PYTHON_VERSION is not defined)
endif

ifdef PACKAGE_VERSION
    $(info PACKAGE_VERSION:$(PACKAGE_VERSION))
else
    $(error PACKAGE_VERSION is not defined)
endif

ifdef ANSIBLE_USER
    $(info ANSIBLE_USER:$(ANSIBLE_USER))
else
    $(error ANSIBLE_USER is not defined)
endif

ifdef APP_ID
    $(info APP_ID:$(APP_ID))
else
    $(error APP_ID is not defined)
endif

$(info HYPERVISOR_HOST:$(HYPERVISOR_HOST))
$(info DASH_PORT:$(DASH_PORT))

.PHONY: \
  coverage \
  dist \
  gen-ops-env-yml \
  lint \
  push-ops \
  ssh-ansible \
  tidy \
  tunnels-start \
  tunnels-stop \
  unit-tests

gen-ops-env-yml:
	@python toolchain/dotenv-toyaml.py  

lint:
	@mypy --config-file mypy.ini .

lint-dev:
	@python toolchain/lint-dev.py	

logs-dash:
	@ssh -t $(ANSIBLE_USER)@$(HYPERVISOR_HOST) sudo journalctl -u dash -f

deploy-dash: push-ops
	@ssh -t $(ANSIBLE_USER)@$(HYPERVISOR_HOST) \
	"cd $(OPS_WORKING_DIR)/ansible;$(ANSIBLE_PATH)/ansible-playbook ./playbooks/deploy_app_hypervisor.yml"

push-ops: gen-ops-env-yml
	@rsync -avz --delete ./ops/ $(ANSIBLE_USER)@$(HYPERVISOR_HOST):$(OPS_WORKING_DIR)/
	@rsync -avz ./dist/ $(ANSIBLE_USER)@$(HYPERVISOR_HOST):/home/$(ANSIBLE_USER)/w/opt/dist/

ssh-ansible: push-ops
	@ssh -t $(ANSIBLE_USER)@$(HYPERVISOR_HOST) "cd $(OPS_WORKING_DIR)/ansible; bash --login"

tunnels-start:
	@ssh -f -L $(DASH_PORT):$(HYPERVISOR_HOST):$(DASH_PORT) $(ANSIBLE_USER)@$(HYPERVISOR_HOST) -N
	@netstat -plunt 2>/dev/null | grep :$(DASH_PORT) | grep -v tcp6

tunnels-stop:
	@pgrep -f "ssh.*$(DASH_PORT):$(HYPERVISOR_HOST):$(DASH_PORT)" | xargs kill
	@netstat -plunt 2>/dev/null | grep :$(DASH_PORT) | grep -v tcp6

dist: lint
	@echo "---\napp_version: $(PACKAGE_VERSION)\npython_version: $(PYTHON_VERSION)" > $(VERSION_YML)
	@mkdir -p $(DIST_D)/packages
	@poetry export -f requirements.txt --output $(DIST_D)/requirements.txt --without-hashes
	@pip download -r $(DIST_D)/requirements.txt -d $(DIST_D)/packages
	@pip download setuptools wheel -d $(DIST_D)/packages
	@echo "$(APP_ID)==$(PACKAGE_VERSION) ;" >> $(DIST_D)/requirements.txt
	@poetry build -o $(DIST_D)/packages/
	@cd $(DIST_D) && tar -czf ../$(APP_ID).bundle.$(PACKAGE_VERSION).tar.gz packages requirements.txt
	@rm -rf $(DIST_D)



unit-tests:
	pytest -v

coverage:
	pytest --cov=viz && coverage html

tidy:
	isort **/*.py
	black .