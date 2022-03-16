# Program to check the rpilocator webstie every x minutes
# it will perform a curl reqeust and parse the html from the website
# every hit that it has will have the "table-success" class
# options for running the program include filter and settings like: refresh rate, location(s), model(s), sound, notification
# when the program gets a hit, it will play a sound and display a message on the screen

import time
import os
import winsound
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import win32ui
import win32con

OPTIONS = {
	"refresh_rate": 10,
	"locations": ["ALL"],
	"models": ["ALL"],
	"sound": True,
	"notification": True,
	"verbose": True
}

# constants
LOCATIONS = [("Canada", "CA"), ("China", "CN"), ("France", "FR"), ("Germany", "DE"), ("Netherlands", "NL"), ("Spain", "ES"), ("Sweden", "SE"), ("Switzerland", "CH"), ("United Kingdom", "UK"), ("United States", "US")]
MODELS = [("CM4", "CM4"), ("Pi 3", "RPI3"), ("Pi 4", "RPI4"), ("Pi Zero", "SC0")]


def PlaySound():
	if OPTIONS['sound']:
		winsound.PlaySound("./Congratulations! Your Pokémon Evolved!.wav", winsound.SND_FILENAME)
		# winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)

def Notify(message):
	if OPTIONS['notification']:
		win32ui.MessageBox("A device is in stock!!!!", "RPi Locator Watcher", win32con.MB_ICONASTERISK)

def CheckWebsite(driver):
	# find the table with the class "table-success"
	driverRows = driver.find_elements(By.CLASS_NAME, "table-success")
	
	if (OPTIONS['verbose']):
		print("%s 📦 Number of Places in stock: \033[0;33m%d\033[0;0m" % (time.strftime("%H:%M:%S"), len(driverRows)))

	notified = False

	for row in driverRows:
		model = row.find_element(By.TAG_NAME, "th").text
		tds = row.find_elements(By.TAG_NAME, "td")
		name = tds[0].text
		link = tds[1].find_element(By.TAG_NAME, "a").get_attribute("href")
		lastChecked = tds[2].text
		website = tds[3].text
		lastStock = tds[5].text
		price = tds[6].text

		# check if the location is in the list of locations
		location = website.split(" ")
		location = location[len(location) - 1][1:-1]
		if (OPTIONS['locations'][0] != "ALL" and location not in OPTIONS['locations']):
			continue

		# check if the model starts with whats in the list of models
		if (OPTIONS['models'][0] != "ALL" and not any(model[0:len(m)] == m for m in OPTIONS['models'])):
			continue

		if not notified:
			print("\033[1;30;42m%s 🎉 %d Hits!\033[0;0m" % (time.strftime("%H:%M:%S"), len(driverRows)))
			PlaySound()
			Notify("RPi Locator hit!")
			notified = True

		print ("\033[0;0m%s | %s %s %s %s %s %s" % (time.strftime("%H:%M:%S"), model, name, link, lastChecked, website, lastStock))

	if not notified and OPTIONS['verbose']:
		print("%s 😪 No hits" % time.strftime("%H:%M:%S"))


def Run():
	running = True
	# selenium webdriver
	options = Options()
	# options.add_argument("--headless")
	options.headless = True
	options.page_load_strategy = "normal"
	driver = webdriver.Chrome()

	# load window
	driver.get("https://rpilocator.com/")

	while running:
		os.system("cls")

		# try catch if exit command is pressed
		try:
			if OPTIONS['verbose']:
				print("%s 🔍 Checking website..." % (time.strftime("%H:%M:%S")))

			driver.refresh()
			CheckWebsite(driver)

			# wait for the refresh rate
			if OPTIONS['verbose']:
				print("%s ⏲  Waiting %d minutes..." % (time.strftime("%H:%M:%S"), OPTIONS['refresh_rate']))

			time.sleep(OPTIONS['refresh_rate'] * 60)
		except KeyboardInterrupt:
			# exit the program
			running = False

	driver.quit()


def SaveOptions():
	# save the options to a json file
	with open("options.json", "w") as file:
		json.dump(OPTIONS, file, indent=4)

def LoadOptions():
	# load the options from a json file
	op = {}
	try:
		with open("options.json", "r") as file:
			op = json.load(file)
	except FileNotFoundError:
		pass
	except ValueError:
		pass

	if (len(op.keys()) > 0):
		for key in OPTIONS.keys():
			if key in op.keys():
				OPTIONS[key] = op[key]

