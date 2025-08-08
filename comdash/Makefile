SHELL := /usr/bin/bash

.PHONY: up down logs sh migrate makemigrations createsuperuser seed

up:
	docker compose up --build -d
	echo "App: http://localhost:8000 | Docs: http://localhost:8000/api/docs/ | Admin: http://localhost:8000/admin/"
	docker compose logs -f web | sed -n '1,120p'

down:
	docker compose down -v

logs:
	docker compose logs -f web

sh:
	docker compose exec web bash

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

createsuperuser:
	docker compose exec web python manage.py createsuperuser

seed:
	docker compose exec web python manage.py seed_demo