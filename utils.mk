

extract_value = $(shell grep $(1): ./ops/ansible/defaults/main.yml | cut -d ' ' -f2-)

# Check if .env file exists, include and export its contents if it does
ifneq (,$(wildcard ./.env))
    include .env
    export
else
    $(error .env file not found)
endif


