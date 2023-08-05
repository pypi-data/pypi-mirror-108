import requests,re
from datetime import datetime

website = "https://www.fotmob.com/"

class Match(object):
    matchID = 0
    homeTeam = ""
    awayTeam = ""
    date = ""
    ko_time = ""

    def __init__(self,matchID,homeTeam,awayTeam,date,ko_time):
        self.matchID = matchID
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.date = date 
        self.ko_time = ko_time

def getLeague(comp: int, page: str="overview", league: str="leagues", timezone: str="America/New_York") -> list:
    """
    Return the overview page for a league or cup competition

    :param comp:
    :param page:
    :param timezone:
    :return: A list of all the matches in the competition
    """
    url = website+league+"/"+str(comp)+"/"+page
    matches_html = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=15).text
    matches_html = re.split(r'window\.__PRELOADED_STATE__(.*)',matches_html)[1]
    matches_html = re.split(r'"matchesTab".*?(\[.*\]"fetching")',matches_html)[0]
    matches_table = re.split(r'"round"',matches_html)[1:]
    matches = []
    for match in matches_table:
        matchID = re.findall(r'"id":"(\d+)"',match)[0]
        homeTeam,awayTeam = re.findall('"name":"(.*?)"',match)
        if 'startTimeStr' in match:
            ko_time = re.findall('"startTimeStr":"(.*?)"',match)[0]
        else:
            ko_time = ""
        date = datetime.strptime(re.findall('"startDateStr":"(.*?)"',match)[0],"%b %d, %Y")
        match = Match(matchID,homeTeam,awayTeam,date,ko_time)
        matches.append(match)
    return matches

def printMatch(m):
    output = m.matchID +" " + m.date.strftime('%b %d, %Y') + " "
    if m.ko_time:
        output += m.ko_time + " "
    output += m.homeTeam + " v " + m.awayTeam
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
    url = website+"livescores/"+matchID
    match_html = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=15).text
    match = re.split(r'window\.__PRELOADED_STATE__(.*)',match_html)[1]
    match= re.split('"matchFacts"(.*)"Tournament"',match)[1]
    matchID = matchID
    homeTeam,awayTeam = re.findall('"name":"(.*?)"',match)[:2]
    if 'startTimeStr' in match:
        ko_time = re.findall('"startTimeStr":"(.*?)"',match)[0]
    else:
        ko_time = ""
    date = datetime.strptime(re.findall('"startDateStr":"(.*?)"',match)[0],"%b %d, %Y")
    match = Match(matchID,homeTeam,awayTeam,date,ko_time)
    return match

def getMatchesByDate(date: str) -> dict:
    """
    Return all the matches being played on a specific date
    
    :param date: A date string in format YYYYMMDD
    return matches: A list of match objects
    """
    url = website+"?date="+date
    match_html = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'},timeout=15).text
    match_html = re.split(r'window\.__PRELOADED_STATE__(.*)',match_html)[1]
    leagues_html = match_html.rpartition('"tv":null}')[0]
    leagues_html = re.split(r'"ccode"',leagues_html)[1:-1]
    leagues = {}
    for league in leagues_html: 
        leagueName,leagueID = re.split(r'"(\w+)","id":(\d+)',league)[1:-1]
        #matches_table = re.split(r'"primaryId"',league)[1:]
        matches_table = re.split(r'"tv":.*?}',league)[:-1]
        matches = []
        for match in matches_table:
            matchID = re.findall(r'{"id":(\d+)',match)[0]
            homeTeam,awayTeam = re.findall('"longName":"(.*?)"',match)
            if 'startTimeStr' in match:
                ko_time = re.findall('"startTimeStr":"(.*?)"',match)[0]
            else:
                ko_time = ""
            date = datetime.strptime(re.findall('"startDateStr":"(.*?)"',match)[0],"%b %d, %Y")
            match = Match(matchID,homeTeam,awayTeam,date,ko_time)
            matches.append(match)
        leagues[leagueName] = matches
    return leagues 


if __name__ == '__main__':
    #getLeague(50,"matches")
    printMatch(getMatch("3585290"))
    #leagues = getMatchesByDate("20210602")
    #printAllMatches(leagues)
