import json
import urllib.request

# Data mining from the FPL API 
teamID = 4538734
lastGameweek = 1

# Detailed info about a given FPL Manager’s Team and a given game week
gameweekData = {}
for i in range(1, lastGameweek + 1):
    base = "https://fantasy.premierleague.com/api/entry/" + str(teamID) + "/event/" + str(i) + "/picks/"
    page = urllib.request.urlopen(base)
    data = {"GW" + str(i) : json.load(page)}
    gameweekData.update(data)

# General info about a given FPL Manager’s Team
base = "https://fantasy.premierleague.com/api/entry/" + str(teamID) + "/"
page = urllib.request.urlopen(base)
dataTeamInfo = json.load(page)

# Generic info about PL teams, the players and the game week details
base = "https://fantasy.premierleague.com/api/bootstrap-static/" 
page = urllib.request.urlopen(base)
dataGeneral = json.load(page)
events = dataGeneral["events"]
elements = dataGeneral["elements"]

# Detailed info about a specific premier league player   
def getPlayerPointsAtOneGW(playerID, gameweek):
    base = "https://fantasy.premierleague.com/api/element-summary/" + str(playerID) + "/"
    page = urllib.request.urlopen(base)
    datagw = json.load(page)
    gwPoints = 0
    for i in range(len(datagw["history"])): 
        if gameweek == datagw["history"][i]["round"]: # to account for absent gameweek in the json
            gwPoints = gwPoints + datagw["history"][i]["total_points"] # to account for double gw            
    return gwPoints

def getPlayerName(playerID):
    i = 0
    while i < len(elements):
        if (elements[i]["id"] == playerID):
            return (elements[i]["first_name"] + " " + elements[i]["second_name"])
        i += 1
    return "ID not found"

positions = ["GK", "DEF", "MID", "ST"]
def getPlayerPosition(playerID):
    i = 0
    while i < len(elements):
        if (elements[i]["id"] == playerID):
                playersElementType = elements[i]["element_type"]
                playerPosition = positions[playersElementType - 1]
                return playerPosition
        i += 1
    return "ID not found"


# Calculations 
# Get the specific team data from the json in organised lists and dictionaries
teamName = dataTeamInfo["name"]
points = []
gameweekRank = []
overallRank = []
teamValue = []
transfers = []
transfersCost = []
averagePoints = []
highestPoints = []
captain = []
captainPoints = []
startingTeam = {}
totalPointsPerLine = {}
totalPointsPerLineSeason = {"GK" : 0, "DEF" : 0, "MID" : 0, "ST" : 0}

for gw in range(1, lastGameweek + 1):
    # List with basic data each gw

    points.append(gameweekData["GW" + str(gw)]["entry_history"]["points"])
    gameweekRank.append(gameweekData["GW" + str(gw)]["entry_history"]["rank"])
    overallRank.append(gameweekData["GW" + str(gw)]["entry_history"]["overall_rank"])
    teamValue.append(gameweekData["GW" + str(gw)]["entry_history"]["value"])
    transfers.append(gameweekData["GW" + str(gw)]["entry_history"]["event_transfers"])
    transfersCost.append(gameweekData["GW" + str(gw)]["entry_history"]["event_transfers_cost"])
    averagePoints.append(events[gw-1]["average_entry_score"])
    highestPoints.append(events[gw-1]["highest_score"])
    
    # Dict with starting team each gw
    startingTeam["GW" + str(gw)] = {}
    for j in range(0, 15):
        if gameweekData["GW" + str(gw)]["picks"][j]["is_captain"] == True:
            captain.append(getPlayerName(gameweekData["GW" + str(gw)]["picks"][j]["element"]))
            captainPoints.append(getPlayerPointsAtOneGW(gameweekData["GW" + str(gw)]["picks"][j]["element"], gw))
    for n in range(0, 15):
        startingTeam["GW" + str(gw)]["player" + str(n)] = {}
        startingTeam["GW" + str(gw)]["player" + str(n)]["name"] = getPlayerName(gameweekData["GW" + str(gw)]["picks"][n]["element"])
        startingTeam["GW" + str(gw)]["player" + str(n)]["position"] = getPlayerPosition(gameweekData["GW" + str(gw)]["picks"][n]["element"])
        startingTeam["GW" + str(gw)]["player" + str(n)]["points"] = getPlayerPointsAtOneGW(gameweekData["GW" + str(gw)]["picks"][n]["element"], gw)

    # Dict with points per line each gw
    totalPointsPerLine["GW" + str(gw)] = {"GK" : 0, "DEF" : 0, "MID" : 0, "ST" : 0}
    for player in range(0, 11): # que les titulaires de 0 à 11 donc
        if startingTeam["GW" + str(gw)]["player" + str(player)]["position"] == "GK":
            totalPointsPerLine["GW" + str(gw)]["GK"] = totalPointsPerLine["GW" + str(gw)]["GK"] + startingTeam["GW" + str(gw)]["player" + str(player)]["points"]
        elif startingTeam["GW" + str(gw)]["player" + str(player)]["position"] == "DEF":
            totalPointsPerLine["GW" + str(gw)]["DEF"] = totalPointsPerLine["GW" + str(gw)]["DEF"] + startingTeam["GW" + str(gw)]["player" + str(player)]["points"]
        elif startingTeam["GW" + str(gw)]["player" + str(player)]["position"] == "MID":
            totalPointsPerLine["GW" + str(gw)]["MID"] = totalPointsPerLine["GW" + str(gw)]["MID"] + startingTeam["GW" + str(gw)]["player" + str(player)]["points"]
        elif startingTeam["GW" + str(gw)]["player" + str(player)]["position"] == "ST":
            totalPointsPerLine["GW" + str(gw)]["ST"] = totalPointsPerLine["GW" + str(gw)]["ST"] + startingTeam["GW" + str(gw)]["player" + str(player)]["points"]
    # Dict with points per line for the entire season       
    totalPointsPerLineSeason["GK"] = totalPointsPerLineSeason["GK"] + totalPointsPerLine["GW" + str(gw)]["GK"]
    totalPointsPerLineSeason["DEF"] = totalPointsPerLineSeason["DEF"] + totalPointsPerLine["GW" + str(gw)]["DEF"]
    totalPointsPerLineSeason["MID"] = totalPointsPerLineSeason["MID"] + totalPointsPerLine["GW" + str(gw)]["MID"]
    totalPointsPerLineSeason["ST"] = totalPointsPerLineSeason["ST"] + totalPointsPerLine["GW" + str(gw)]["ST"]
    
    print("GW" + str(gw) + " : Done.")
    
