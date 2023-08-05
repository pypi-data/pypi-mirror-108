import requests,re,json
from datetime import datetime

website = "https://www.fotmob.com/"

class Match(object):
    matchID = 0
    homeTeam = ""
    awayTeam = ""
    date = ""
    ko_time = ""
    result = ""

    def __init__(self,matchID,homeTeam,awayTeam,date,ko_time,result):
        self.matchID = matchID
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.date = date 
        self.ko_time = ko_time
        self.result = result

    def getMatchID(self):
        return self.matchID

    def getDate(self):
        return self.date.strftime('%b %d, %Y')

    def getKickOff(self):
        return self.ko_time

    def getHomeTeam(self):
        return self.homeTeam

    def getAwayTeam(self):
        return self.awayTeam

    def getResult(self):
        return self.result

def getLeague(comp: int, page: str="overview", league: str="league", timezone: str="America/New_York", matchDate: str=None) -> list:
    """
    Return the overview page for a league or cup competition

    :param comp:
    :param page:
    :param timezone:
    :return: A list of all the matches in the competition
    """
    url = website+"leagues?id="+str(comp)+"&tab="+page+"&type="+league+"&timeZone="+timezone
    matches_html = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=15).text
    fixtures = json.loads(matches_html)['fixtures']
    matches = []
    #for match in matches_table:
    for match in fixtures:
        matchID = match['id']
        homeTeam,awayTeam = match['home']['name'],match['away']['name']
        if match['notStarted']:
            ko_time = match['status']['startTimeStr']
            result = ""
        else:
            result = match['status']['scoreStr']
            ko_time = ""
        try:
            date = datetime.strptime(match['status']['startDateStr'],"%d %B %Y")
        except ValueError:
            date = datetime.strptime(match['status']['startDateStrShort'],"%d. %b.")
            date = date.replace(year=int(datetime.today().strftime('%Y')))
        if matchDate is not None:
            if date.strftime('%Y%m%d') < matchDate:
                continue
            elif date.strftime('%Y%m%d') > matchDate:
                return matches
        match = Match(matchID,homeTeam,awayTeam,date,ko_time,result)
        matches.append(match)
    return matches

def printMatch(m):
    output = m.matchID +" " + m.date.strftime('%b %d, %Y') + " "
    if m.ko_time:
        output += m.ko_time + " "
    output += m.homeTeam
    if m.result:
        output += " " + m.result + " "
    else:
        output += " v "
    output += m.awayTeam
    return output

def printAllMatches(day):
    for key,matches in day.items():
        print(key)
        for match in matches:
            print(printMatch(match))


def getMatch(matchID: str) -> Match:
    """
    Return the info for a specific match

    :param matchID: Fotmob Match ID
    return Match: a Match object with relevant info
    """
    url = website+"matchDetails?matchId="+matchID
    match_html = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=15).text
    match = json.loads(match_html)['header']
    matchID = matchID
    homeTeam,awayTeam = match['teams'][0]['name'],match['teams'][1]['name']
    if not match['status']['started']:
        ko_time = match['status']['startTimeStr']
        result = ""
    else:
        result = match['status']['scoreStr']
        ko_time = ""
    date = datetime.strptime(match['status']['startDateStr'],'%b %d, %Y')
    match = Match(matchID,homeTeam,awayTeam,date,ko_time,result)
    return match

def getMatchesByDate(date: str) -> dict:
    """
    Return all the matches being played on a specific date
    
    :param date: A date string in format YYYYMMDD
    return matches: A list of match objects
    """
    url = website+"matches?date="+date
    match_html = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=15).text
    matches_json = json.loads(match_html)
    fixtures = matches_json['leagues']
    leagues = {}
    for league in fixtures: 
        leagueName,leagueID = league['ccode'],league['id']
        #matches_table = re.split(r'"primaryId"',league)[1:]
        matches_table = league['matches']
        matches = []
        for match in matches_table:
            matchID = match['id']
            homeTeam,awayTeam = match['home']['name'],match['away']['name']
            if not match['status']['started']:
                ko_time = match['status']['startTimeStr']
                result = ""
            else:
                result = match['status']['scoreStr']
                ko_time = ""
            date = datetime.today().strftime("%b %d, %Y")
            match = Match(matchID,homeTeam,awayTeam,date,ko_time,result)
            matches.append(match)
        leagues[leagueName] = matches
    return leagues 


if __name__ == '__main__':
    #matches = getLeague(42,"overview","league","America/New_York","20210317")
    matches = getLeague(50,"overview","league","UTC","20210612")
    #printMatch()
    #leagues = getMatchesByDate("20210602")
    #info = getMatch('3585290')
    #printAllMatches(leagues)
    #date = datetime.today().strftime('%Y%m%d')
    #leagues = getMatchesByDate(date)
    print("done")
