up:
	@docker compose up -d

down:
	@docker compose down

exec:
	@docker compose exec python3 bash

cp:
	@docker cp research-python:/works ./sources

install:
	@pip install -r requirements.txt

build:
	@pip install setuptools wheel
	@python setup.py sdist bdist_wheel
