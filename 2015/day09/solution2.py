from collections import defaultdict, namedtuple

import utils

Link = namedtuple('Link', ['start', 'end', 'weight'])


def build_graph(links: list[Link]) -> tuple:
    graph: dict = defaultdict(lambda: defaultdict(lambda: float('inf')))
    vertices = set()
    for link in links:
        graph[link.start][link.end] = int(link.weight)
        graph[link.end]

        vertices.add(link.start)
        vertices.add(link.end)

    return graph, vertices


def parse_lines(lines: list[str]) -> list[Link]:
    links = []
    for line in lines:
        nodes, weight = line.split(" = ")
        start, end = nodes.split(" to ")
        links.append(Link(start, end, weight))

    return links


def find_shortest_path_for_node(
    curr_node: str, graph: dict, nodes_to_visit: set
) -> float:
    if len(nodes_to_visit) == 0:
        return 0

    weights = [float('inf')]
    for next_node in nodes_to_visit:
        weights.append(
            graph[curr_node][next_node]
            + find_shortest_path_for_node(
                next_node, graph, nodes_to_visit - {next_node}
            )
        )

    return min(weights)


def find_shortest_path_in_graph(graph: dict, vertices: set) -> float:
    weights = [float('inf')]
    for node in graph.keys():
        weights.append(
            find_shortest_path_for_node(node, graph, vertices - {node})
        )  # noqa

    return min(weights)


def main(filename) -> float:
    file_lines = utils.import_file(filename)
    links = parse_lines(file_lines)
    graph, vertices = build_graph(links)

    return find_shortest_path_in_graph(graph, vertices)


print(main("input_missing_edges"))

print(main("input"))
