## Blum Game AI Clicker
Clicker to auto-collect stars in game and farm $BLUM automatically. Object detection (stars, bombs, freeze) is based on yolo4 computer vision.
Script intended to help with large numbers of games, it is not effective to run it for 2–3 games, that's why I advise you to accumulate 50+ tickets and then run the script.

# Getting started / Prerequisites
- Supported OS: Windows 
- Python 3.10+ required

**Please read the instruction below completely before running the script.**

1. Clone the repository to your machine
    ```shell
    git clone https://github.com/dKibi/blum-game-ai-clicker.git
    ```

2. Create a virtual environment and activate it
    ```shell
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install project dependencies (run in venv) -
    `python pip install -r requirements`

4. Download and install BlueStacks - https://www.bluestacks.com/download.html

5. Launch BlueStacks Multi Instance Manager and create profile with the name you can identify an account (for example, Blum1)
6. Launch created instance and make sure you have horizontal orientation
7. Inside launched Android instance - install, launch and log in into Telegram app
8. Launch Blum bot and go to home page (if you have any other windows like daily bonus, close them all). You should be at home page where visible **Play** button exists.
9. Launch the script from project root with `python main.py` or `python3 main.py`
10. Wait a few seconds, and you will be prompted to enter how many games should be played. Be careful and do not enter more games than your account have, there is no system to detect that you are out of tickets.
11. Now script will play as many games as you entered and than will be stopped. If you need to stop the script during the game, hold down the English key **q** for a few seconds.