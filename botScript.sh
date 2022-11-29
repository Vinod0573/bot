#!/bin/bash

echo "starting english>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

sudo kill -9 $(sudo lsof -t -i:7114)
sudo kill -9 $(sudo lsof -t -i:8030)
sudo kill -9 $(sudo lsof -t -i:8031)
sudo kill -9 $(sudo lsof -t -i:5030)
sudo kill -9 $(sudo lsof -t -i:5031)
sudo kill -9 $(sudo lsof -t -i:5032)
sudo kill -9 $(sudo lsof -t -i:5033)
sudo kill -9 $(sudo lsof -t -i:12214)
sudo kill -9 $(sudo lsof -t -i:13279)

sudo kill -9 $(sudo lsof -t -i:8930)
sudo kill -9 $(sudo lsof -t -i:8931)
sudo kill -9 $(sudo lsof -t -i:5930)
sudo kill -9 $(sudo lsof -t -i:5931)
sudo kill -9 $(sudo lsof -t -i:5932)
sudo kill -9 $(sudo lsof -t -i:5933)
sudo kill -9 $(sudo lsof -t -i:12217)
sudo kill -9 $(sudo lsof -t -i:13317)
sudo kill -9 $(sudo lsof -t -i:7117)

sudo kill -9 $(sudo lsof -t -i:8830)
sudo kill -9 $(sudo lsof -t -i:8831)
sudo kill -9 $(sudo lsof -t -i:5830)
sudo kill -9 $(sudo lsof -t -i:5831)
sudo kill -9 $(sudo lsof -t -i:5832)
sudo kill -9 $(sudo lsof -t -i:5833)
sudo kill -9 $(sudo lsof -t -i:12216)
sudo kill -9 $(sudo lsof -t -i:13216)
sudo kill -9 $(sudo lsof -t -i:7116)

sudo kill -9 $(sudo lsof -t -i:8730)
sudo kill -9 $(sudo lsof -t -i:8731)
sudo kill -9 $(sudo lsof -t -i:5730)
sudo kill -9 $(sudo lsof -t -i:5731)
sudo kill -9 $(sudo lsof -t -i:5732)
sudo kill -9 $(sudo lsof -t -i:5733)
sudo kill -9 $(sudo lsof -t -i:12616)
sudo kill -9 $(sudo lsof -t -i:13616)
sudo kill -9 $(sudo lsof -t -i:7616)

sudo kill -9 $(sudo lsof -t -i:8630)
sudo kill -9 $(sudo lsof -t -i:8631)
sudo kill -9 $(sudo lsof -t -i:5630)
sudo kill -9 $(sudo lsof -t -i:5631)
sudo kill -9 $(sudo lsof -t -i:5632)
sudo kill -9 $(sudo lsof -t -i:5633)
sudo kill -9 $(sudo lsof -t -i:12716)
sudo kill -9 $(sudo lsof -t -i:13716)
sudo kill -9 $(sudo lsof -t -i:7716)

sudo kill -9 $(sudo lsof -t -i:8530)
sudo kill -9 $(sudo lsof -t -i:8531)
sudo kill -9 $(sudo lsof -t -i:5530)
sudo kill -9 $(sudo lsof -t -i:5531)
sudo kill -9 $(sudo lsof -t -i:5532)
sudo kill -9 $(sudo lsof -t -i:5533)
sudo kill -9 $(sudo lsof -t -i:12339)
sudo kill -9 $(sudo lsof -t -i:13249)
sudo kill -9 $(sudo lsof -t -i:7239)

sudo kill -9 $(sudo lsof -t -i:8430)
sudo kill -9 $(sudo lsof -t -i:8431)
sudo kill -9 $(sudo lsof -t -i:5430)
sudo kill -9 $(sudo lsof -t -i:5431)
sudo kill -9 $(sudo lsof -t -i:5432)
sudo kill -9 $(sudo lsof -t -i:5433)
sudo kill -9 $(sudo lsof -t -i:12676)
sudo kill -9 $(sudo lsof -t -i:13166)
sudo kill -9 $(sudo lsof -t -i:7566)

sudo kill -9 $(sudo lsof -t -i:8330)
sudo kill -9 $(sudo lsof -t -i:8331)
sudo kill -9 $(sudo lsof -t -i:5330)
sudo kill -9 $(sudo lsof -t -i:5331)
sudo kill -9 $(sudo lsof -t -i:5332)
sudo kill -9 $(sudo lsof -t -i:5333)
sudo kill -9 $(sudo lsof -t -i:12215)
sudo kill -9 $(sudo lsof -t -i:13315)
sudo kill -9 $(sudo lsof -t -i:7115)

