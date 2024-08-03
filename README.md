# Blum Game AI Clicker - event update

![Blum AI clicker - bg small - git repo](https://github.com/deKibi/blum-game-ai-clicker/assets/112882532/7e89d50b-3670-460e-b537-24c4824ddfd6)

### Telegram https://t.me/arbyzeru

Clicker to auto-collect stars in game and farm $BLUM automatically. Blum AI clicker works on object detection (stars, bombs, freeze), it means that there is no any interaction with Blum code or API itself.

Script intended to help with large numbers of games, it is not effective to run it for 2–3 games, that's why I advise you to accumulate 50+ tickets and then run the script.

### Buy me a coffee
- MetaMask (any evm) `0x79002fD8bA43a5BFd26CD237BaC0a3677fcA9e55`
- Phantom (Solana) `Fskayrpu1BQhPz333F6Q8WfQL3Kt2kWEv4U5y82gm5Hh`

## Features
- Works on AI (computer vision) — interacting only with image, there is no interaction with the BLUM code/API
- Auto-collecting stars (with the currently trained model the productivity is about 140 points per game)
- Auto-avoiding in-game bombs (with the ability to configure safe distance in the config)
- Prioritization of freezes (if a freeze is detected, it will be pressed first)
- Ability to run on different screen resolutions (screen resolution is specified in the config)

## System requirements
- OS: Windows (tested on Windows 10)
- CPU: 8+ cores with a recommended minimum frequency of 4 GHz (on weaker CPUs the script may not work correctly)
- RAM: 8+ GB
- GPU: at least 512 MB GPU memory recommended

## Installation
Required:
- Python 3.10+ https://www.python.org/downloads/ (when installing, **add Python to the system path**, first installer window, checkbox **Add Python to PATH**)
- BlueStacks https://www.bluestacks.com/download.html
- Git https://git-scm.com/downloads

**Please read the instruction below completely before running the script.**

1. Clone the repository to your machine (git should be installed on your machine)
    ```shell
    git clone https://github.com/deKibi/blum-game-ai-clicker.git
    ```

2. Create a virtual environment and activate it (for Windows)
    ```shell
    python -m venv venv
    venv\Scripts\activate
    ```

3. Install project dependencies (run in venv) -
    `pip install -r requirements.txt`

4. Download and install BlueStacks — https://www.bluestacks.com/download.html

5. Launch BlueStacks Multi Instance Manager and create a profile with the name you can identify an account (for example, Blum1).
6. Launch created instance and make sure you have horizontal orientation. 
7. Inside launched Android instance - install, launch and log in into Telegram app where you will run Blum bot.
8. Launch Blum and go to home page (if you have any other windows like daily bonus, close them all). You should be at home page where visible **Play** button exists. The lower the resolution, the better the software performance, the main thing is that the resolution is not too small and the **Play** and **Play again** buttons are always visible. 
9. Launch the script from project root with `python main.py` or `python3 main.py`. Launch and stop the script (it can crash itself, it's okay).
10. Project config should be generated in `files/config.yaml`. Open config (for example, with Notepad++) and edit screen resolution and window name according to your host. 
11. Wait a few seconds, and you will be prompted to enter how many games should be played. Be careful and do not enter more games than your account have, there is no system to detect that you are out of tickets.
12. Now Blum AI clicker will play as many games as you entered and then will be stopped. If you need to stop the script during the game, hold down the English key **q** for a few seconds.



## Credits
- Thanks [@moises-dias](https://github.com/moises-dias) for Yolo object detection tutorial
- Thanks [@hokageR1s](https://t.me/hokageR1s) for help with testing

## Disclaimer
The script was written for educational purposes and has never been used on my accounts to earn money or violate rules.
Use the software at your own risk.
