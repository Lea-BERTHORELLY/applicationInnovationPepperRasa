ps -A | grep "rasa run" | awk '{print $1}' | xargs kill -9 $1

