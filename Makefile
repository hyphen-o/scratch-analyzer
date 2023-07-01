up:
	@docker compose up -d

down:
	@docker compose down

exec:
	@docker compose exec python3 bash

cp:
	@docker cp research-python:/works ./sources

install:
	@pip install -r src/requirements.txt
