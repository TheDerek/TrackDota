from bs4 import BeautifulSoup
import requests
import re
import operator


def find_between(s, first, last):
    return re.search(first + r'(.*)' + last, s, re.DOTALL | re.MULTILINE).group(1)



def get_teams(teams=[]):
    page = 0;

    while True:
        page += 1
        soup = BeautifulSoup(requests.get("http://www.gosugamers.net/dota2/rankings?page=" + str(page)).text)


        for index, data in enumerate(soup.find_all(class_="main no-game")):
            html = str(data)

            country = re.findall(r'\"(.+?)\"', html)[2]
            team = find_between(html, '<span>', "</span></span>")
            rank = index + ((page -1) * 50)
            show_rank = str(rank + 1)
            teams.insert(rank, {"rank": show_rank, "irank": (rank + 1), "country": country, "name": team})

            #Somehow this stops the loop if it reaches the end - no idea why
            try:
                if teams[rank] is None:
                    pass
            except IndexError:
                teams.pop(len(teams) - 1)
                teams.reverse()
                return teams

def get_games(teams, games=[]):
    # Need to complete team names which end in ...
    # teams is an optional parameter as there is no need to load the teams twice
    page = 0
    nows = 0

    while True:
        page += 1
        soup = BeautifulSoup(requests.get("http://www.gosugamers.net/dota2/gosubet?u-page=" + str(page)).text)
        for index, data in enumerate(soup.find_all(class_="match hover-background")):
            html = str(data)

            #Finding the time the match starts at
            time_html = data.parent.parent.find(class_="live-in")

            if time_html is None:
                if data.parent.parent.find(class_="score-wrap") is None:
                    if page is 1:
                        time = "Now"
                    else:
                        continue
                else:
                    continue
            else:
                time = str(time_html.text).rstrip().replace('\n', '')

            #Finds the first team and auto completes if name ends with ...
            team1 = find_between(html, "<span>", "</span><span class=")
            if team1.endswith("..."):
                for team in teams:
                    if team["name"].startswith(team1.strip("...")):
                        team1 = team["name"]
                        break

            #Finds the second team and auto completes if name ends with ...
            team2 = find_between(html, "></span><span>", "</span> </span>")
            if team2.endswith("..."):
                for team in teams:
                    if team["name"].startswith(team2.strip("...")):
                        team2 = team["name"]
                        break

            #time_test = find_between(time_html, '<td class="type-specific">\n<span>', '</span>')

            rank = index + ((page - 1) * 15)

            games.insert(rank, {"position": rank, "team1": team1, "team2": team2, "time": time})


            #Somehow this stops the loop if it reaches the end - no idea why
            try:
                if games[rank] is None:
                    pass
            except IndexError:
                games.pop(len(games) - 1)
                games.reverse()
                return games


def get_team(name, teams):
    for team in teams:
        if team["name"] == name:
            return team

def get_next_match(team_name, teams, games):
    games.sort(key=operator.itemgetter('position'))
    for game in games:
        if (game["team1"] == team_name) | (game["team2"] == team_name):
            games.reverse()
            return game









