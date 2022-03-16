from curses import color_pair
from enum import Enum
import re
import requests
from bs4 import BeautifulSoup as bs


class Color:
    ERROR_RED = "\033[31m"
    BLUE = "\033[36m"
    RESET = "\033[0m"


def get_search_query():
    SEARCH_URL = "https://smite.guru/search?term={playerName}&type=Player"
    playerName = input("Search for player: ")
    return SEARCH_URL.format(playerName=playerName)


def get_search_results(url):
    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    results = soup.find("div", class_="columns")
    return results.findAll(class_="column col-3")


def get_player(players):
    if not players:
        raise SystemExit("\nNo players found with this name. Quitting")

    if len(players) == 1:
        return players[0]

    for i, player in enumerate(players, 1):
        find = player.find
        name = extract(find("a", class_="player-widget__a"))
        clan = extract(find("h3", class_="player-widget__h3"))
        last_seen = extract(find("div", class_="value"))
        play_time = extract(player.findAll(class_="value")[1])

        pairs = [
            ("Name", name),
            ("Clan", clan),
            ("Last seen", last_seen),
            ("Playtime", play_time),
        ]

        print(f"[{i}]")
        for pair in pairs:
            print_row(*pair)

    print(f"{len(players)} results found.\n")
    selection = int(input("Which player do you want to see stats for?\n"))
    return players[selection - 1]


def get_player_stats(player):
    profile_link = player.find("a")["href"]
    url = f"https://smite.guru{profile_link}"
    print(f"Scrapping stats from {url}\n")

    page = requests.get(url)
    soup = bs(page.content, "html.parser")

    player = soup.find(id="cw")

    find = player.find
    name = extract(find("div", class_="profile-header__name"))
    level = extract(find("div", class_="profile-header__level"))
    play_time = extract(find("div", class_="ptw__val"))
    win_loss = extract(player.findAll(class_="ptw__val")[1])
    kda = extract(
        player.findAll(class_="tsw__grid")[1].find("div", class_="tsw__grid__stat")
    )
    matches_played = extract(
        find("div", class_="tsw__grid").find("div", class_="tsw__grid__stat")
    )

    print(f"Name:           {name}")
    print(f"Level:          {level}")
    print(f"Playtime:       {play_time}")
    print(f"Win/Loss:       {win_loss}")
    print(f"KDA:            {kda}")
    print(f"Matches Played: {matches_played}\n")


def extract(tag):
    try:
        return tag.text.strip()
    except:
        return Color.ERROR_RED + "error" + Color.RESET


def print_row(header, value):
    print(
        "{color}{header:<15}{color_reset}{value}".format(
            color=Color.BLUE, header=header, color_reset=Color.RESET, value=value
        )
    )


if __name__ == "__main__":
    query = get_search_query()
    players = get_search_results(query)
    player = get_player(players)
    stats = get_player_stats(player)
