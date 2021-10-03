# Wafer

A Cookie Clicker Steam companion app utilizing GUI automation.  
This was made as an experiment in text identification and image recognition. As the game supports
mods to interact with the code directly, this is not the most optimal way to automate
CC. This application only knows the information that *you* know by opening the game!

## Features

Unchecked boxes are planned, but not yet implemented, features. As the project is still in an early stage and relies on objection detection, things may slip through the cracks occasionally.


[x] Click the large cookie at a steady rate  
[x] Locate and click around 80% of gold cookies that appear  
[ ] Manage wrinklers  
[x] Autoharvest garden crops that are about to decay  
[ ] Prioritize crop buffs OR new seeds  
[ ] Harvest ripe sugar lumps  
[ ] Cast useful spells  
[ ] Play the stock market  
[ ] Prioritize buying specific buildings OR buying new upgrades  

## Usage

This program has only been tested on Windows computers with one monitor thus far.

Run
`pip install requirements.txt && python app.py` in the directory.
Then, minimize the command window and focus the game screen.

Python 3.7+, tesseract, and opencv are required.

To improve consistency, turn particles off.
Make sure that your save is stored in `C:\Program Files (x86)\Steam\steamapps\common\Cookie Clicker\resources\app\save\save.cki`.

## Screenshots/Videos
### Golden cookie collection
![Golden cookie collection](demo/goldenCookieDemo.gif)

### Garden harvesting
![Garden havesting](demo/gardenDemo.gif)

## Credits

Cookie Clicker is the property of Orteil (https://orteil.dashnet.org/). I do not own anything.
