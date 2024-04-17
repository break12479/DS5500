import requests
import time
import pandas as pd
import json

request_url = "http://americas.api.riotgames.com/"
apiKey = "RGAPI-3720c8a5-5019-4860-a9a7-54dcf562ec14"
request_count_in_second = 0
request_count_in_two_mins = 0
timestamp_in_second = time.time()
timestamp_in_two_mins = time.time()
iseN = 0

class LOLAPI:
    def __init__(self, name, tagline, apikey = apiKey):
        self.name = name
        self.tagLine = tagline
        self.apiKey = apiKey
        self.reqiestNo = 10
        self.puuid = "kaP-aoh24Dv-ElpmbKf085bZyWb1aSUagNX1NCi9gfVAVwocBTQ9jCQbsWgrukwAHbgauIxY447E8g"

    def controllLimit(self, cur):
        global request_count_in_second, request_count_in_two_mins, timestamp_in_second, timestamp_in_two_mins
        request_count_in_second += 1
        request_count_in_two_mins += 1
        print("request_count_in_second:", request_count_in_second, "\nrequest_count_in_two_mins:", request_count_in_two_mins, 
              '\ncurrent step:', cur, "!!!!")
        # Check if 1 second has passed since the last request
        if time.time() - timestamp_in_second >= 1:
            request_count_in_second = 0
            timestamp_in_second = time.time()
            print("reset one second")

        if time.time() - timestamp_in_two_mins >= 120:
            request_count_in_two_mins = 0
            timestamp_in_two_mins = time.time()
            print("reset two mins")

        # Check if the request count exceeds the limit for 1 second
        if request_count_in_second >= 20:
            # Wait for the next second to make the request
            print("wait one second")
            time.sleep(1 - (time.time() - timestamp_in_second))
            request_count_in_second = 0
            timestamp_in_second = time.time()

        if request_count_in_two_mins >= 100:
            # Wait for the next 2mins to make the request
            print("wait two mins")
            time.sleep(130 - (time.time() - timestamp_in_two_mins))
            request_count_in_two_mins = 0
            timestamp_in_two_mins = time.time()

        

    def find_my_puuid(self):
        self.controllLimit('finding my puuid')
        url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/" + self.name + "/" + self.tagLine + "?api_key=" + apiKey
        response = requests.get(url)
        response = response.json()
        puuid = response["puuid"]
        return puuid

    def getPuuid(self):
        return self.puuid

    def getChallengerSid(self):
        self.controllLimit('getting challenger sid')
        url = "https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + apiKey
        response = requests.get(url)
        response = response.json()
        summoners = response['entries']
        summIdNPoints = []
        for summoner in summoners:
            summIdNPoints.append((summoner['summonerId'], summoner['leaguePoints']))
        summIdNPoints = sorted(summIdNPoints, key=lambda x: x[1], reverse=True)
        return summIdNPoints

    def getPuuidBySid(self):
        summIdNPoints = self.getChallengerSid()
        puuids = []
        for summ in summIdNPoints:
            self.controllLimit('getting puuid by sid')
            url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/" + summ[0] + "?api_key=" + apiKey
            response = requests.get(url)
            response = response.json() 
            puuids.append(response["puuid"])
        return puuids

    def getMatchesIdByPuuid(self):
        puuids = self.getPuuidBySid()
        matches_id = set()
        for puuid in puuids:
            self.controllLimit('getting matches by puuid')
            url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?type=ranked&start=0&count=100&api_key=" + apiKey
            response = requests.get(url)
            response = response.json()
            matches_id.update(response)
        return matches_id
    
    def getMatchesById(self, n):
                # # File path to save JSON data
        file_path = "matchesId.json"

        # Write list to JSON file
        with open(file_path, "r") as json_file:
            matches_id = json.load(json_file)

        matches_id = list(set(matches_id))

        global iseN
        lastErr = -1
        matches = []
        skip = False
        j = n
        while j < len(matches_id):
            id = matches_id[j]
            j += 1
            self.controllLimit('getting matches by matches id')
            url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + id + "?api_key=" + apiKey
            response = requests.get(url)
            response = response.json()
            # response = json.loads(response)
            
            while 'status' in response:
                if lastErr != j:
                    lastErr = j
                    iseN = 0
                if matches != []:
                    df = pd.DataFrame(matches)
                    df.to_csv('./data/matches/matches_' + str(j) + '.csv', index=False)
                    matches = []
                print(response['status'])
                print('error re-try times:', iseN)
                time.sleep(120 + 2 ** iseN * 60)
                iseN += 1
                skip = True
                j -= 1
                break
                
            if skip or response["info"]["teams"] == []:
                skip = False
                continue

            match = dict()
            match["matchId"] = response["metadata"]["matchId"]
            match["participants"] = response["metadata"]["participants"]
            match["gameDuration"] = response["info"]["gameDuration"]
            match["gameMode"] = response["info"]["gameMode"]
            match["gameVersion"] = response["info"]["gameVersion"]

            match["red_number_pings"] = 0
            match["red_assists"] = 0
            match["red_deaths"] = 0
            match["red_wards_placed"] = 0
            match["red_wards_killes"] = 0
            match["red_gold_earned"] = 0
            match["red_inhibitor_takedowns"] = response["info"]["teams"][0]["objectives"]["inhibitor"]["kills"]
            match["red_inhibitor_lost"] = 0
            match["red_total_minions_killed"] = 0
            match["red_total_time_CC_dealt"] = 0
            match["red_vision_score"] = 0
            match["red_win"] = 0
            match["red_first_baron"] = 1 if response["info"]["teams"][0]["objectives"]["baron"]["first"] == True else 0
            match["red_first_blood"] = 1 if response["info"]["teams"][0]["objectives"]["champion"]["first"] == True else 0
            match["red_first_dragon"] = 1 if response["info"]["teams"][0]["objectives"]["dragon"]["first"] == True else 0
            match["red_first_inhibitor"] = 1 if response["info"]["teams"][0]["objectives"]["inhibitor"]["first"] == True else 0
            match["red_first_riftHerald"] = 1 if response["info"]["teams"][0]["objectives"]["riftHerald"]["first"] == True else 0
            match["red_first_tower"] = 1 if response["info"]["teams"][0]["objectives"]["tower"]["first"] == True else 0
            # champLevel championName item0-6 lane
            match["red_champion"] = []
            # spell1times spell1 spell2times spell2 
            match["red_summoner_spell"] = []
            match["red_bans"] = []

            match["blue_number_pings"] = 0
            match["blue_assists"] = 0
            match["blue_deaths"] = 0
            match["blue_wards_placed"] = 0
            match["blue_wards_killes"] = 0
            match["blue_gold_earned"] = 0
            match["blue_inhibitor_takedowns"] = response["info"]["teams"][1]["objectives"]["inhibitor"]["kills"]
            match["blue_inhibitor_lost"] = 0
            match["blue_total_minions_killed"] = 0
            match["blue_total_time_CC_dealt"] = 0
            match["blue_vision_score"] = 0
            match["blue_win"] = 0
            match["blue_first_baron"] = 1 if response["info"]["teams"][1]["objectives"]["baron"]["first"] == True else 0
            match["blue_first_blood"] = 1 if response["info"]["teams"][1]["objectives"]["champion"]["first"] == True else 0
            match["blue_first_dragon"] = 1 if response["info"]["teams"][1]["objectives"]["dragon"]["first"] == True else 0
            match["blue_first_inhibitor"] = 1 if response["info"]["teams"][1]["objectives"]["inhibitor"]["first"] == True else 0
            match["blue_first_riftHerald"] = 1 if response["info"]["teams"][1]["objectives"]["riftHerald"]["first"] == True else 0
            match["blue_first_tower"] = 1 if response["info"]["teams"][1]["objectives"]["tower"]["first"] == True else 0
            # champLevel championName item0-6 lane
            match["blue_champion"] = []
            # spell1times spell1 spell2times spell2 
            match["blue_summoner_spell"] = []
            match["blue_bans"] = []

            for i in range(len(response["info"]["participants"])):
                participant = response["info"]["participants"][i]
                player = []
                spell = []
                if i <= 4:
                    for key, value in participant.items():
                        if key[-5:] == "Pings":
                            match["red_number_pings"] += value
                        elif key == "assists":
                            match["red_assists"] += value
                        elif key == "baronKills":
                            match["red_baron_kills"] = value
                        elif key == "champLevel":
                            player.append(value)
                        elif key == "championName":
                            player.append(value)
                        elif key[:4] == "item":
                            player.append(value)
                        elif key == "lane":
                            player.append(value)
                        elif key == "deaths":
                            match["red_deaths"] += value
                        elif key == "detectorWardsPlaced" or key == "wardsPlaced":
                            match["red_wards_placed"] += value
                        elif key == "wardsKilled":
                            match["red_wards_killes"] += value
                        elif key == "goldEarned":
                            match["red_gold_earned"] += value
                        elif key == "inhibitorsLost":
                            match["red_inhibitor_lost"] = value
                        elif key[:9] == "summoner1" or key[:9] == "summoner2":
                            spell.append(value)
                        elif key == "totalMinionsKilled":
                            match["red_total_minions_killed"] += value
                        elif key == "totalTimeCCDealt":
                            match["red_total_time_CC_dealt"] += value
                        elif key == "visionScore":
                            match["red_vision_score"] += value
                        elif key == "win":
                            match["red_win"] = 1 if value == True else 0
                    match["red_champion"].append(player)
                    match["red_summoner_spell"].append(spell)
                else:
                    for key, value in participant.items():
                        if key[-5:] == "Pings":
                            match["blue_number_pings"] += value
                        elif key == "assists":
                            match["blue_assists"] += value
                        elif key == "baronKills":
                            match["blue_baron_kills"] = value
                        elif key == "champLevel":
                            player.append(value)
                        elif key == "championName":
                            player.append(value)
                        elif key[:4] == "item":
                            player.append(value)
                        elif key == "lane":
                            player.append(value)
                        elif key == "deaths":
                            match["blue_deaths"] += value
                        elif key == "detectorWardsPlaced" or key == "wardsPlaced":
                            match["blue_wards_placed"] += value
                        elif key == "wardsKilled":
                            match["blue_wards_killes"] += value
                        elif key == "goldEarned":
                            match["blue_gold_earned"] += value
                        elif key == "inhibitorsLost":
                            match["blue_inhibitor_lost"] = value
                        elif key[:9] == "summoner1" or key[:9] == "summoner2":
                            spell.append(value)
                        elif key == "totalMinionsKilled":
                            match["blue_total_minions_killed"] += value
                        elif key == "totalTimeCCDealt":
                            match["blue_total_time_CC_dealt"] += value
                        elif key == "visionScore":
                            match["blue_vision_score"] += value
                        elif key == "win":
                            match["blue_win"] = 1 if value == True else 0
                    match["blue_champion"].append(player)
                    match["blue_summoner_spell"].append(spell)

            for ban in response["info"]["teams"][0]["bans"]:
                match["red_bans"].append(ban["championId"])

            for ban in response["info"]["teams"][1]["bans"]:
                match["blue_bans"].append(ban["championId"])

            matches.append(match)

        df = pd.DataFrame(matches)
        df.to_csv('./data/matches/matches_' + str(j) + '.csv', index=False)
        return 1
        # return matches
        
    # def writeMatchesToCSV(self):
    #     matches = self.getMatchesById()
    #     if matches == 0:
    #         return 0
    #     else:
    #         df = pd.DataFrame(matches)
    #         df.to_csv('data.csv', index=False)

    def getMatchesTimeLineById(self, n):
        # # File path to save JSON data
        file_path = "matchesId.json"

        # Write list to JSON file
        with open(file_path, "r") as json_file:
            matchesId = json.load(json_file)

        matchesId = list(set(matchesId))
        machesWithTimeLine = []
        i = n
        skip = False
        lastErr = -1
        global iseN

        while i < len(matchesId):
            id = matchesId[i]
            i += 1
            self.controllLimit('getting matches with timeline by matches Id')
            url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + id + "/timeline?api_key=" + apiKey
            response = requests.get(url)
            response = response.json()

            while 'status' in response:
                if lastErr != i:
                    lastErr = i
                    iseN = 0
                if machesWithTimeLine != []:
                    df = pd.DataFrame(machesWithTimeLine)
                    df.to_csv('./data/timeline/matchesWithTimeLine_' + str(i) + '.csv', index=False)
                    machesWithTimeLine = []
                print(response['status'])
                print('error re-try times:', iseN)
                time.sleep(120 + 2 ** iseN * 60)
                iseN += 1
                skip = True
                i -= 1
                break
                
            if skip:
                skip = False
                continue
            
            match = dict()
            match['matchId'] = response['metadata']['matchId']
            match['frameInterval'] = response['info']['frameInterval']
            for j in range(len(response['info']['frames'])):
                frame = response['info']['frames'][j]
                events = frame['events']
                match[j] = events

            machesWithTimeLine.append(match)

        df = pd.DataFrame(machesWithTimeLine)
        df.to_csv('./data/timeline/matchesWithTimeLine_' + str(i) + '.csv', index=False)
        return 1


if __name__ == "__main__":
    lolApi = LOLAPI(name = "break", tagline = "12479")
    matchesId = list(lolApi.getMatchesIdByPuuid())
    # # File path to save JSON data
    file_path = "matchesId.json"

    # Write list to JSON file
    with open(file_path, "w") as json_file:
        json.dump(matchesId, json_file)


    # File path to the JSON data
    file_path = "matchesIdMore.json"

    # Read list from JSON file
    with open(file_path, "r") as json_file:
        data = json.load(json_file)



