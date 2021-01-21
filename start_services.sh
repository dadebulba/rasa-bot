# cd /app
# Start rasa server with nlu model
rasa run --model app/models/20210119-214452.tar.gz --enable-api --cors "*" --debug -p $PORT