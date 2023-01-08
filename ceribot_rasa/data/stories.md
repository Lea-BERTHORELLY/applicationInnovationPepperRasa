## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## EDT

* ask_schedule
    - utter_ask_section
* give_section{"section":"M2"}
    - slot{"section":"M2"}
    - slot{"section":"M2"}
    - utter_ask_spe
* give_spe{"spe":"ilsen"}
    - slot{"spe":"ilsen"}
    - slot{"section":"M2"}
    - slot{"spe":"ilsen"}
    - utter_ask_group
* give_group
    - slot{"section":"M2"}
    - slot{"spe":"ilsen"}
    - action_schedule

## ask_weather

* intent:ask_meteo
    - action_weather

## weather
* weather
  - action_weather

## Movies

* ask_movies
    - action_movies
