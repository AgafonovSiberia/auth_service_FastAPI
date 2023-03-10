run:
	docker-compose up --build

stop:
	docker-compose stop


clear_data:
	docker-compose down -v


#docker-compose exec web bash
#alembic revision --autogenerate -m "Initial" --rev-id 1
#alembic upgrade 1