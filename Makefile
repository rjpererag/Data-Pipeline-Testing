POSTGRES_USERS_CONTAINER_NAME=postgres-users
POSTGRES_USERS_DB=postgres_users
POSTGRES_USERS_USER=admin
POSTGRES_USERS_PASSWORD=admin
POSTGRES_USERS_PORT=5432

# USER DB ------------------------------------------------------

.PHONY: start-user-db
start-user-db:
	@make user-db-build
	@make user-db-wait
	@make user-db-populate
	@echo "DB running and populated"


.PHONY: user-db-build
user-db-build:
	@echo "Building $(POSTGRES_USERS_CONTAINER_NAME) ..."
	@docker compose up $(POSTGRES_USERS_CONTAINER_NAME) --build -d
	@echo "Built!"

.PHONY: user-db-down-full
user-db-down-full:
	@echo "Stopping and removing volumes to $(POSTGRES_USERS_CONTAINER_NAME) ..."
	@docker compose down $(POSTGRES_USERS_CONTAINER_NAME) -v


.PHONY: user-db-wait
user-db-wait:
	@echo "Waiting for $(POSTGRES_USERS_CONTAINER_NAME) to be ready..."
	@until docker exec $(POSTGRES_USERS_CONTAINER_NAME) \
		pg_isready -U $(POSTGRES_USERS_USER) -d $(POSTGRES_USERS_DB) -q; do \
			echo "  still waiting..."; \
			sleep 1; \
	done
	@echo "DB is ready!"


.PHONY: user-db-populate
user-db-populate:
	@echo "Populating users DB"
	@docker exec -i $(POSTGRES_USERS_CONTAINER_NAME) \
		env PGPASSWORD=$(POSTGRES_USERS_PASSWORD) \
		psql -U $(POSTGRES_USERS_USER) -d $(POSTGRES_USERS_DB) < dev_scripts/populate.sql
	@echo "Done."


# API  ------------------------------------------------------
API_URL ?=  http://127.0.0.1:5001
TOKEN ?= parameta-dev-2026
ENDPOINT = /auth/status

.PHONY: api-auth
api-auth:
	@echo "Verifying Authorization against $(API_URL)..."
	curl -H "Authorization: Bearer $(TOKEN)" $(API_URL)$(ENDPOINT)

