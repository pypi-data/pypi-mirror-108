from typing import Optional, Union
from lxml import html
import requests


def from_chessgames(game_id: Union[int, str]) -> Optional[str]:
    url = f"https://www.chessgames.com/perl/chessgame?gid={game_id}"
    xpath = """//*[@id="olga-data"]/@pgn"""

    try:
        r = requests.get(url)
        tree = html.fromstring(r.content)
        pgn = tree.xpath(xpath)[0]
    # TODO: Add specific exceptions and handle each of them
    except Exception:
        pgn = None

    return pgn


def from_lichess(game_id: Union[int, str]) -> Optional[str]:
    url = f"https://lichess.org/game/export/{game_id}"

    try:
        r = requests.get(url)
        pgn = r.text
    # TODO: Add specific exceptions and handle each of them
    except Exception:
        pgn = None

    return pgn


def from_chesscom(game_id: Union[int, str]) -> Optional[str]:
    url = f"https://www.chess.com/game/live/{game_id}"
    download_button_xpath = "/html/body/div[3]/div/div[2]/div[1]/div[4]/div/div/div[1]/a[2]/span"


if __name__ == "__main__":
    p = from_chesscom(16053333689)
    print(p)
