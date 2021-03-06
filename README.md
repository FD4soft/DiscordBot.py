 # DiscordBot.py

A simple Discord bot constructed using Python 3 and some other libraries made by Bruno Dantas.

Betina is an original Discord bot written in Python 3.6+ entirely in Portuguese, using the discord.py library. It plays requested songs from YouTube and other services in a Discord server and also has funny functions that might help the server administrator. The project is simple according to the functionalities and how other bots use the permission system, but it still in progress.


## Important 
This bot is only compatible with the discord.py rewrite library, which can be installed using python3 -m pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]. Some of the commands doesn't work with Python2. 


### Setup
Setting up Betina is a no-brainer, just follow the guide below:
1. Install the discord.py rewrite library;
2. Install all the libraries located at the [requirements.txt](requirements.txt);
3. Copy the [main.py](main.py) archive and the [Music.py](Music.py);
4. Acess the https://discordapp.com/developers/applications/ and create your own bot;


### Commands
- $deve @user => displays how much a user owes you;
- $devemais @user quantity => increases a quantity on how much a user owes you;
- $devemenos @user quantity => decrease a quantity on how much a user owes you;
- $conversor coin1 coin2 => displays how much is the coin1 in relation to coin2;
- $ppt (pedra, papel ou tesoura) => It's a rock-paper-scissors game;

There are many commands that can be used with the bot. Mainly, the $play command will download and play a song from YouTube or a similar site. A full list of commands can be found using the $help command.


### To get introduced
Using a bot in discord is a good thing and will help you to manage or have fun in your server. According to this, there are some files that will help you to improve Betina or construct a bot from the drawing board:
1. https://discordapp.com/developers/docs/intro
2. https://discordpy.readthedocs.io/en/rewrite/
3. https://sourcecode.glitch.me/
4. https://leovoel.github.io/embed-visualizer/

If you still need help, join us on [discord](https://discord.gg/eZrzDfs)
