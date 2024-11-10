train:
	docker compose run --rm core-server rasa train --domain domain --config config.yml --fixed-model-name 1001_nights_model --debug

run:
	docker compose up -d

stop:
	docker compose down

core-logs:
	docker compose logs -f core-server

action-logs:
	docker compose logs -f action-server

restart-core:
	docker compose restart core-server

restart-action:
	docker compose restart action-server

start-action:
	docker compose up action-server -d

train-redeploy-logs:
	make -f Makefile train
	make -f Makefile stop
	make -f Makefile run
	make -f Makefile core-logs

redeploy-logs:
	make -f Makefile stop
	make -f Makefile run
	make -f Makefile core-logs

action-redeploy-logs:
	make restart-action
	make action-logs

build:
	docker compose build


ui:
	echo "http://localhost:7999/"
	python -m http.server --directory front_end 7999

visualize:
	rasa visualize --domain domain
