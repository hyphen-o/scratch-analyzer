init:
	@docker compose build
	@docker compose up -d

up:
	@docker compose up -d

down:
	@docker compose down

exec:
	@docker compose exec scratcher bash

cp:
	@docker cp research-python:/works ./scratcher

install:
	@pip install -r requirements.txt

generate-require:
	@pipreqs . && cat ./scartcher/requirements.txt

setup:
	@pip install setuptools wheel
	@python setup.py sdist bdist_wheel
