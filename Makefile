# Makefile para GitBash
up:
	docker-compose build
	docker-compose up

makemigrations:
	docker-compose exec web python manage.py makemigrations

migrate:
	docker-compose exec web python manage.py migrate

migrate_celery:
	docker-compose exec web python manage.py migrate django_celery_beat
	docker-compose exec web python manage.py shell < scripts/libro_del_dia.py

startapp:
	@read -p "Nombre de la nueva app: " app_name; \
	docker-compose exec web python manage.py startapp $$app_name

superuser:
	winpty docker-compose exec -it web python manage.py createsuperuser

shell:
	winpty docker-compose exec web python manage.py Shell

show_urls:
	docker-compose exec web python manage.py show_urls

inspect_db:
	winpty docker exec -it git-db-1 psql -U postgres -d postgres
