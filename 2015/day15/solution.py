""" Changing the > to >= in method "mix_best_cookie",
    `if best_cookie.score == 0 or new_cookie.score > best_cookie.score:`
    produces value 13872000, but with strict > produces value 13882464
    this indicates that the sort of the input matters. indeed, moving sugar 
    to the top of the input file confirms this (using strict >)

    in these cases, the tie # breaker is either the first or last collision 
    if the tie is 3-way, it is possible that the best value may be produced 
    from the middle tie, but i will not handle that

    i have added a flag `first_max` to `mix_best_cookie` to allow for finding
    both the first max with > and the last max with >=, to compare and take
    the greater
"""


from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
import math

import utils


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def parse_cookie_ingredient(input: str) -> Ingredient:
    name, remaining = input.split(":")
    properties = remaining.split(",")
    capacity = int(properties[0].split(" capacity ")[1])
    durability = int(properties[1].split(" durability ")[1])
    flavor = int(properties[2].split(" flavor ")[1])
    texture = int(properties[3].split(" texture ")[1])
    calories = int(properties[4].split(" calories ")[1])

    return Ingredient(name, capacity, durability, flavor, texture, calories)


@dataclass
class Cookie:
    """
    ingredients = {
        "Butterscotch": {
            "ingredient": {
                name: str
                capacity: int
                durability: int
                flavor: int
                texture: int
                calories: int
            }
            "num_tsp": #
        }
        "Cinnamon": {...},
        ...
    }

    """

    ingredients: dict = field(default_factory=lambda: {})  # type: ignore
    capacity: int = 0
    durability: int = 0
    flavor: int = 0
    texture: int = 0
    calories: int = 0

    @classmethod
    def build_from_ingredients(cls, ingredients: dict) -> "Cookie":
        cookie = cls(ingredients)
        cookie.calc_property_values()

        return cookie

    @property
    def num_tsp(self) -> int:
        num_tsp = 0
        for ingr in self.ingredients.values():
            num_tsp += ingr["num_tsp"]

        return num_tsp

    @property
    def score(self) -> int:
        return self.capacity * self.durability * self.flavor * self.texture

    def add_ingredient(self, ingredient: Ingredient) -> None:
        if ingredient.name in self.ingredients:
            self.ingredients[ingredient.name]["num_tsp"] += 1
        else:
            self.ingredients[ingredient.name] = {"num_tsp": 1, "ingredient": ingredient}

        self.calc_property_values()
        return

    def has_zero_properties(self, excl_calories: bool = True) -> list[str]:
        properties = list(self.__dict__.keys())
        if excl_calories:
            properties.remove("calories")

        zeros = []
        for property in properties:
            if getattr(self, property) == 0:
                zeros.append(property)
        return zeros

    def ingredient_fills_zero(self, ingredient: Ingredient) -> bool:
        zeros = self.has_zero_properties()
        for zero in zeros:
            raw_property_value = self.calc_property(zero, return_raw=True)
            if raw_property_value + getattr(ingredient, zero) > 0:
                return True

        return False

    def calc_property(self, property_: str, return_raw: bool = False) -> int:
        # this method so not 5 separate methods for calc'ing each property
        total = 0

        ingredients = self.ingredients.values()
        for ingr in ingredients:
            ingr_property = getattr(ingr["ingredient"], property_)
            total += ingr["num_tsp"] * ingr_property

        if return_raw:
            return total

        return total if total > 0 else 0

    def calc_property_values(self) -> None:
        properties = list(self.__dict__.keys())
        properties.remove("ingredients")
        for property in properties:
            setattr(self, property, self.calc_property(property))

    def copy(self) -> "Cookie":
        ingredients_copy = deepcopy(self.ingredients)
        return Cookie(
            ingredients_copy,
            capacity=self.capacity,
            durability=self.durability,
            flavor=self.flavor,
            texture=self.texture,
            calories=self.calories,
        )

    def combine_cookies(self, cookie: "Cookie") -> "Cookie":
        combined_ingredients: dict = defaultdict(lambda: defaultdict(int))
        for name, ingr in self.ingredients.items():
            combined_ingredients[name]["ingredient"] = ingr["ingredient"]
            combined_ingredients[name]["num_tsp"] += ingr["num_tsp"]
        for name, ingr in cookie.ingredients.items():
            combined_ingredients[name]["ingredient"] = ingr["ingredient"]
            combined_ingredients[name]["num_tsp"] += ingr["num_tsp"]

        return Cookie.build_from_ingredients(combined_ingredients)


