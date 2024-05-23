import json
from datetime import datetime, timezone, timedelta

import requests

from ba_config import calendar
from config import api_sports_key


class BasketballAPI:
    url = 'https://v1.basketball.api-sports.io'
    payload = {}
    headers = {
        'x-rapidapi-host': "v1.basketball.api-sports.io",
        'x-rapidapi-key': api_sports_key
    }

    @classmethod
    def get_nba_match_dates(cls, date: str):
        tz = 'America/Los_Angeles'
        url = f'{cls.url}/games?league=12&season=2023-2024&date={date}&timezone={tz}'
        response = requests.get(url=url, headers=cls.headers, data=cls.payload)
        matches = json.loads(response.text).get('response')

        daily_match_data = []
        last_date = datetime.fromtimestamp(1650000000, timezone.utc)
        i = 0
        for match in matches:
            date = datetime.strptime(match.get('date'), '%Y-%m-%dT%H:%M:%S%z')
            if date == last_date:
                i += 1
                date += timedelta(minutes=i)
            else:
                last_date = date
                i = 0
            teams = match.get('teams')
            home_team_name = teams.get('home').get('name')
            away_team_name = teams.get('away').get('name')
            daily_match_data.append({
                'year': str(date.astimezone().year),
                'month': calendar[date.astimezone().month],
                'day': str(date.astimezone().day),
                'hour': str(date.astimezone().hour).zfill(2),
                'minute': str(date.astimezone().minute).zfill(2),
                'name': f'{home_team_name} - {away_team_name}'
            })
        return daily_match_data

    @staticmethod
    def write_data(daily_match_data):
        with open('bets_data/nba_match_dates.json', 'w', encoding='utf8') as f:
            json.dump(daily_match_data, f, indent=4, ensure_ascii=False)
