# deploy custom action

## client side
docker build -t dadebulba/rasa-custom-action .
docker push dadebulba/rasa-custom-action

## server side
docker pull dadebulba/rasa-custom-action
cd /etc/rasa
sudo docker-compose down
sudo docker-compose up -d
