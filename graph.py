from collections import defaultdict

# inspired by https://gist.github.com/econchick/4666413
class Graph:
    ''' Used by Car to analyze the road network and perform Dijkstra's algo '''
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def node_exists(self, value):
        return value in self.nodes

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.distances[(from_node, to_node)] = distance

    def dijkstra(graph, initial):
        ''' Perform dijkstra's algorithm, finding the shortest path to all
            nodes from the initial '''
        visited = {initial: 0}
        path = {}

        # while there are still nodes to examine in the graph
        while graph.nodes:
            min_node = None
            for node in graph.nodes:
                # get the node with minimum distance
                if node in visited:
                    if min_node is None:
                        min_node = node
                    elif visited[node] < visited[min_node]:
                        min_node = node

            if min_node is None:
                break

            graph.nodes.remove(min_node)
            current_weight = visited[min_node]

            for edge in graph.edges[min_node]:
                weight = current_weight + graph.distances[(min_node, edge)]
                if edge not in visited or weight < visited[edge]:
                    visited[edge] = weight
                    path[edge] = min_node

        # the returned path has the form {next: parent} where parent
        # is the node visited immediately prior to 'next'
        return path

    def get_path(graph, initial, destination):
        ''' Using the result of dijkstra, use the returned paths to determine
            the most efficient path to the destination '''

        # Get shortest path to all nodes.
        all_paths = graph.dijkstra(initial)

        # Select path to the destination.
        path = [destination]

        while destination != initial:
            # Change the 'destination' to the intersection just before
            # the last destination.
            destination = all_paths[destination]
            path = [destination] + path

        return path


