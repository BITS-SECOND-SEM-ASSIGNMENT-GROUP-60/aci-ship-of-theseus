from queue import Queue


class AdjacencyList:

    def __init__(self):
        self.adj_list = {}
        self.edge_weights = {}

    def add_edge(self,u,v,dist):
        # Creating adj list
        if u not in self.adj_list.keys():
            self.adj_list[u] = list()
        if v not in self.adj_list.keys():
            self.adj_list[v] = list()

        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

        self.adj_list[u].sort()
        self.adj_list[v].sort()

        # Creating edge weights dictionary
        if (u+""+v) not in self.edge_weights.keys() or (v+""+u) not in self.edge_weights.keys():
            self.edge_weights[u+""+v] = dist

    def display(self):
        print(self.adj_list)
        print(self.edge_weights)


class Bfs:

    def __init__(self):
        pass

    def search(self,direction,elem,visited,queue,parent,level):
        for node in adj_list.adj_list[elem]:
            if not visited[node]:
                queue.put(node)
                visited[node] = True
                parent[node] = elem
                level[node] = level[elem] + 1
        # if direction.lower() == "backward":
        #     pass

    def check_intersecting_node(self,visited_src,visited_dest):
        print(f"Visited vertices from source dictionary - {visited_src}")
        print(f"Visited vertices from dest dictionary - {visited_dest}")
        for key,value in adj_list.adj_list.items():
            if key == "B" :
                pass
            if visited_src[key] and visited_dest[key]:
                return key

        return -1


# Bidirectional Search
class BidirectionalSearch:

    def __init__(self, adjlist):
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

        self.bfs = Bfs()

        self.intersecting = None

        # initializing dictionaries
        for node in adjlist.keys():
            self.visited_src[node] = False
            self.visited_dest[node] = False
            self.parent_src[node] = None
            self.parent_dest[node] = None
            self.level_src[node] = -1  # inf
            self.level_dest[node] = -1  # inf

        # print(visited),print(parent),print(level)
    def search_strategy(self,start,dest):
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
            self.bfs.search("forward",elem,self.visited_src,self.forward_queue,self.parent_src,self.level_src)

            lastelem = self.backward_queue.get()
            self.bfs_traversal_output_backward.append(lastelem)
            self.bfs.search("backward",lastelem,self.visited_dest,self.backward_queue,self.parent_dest,self.level_dest)

            self.intersecting = self.bfs.check_intersecting_node(self.visited_src,self.visited_dest)
            if self.intersecting != -1:
                self.bfs_traversal_output_backward.reverse()
                break
        print(f"BFS forward output is {self.bfs_traversal_output_forward}")
        print(f"BFS backward output is {self.bfs_traversal_output_backward}")
        print(f"Intersecting node is {self.intersecting}")

    def getPathAndCost(self,edge_weights,start,dest):
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
# adj_list.display()

source = "A"
destination = "G"

bidirsearch = BidirectionalSearch(adj_list.adj_list)
bidirsearch.search_strategy(source,destination)
bidirsearch.getPathAndCost(adj_list.edge_weights,source,destination)