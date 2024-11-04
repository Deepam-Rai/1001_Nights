run-server-debug:
	rasa run --enable-api --cors "*" --debug

run-action-server:
	rasa run actions --debug

train:
	rasa train --domain domain --fixed-model-name 1001_nights