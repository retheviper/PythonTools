from datetime import datetime
import sys

if len(sys.argv) < 2:
    print("Need argument of birth year. quitting.")
    sys.exit(1)

def range_dict(*args):
    result = {}
    for k, v in args:
        for i in k:
            result[i] = v
    return result

stems = [
    "Metal (庚)",
    "Metal (辛)",
    "Water (壬)",
    "Water (癸)",
    "Wood (甲)",
    "Wood (乙)",
    "Fire (丙)",
    "Fire (丁)",
    "Earth (戊)",
    "Earth (己)",
]

yin_yangs = [
    "Yang (陽)",
    "Yin (陰)"
]

colors = range_dict(
    (range(0, 2), "White (白)"),
    (range(2, 4), "Black (黑)"),
    (range(4, 6), "Blue (靑)"),
    (range(6, 8), "Red (赤)"),
    (range(8, 10), "Yellow (黃)")
)

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
    "Sheep (未)",
]


birth_year = int(sys.argv[1])
current_year = datetime.now().year

age = current_year - birth_year + 1
stem = stems[birth_year % 10]
color = colors[birth_year % 10]
yin_yang = yin_yangs[birth_year % 2]
animal = animals[birth_year % 12]

print("Your Korean age is:", age)
print("Your heavenly stem is:", stem)
print("Your Yin-yang is:", yin_yang)
print("Your associated color is:", color)
print("Your associated animal is:", animal)
