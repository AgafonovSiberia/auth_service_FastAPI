run:
	docker compose up --build

run_test:
	docker compose exec web pytest -v

stop:
	docker compose stop


clear_data:
	docker compose down -v


#docker-compose exec web bash
#alembic revision --autogenerate -m "Initial" --rev-id 1
#alembic upgrade 1