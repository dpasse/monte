scrap-pfr-2019:
	python3 scripts/nfl/scrap-pfr-schedule.py 2019

scrap-pfr-2020:
	python3 scripts/nfl/scrap-pfr-schedule.py 2020

scrap-pfr-2021:
	python3 scripts/nfl/scrap-pfr-schedule.py 2021

historical_ncaa_tourny_win_perc:
	python3 scripts/ncaa/historical-tourny-win-perc.py

scrap_league_rosters:
	python3 scripts/mlb/scrap-league-rosters.py 2022 853208662

scrap_game_stats:
	python3 scripts/mlb/scrap-game-stats.py 853208662 "Snoring Eeyores" "eeyores-853208662"

scrap_job_descriptions:
	python3 scripts/disney/get_job_descriptions.py

scrap_imagineering_job_descriptions:
	python3 scripts/disney/get_job_descriptions.py "imagineering"

merge_imagineering_datasets:
	python3 scripts/disney/merge_datasets.py "imagineering"

run_fantasy_jobs:
	make scrap_league_rosters
	make scrap_game_stats

unique_identifier = $(shell date +%Y%m%d_%H%M%S)

imagineering:
	cd ./projects/disney; scrapy crawl ImagineeringSpider -o ../../data/disney/job_dumps/Imagineering_${unique_identifier}.json
	python3 scripts/disney/dumps_to_job_csv.py "./data/disney/job_dumps" "./data/disney/imagineering_jobs.csv"
	python3 scripts/disney/job_post.py "./data/disney/imagineering_jobs.csv"
	python3 scripts/disney/transform.py "./data/disney/imagineering_jobs.csv"

fantasy_rosters:
	cd ./projects/espn; scrapy crawl FantasyLeagueRosterSpider -o ../../data/espn/job_dumps/rosters_${unique_identifier}.json