sudo kill -9 $(sudo lsof -t -i:8130)
sudo kill -9 $(sudo lsof -t -i:8131)
sudo kill -9 $(sudo lsof -t -i:5130)
sudo kill -9 $(sudo lsof -t -i:5131)
sudo kill -9 $(sudo lsof -t -i:5132)
sudo kill -9 $(sudo lsof -t -i:5133)
sudo kill -9 $(sudo lsof -t -i:12633)
sudo kill -9 $(sudo lsof -t -i:13133)
sudo kill -9 $(sudo lsof -t -i:7133)

sudo kill -9 $(sudo lsof -t -i:8230)
sudo kill -9 $(sudo lsof -t -i:8231)
sudo kill -9 $(sudo lsof -t -i:5230)
sudo kill -9 $(sudo lsof -t -i:5231)
sudo kill -9 $(sudo lsof -t -i:5232)
sudo kill -9 $(sudo lsof -t -i:5233)
sudo kill -9 $(sudo lsof -t -i:12816)
sudo kill -9 $(sudo lsof -t -i:13816)
sudo kill -9 $(sudo lsof -t -i:7617)
sudo kill -9 $(sudo lsof -t -i:7222)
# sudo kill -9 $(sudo lsof -t -i:5672)


# sudo kill -9 $(sudo lsof -t -i:7617)
exec nohup python get_customer_details &

# sudo docker run -d -p 5672:5672 -e RABBITMQ_DEFAULT_USER=saarthi -e RABBITMQ_DEFAULT_PASS=analytics rabbitmq:3-management

echo "Starting Redis"

exec nohup python get_customer_details.py &

echo "Starting English Server"

exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core.yml --port 8030 -vv &
exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core.yml --port 8031 -vv &
exec nohup rasa run actions --actions actions.actions --port 5030 -vv &
exec nohup rasa run actions --actions actions.actions --port 5031 -vv &
exec nohup rasa run actions --actions actions.actions --port 5032 -vv &
exec nohup rasa run actions --actions actions.actions --port 5033 -vv &
exec nohup python nlu/emi_english/app.py &
exec nohup python nlg/emi_english/nlg_server.py &
exec nohup python Orchestrator/CZ/orchestrator.py &

echo "starting hindi>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_hindi.yml --port 8330 -vv &
exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_hindi.yml --port 8331 -vv &
exec nohup rasa run actions --actions actions.actions --port 5330 -vv &
exec nohup rasa run actions --actions actions.actions --port 5331 -vv &
exec nohup rasa run actions --actions actions.actions --port 5332 -vv &
exec nohup rasa run actions --actions actions.actions --port 5333 -vv &
exec nohup python nlu/emi_english/app_hindi.py &
exec nohup python nlg/emi_english/nlg_server_hindi.py &
exec nohup python Orchestrator/CZ/orchestrator_hindi.py &


echo "starting kannada>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_kannada.yml --port 8430 -vv &
exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_kannada.yml --port 8431 -vv &
exec nohup rasa run actions --actions actions.actions --port 5430 -vv &
exec nohup rasa run actions --actions actions.actions --port 5431 -vv &
exec nohup rasa run actions --actions actions.actions --port 5432 -vv &
exec nohup rasa run actions --actions actions.actions --port 5433 -vv &
exec nohup python nlu/emi_english/app_kannada.py &
exec nohup python nlg/emi_english/nlg_server_kannada.py &
exec nohup python Orchestrator/CZ/orchestrator_kannada.py &


echo "starting malayalam>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_malayalam.yml --port 8530 -vv &
exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_malayalam.yml --port 8531 -vv &
exec nohup rasa run actions --actions actions.actions --port 5530 -vv &
exec nohup rasa run actions --actions actions.actions --port 5531 -vv &
exec nohup rasa run actions --actions actions.actions --port 5532 -vv &
exec nohup rasa run actions --actions actions.actions --port 5533 -vv &
exec nohup python nlu/emi_english/app_malayalam.py &
exec nohup python nlg/emi_english/nlg_server_malayalam.py &
exec nohup python Orchestrator/CZ/orchestrator_malayalam.py &


