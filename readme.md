# Installation Instructions (2 ways):

Required Packages: pygame@2.1.3.dev8, geomdl@latest, cachetools@latest
This project was made with python 3.11.1 so to avoid issues, i recommend using that version when running it.

## Via Git: 

Step 1: clone it
```bash
git clone https://github.com/Axzurey/py-lylac
```

Step 2: Cd to the cloned folder

```bash
cd py-lylac
```

Step 3: Install dependencies

If you only have python 3.11.1:
```bash
python3 -m pip install pygame==2.1.3.dev8 cachetools geomdl
```

If you have mutliple versions you may need to specify:
```bash
py -3.11 -m pip install pygame=2.1.3.dev8 cachetools geomdl
```

Step 4: Run it

If you only have python 3.11.1:
```bash
python3 main.py
```

If you have mutliple versions you may need to specify:
```bash
py -3.11 main.py
```

## Via Github:

Step 1: Download the folder by clicking the green "<> Code" button and then clicking "Download Zip"

Step 2: Unzip the folder

Step 2: Cd to the downloaded folder

```bash
cd py-lylac-master
```

Step 3: Install dependencies

If you only have python 3.11.1:
```bash
python3 -m pip install pygame==2.1.3.dev8 cachetools geomdl
```

If you have mutliple versions you may need to specify:
```bash
py -3.11 -m pip install pygame=2.1.3.dev8 cachetools geomdl
```

Step 4: Run it

If you only have python 3.11.1:
```bash
python3 main.py
```

If you have mutliple versions you may need to specify:
```bash
py -3.11 main.py
```



File structure & Additional Information:

1. The "lylac" folder is the framework used to make this game, created by me.
2. The "levels" folder is data for each of the levels in the event you want to modify them.
3. The "fonts" folder is just a place to put fonts and holds not significance in the framework.
4. The "editor" folder contains two files: "enemy_path_editor.py" & "tower_area_editor.py". These
   files are used to generate layouts for the respective parts of the game, into json files. When in use,
   I bring these into the main scope of the project to make my life easier.
5. The "data" folder contains a "towers" folder, a "enemies" folder, and a few base classes and controllers
   for different aspects of the game.
6. The "custom" folder contains most of the widgets and displays that the program uses for different phases
   in the game.
7. The "assets" folder is a container for all the assets I used in the game.
8. Ignore ".gitignore".