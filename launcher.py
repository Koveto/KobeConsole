import subprocess

while True:
    print()
    print("1. Heads or Tails")
    print("2. Test Game")
    print("Q. Quit")

    choice = input("Select game: ")

    if choice == "1":
        subprocess.run(["python", "games/heads_or_tails.py"])

    elif choice == "2":
        subprocess.run(["python", "games/test_game.py"])

    elif choice.lower() == "q":
        break