init:
	@docker compose build
	@docker compose up -d

up:
	@docker compose up -d

down:
	@docker compose down

exec:
	@docker compose exec scratcher bash

cp-out:
	@docker cp scratcher:/works/out ./scratcher

install:
	@pip install -r requirements.txt

format:
	@black .

lint:
	@pylint .

generate-require:
	@pipreqs . && cat ./scratcher/requirements.txt

setup:
	@pip install setuptools wheel
	@python setup.py sdist bdist_wheel
