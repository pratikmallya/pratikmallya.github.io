.PHONY: phony

update: phony ## update dependencies
	docker run \
		-v $(PWD):/apps \
		alpine/bundle:2.7.0 \
		bundle update

# help boilerplate                                                   
#------------------------------------------------------------------------------#
BLUE := $(shell tput setaf 4)
RESET := $(shell tput sgr0)
.PHONY: help
help: ## List all targets and short descriptions of each
	@grep -E '^[^ .]+: .*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk '\
			BEGIN { FS = ": .*##" };\
			{ printf "$(BLUE)%-29s$(RESET) %s\n", $$1, $$2  }'
