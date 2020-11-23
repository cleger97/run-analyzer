import csv
import os
import sys
from decimal import Decimal
from datetime import timedelta
from datetime import datetime
from datetime import date
from os import listdir
from os.path import isfile, join

has_config = False

#print(os.path.dirname(os.path.realpath(__file__)))

#curr_dir = listdir(os.path.dirname(os.path.realpath(__file__)))
#for f in curr_dir:
#	if (f == 'run_config.ini'):
#		has_config = True
#		config = open(f)
#		for line in config:
#			if line[0] =='#':
#				continue
#			split = line.split('=')
#			if (split[0] == 'dir'):
#				filepath = split[1]
#				print(filepath)

if (len(sys.argv) == 1 or sys.argv[1] == 'default'):
	dirname = os.path.dirname(__file__)
	#filename = os.path.join(dirname, 'Summoners War Exporter Files/Nuparu11-22975128-runs.csv')
	filepath = os.path.join(dirname, 'Summoners War Exporter Files/')
	filename = ''

	for f in listdir(filepath):
		if (isfile(join(filepath, f))):
			k = f[-9:]
			l = f[-14:]
			if ( k == "-runs.csv" and l != "-raid-runs.csv"):
				filename = os.path.join(filepath, f)

else:
	filename = sys.argv[1]
	if (not isfile(filename)):
		filename = os.path.join(__file__, filename)

		if (not isfile(filename)):
			print("Not a file")
			exit()

defaultdate = '2020-07-01'
fromdate = datetime.strptime(defaultdate, '%Y-%m-%d')
if (len(sys.argv) > 2 and sys.argv[2] != 'default'):
	try:
		fromdate = datetime.strptime(sys.argv[2], '%Y-%m-%d')
	except ValueError:
		print("Incorrect format of date argument - use 'default' or Y-m-d format")
		exit()

