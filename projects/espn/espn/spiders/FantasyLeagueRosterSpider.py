import re
import scrapy


class FantasyLeagueRosterSpider(scrapy.Spider):
    name = 'FantasyLeagueRosterSpider'
    allowed_domains = ['fantasy.espn.com']
    start_urls = [
        'https://fantasy.espn.com/apis/v3/games/flb/seasons/2022/segments/0/leagues/853208662?view=mSettings&view=mRoster&view=mTeam&view=modular&view=mNav',
        'https://fantasy.espn.com/apis/v3/games/wfba/seasons/2022/segments/0/leagues/1036982622?view=mSettings&view=mRoster&view=mTeam&view=modular&view=mNav',
    ]

    def parse(self, response):
        league_type = re.findall(r'\/games\/(\w+)\/seasons\/', response.url)[0]
        json_obj = response.json()

        teams = []
        for team in json_obj['teams']:
            location = team['location']
            nickname = team['nickname']
            team_name = f'{location} {nickname}'

            roster = []
            for individual in team['roster']['entries']:
                player = individual['playerPoolEntry']['player']
                roster.append({
                    'id': player['id'],
                    'first_name': player['firstName'],
                    'last_name': player['lastName'],
                    'full_name': player['fullName'],
                    'slots': player['eligibleSlots'],
                    'pro_id': player['proTeamId'],
                })

                ## slots = player['eligibleSlots']
                ## if any(filter(lambda x: x >= 13 and x <= 15, slots)):
                ##     response['is_a'].append('PITCHER')
                ##
                ## if any(filter(lambda x: x < 13, slots)):
                ##     response['is_a'].append('BATTER')

            teams.append({
                'name': team_name,
                'roster': roster,
            })

        yield {
            'league_id': json_obj['id'],
            'league_type': league_type,
            'teams': teams,
        }
