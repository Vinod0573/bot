#!/bin/bash

exec python get_customer_details.py &

#english
exec python nlu/emi_english/app.py &
exec python nlg/emi_english/nlg_server.py &
exec python -m rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core.yml --port 8030 -vv &
exec python -m rasa run actions --actions actions.actions --port 5030 -vv &
exec python Orchestrator/CZ/orchestrator.py --port 7114   &


#hindi
exec python nlu/emi_english/app_hindi.py &
exec python nlg/emi_english/nlg_server_hindi.py &
exec python -m rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_hindi.yml --port 8330 -vv &
exec python -m rasa run actions --actions actions.actions --port 5330 -vv &
exec python Orchestrator/CZ/orchestrator_hindi.py --port 7115   &


# Kannada
exec python Orchestrator/CZ/orchestrator_kannada.py --port 7566 &

exec python nlu/emi_english/app_kannada.py &
exec python nlg/emi_english/nlg_server_kannada.py &
exec python -m rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_kannada.yml --port 8430 -vv &
exec python -m rasa run actions --actions actions.actions --port 5430 -vv &

#telugu

exec python Orchestrator/CZ/orchestrator_telugu.py --port 7117  &

exec python nlu/emi_english/app_telugu.py &
exec python nlg/emi_english/nlg_server_telugu.py &
exec python -m rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_telugu.yml --port 8930 -vv &
exec python -m rasa run actions --actions actions.actions --port 5930 -vv 
# echo "entering into sbot side"