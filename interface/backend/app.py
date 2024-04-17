from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import joblib
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np 
import openai


app = Flask(__name__)
CORS(app)

# put openai api key here
openai.api_key = ""

########################################################
#                      Class match                     #
########################################################
class Match:
    def __init__(self):
        self.columns_name = ['red_assists', 'red_deaths', \
            'red_wards_placed','red_wards_killes', 'red_gold_earned', \
            'red_inhibitor_takedowns','red_total_minions_killed',\
            'red_total_time_CC_dealt', 'red_vision_score','red_first_baron', \
            'red_first_blood', 'red_first_dragon','red_first_inhibitor', \
            'red_first_riftHerald', 'red_first_tower','blue_number_pings',\
            'blue_assists', 'blue_deaths', 'blue_wards_placed', 'blue_wards_killes',\
            'blue_gold_earned', 'blue_inhibitor_takedowns','blue_total_minions_killed', \
            'blue_total_time_CC_dealt','blue_vision_score',  'blue_first_baron', \
            'blue_first_blood','blue_first_dragon', 'blue_first_inhibitor', \
            'blue_first_riftHerald','blue_first_tower', 'red_baron_kills', 'blue_baron_kills']
        self.events = pd.DataFrame(columns=self.columns_name+'red_win')
        self.model = joblib.load('random_forest_model.pkl')
        self.result = None
        self.win_rate = []

    def add_events(self, events):
        for event in events['event']:
            self.events.loc[0, event['name']] += event['value']
        return self.predict(events['time'])

    def predict(self, time):
        new_status = self.events[self.columns_name]
        result = {'red_win':0, 'red_lose':0}
        for i in range(100):
            prediction = self.model(new_status)
            if prediction == 0: 
                result['red_lose'] += 1
            else:
                result['red_win'] += 1
        rate = result['red_win'] / (result['red_win'] + result['red_lose'])
        self.win_rate.append({'time': time, 'rate': rate})
        return rate

    def get_win_rate(self):
        return self.win_rate
    
match = Match()
########################################################
#                Prediction and Comment                #
########################################################
@app.route('/api/prediction', methods=['GET'])
def prediction():
    try:
        # get events from frontend
        events = request.args.get('events')

        match.add_events(events)

        result = match.get_win_rate()

        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/api/gpt', methods=['GET'])
def gpt():
    try:
        # get events from frontend
        events = request.args.get('events')

        input_messages = {"role": "user",
            "content":'There is a ongoing League of legends match, \
            now below game events occur, please make a comment(words litmit:50) \
            to explain what happen' + events['event']}

        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[input_messages]
        )

        response = completion.choices[0].message.content

        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)})
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug = True)
    # debug = True, use_reloader=False