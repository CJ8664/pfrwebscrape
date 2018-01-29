#!/usr/local/bin/python

import ssl

from urllib import request
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd

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

def getPlayByPlayData(game, save=True, matrix=False, dataframe=False):

    context = ssl._create_unverified_context()
    gameUrl = "http://www.pro-football-reference.com/boxscores/" + game + ".htm"

    if Path('../data/rawpage/'+ game + '.html').exists():
        print("Getting Play by Play data for game {0} from cache".format(game))
        with open('../data/rawpage/'+ game + '.html', 'r') as inputHandle:
            rawPageData = inputHandle.read()
    else:
        print("Getting Play by Play data for game {0} from web".format(game))
        rawPageData = request.urlopen(gameUrl, context=context).read().decode()
        with open('../data/rawpage/'+ game + '.html', 'w') as outputHandle:
            outputHandle.write(rawPageData)

    rawSoup = BeautifulSoup(rawPageData, 'lxml')
    outerDiveSoup = rawSoup.find(id='all_pbp')
    mainSoup = BeautifulSoup(str(outerDiveSoup).replace('<!--','').replace('-->',''), 'lxml')
    mainData = mainSoup.find_all('tr')

    matrixData = []

    with open('../data/pbp/' + game + '.txt', 'w') as fileHandle:
        headerAdded = False
        for tableRow in mainData:
            textdata = ''
            dataRow = tableRow.find_all('th') + tableRow.find_all('td')
            if len(dataRow) == 1 or (dataRow[0].get_text() == 'Quarter' and headerAdded):
                continue

            for dataElement in dataRow:
                textdata += dataElement.get_text() + '|'
            fileHandle.write(textdata[:-1] + '\n')

            if not headerAdded :
                headerAdded = True

            if matrix or dataframe:
                matrixData.append(textdata[:-1].split('|'))
    if matrix:
        return matrixData
    if dataframe:
        df = pd.DataFrame(matrixData)
        df.columns = df.iloc[0]
        df.drop(df.index[0], inplace=True)
        return df

def main():
    years =[str(x + 1994) for x in range(24)]
    for year in years:
        games = getGames(year)
        for game in games:
            print(getPlayByPlayData(game, dataframe=True))
            break
        break

if __name__ == "__main__":
    main()
