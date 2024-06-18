yes_variations = ["yes", "y"]
no_variations = ["no", "n"]


def ask_how_much_games_to_play() -> int:
    while True:
        user_input = input("Enter how much games to you need to play (number): ")

        try:
            input_int = int(user_input)

            if input_int < 1:
                print("Please, enter a positive number")
            else:
                return input_int
        except ValueError:
            print("Please enter a valid integer!")
