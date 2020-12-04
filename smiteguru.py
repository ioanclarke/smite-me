import os
import requests
from bs4 import BeautifulSoup as bs

def search():
    
    playerName = input('Search for player:')
    print('')
    
    url = f'https://smite.guru/search?term={playerName}&type=Player'
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')
    results = soup.find('div', class_='columns')
    players = results.findAll(class_='column col-3')  
    if players==None:
        print('No results\n')
        search()
    player = players[0]
    
    if len(players)>1:
        count=1
        for player in players:
            rawName = player.find('a', class_='player-widget__a')
            rawClan = player.find('h3', class_='player-widget__h3')
            rawLastSeen = player.find('div', class_='value')
            rawPlaytime = player.findAll(class_='value')
            if None in (rawName, rawClan, rawLastSeen, rawPlaytime):
                continue
            
            name = rawName.text.strip()
            clan = rawClan.text.strip()
            lastSeen = rawLastSeen.text.strip()
            playtime = rawPlaytime[1].text.strip()
            
            print(f'[{count}]')
            print(f'Name:      {name}')
            print(f'Clan:      {clan}')
            print(f'Last seen: {lastSeen}')
            print(f'Playtime:  {playtime}')
            print('')
            count = count+1
        resultsNum = count-1
        print(f'{resultsNum} results found.\n')
        selection = input('Which player?\n')
        print('')
        player = players[int(selection)-1]


    link = player.find('a')['href']
    url = f'https://smite.guru{link}'
    print(f'URL: {url}\n')
    page = requests.get(url)
    soup=bs(page.content, 'html.parser')
    player = soup.find(id='cw')

    rawName = player.find('div', class_='profile-header__name')
    rawLevel = player.find('div', class_='profile-header__level')
    rawPlaytime = player.find('div', class_='ptw__val')
    rawWinLoss = player.findAll(class_='ptw__val')
    rawKDA = player.findAll(class_='tsw__grid')
    rawMatchesPlayed = player.find('div', class_='tsw__grid')
    if None not in (rawName, rawLevel, rawPlaytime, rawWinLoss, rawKDA, rawMatchesPlayed):
            name = rawName.text.strip()
            level = rawLevel.text.strip()
            playtime = rawPlaytime.text.strip()
            winLoss = rawWinLoss[1].text.strip()
            KDA = rawKDA[1].find('div', class_='tsw__grid__stat').text.strip()
            matchesPlayed = rawMatchesPlayed.find('div', class_='tsw__grid__stat').text.strip()


            print(f'Name:           {name}')
            print(f'Level:          {level}')
            print(f'Playtime:       {playtime}')
            print(f'Win/Loss:       {winLoss}')
            print(f'KDA:            {KDA}')
            print(f'Matches Played: {matchesPlayed}\n')
    else:
        print('Error')
    inp = input('Search again? (y/n)\n')
    if inp == 'y':
        search()
        
search()
            
            

    
    
