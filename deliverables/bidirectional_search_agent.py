from queue import Queue


class AdjacencyList:

    def __init__(self):
        self.adj_list = {}
        self.edge_weights = {}

    def add_edge(self, u, v, dist):
        # Creating adj list
        if u not in self.adj_list.keys():
            self.adj_list[u] = list()
        if v not in self.adj_list.keys():
            self.adj_list[v] = list()

        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

        # Creating edge weights dictionary
        if (u + "" + v) not in self.edge_weights.keys() or (v + "" + u) not in self.edge_weights.keys():
            self.edge_weights[u + "" + v] = dist

        # Sorting adjacency lists in order of edge weights
        self.adj_list[u].sort(key=lambda x: self.edge_weights[u + "" + x] if u + "" + x in self.edge_weights else self.edge_weights[x + "" + u])
        self.adj_list[v].sort(key=lambda x: self.edge_weights[v + "" + x] if v + "" + x in self.edge_weights else self.edge_weights[x + "" + v])


class BFS:

    def __init__(self, adjacency_list):
        self.adj_list = adjacency_list
        self.visited_sources = []
        self.visited_destinations = []

    def search(self, direction, elem, visited, queue, parent, level):
        for node in self.adj_list[elem]:
            if not visited[node]:
                self.visited_sources.append(node) if direction == 'forward' else self.visited_destinations.append(node)
                queue.put(node)
                visited[node] = True
                parent[node] = elem
                level[node] = level[elem] + 1

    def check_intersecting_node(self, visited_src, visited_dest):
        print(f"Visited vertices from source dictionary - {visited_src}")
        print(f"Visited vertices from dest dictionary - {visited_dest}")

        # Catching the first intersecting node instead to try to get an optimal path
        for node in self.visited_sources:
            if node in self.visited_destinations:
                # print("intersection", node)
                return node
        return -1
        #
        # for key, value in self.adj_list.items():
        #     if key == "B":
        #         pass
        #     if visited_src[key] and visited_dest[key]:
        #         return key
        # return -1


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

    def search_strategy(self, start, dest):
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

            self.intersecting = self.bfs.check_intersecting_node(self.visited_src, self.visited_dest)
            if self.intersecting != -1:
                self.bfs_traversal_output_backward.reverse()
                break
                
        print(f"BFS forward output is {self.bfs_traversal_output_forward}")
        print(f"BFS backward output is {self.bfs_traversal_output_backward}")
        print(f"Intersecting node is {self.intersecting}")

    def get_path_and_cost(self, edge_weights, start, dest):
        if self.intersecting in self.bfs_traversal_output_forward or \
                self.intersecting in self.bfs_traversal_output_backward:
            path = self.bfs_traversal_output_forward + self.bfs_traversal_output_backward
        else:
            path = self.bfs_traversal_output_forward + [self.intersecting] + self.bfs_traversal_output_backward
        print(f"Path from {start} to {dest} is {path}")
        cost = 0
        for i in range(len(path) - 1):
            for key, value in edge_weights.items():
                if (key == path[i] + "" + path[i + 1]) or (key == path[i + 1] + "" + path[i]):
                    cost = cost + value
        print(f"Cost to go from {start} to {dest} is {cost}")


def main():
    """
    Entry point of our execution. This given will create the given graph, take inputs from the user for source and
    destination nodes and prints the path, cost and visited vertices traversed while looking for the path
    :return: None
    """

    """ Creating the graph given in the problem """
    adj_list = AdjacencyList()
    adj_list.add_edge("A", "B", 110)
    adj_list.add_edge("B", "D", 159)
    adj_list.add_edge("D", "F", 98)
    adj_list.add_edge("F", "E", 68)
    adj_list.add_edge("E", "C", 89)
    adj_list.add_edge("A", "C", 132)
    adj_list.add_edge("B", "G", 59)
    adj_list.add_edge("D", "G", 108)
    adj_list.add_edge("F", "G", 92)
    adj_list.add_edge("E", "G", 102)
    adj_list.add_edge("C", "G", 120)

    """ Taking input from the user """
    valid_nodes = ["A", "B", "C", "D", "E", "F", "G"]
    source_node = input(f"Please enter your source location/city?: ")
    if source_node not in valid_nodes:
        print(f"'{source_node}' is not available as source city. You can only choose from - {str(valid_nodes)}")
        return
    
    valid_nodes.remove(source_node)
    
    destination_node = input(f"Please enter your dream destination location/city?: ")
    if destination_node not in valid_nodes:
        print(f"'{destination_node}' is not available as destination city. You can only choose from - {str(valid_nodes)}")
        return

    """ Listing visited vertices, path and cost using Bidirectional search """
    bidirectional_search = BidirectionalSearch(adj_list.adj_list)
    bidirectional_search.search_strategy(source_node, destination_node)
    bidirectional_search.get_path_and_cost(adj_list.edge_weights, source_node, destination_node)


if __name__ == "__main__":
    main()
