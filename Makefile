.PHONY: up down logs

DOCKER := docker-compose

up:
	@$(DOCKER) up -d

down:
	@$(DOCKER) down

logs:
	@$(DOCKER) logs -f
