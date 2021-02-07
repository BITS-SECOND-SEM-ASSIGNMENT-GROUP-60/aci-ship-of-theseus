"""
This module includes all the classed and methods for building an AI search agent using bidirectional search
to find the optimal cost from user given source and destination city
"""

from queue import Queue


class AdjacencyList:

    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_edge(self, u, v, dist):
        # Creating adjacency list
        if u not in self.adjacency_list.keys():
            self.adjacency_list[u] = list()
        if v not in self.adjacency_list.keys():
            self.adjacency_list[v] = list()

        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)

        self.adjacency_list[u].sort()
        self.adjacency_list[v].sort()

        # Creating edge weights dictionary
        if (u + "" + v) not in self.edge_weights.keys() or (v + "" + u) not in self.edge_weights.keys():
            self.edge_weights[u + "" + v] = dist


class BFS:

    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    def search(self, direction, elem, visited, queue, parent, level):
        for node in self.adjacency_list[elem]:
            if not visited[node]:
                queue.put(node)
                visited[node] = True
                parent[node] = elem
                level[node] = level[elem] + 1

    def check_intersecting_node(self, visited_src, visited_dest):
        bfs_traversal_intersection = []
        for key, value in self.adjacency_list.items():
            if visited_src[key] and visited_dest[key]:
                bfs_traversal_intersection.append(key)
        return bfs_traversal_intersection


# Bidirectional Search
class BidirectionalSearch:

    def __init__(self, adjacency_list):
        self.visited_src = {}
        self.visited_dest = {}

        self.level_src = {}
        self.level_dest = {}

        self.parent_src = {}
        self.parent_dest = {}

        self.bfs_traversal_output_forward = []
        self.bfs_traversal_output_backward = []

        self.bfs_traversal_intersection_path_cost = []
        self.path_list = {}

        self.forward_queue = Queue()
        self.backward_queue = Queue()

        self.bfs = BFS(adjacency_list)

        self.intersecting = None

        # initializing dictionaries
        for node in adjacency_list.keys():
            self.visited_src[node] = False
            self.visited_dest[node] = False
            self.parent_src[node] = None
            self.parent_dest[node] = None
            self.level_src[node] = -1  # inf
            self.level_dest[node] = -1  # inf

    def search_strategy(self, start_vertex, dest_vertex):
        self.visited_src[start_vertex] = True
        self.level_src[start_vertex] = 0
        self.forward_queue.put(start_vertex)

        self.visited_dest[dest_vertex] = True
        self.level_dest[dest_vertex] = 0
        self.backward_queue.put(dest_vertex)

        while not self.forward_queue.empty() and not self.backward_queue.empty():
            elem = self.forward_queue.get()
            self.bfs_traversal_output_forward.append(elem)
            self.bfs.search("forward", elem, self.visited_src, self.forward_queue, self.parent_src, self.level_src)

            last_elem = self.backward_queue.get()
            self.bfs_traversal_output_backward.append(last_elem)
            self.bfs.search("backward", last_elem, self.visited_dest, self.backward_queue, self.parent_dest,
                            self.level_dest)

            print(f"Current level - {self.level_src}")
            print(f"Visited vertices from source dictionary - {self.visited_src}")
            print(f"Visited vertices from dest dictionary - {self.visited_dest}")

            self.bfs_traversal_intersection_path_cost = self.bfs.check_intersecting_node(self.visited_src,
                                                                                         self.visited_dest)
            if self.bfs_traversal_intersection_path_cost:
                self.bfs_traversal_output_backward.reverse()
                break

        print(f"Intersecting nodelist is {self.bfs_traversal_intersection_path_cost}")

    def get_path_and_cost(self, edge_weights, start, dest):
        ctr = -1
        min_cost = 0
        for i in self.bfs_traversal_intersection_path_cost:
            self.intersecting = i
            if self.intersecting in self.bfs_traversal_output_forward or self.intersecting in self.bfs_traversal_output_backward:
                path = self.bfs_traversal_output_forward + self.bfs_traversal_output_backward
            else:
                path = self.bfs_traversal_output_forward + [self.intersecting] + self.bfs_traversal_output_backward
            self.path_list[++ctr] = path
            # print(f"Path from {start} to {dest} is {path}")
            cost = 0
            for i in range(len(path) - 1):
                for key, value in edge_weights.items():
                    if (key == path[i] + "" + path[i + 1]) or (key == path[i + 1] + "" + path[i]):
                        cost = cost + value
            if min_cost == 0:
                min_cost = cost
                min_path = self.path_list[ctr]
            if min_cost != 0 and min_cost > cost:
                min_cost = cost
                min_path = self.path_list[ctr]

        print(f"Optimal Path from {start} to {dest} is {min_path}")
        print(f"Cost to go from {start} to {dest} is {min_cost}")


