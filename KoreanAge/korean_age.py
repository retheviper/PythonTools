from datetime import datetime
import sys

if len(sys.argv) < 2:
    print('Need argument of birth year. quitting.')
    sys.exit(1)

branches = [
    "Monkey (申)",
    "Rooster (酉)",
    "Dog (戌)",
    "Pig (亥)",
    "Rat (子)",
    "Ox (丑)",
    "Tiger (寅)",
    "Rabbit (卯)",
    "Dragon (辰)",
    "Snake (巳)",
    "Horse (午)",
    "Goat (未)"
    ]

birth_year = int(sys.argv[1])
currentYear = datetime.now().year

age = currentYear - birth_year + 1
branch = branches[birth_year % 12]

print("Your korean age is:", age)
print("Your Earthly branch is:", branch)