echo "starting tamil>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_tamil.yml --port 8830 -vv &
exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_tamil.yml --port 8831 -vv &
exec nohup rasa run actions --actions actions.actions --port 5830 -vv &
exec nohup rasa run actions --actions actions.actions --port 5831 -vv &
exec nohup rasa run actions --actions actions.actions --port 5832 -vv &
exec nohup rasa run actions --actions actions.actions --port 5833 -vv &
exec nohup python nlu/emi_english/app_tamil.py &
exec nohup python nlg/emi_english/nlg_server_tamil.py &
exec nohup python Orchestrator/CZ/orchestrator_tamil.py &


echo "starting telugu>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_telugu.yml --port 8930 -vv &
exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_telugu.yml --port 8931 -vv &
exec nohup rasa run actions --actions actions.actions --port 5930 -vv &
exec nohup rasa run actions --actions actions.actions --port 5931 -vv &
exec nohup rasa run actions --actions actions.actions --port 5932 -vv &
exec nohup rasa run actions --actions actions.actions --port 5933 -vv &
exec nohup python nlu/emi_english/app_telugu.py &
exec nohup python nlg/emi_english/nlg_server_telugu.py &
exec nohup python Orchestrator/CZ/orchestrator_telugu.py &

echo "starting bengali"


exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_bengali.yml --port 8130 -vv &
exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_bengali.yml --port 8131 -vv &
exec nohup rasa run actions --actions actions.actions --port 5130 -vv &
exec nohup rasa run actions --actions actions.actions --port 5131 -vv &
exec nohup rasa run actions --actions actions.actions --port 5132 -vv &
exec nohup rasa run actions --actions actions.actions --port 5133 -vv &
exec nohup python nlu/emi_english/app_bengali.py &
exec nohup python nlg/emi_english/nlg_server_bengali.py &
exec nohup python Orchestrator/CZ/orchestrator_bengali.py &

echo "starting Gujarati>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"


exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_gujarati.yml --port 8230 -vv &
exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_gujarati.yml --port 8231 -vv &
exec nohup rasa run actions --actions actions.actions --port 5230 -vv &
exec nohup rasa run actions --actions actions.actions --port 5231 -vv &
exec nohup rasa run actions --actions actions.actions --port 5232 -vv &
exec nohup rasa run actions --actions actions.actions --port 5233 -vv &
exec nohup python nlu/emi_english/app_gujarati.py &
exec nohup python nlg/emi_english/nlg_server_gujarati.py &
exec nohup python Orchestrator/CZ/orchestrator_gujarati.py &

echo "starting Punjabi>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"


exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_punjabi.yml --port 8730 -vv &
exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_punjabi.yml --port 8731 -vv &
exec nohup rasa run actions --actions actions.actions --port 5730 -vv &
exec nohup rasa run actions --actions actions.actions --port 5731 -vv &
exec nohup rasa run actions --actions actions.actions --port 5732 -vv &
exec nohup rasa run actions --actions actions.actions --port 5733 -vv &
exec nohup python nlu/emi_english/app_punjabi.py &
exec nohup python nlg/emi_english/nlg_server_punjabi.py &
exec nohup python Orchestrator/CZ/orchestrator_punjabi.py &

echo "starting Marathi>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"


exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_marathi.yml --port 8630 -vv &
exec nohup rasa run --enable-api -m models/emi_english/emi_english_core.tar.gz --endpoints constants/emi_english/endpoints_core_marathi.yml --port 8631 -vv &
exec nohup rasa run actions --actions actions.actions --port 5630 -vv &
exec nohup rasa run actions --actions actions.actions --port 5631 -vv &
exec nohup rasa run actions --actions actions.actions --port 5632 -vv &
exec nohup rasa run actions --actions actions.actions --port 5633 -vv &
exec nohup python nlu/emi_english/app_marathi.py &
exec nohup python nlg/emi_english/nlg_server_marathi.py &
exec nohup python Orchestrator/CZ/orchestrator_marathi.py &

# echo "starting pika hindi>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

