
docker_run_sam_cli=docker-compose run --rm sam-cli

.PHONY: validate
validate:
	@echo "validate the package"
	$(docker_run_sam_cli) ./scripts/validate.sh

.PHONY: build
build:
	@echo "build the package"
	$(docker_run_sam_cli) sam build

.PHONY: deploy
deploy:
	@echo "deploy the package"
	sam deploy --confirm-changeset
