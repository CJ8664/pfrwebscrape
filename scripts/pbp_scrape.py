#!/usr/local/bin/python

import ssl

from urllib import request
from bs4 import BeautifulSoup

def savePlayByPlayData(game):

    context = ssl._create_unverified_context()
    gameUrl = "http://www.pro-football-reference.com/boxscores/" + game + ".htm"
    rawPageData = request.urlopen(gameUrl, context=context).read().decode()

    rawSoup = BeautifulSoup(rawPageData, 'lxml')
    outerDiveSoup = rawSoup.find(id='all_pbp')
    mainSoup = BeautifulSoup(str(outerDiveSoup).replace('<!--','').replace('-->',''), 'lxml')
    mainData = mainSoup.find_all('tr')

    with open('data/pbp/' + game + '.csv', 'w') as outputHandle:
        for tableRow in mainData:
            textdata = ''
            dataRow = tableRow.find_all('td')
            if len(dataRow) == 0:
                dataRow = tableRow.find_all('th')
            for dataElement in dataRow:
                textdata += dataElement.get_text() + '|'
            outputHandle.write(textdata[:-1] + '\n')

def main():
    games = ["201709170nor"]

    for game in games:
        savePlayByPlayData(game)

if __name__ == "__main__":
    main()