class BidirectionalSearch_new:

    def __init__(self, adjacency_list):
        self.visited_src = {}
        self.visited_dest = {}

        self.level_src = {}
        self.level_dest = {}

        self.parent_src = {}
        self.parent_dest = {}

        self.bfs_traversal_output_forward = []
        self.bfs_traversal_output_backward = []

        self.bfs_traversal_intersection_path_cost = []
        self.path_list = {}

        self.forward_queue = Queue()
        self.backward_queue = Queue()

        self.bfs = BFS(adjacency_list)

        self.intersecting = None

        # initializing dictionaries
        for node in adjacency_list.keys():
            self.visited_src[node] = False
            self.visited_dest[node] = False
            self.parent_src[node] = None
            self.parent_dest[node] = None
            self.level_src[node] = -1  # inf
            self.level_dest[node] = -1  # inf

        # print(visited),print(parent),print(level)

    def cover_all_nodes(self, edge_weights, start, dest):
        start_vertex = start
        self.visited_src[start_vertex] = True
        self.level_src[start_vertex] = 0
        self.forward_queue.put(start_vertex)

        dest_vertex = dest
        self.visited_dest[dest_vertex] = True
        self.level_dest[dest_vertex] = 0
        self.backward_queue.put(dest_vertex)

        while not self.forward_queue.empty() and not self.backward_queue.empty():
            elem = self.forward_queue.get()
            self.bfs_traversal_output_forward.append(elem)
            self.bfs.search("forward", elem, self.visited_src, self.forward_queue, self.parent_src, self.level_src)

            last_elem = self.backward_queue.get()
            self.bfs_traversal_output_backward.append(last_elem)
            self.bfs.search("backward", last_elem, self.visited_dest, self.backward_queue, self.parent_dest,
                            self.level_dest)

        print(f"Current levels for source - {self.level_src}")
        print(f"Current levels for destination - {self.level_dest}")


# insert code to check if level_src and level_dest have have keys/edges at lvel 2--this is itersection point
# if no--> return no path covering all points exists
# if yes then find path, using the parent with the intersection point in centre (source to int point+intpont to dest)


def main():
    """
    Entry point of our execution. This given will create the given graph, take inputs from the user for source and
    destination nodes and prints the path, cost and visited vertices traversed while looking for the path
    :return: None
    """

    """ Creating the graph given in the problem """
    adjacency_list = AdjacencyList()
    adjacency_list.add_edge("A", "B", 110)
    adjacency_list.add_edge("B", "D", 159)
    adjacency_list.add_edge("D", "F", 98)
    adjacency_list.add_edge("F", "E", 68)
    adjacency_list.add_edge("E", "C", 89)
    adjacency_list.add_edge("A", "C", 132)
    adjacency_list.add_edge("B", "G", 59)
    adjacency_list.add_edge("D", "G", 108)
    adjacency_list.add_edge("F", "G", 92)
    adjacency_list.add_edge("E", "G", 102)
    adjacency_list.add_edge("C", "G", 120)

    """ Taking input from the user """
    valid_nodes = ["A", "B", "C", "D", "E", "F", "G"]
    source_node = input(f"Please enter your source location/city?: ")
    if source_node not in valid_nodes:
        print(f"'{source_node}' is not available as source city. You can only choose from - {str(valid_nodes)}")
        return

    valid_nodes.remove(source_node)

    destination_node = input(f"Please enter your dream destination location/city?: ")
    if destination_node not in valid_nodes:
        print(
            f"'{destination_node}' is not available as destination city. You can only choose from - {str(valid_nodes)}")
        return

    """ Listing visited vertices, path and cost using Bidirectional search """
    bidirectional_search = BidirectionalSearch(adjacency_list.adjacency_list)
    bidirectional_search.search_strategy(source_node, destination_node)
    bidirectional_search.get_path_and_cost(adjacency_list.edge_weights, source_node, destination_node)
    bidirectional_search_new = BidirectionalSearch_new(adjacency_list.adjacency_list)
    bidirectional_search_new.cover_all_nodes(adjacency_list.edge_weights, source_node, destination_node)


if __name__ == "__main__":
    main()
