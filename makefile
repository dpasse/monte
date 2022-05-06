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

scrap_jobs:
	python3 scripts/disney/get_jobs.py

scrap_imagineering_jobs:
	python3 scripts/disney/get_jobs.py "imagineering"

scrap_job_descriptions:
	python3 scripts/disney/get_job_descriptions.py

scrap_imagineering_job_descriptions:
	python3 scripts/disney/get_job_descriptions.py "imagineering"

run_jobs:
	make scrap_jobs
	make scrap_job_descriptions

run_imagineering_jobs:
	make scrap_imagineering_jobs
	make scrap_imagineering_job_descriptions

run_fantasy_jobs:
	make scrap_league_rosters
	make scrap_game_stats
