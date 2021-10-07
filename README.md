# Wafer

A Cookie Clicker Steam companion app utilizing GUI automation.  
This was made as an experiment in text identification and image recognition. As the game supports
mods to interact with the code directly, this app is **not** the most optimal way to automate
CC. This application only knows the information that *you* know by opening the game or that you can glean from calculations!

## Features

Unchecked boxes are planned, but not yet implemented, features. As the project is still in an early stage and relies on object detection, things may slip through the cracks occasionally.


[x] Click the large cookie at a steady rate  
[x] Locate and click around 80% of gold cookies that appear  
[x] Play the stock market  
[x] Autoharvest garden crops that are about to decay  
[ ] Prioritize crop buffs OR new seeds  
[ ] Harvest ripe sugar lumps  
[ ] Cast useful spells  
[ ] Manage wrinklers  
[ ] Prioritize buying specific buildings OR buying new upgrades  

## Usage

This program has only been tested on Windows computers with one monitor thus far.

Run
`pip install requirements.txt && python app.py` in the directory.
Then, minimize the command window and focus the game screen.

Python 3.7+, tesseract, and opencv are required.

To improve consistency, turn particles off. Make sure to make any adjustments
you would like to `config.toml` before running!

## Acronyms / Definitions
Most methods/classes are documented with their purpose.

A few common acronyms used in the codebase:
- CPS = cookies per second

Definitions:
- Wrinklers = Creatures that consume CPS, but can be popped to give more cookies.
- Spells = Buttons with a % chance of backfiring that can do a variety of tasks,
like generating new cookies or creating wrinklers.
- Golden cookies = Cookies that randomly appear on the screen that usually massively
increase production for a limited period of time.
- Ascension - Resetting building amounts and CPS to unlock more bonuses in the next playthrough.
- Sugar lumps - can be spent on buildings to increase their levels and unlock bonuses

## Screenshots/Videos
### Golden cookie collection
![Golden cookie collection](demo/goldenCookieDemo.gif)

### Garden harvesting
![Garden havesting](demo/gardenDemo.gif)

## Credits

Cookie Clicker is the property of Orteil (https://orteil.dashnet.org/). I do not own anything.
