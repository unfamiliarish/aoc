# i wanted to have a cool animation output thing, which would've shown the changing
# light states each step, but it ended up being way overengineered and not
# as simple to implement as i originally thought
# i poked into asciimatics, colorama, etc, and ultimately decided to only
# do the logic, however much that was soul-crushing


# from pprint import pprint

from copy import deepcopy
import utils


class LightGrid:
    def __init__(self, lights: list[str]) -> None:
        self.lights = [list(light) for light in lights]

    def get_on_neighbors_count(self, x: int, y: int) -> int:
        # x and y indicate a light location
        on_count = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i < 0 or i >= len(self.lights) or j < 0 or j >= len(self.lights):
                    continue
                if i == x and j == y:
                    continue

                if self.lights[i][j] == "#":
                    on_count += 1

        return on_count

    def flip_light(self, x: int, y: int) -> tuple[bool, str]:
        num_on_neighbors = self.get_on_neighbors_count(x, y)
        if self.lights[x][y] == "#" and not (2 <= num_on_neighbors <= 3):
            return (True, ".")
        elif self.lights[x][y] == "." and (num_on_neighbors == 3):
            return (True, "#")

        return (False, self.lights[x][y])

    def get_new_state(self) -> list[list]:
        old_lights = self.lights

        new_lights_grid = deepcopy(self.lights)
        for i in range(len(old_lights)):
            for j in range(len(old_lights[0])):
                flip_light, char = self.flip_light(i, j)
                if flip_light:
                    new_lights_grid[i][j] = char

        return new_lights_grid

    def count_on_lights(self) -> int:
        count = 0
        lights = self.lights
        for i in range(len(lights)):
            for j in range(len(lights[0])):
                if lights[i][j] == "#":
                    count += 1

        return count


def count_lights_on(filename, num_steps: int) -> int:
    lights = utils.import_file(filename)

    light_grid = LightGrid(lights)
    for _ in range(num_steps):
        new_grid_state = light_grid.get_new_state()
        light_grid.lights = new_grid_state

    return light_grid.count_on_lights()


assert count_lights_on("input_sm", 4) == 4
part_1_result = count_lights_on("input", 100)
print(f"part 1: {part_1_result}")
