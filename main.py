from bs4 import BeautifulSoup
from pandas.core.construction import com
import requests
import pandas as pd
URL = 'https://soccer365.ru/competitions/13/'

r = requests.get(URL)

soap = BeautifulSoup(r.text, "html.parser")  # html.parser lxml


def parseTable(tableName, className):
    table2 = soap.find_all('table', attrs={'class': className})
    for table in table2:
        th_tags = table.find_all('th')
        if any(tableName in th.get_text() for th in th_tags):
            return table


def parseContentTable(table):

    mainData = []
    colTeamNameData = []

    tableBody = table.find('tbody')
    rows = tableBody.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        colTeamName = row.find_all('img')
        colTeamNameData.append([(ele.get('title'), ele['src'])
                                for ele in colTeamName if ele.get('title')])
        cols = [(ele.text.strip()) for ele in cols]
        mainData.append([ele for ele in cols])

    return [l2 + l1 for l2, l1 in zip(colTeamNameData, mainData)]


mainTable = parseTable('', 'stngs')
assistantTable = parseTable('Ассистенты', 'comp_table_v2')
golersTable = parseTable('Бомбардиры', 'comp_table_v2')
penaltiesTable = parseTable('Штрафники', 'comp_table_v2')
assistantTableData = parseContentTable(assistantTable)
golersTableData = parseContentTable(golersTable)
penaltiesTableData = parseContentTable(penaltiesTable)
mainTableData = parseContentTable(mainTable)
print(mainTable)
print(golersTableData)
dfAssistant = pd.DataFrame(
    assistantTableData, columns=['Team', 'player_name', 'assisnts', 'matches'])
dfGolers = pd.DataFrame(
    golersTableData, columns=['Team', 'player_name', 'regular_goals', 'penalties_goals', 'matches'])
dfPenalties = pd.DataFrame(
    penaltiesTableData, columns=['Team', 'player_name', 'fair_play', 'yellow_card', 'yellow_to_red_card', 'red_card', 'matches'])
dfMain = pd.DataFrame(
    mainTableData, columns=['place', 'team_name', 'games', 'wins', 'draws', 'loss', 'goals', 'enemy_goals', 'difference_goals', 'points'])
dfMain = dfMain.set_index('place')

combinedDf = pd.concat(
    [dfAssistant, dfGolers, dfPenalties], ignore_index=True)
combinedDfClean = combinedDf.groupby(['Team', 'player_name', 'matches']).agg(
    {'assisnts': lambda x: ''.join(x.dropna()),
     'regular_goals': lambda x: ''.join(x.dropna()),
     'penalties_goals': lambda x: ''.join(x.dropna()),
     'fair_play': lambda x: ''.join(x.dropna()),
     'yellow_card': lambda x: ''.join(x.dropna()),
     'yellow_to_red_card': lambda x: ''.join(x.dropna()),
     'red_card': lambda x: ''.join(x.dropna()),
     }).reset_index()
dfPenalties = pd.DataFrame(
    penaltiesTableData, columns=['Team', 'player_name', 'fair_play', 'yellow_card', 'yellow_to_red_card', 'red_card', 'matches'])


combinedDfClean.regular_goals = pd.to_numeric(
    combinedDfClean.regular_goals, errors='coerce')
combinedDfClean.penalties_goals = pd.to_numeric(
    combinedDfClean.penalties_goals, errors='coerce')
combinedDfClean.assisnts = pd.to_numeric(
    combinedDfClean.assisnts, errors='coerce')
combinedDfClean.matches = pd.to_numeric(
    combinedDfClean.matches, errors='coerce')
combinedDfClean.fair_play = pd.to_numeric(
    combinedDfClean.fair_play, errors='coerce')
combinedDfClean.yellow_card = pd.to_numeric(
    combinedDfClean.yellow_card, errors='coerce')
combinedDfClean.yellow_to_red_card = pd.to_numeric(
    combinedDfClean.yellow_to_red_card, errors='coerce')
combinedDfClean.red_card = pd.to_numeric(
    combinedDfClean.red_card, errors='coerce')

combinedDfCleanFilled = combinedDfClean.fillna(0)
combinedDfCleanFilled['combined_goals'] = combinedDfCleanFilled['penalties_goals'].add(
    combinedDfCleanFilled['regular_goals'], fill_value=0)

print(combinedDfClean)

countTeamGoals = combinedDfCleanFilled.groupby(
    ['Team'])['combined_goals'].sum()
print(countTeamGoals.sort_values(ascending=False).head(3))

combinedDfCleanFilled['combined_yellow_card'] = combinedDfCleanFilled['yellow_card'].add(
    combinedDfCleanFilled['yellow_to_red_card'], fill_value=0)

countYellowCard = combinedDfCleanFilled.groupby(
    ['Team'])['combined_yellow_card'].sum().sort_values(ascending=False).head(3)

print(countYellowCard)

maxMatches = combinedDfCleanFilled.groupby(['Team'])[
    'matches'].max()
combinedDfCleanFilled = combinedDfCleanFilled.merge(
    maxMatches, on='Team', how='left')

playersThatMissed = combinedDfCleanFilled[combinedDfCleanFilled['matches_x']
                                          < combinedDfCleanFilled['matches_y']]

print(playersThatMissed)

countPenalties = combinedDfCleanFilled.groupby(
    ['Team'])['penalties_goals'].sum()
print(countPenalties)
dfTeamGoals = countTeamGoals.reset_index().rename(
    columns={'index': 'Team', 0: 'Value1'})
print(dfTeamGoals)
dfPenalties = countPenalties.reset_index().rename(
    columns={'index': 'Team', 0: 'Value2'})
print(dfPenalties)

dfTeamGoals['proportion'] = (
    dfPenalties['penalties_goals'] / dfTeamGoals['combined_goals']).dropna()
print(dfTeamGoals)

print(dfMain)
dfTeamGoalsCorr = dfMain['goals']
dfTeamPointsCorr = dfMain['points']
corr = dfTeamPointsCorr.corr(dfTeamGoalsCorr)
print(corr)
combinedDfCleanFilled.to_csv('D:\\programming\\python\\laba8\\out.csv')

