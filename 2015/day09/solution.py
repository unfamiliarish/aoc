from collections import defaultdict, namedtuple
from dataclasses import dataclass

import utils


Connection = namedtuple('Connection', ['start', 'end', 'distance'])


def parse_connection(connection: str) -> Connection:
    cities, distance = connection.split(" = ")
    start, end = cities.split(" to ")

    return Connection(start, end, int(distance))


@dataclass
class Graph:
    graph: dict[str, dict[str, int]]

    def __init__(self, connections: list[Connection] = []) -> None:
        self.graph = defaultdict(lambda: defaultdict(int))
        for connection in connections:
            self.graph[connection.start][connection.end] = connection.distance
            self.graph[connection.end][connection.start] = connection.distance

    def find_shortest_path_recurse(
        self, curr_city: str, unvisited_cities: set
    ) -> float:
        if unvisited_cities == set():
            return 0

        total_distances = [float("inf")]
        next_cities = unvisited_cities.copy()

        for next_city in next_cities:
            curr_dist = self.graph[curr_city][next_city]

            distance = curr_dist + self.find_shortest_path_recurse(
                next_city, unvisited_cities - {next_city}
            )

            total_distances.append(distance)

        return min(total_distances)

    def find_shortest_path_for_city(self, city: str) -> float:
        all_cities = set(self.graph.keys())
        return self.find_shortest_path_recurse(city, all_cities - {city})

    def find_shortest_path(self) -> float:
        distances = [float("inf")]
        for city in self.graph.keys():
            city_min_dist = self.find_shortest_path_for_city(city)
            distances.append(city_min_dist)

        return min(distances)

    def find_longest_path_recurse(self, curr_city: str, unvisited_cities: set) -> int:
        if unvisited_cities == set():
            return 0

        total_distances = [0]
        next_cities = unvisited_cities.copy()

        for next_city in next_cities:
            curr_dist = self.graph[curr_city][next_city]

            distance = curr_dist + self.find_longest_path_recurse(
                next_city, unvisited_cities - {next_city}
            )

            total_distances.append(distance)

        return max(total_distances)

    def find_longest_path_for_city(self, city: str) -> int:
        all_cities = set(self.graph.keys())
        return self.find_longest_path_recurse(city, all_cities - {city})

    def find_longest_path(self) -> int:
        distances = [0]
        for city in self.graph.keys():
            city_max_dist = self.find_longest_path_for_city(city)
            distances.append(city_max_dist)

        return max(distances)


def find_shortest_route(filename: str) -> float:
    raw_connections = utils.import_file(filename)
    parsed_connections = [parse_connection(c) for c in raw_connections]
    graph = Graph(parsed_connections)

    return graph.find_shortest_path()


def find_longest_route(filename: str) -> int:
    raw_connections = utils.import_file(filename)
    parsed_connections = [parse_connection(c) for c in raw_connections]
    graph = Graph(parsed_connections)

    return graph.find_longest_path()


# build graph
raw_connections = utils.import_file("input_TSP_undirected")
g = Graph([parse_connection(c) for c in raw_connections])
assert g.graph == {
    '1': {'2': 10, '3': 15, '4': 20},
    '2': {'1': 10, '3': 35, '4': 25},
    '3': {'1': 15, '2': 35, '4': 30},
    '4': {'1': 20, '2': 25, '3': 30},
}

# complete undirected graph
assert g.find_shortest_path_for_city("1") == 65
assert g.find_shortest_path_for_city("2") == 55
assert g.find_shortest_path_for_city("3") == 50
assert g.find_shortest_path_for_city("4") == 50
assert g.find_shortest_path() == 50

# directed graph missing edges
assert find_shortest_route("input_sm") == 605
assert find_longest_route("input_sm") == 982

# # 458 too high
part_1_result = find_shortest_route("input")
print(f"part 1: {part_1_result}")

part_2_result = find_longest_route("input")
print(f"part 2: {part_2_result}")
