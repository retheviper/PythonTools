from datetime import datetime
import sys

if len(sys.argv) < 2:
    print('Need argument of birth year. quitting.')
    sys.exit(1)

animals = [
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
    "Sheep (未)"
    ]

birth_year = int(sys.argv[1])
current_year = datetime.now().year

age = current_year - birth_year + 1
animal = animals[birth_year % 12]

print("Your Korean age is:", age)
print("Your associated animal is:", animal)