def SetRefreshRate():
	# get the user input
	userInput = input("Enter the new refresh rate (in minutes): ")

	# check if the input is a number
	try:
		OPTIONS['refresh_rate'] = int(userInput)
		return
	except ValueError:
		print("Invalid input")
		SetRefreshRate()
		return

def SelectLocations():
	# if the user wants to change the locations
	# print the locations
	print("================================================")
	print("Locations:")
	for (i, location) in enumerate(LOCATIONS, 1):
		print("\t" + str(i) + ") " + location[0])
	print("\t" + str(i+1) + ") ALL")
	print("\t" + str(i+2) + ") Back")
	print("================================================")

	# get the user input
	userInput = list(map(int, (input("Enter the new locations (seperate with a \",\" for multiple): ").replace(" ", "").split(","))))

	OPTIONS['locations'] = []
	if i+1 in userInput:
		# if the user wants to select all locations
		OPTIONS['locations'] = ["ALL"]
	elif i+2 in userInput:
		return
	else:
		# if the user wants to select locations seperated by a comma
		# push valid inputs into the selected locations list
		for location in userInput:
			location = int(location)
			if (location - 1) <= len(LOCATIONS) and (location - 1) >= 0:
				OPTIONS['locations'].append(LOCATIONS[location-1][1])
			else:
				print("Invalid input")
				SelectLocations()

def SelectModels():
	# if the user wants to change the models
	# print the models
	print("================================================")
	print("Models:")
	for (i, model) in enumerate(MODELS, 1):
		print("\t" + str(i) + ") " + model[0])
	print("\t" + str(i+1) + ") ALL")
	print("\t" + str(i+2) + ") Back")
	print("================================================")

	# get the user input
	userInput = list(map(int, input("Enter the new models (seperate with a \",\" for multiple): ").replace(" ", "").split(",")))

	if i+1 in userInput:
		# if the user wants to select all models
		OPTIONS['models'] = ["ALL"]
	elif i+2 in userInput:
		return
	else:
		# if the user wants to select models seperated by a comma
		# push valid inputs into the selected models list
		for model in userInput:
			model = int(model)
			if (model - 1) <= len(MODELS) and (model - 1) >= 0:
				OPTIONS['models'].append(MODELS[model-1][1])
			else:
				print("Invalid input")
				SelectModels()

def ToggleSound():
	# ask the user if they want to turn the sound on or off
	userInput = input("Sound on? (True/False or 1/0): ").lower()
	# if the user wants to turn the sound on
	OPTIONS['sound'] = (userInput == "true" or userInput == "1")
	
def ToggleNotification():
	# ask the user if they want to turn the notification on or off
	userInput = input("Notifications on? (True/False or 1/0): ").lower()
	# if the user wants to turn the notification on
	OPTIONS['notifications'] = (userInput == "true" or userInput == "1")

def SetVerbose():
	# ask the user if they want to turn the verbose on or off
	userInput = input("Verbose on? (True/False or 1/0): ").lower()
	# if the user wants to turn the verbose on
	OPTIONS['verbose'] = (userInput == "true" or userInput == "1")

if __name__ == "__main__":
	menuOPTIONS = {
		1: SetRefreshRate,
		2: SelectLocations,
		3: SelectModels,
		4: ToggleSound,
		5: ToggleNotification,
		6: SetVerbose,
		7: Run,
		8: exit
	}

	LoadOptions()

	while True:
		try:
			# clear cmd line
			os.system("cls")

			# menu
			print("RPi Locator Watch")
			print("================================================")
			print("OPTIONS:")
			print("\t1. Refresh Rate: " + str(OPTIONS['refresh_rate']) + " minutes")
			print("\t2. Locations: " + str(OPTIONS['locations']))
			print("\t3. Models: " + str(OPTIONS['models']))
			print("\t4. Sound: " + str(OPTIONS['sound']))
			print("\t5. Notification: " + str(OPTIONS['notification']))
			print("\t6. Verbose: " + str(OPTIONS['verbose']))
			print("\t7. Run the program")
			print("\t8. Exit")
			print("================================================")

			# get the user input
			choice = int(input("Enter your choice: ").replace(" ", ""))
			
			os.system("cls")

			if choice in menuOPTIONS:
				menuOPTIONS[choice]()
				SaveOptions()
			else:
				print("Invalid choice")
				input("Press enter to continue...")

		except KeyboardInterrupt:
			exit()
		except ValueError:
			print("Invalid choice")
			input("Press enter to continue...")