def mix_best_cookie(
    ingredients: list[Ingredient], num_tsp: int, first_max: bool = True
) -> Cookie:
    cookies: list[Cookie] = [Cookie()]

    for i in range(1, num_tsp + 1):
        prev_cookie = cookies[i - 1]
        best_cookie = Cookie()  # best is blank cookie to start, always add 1 tsp
        for ingr in ingredients:
            new_cookie = prev_cookie.copy()
            if (
                prev_cookie.has_zero_properties()
                and not prev_cookie.ingredient_fills_zero(ingr)
            ):
                continue

            new_cookie.add_ingredient(ingr)
            if (
                best_cookie.score == 0
                or (first_max and new_cookie.score > best_cookie.score)
                or (not first_max and new_cookie.score >= best_cookie.score)
            ):
                best_cookie = new_cookie

        cookies.append(best_cookie)

    return cookies[num_tsp]


def mix_best_cookie_exactly_500_cals(
    ingredients: list[Ingredient], first_max: bool = True
) -> Cookie:
    # basic knapsack algorithm, but with add'l constrainst
    # allowed num of tsp:
    # 1,2,3,4,5, -> 1 tsp
    # 6,7,8,9,10 -> 2 tsp
    # etc
    # calc'd with ceil(knapsack slot / 5)
    #
    # balancing constraints: calories = 500, num tsp = 100
    #
    # chose to hardcode these calcs, as handling allowed cals and
    # allowed tsp would've req'd some complex calcs that are
    # unnecessary

    cookies: list = [Cookie()]  # will have len 501 knapsack

    for i in range(1, 501):
        best_cookie = Cookie()
        for ingr in ingredients:
            # breakpoint()
            if i - ingr.calories < 0:
                continue

            allowed_num_ingredients = math.ceil(i / 5)
            knapsack_cookie = cookies[i - ingr.calories]

            # breakpoint()
            # could not set knapsack slot with exact tsp
            if knapsack_cookie is None:
                continue
            # using previous cookie would use invalid num of tsp
            if knapsack_cookie.num_tsp + 1 != allowed_num_ingredients:
                continue

            new_cookie = knapsack_cookie.copy()
            new_cookie.add_ingredient(ingr)

            if (
                (best_cookie.score == 0)
                or (first_max and new_cookie.score > best_cookie.score)
                or (not first_max and new_cookie.score >= best_cookie.score)
            ):
                best_cookie = new_cookie

        if best_cookie == Cookie():
            # could not populate exact num of calories with
            # allowed num of tsp
            cookies.append(None)
            continue

        # breakpoint()
        cookies.append(best_cookie)

    # breakpoint()
    return cookies[500]


def determine_best_cookie_score(filename: str, num_tsp: int) -> int:
    rows = utils.import_file(filename)
    ingredients: list[Ingredient] = [parse_cookie_ingredient(r) for r in rows]

    first_max_cookie = mix_best_cookie(ingredients, num_tsp, first_max=True)
    last_max_cookie = mix_best_cookie(ingredients, num_tsp, first_max=False)

    return max(first_max_cookie.score, last_max_cookie.score)


def determine_best_cookie_score_exactly_500_cals(filename: str, num_tsp: int) -> int:
    rows = utils.import_file(filename)
    ingredients: list[Ingredient] = [parse_cookie_ingredient(r) for r in rows]

    first_max_cookie = mix_best_cookie_exactly_500_cals(ingredients, first_max=True)
    last_max_cookie = mix_best_cookie_exactly_500_cals(ingredients, first_max=False)

    breakpoint()
    return max(first_max_cookie.score, last_max_cookie.score)


# butterscotch = Ingredient("Butterscotch", -1, -2, 6, 3, 8)

# assert (
#     parse_cookie_ingredient(
#         "Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8"
#     )
#     == butterscotch
# )
# assert determine_best_cookie_score("input_sm", 100) == 62842880

# # 13872000 too low
# part_1_result = determine_best_cookie_score("input", 100)
# print(f"part 1: {part_1_result}")

# assert determine_best_cookie_score_exactly_500_cals("input_sm", 100) == 57600000

# 32503680 too high
# 9409920 too low
part_2_result = determine_best_cookie_score_exactly_500_cals("input", 100)
print(f"part 2: {part_2_result}")
