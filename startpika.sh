
# sudo docker run -d -p 5672:5672 -e RABBITMQ_DEFAULT_USER=saarthi -e RABBITMQ_DEFAULT_PASS=analytics rabbitmq:3-management
echo "starting pika english>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"


exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 
exec nohup python analytics/pika-consumer.py --endpoints constants/emi_english/endpoints_core.yml & 


echo "starting pika Tamil>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 
exec nohup python analytics/pika-consumer-tamil.py --endpoints constants/emi_english/endpoints_core_tamil.yml & 


echo "starting pika Telugu>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 
exec nohup python analytics/pika-consumer-telugu.py --endpoints constants/emi_english/endpoints_core_telugu.yml & 


echo "starting pika Kannada>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &
exec nohup python analytics/pika-consumer-kannada.py --endpoints constants/emi_english/endpoints_core_kannada.yml &


echo "starting pika Malayalam>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &
exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &
exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &
exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &
exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &
exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &
exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &
exec nohup python analytics/pika-consumer-malayalam.py --endpoints constants/emi_english/endpoints_core_malayalam.yml &


echo "starting pika Bengali>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &
exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &
exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &
exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &
exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &
exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &
exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &
exec nohup python analytics/pika-consumer-bengali.py --endpoints constants/emi_english/endpoints_core_bengali.yml &

echo "starting pika Marathi>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &
exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &
exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &
exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &
exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &
exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &
exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &
exec nohup python analytics/pika-consumer-marathi.py --endpoints constants/emi_english/endpoints_core_marathi.yml &

echo "starting pika punjabi>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

exec nohup python analytics/pika-consumer-punjabi.py --endpoints constants/emi_english/endpoints_core_punjabi.yml &
exec nohup python analytics/pika-consumer-punjabi.py --endpoints constants/emi_english/endpoints_core_punjabi.yml &
exec nohup python analytics/pika-consumer-punjabi.py --endpoints constants/emi_english/endpoints_core_punjabi.yml &
exec nohup python analytics/pika-consumer-punjabi.py --endpoints constants/emi_english/endpoints_core_punjabi.yml &
exec nohup python analytics/pika-consumer-punjabi.py --endpoints constants/emi_english/endpoints_core_punjabi.yml &
exec nohup python analytics/pika-consumer-punjabi.py --endpoints constants/emi_english/endpoints_core_punjabi.yml &
exec nohup python analytics/pika-consumer-punjabi.py --endpoints constants/emi_english/endpoints_core_punjabi.yml &


echo "starting pika gujarati>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

exec nohup python analytics/pika-consumer-gujarathi.py --endpoints constants/emi_english/endpoints_core_gujarati.yml &
exec nohup python analytics/pika-consumer-gujarathi.py --endpoints constants/emi_english/endpoints_core_gujarati.yml &
exec nohup python analytics/pika-consumer-gujarathi.py --endpoints constants/emi_english/endpoints_core_gujarati.yml &
exec nohup python analytics/pika-consumer-gujarathi.py --endpoints constants/emi_english/endpoints_core_gujarati.yml &
exec nohup python analytics/pika-consumer-gujarathi.py --endpoints constants/emi_english/endpoints_core_gujarati.yml &
exec nohup python analytics/pika-consumer-gujarathi.py --endpoints constants/emi_english/endpoints_core_gujarati.yml &