while True:
	with open(filename) as f:
		reader = csv.reader(f)
		header_row = next(reader)
		
		
		dungeon_input = input("\nShow stats for which dungeon? (gb12/db12/nb12/sf10/pc10)  ")
		if dungeon_input == "gb12":
			dungeon = "Giant's Keep B12"
		elif dungeon_input == "db12":
			dungeon = "Dragon's Lair B12"
		elif dungeon_input == "nb12":
			dungeon = "Necropolis B12"
		elif dungeon_input == "sf10" or dungeon_input == "sb10":
			dungeon = "Steel Fortress B10"
		elif dungeon_input == "pc10" or dungeon_input == "pb10":
			dungeon = "Punisher's Crypt B10"
		elif dungeon_input == "q":
			exit()
		else:
			print("\nInvalid input, restart the app!")
			print("_____________________________________")
			break

		#dung_fails = 0
		#dung_runs = []

		dung_fails = 0
		dung_runs = 1
		dung_success = 2
		dung_average = 3

		dung_teams = {}
		
		for row in reader:
			currdate = datetime.strptime(row[0], '%Y-%m-%d %H:%M')
			if (currdate.year < fromdate.year 
				or currdate.month < fromdate.month 
				or currdate.day < fromdate.day):
				continue

			# If not correct dungeon
			if (not row[1] == dungeon):
				continue

			#20 - 24 for team members
			x = [row[21], row[22], row[23], row[24]]
			x.sort()
			team = row[20] + ' ' + ' '.join(x)

			if (not team in dung_teams):
				dung_teams[team] = [0, [], 0, 0, 0, 0] # Fails / Runs / Success Rate / Average Time / reserved

			if row[2] == "Lost":
				#dung_fails += 1
				dung_teams[team][dung_fails] += 1
			elif row[2] == "Win":
				dung_teams[team][dung_runs].append(row)
				#dung_runs.append(row)

		if len(dung_teams) == 0:
			print(f"\nNo runs logged for {dungeon} yet.\n")
			continue

		super_list = []
		print("_____________________________________")	
		print(f"\nShowing stats for {dungeon}:")
		for dung_team in dung_teams:
			curr_team = dung_teams[dung_team]
			dung_time_cache = []

			#print( (curr_team[dung_runs]) )

			for run in curr_team[dung_runs]:
				split_time = run[3].split(":")
				formatted_time = timedelta(minutes=int(split_time[0]), seconds=int(split_time[1]))
				dung_time_cache.append(formatted_time)

			dung_time_sum = timedelta(0)
			for time in dung_time_cache:
				dung_time_sum += time

			if (len(dung_time_cache) == 0):
				continue

			dung_time_avg = dung_time_sum/len(dung_time_cache)
			time_string = str(dung_time_avg).strip('00:')
			final_time_string = time_string[0:4]
			print(f"Team: {dung_team}")
			print(f"Runs completed: {len(curr_team[dung_runs]) + curr_team[dung_fails]}")
			print(f"Success rate: {format((len(curr_team[dung_runs])/(len(curr_team[dung_runs])+curr_team[dung_fails]))*100, '.2f')}%")
			print(f"Average time: {final_time_string}")


		print(f"_____________________________________\n")

		dung_norune = 0
		dung_rare = 0
		dung_hero = 0
		dung_leg = 0
		total_runs = 0

		water_art = 0
		fire_art = 0
		wind_art = 0
		light_art = 0
		dark_art = 0
		no_art = 0

		name = ord('K') - ord('A')

		isArti = (dungeon == "Steel Fortress B10" or dungeon == "Punisher's Crypt B10")

		for dung_team in dung_teams:
			curr_team = dung_teams[dung_team]

			for run in curr_team[dung_runs]:
				total_runs += 1

				if isArti:
					#print(run[name][11:-1])
					if run[name][11:-1] == "Water":
						water_art += 1
					elif run[name][11:-1] == "Fire":
						fire_art += 1
					elif run[name][11:-1] == "Wind":
						wind_art += 1
					elif run[name][11:-1] == "Light":
						light_art += 1
					elif run[name][11:-1] == "Dark":
						dark_art += 1
					else:
						no_art += 1

				if run[13] == "Rare":
					dung_rare += 1
				elif run[13] == "Hero":
					dung_hero += 1
				elif run[13] == "Legendary":
					dung_leg += 1
				elif run[7] != "Rune":
					dung_norune += 1


		if isArti:
			print("Artifact Drop Information")
			print(f"\nNon artifact drops: {no_art} - Rate: {format(Decimal(no_art/total_runs)*100, '.2f')}%")	
			print(f"Fire artifacts: {fire_art} - Rate: {format(Decimal(fire_art/total_runs)*100, '.2f')}%")
			print(f"Water artifacts: {water_art} - Rate: {format(Decimal(water_art/total_runs)*100, '.2f')}%")
			print(f"Wind artifacts: {wind_art} - Rate: {format(Decimal(wind_art/total_runs)*100, '.2f')}%")
			print(f"Light artifacts: {light_art} - Rate: {format(Decimal(light_art/total_runs)*100, '.2f')}%")
			print(f"Dark artifacts: {dark_art} - Rate: {format(Decimal(dark_art/total_runs)*100, '.2f')}%")

			print(f"_____________________________________\n")
			
		
		
		print("Rune drop data")	
		print(f"\nNon rune drops: {dung_norune} - Rate: {format(Decimal(dung_norune/total_runs)*100, '.2f')}%")	
		print(f"Rare runes: {dung_rare} - Rate: {format(Decimal(dung_rare/total_runs)*100, '.2f')}%")
		print(f"Hero runes: {dung_hero} - Rate: {format(Decimal(dung_hero/total_runs)*100, '.2f')}%")
		print(f"Legend runes: {dung_leg} - Rate: {format(Decimal(dung_leg/total_runs)*100, '.2f')}%")
		print(f"_____________________________________\n")
	
