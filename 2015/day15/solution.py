""" Changing the > to >= in method "mix_best_cookie",
    `if best_cookie.score == 0 or new_cookie.score > best_cookie.score:`
    produces value 13872000, but with strict > produces value 13882464
    this indicates that the sort of the input matters. indeed, moving sugar 
    to the top of the input file confirms this (using strict >)

    in these cases, the tie # # breaker is either the first or last collision 
    if the tie is 3-way, it is possible that the best value may be produced 
    from the middle tie, but i will not handle that

    i have added a flag `first_max` to `mix_best_cookie` to allow for finding
    both the first max with > and the last max with >=, to compare and take
    the greater
"""


from copy import deepcopy
from dataclasses import dataclass, field

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

    @property
    def score(self) -> int:
        return self.capacity * self.durability * self.flavor * self.texture

    def add_ingredient(self, ingredient: Ingredient) -> "Cookie":
        cookie_copy = self.copy()
        if ingredient.name in cookie_copy.ingredients:
            cookie_copy.ingredients[ingredient.name]["num_tsp"] += 1
        else:
            cookie_copy.ingredients[ingredient.name] = {
                "num_tsp": 1,
                "ingredient": ingredient,
            }

        cookie_copy.calc_property_values()

        return cookie_copy

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


def mix_best_cookie(
    ingredients: list[Ingredient], num_tsp: int, first_max: bool = True
) -> Cookie:
    cookies: list[Cookie] = [Cookie()]

    for i in range(1, num_tsp + 1):
        prev_cookie = cookies[i - 1]
        best_cookie = Cookie()  # best is blank cookie to start, always add 1 tsp
        for ingr in ingredients:
            if (
                prev_cookie.has_zero_properties()
                and not prev_cookie.ingredient_fills_zero(ingr)
            ):
                continue

            new_cookie = prev_cookie.add_ingredient(ingr)
            if (
                best_cookie.score == 0
                or (first_max and new_cookie.score > best_cookie.score)
                or (not first_max and new_cookie.score >= best_cookie.score)
            ):
                best_cookie = new_cookie

        cookies.append(best_cookie)

    return cookies[num_tsp]


def determine_best_cookie_score(filename: str, num_tsp: int) -> int:
    rows = utils.import_file(filename)
    ingredients: list[Ingredient] = [parse_cookie_ingredient(r) for r in rows]

    first_max_cookie = mix_best_cookie(ingredients, num_tsp, first_max=True)
    last_max_cookie = mix_best_cookie(ingredients, num_tsp, first_max=False)

    return max(first_max_cookie.score, last_max_cookie.score)


butterscotch = Ingredient("Butterscotch", -1, -2, 6, 3, 8)

assert (
    parse_cookie_ingredient(
        "Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8"
    )
    == butterscotch
)
assert determine_best_cookie_score("input_sm", 100) == 62842880

# 13872000 too low
part_1_result = determine_best_cookie_score("input", 100)
print(f"part 1: {part_1_result}")
