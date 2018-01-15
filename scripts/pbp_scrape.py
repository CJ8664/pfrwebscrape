#!/usr/local/bin/python

import ssl

from urllib import request
from bs4 import BeautifulSoup

def getGames(year):

    context = ssl._create_unverified_context()
    gameUrl = "https://www.pro-football-reference.com/years/" + year
    rawPageData = request.urlopen(gameUrl, context=context).read().decode()

    rawSoup = BeautifulSoup(rawPageData, 'lxml')
    outerDiveSoup = rawSoup.find(id='all_playoff_results')
    mainSoup = BeautifulSoup(str(outerDiveSoup).replace('<!--','').replace('-->',''), 'lxml')
    mainData = mainSoup.find_all('tr')

    games = []
    for tableRow in mainData:
        textdata = ''
        dataRow = tableRow.find_all('td')
        for dataElement in dataRow:
            if dataElement.get_text() == "boxscore":
                games += (dataElement.find("a").get('href').split('/')[2]).split('.')[0],

    return games

def savePlayByPlayData(game):

    print("Getting Play by Play data for game {0}".format(game))
    context = ssl._create_unverified_context()
    gameUrl = "http://www.pro-football-reference.com/boxscores/" + game + ".htm"
    rawPageData = request.urlopen(gameUrl, context=context).read().decode()

    rawSoup = BeautifulSoup(rawPageData, 'lxml')
    outerDiveSoup = rawSoup.find(id='all_pbp')
    mainSoup = BeautifulSoup(str(outerDiveSoup).replace('<!--','').replace('-->',''), 'lxml')
    mainData = mainSoup.find_all('tr')

    with open('../data/pbp/' + game + '.txt', 'w') as outputHandle:
        for tableRow in mainData:
            textdata = ''
            dataRow = tableRow.find_all('th') + tableRow.find_all('td')
            for dataElement in dataRow:
                textdata += dataElement.get_text() + '|'
            outputHandle.write(textdata[:-1] + '\n')

def main():
    years =[str(x + 2000) for x in range(18)]
    for year in years:
        games = getGames(year)
        for game in games:
            savePlayByPlayData(game)

if __name__ == "__main__":
    main()
