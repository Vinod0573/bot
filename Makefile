# .PHONY: clean train-nlu train-core 

help:
	@echo "    clean"
	@echo "        Remove python artifacts and build artifacts."
	@echo "    train-nlu"
	@echo "        Trains a new nlu model using the projects Rasa NLU config."
	@echo "    train-core"
	@echo "        Trains a new dialogue model using the story training data."
	@echo "    action-server"
	@echo "        Starts the server for custom action."
	@echo "    run-nlu"
	@echo "        Run nlu server"
	@echo "    run-core"
	@echo "        Run rasa core server."
	@echo "    killnlu"
	@echo "        Kill nlu server"
	@echo "    killcore"
	@echo "        Kill rasa core server."

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf docs/_build


	
train-nlu:
	rasa train --data nlu/emi_english/ -c configs/emi_english/config.yml --out models/emi_english/ --fixed-model-name emi_english_nlu -vv --domain domains/emi_english/domain.yml


train-nlu-hindi:
	rasa train --data nlu/emi_english/ -c configs/emi_english/config.yml --out models/emi_english/ --fixed-model-name emi_english_nlu_hindi -vv --domain domains/emi_english/domain.yml

train-core:
	rasa train --data stories/emi_english/stories.md -c configs/emi_english/config.yml --out models/emi_english/ --fixed-model-name emi_english_core -vv --domain domains/emi_english/domain.yml



kill-nlu:
	fuser 9135/tcp -k

kill-core:
	fuser 8135/tcp -k

run-nlu:
	rasa run --enable-api -m models/emi_english/emi_english_nlu.tar.gz --log-file rasa_nlu.log --endpoints constants/emi_english/endpoints_nlu.yml --port 9134 -vv

run-nlu_hindi:
	rasa run --enable-api -m models/emi_english/emi_english_nlu_hindi.tar.gz --log-file rasa_nlu.log --endpoints constants/emi_english/endpoints_nlu.yml --port 9135 -vv

run-core:
	rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --log-file rasa_core.log --endpoints constants/emi_english/endpoints_core.yml --port 8134 -vv

run-core-hindi:
	rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --log-file rasa_core.log --endpoints constants/emi_english/endpoints_core_hindi.yml --port 8135 -vv

run-core-kannada:
	rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --log-file rasa_core.log --endpoints constants/emi_english/endpoints_core_kannada.yml --port 8136 -vv

action-server:
	rasa run actions --actions actions.actions --port 5134 -vv
action-server-hindi:
	rasa run actions --actions actions.actions --port 5135 -vv
action-server-kannada:
	rasa run actions --actions actions.actions --port 5136 -vv