# exec nohup python analytics/pika-consumer-hindi.py --endpoints constants/emi_english/endpoints_core_hindi.yml & 
# exec nohup python analytics/pika-consumer-hindi.py --endpoints constants/emi_english/endpoints_core_hindi.yml & 
# exec nohup python analytics/pika-consumer-hindi.py --endpoints constants/emi_english/endpoints_core_hindi.yml & 
# exec nohup python analytics/pika-consumer-hindi.py --endpoints constants/emi_english/endpoints_core_hindi.yml & 
# exec nohup python analytics/pika-consumer-hindi.py --endpoints constants/emi_english/endpoints_core_hindi.yml & 
# exec nohup python analytics/pika-consumer-hindi.py --endpoints constants/emi_english/endpoints_core_hindi.yml & 
# exec nohup python analytics/pika-consumer-hindi.py --endpoints constants/emi_english/endpoints_core_hindi.yml & 
# exec nohup python analytics/pika-consumer-hindi.py --endpoints constants/emi_english/endpoints_core_hindi.yml & 
# exec nohup python analytics/pika-consumer-hindi.py --endpoints constants/emi_english/endpoints_core_hindi.yml & 
# exec nohup python analytics/pika-consumer-hindi.py --endpoints constants/emi_english/endpoints_core_hindi.yml & 
# exec nohup python analytics/pika-consumer-hindi.py --endpoints constants/emi_english/endpoints_core_hindi.yml & 
# exec nohup python analytics/pika-consumer-hindi.py --endpoints constants/emi_english/endpoints_core_hindi.yml & 
# exec nohup python analytics/pika-consumer-hindi.py --endpoints constants/emi_english/endpoints_core_hindi.yml & 
# exec nohup python analytics/pika-consumer-hindi.py --endpoints constants/emi_english/endpoints_core_hindi.yml & 


# echo "starting pika english>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"


# exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
# exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
# exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
# exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
# exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
# exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
# exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
# exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
# exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
# exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
# exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
# exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
# exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
# exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
# exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 


# echo "starting pika Tamil>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

# exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
# exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
# exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
# exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
# exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
# exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
# exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
# exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
# exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 


# echo "starting pika Telugu>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

# exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
# exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
# exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
# exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
# exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
# exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
# exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
# exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
# exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 


# echo "starting pika Kannada>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

# exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
# exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
# exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
# exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
# exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
# exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
# exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
# exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
# exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &


# echo "starting pika Malayalam>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

# exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &
# exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &
# exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &
# exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &
# exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &
# exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &
# exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &
# exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &


# echo "starting pika Bengali>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

# exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &
# exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &
# exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &
# exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &
# exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &
# exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &
# exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &
# exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &

# echo "starting pika Marathi>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

# exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &
# exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &
# exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &
# exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &
# exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &
# exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &
# exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &
# exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &

# echo "starting pika punjabi>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

# exec nohup python analytics/pika-consumer-punjabi.py --endpoints constants/emi_english/endpoints_core_punjabi.yml &
# exec nohup python analytics/pika-consumer-punjabi.py --endpoints constants/emi_english/endpoints_core_punjabi.yml &
# exec nohup python analytics/pika-consumer-punjabi.py --endpoints constants/emi_english/endpoints_core_punjabi.yml &
# exec nohup python analytics/pika-consumer-punjabi.py --endpoints constants/emi_english/endpoints_core_punjabi.yml &
# exec nohup python analytics/pika-consumer-punjabi.py --endpoints constants/emi_english/endpoints_core_punjabi.yml &
# exec nohup python analytics/pika-consumer-punjabi.py --endpoints constants/emi_english/endpoints_core_punjabi.yml &
# exec nohup python analytics/pika-consumer-punjabi.py --endpoints constants/emi_english/endpoints_core_punjabi.yml &


# echo "starting pika gujarati>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

# exec nohup python analytics/pika-consumer-gujarathi.py --endpoints constants/emi_english/endpoints_core_gujarati.yml &
# exec nohup python analytics/pika-consumer-gujarathi.py --endpoints constants/emi_english/endpoints_core_gujarati.yml &
# exec nohup python analytics/pika-consumer-gujarathi.py --endpoints constants/emi_english/endpoints_core_gujarati.yml &
# exec nohup python analytics/pika-consumer-gujarathi.py --endpoints constants/emi_english/endpoints_core_gujarati.yml &
# exec nohup python analytics/pika-consumer-gujarathi.py --endpoints constants/emi_english/endpoints_core_gujarati.yml &
# exec nohup python analytics/pika-consumer-gujarathi.py --endpoints constants/emi_english/endpoints_core_gujarati.yml &