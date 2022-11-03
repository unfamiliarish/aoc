from collections import defaultdict, namedtuple
from dataclasses import dataclass
from time import sleep

import utils


Connection = namedtuple('Connection', ['start', 'end', 'distance'])

inf = float('inf')


def parse_connection(connection: str) -> Connection:
    cities, distance = connection.split(" = ")
    start, end = cities.split(" to ")

    return Connection(start, end, int(distance))


@dataclass
class Graph:
    graph: dict[str, dict[str, float]]
    vertices: set

    def __init__(self, connections: list[Connection] = []) -> None:
        self.graph = defaultdict(lambda: defaultdict(lambda: inf))
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
        sleep(0.1)
        print("in TSP recurse")
        print(f"curr city: {curr_city}, unvisited cities: {unvisited_cities}")
        if unvisited_cities == set():
            return 0

        total_distances = [inf]
        next_cities = unvisited_cities.copy()
        for next_city in next_cities:
            print(f"curr city: {curr_city}, next city: {next_city}")
            curr_dist = self.graph[curr_city][next_city]
            if curr_dist == inf:
                return inf

            print(f"dist beween cities: {curr_dist}")
            distance = curr_dist + self.TSP_recurse(
                next_city, unvisited_cities - {next_city}
            )
            print(
                f"recursive distance from {curr_city} through {next_city} to the end: {distance}\n"
            )
            total_distances.append(distance)

        sleep(0.1)
        return min(total_distances)

    def TSP_for_city(self, city: str) -> float:
        return self.TSP_recurse(city, self.vertices.copy() - {city})

    def find_shortest_route(self) -> float:
        print(f"in find shortest route for graph")
        if len(self.vertices) == 0 or len(self.vertices) == 1:
            return 0

        distances = [inf]
        for city in self.vertices:
            print(f"\nfor city: {city}")
            city_min_dist = self.TSP_for_city(city)
            print(f"city {city}. shortest route from city: {city_min_dist}")
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

# # # complete undirected graph
# assert g.TSP_for_city("1") == 65
# assert g.TSP_for_city("2") == 55
# assert g.TSP_for_city("3") == 50
# assert g.TSP_for_city("4") == 50
# assert g.find_shortest_route() == 50

# # complete directed graph
# raw_connections = utils.import_file("input_TSP_directed")
# g = Graph([parse_connection(c) for c in raw_connections])
# val = g.TSP_for_city("1") == 29

# # directed graph missing edges
# assert find_shortest_route("input_missing_edges") == 605

# # null graph
# g = Graph()
# assert g.find_shortest_route() == 0

# 458 too high
part_1_result = find_shortest_route("input")
print(f"part 1: {part_1_result}")
