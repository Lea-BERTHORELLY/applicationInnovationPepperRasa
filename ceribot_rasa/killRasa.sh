ps -A | grep rasa | awk '{print $1}' | xargs kill -9 $1

