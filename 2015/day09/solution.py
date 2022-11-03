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
    graph: dict[str, dict[str, float]]
    vertices: set

    def __init__(self, connections: list[Connection] = []) -> None:
        self.graph = defaultdict(lambda: defaultdict(lambda: float('inf')))
        self.vertices = set()
        for connection in connections:
            self.graph[connection.start][connection.end] = connection.distance
            self.vertices.add(connection.start)
            self.vertices.add(connection.end)

        for vertex in self.vertices:
            other_vertices = self.vertices.copy() - {vertex}
            for other_vertex in other_vertices:
                self.graph[vertex][other_vertex]

    def TSP_recurse(self, curr_city: str, unvisited_cities: set) -> float:
        if unvisited_cities == set():
            return 0

        total_distances = [float('inf')]
        next_cities = unvisited_cities.copy()
        for next_city in next_cities:
            curr_dist = self.graph[curr_city][next_city]
            distance = curr_dist + self.TSP_recurse(
                next_city, unvisited_cities - {next_city}
            )
            total_distances.append(distance)

        return min(total_distances)

    def TSP_for_city(self, city: str) -> float:
        return self.TSP_recurse(city, self.vertices.copy() - {city})

    def find_shortest_route(self) -> float:
        if len(self.vertices) == 0 or len(self.vertices) == 1:
            return 0

        distances = [float('inf')]
        for city in self.vertices:
            city_min_dist = self.TSP_for_city(city)
            distances.append(city_min_dist)

        return min(distances)


def find_shortest_route(filename: str) -> float:
    raw_connections = utils.import_file(filename)
    parsed_connections = [parse_connection(c) for c in raw_connections]
    graph = Graph(parsed_connections)

    return graph.find_shortest_route()


# # build graph
# raw_connections = utils.import_file("input_TSP_undirected")
# g = Graph([parse_connection(c) for c in raw_connections])
# assert g.graph == {
#     '1': {'2': 10, '3': 15, '4': 20},
#     '2': {'1': 10, '3': 35, '4': 25},
#     '3': {'1': 15, '2': 35, '4': 30},
#     '4': {'1': 20, '2': 25, '3': 30},
# }
# assert g.vertices == {'1', '2', '3', '4'}

# # complete undirected graph
# assert g.TSP_for_city("1") == 65

# complete directed graph
raw_connections = utils.import_file("input_TSP_directed")
g = Graph([parse_connection(c) for c in raw_connections])
val = g.TSP_for_city("1") == 29

# # directed graph missing edges
# assert find_shortest_route("input_missing_edges") == 605

# # null graph
# g = Graph()
# assert g.find_shortest_route() == 0

# 458 too high
part_1_result = find_shortest_route("input")

print(f"part 1: {part_1_result}")
