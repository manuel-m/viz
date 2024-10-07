include utils.mk

PACKAGE_VERSION := $(shell poetry version | cut -d ' ' -f2-)
DIST_D := ops/dist/$(PACKAGE_VERSION)

ifdef PACKAGE_VERSION
    $(info PACKAGE_VERSION:$(PACKAGE_VERSION))
else
    $(error PACKAGE_VERSION is not defined)
endif

.PHONY: \
  publish \
  setup \
  tunnels-start \
  tunnels-stop \
  
publish:
	@poetry build
	@poetry publish --repository devpi	


tunnels-start:
	@ssh -f -L $(DEVPI_PORT):$(DEVPI_HOST):$(DEVPI_PORT) $(ANSIBLE_USER)@$(HYPERVISER_HOST) -N
	@netstat -plunt 2>/dev/null | grep :$(DEVPI_PORT) | grep -v tcp6

tunnels-stop:
	@pgrep -f "ssh.*$(DEVPI_PORT):$(DEVPI_HOST):$(DEVPI_PORT)" | xargs kill
	@netstat -plunt 2>/dev/null | grep :$(DEVPI_PORT) | grep -v tcp6


setup:
	@devpi login $(DEVPI_USER) --password=$(DEVPI_USER)	
	@devpi index -c $(DEVPI_INDEX) bases=root/pypi
	@devpi logoff
	@poetry config repositories.devpi http://localhost:$(DEVPI_PORT)/$(DEVPI_USER)/$(DEVPI_INDEX)
	@poetry config http-basic.devpi $(DEVPI_USER) $(DEVPI_USER)


