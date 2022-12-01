from collections import namedtuple
from itertools import product

import utils


Ingredient = namedtuple(
    "Ingredient", ["name", "capacity", "durability", "flavor", "texture", "calories"]
)


def parse_cookie_ingredient(input: str) -> Ingredient:
    name, remaining = input.split(":")
    properties = remaining.split(",")
    capacity = int(properties[0].split(" capacity ")[1])
    durability = int(properties[1].split(" durability ")[1])
    flavor = int(properties[2].split(" flavor ")[1])
    texture = int(properties[3].split(" texture ")[1])
    calories = int(properties[4].split(" calories ")[1])

    return Ingredient(name, capacity, durability, flavor, texture, calories)


def calc_score(cookie: list) -> int:
    # input <- [(num_tsp, ingredient),...]
    capacity = sum([ingr[0] * ingr[1].capacity for ingr in cookie])
    durability = sum([ingr[0] * ingr[1].durability for ingr in cookie])
    flavor = sum([ingr[0] * ingr[1].flavor for ingr in cookie])
    texture = sum([ingr[0] * ingr[1].texture for ingr in cookie])

    capacity = capacity if capacity > 0 else 0
    durability = durability if durability > 0 else 0
    flavor = flavor if flavor > 0 else 0
    texture = texture if texture > 0 else 0

    return capacity * durability * flavor * texture


def calc_calories(cookie: list) -> int:
    # input <- [(num_tsp, ingredient),...]
    return sum([ingr[0] * ingr[1].calories for ingr in cookie])


def determine_best_500_cal_cookie_score(filename: str, num_tsp: int) -> int:
    rows = utils.import_file(filename)
    ingredients = [parse_cookie_ingredient(row) for row in rows]

    recipes = [
        teaspoons
        for teaspoons in product(range(0, num_tsp + 1), repeat=len(ingredients))
        if sum(teaspoons) == num_tsp
    ]

    print(f"{len(recipes)} recipes printed")
    cookies = [list(zip(recipe, ingredients)) for recipe in recipes]
    print("cookies baked")

    best_score = 0
    for cookie in cookies:
        if calc_calories(cookie) != 500:
            continue

        score = calc_score(cookie)
        if score > best_score:
            print("tastier cookie found")
            best_score = score

    return best_score


assert determine_best_500_cal_cookie_score("input_sm", 100) == 57600000

# 19150560 is too high
# 11171160 <- correct answer
# 11162880 is too low
# 13882464 incorrect (value when excluding the 500 cal constraint)
part_2_result = determine_best_500_cal_cookie_score("input", 100)
print(f"part 2: {part_2_result}")
