import typing

class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
    

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.

        Outputs:
        -----------
        None
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1
    

    def get_path_with_power(self, src, dest, power):
        """
        The aim of this function is to indicate if a traject can be travelled with
        a given power.
        More practically, given a power and a traject the function return None if the traject 
        can not be travelled and else return the path
        
        Parameters: 
        -----------
        src : NodeType
            First node of the traject
        dest : NodeType
            Last node of the traject
        power : numeric (int or float)
            Power to test
        """
        visited = set()
        stack = [(src, [], 0)]  #(node, path, total power)
        while stack:
            node, path, total_power = stack.pop()
            if node == dest and total_power <=power:
                return path + [dest]
            if node not in visited:
                visited.add(node)
                for neighbor, min_power, _ in self.graph[node]:
                    if min_power <= power and neighbor not in visited:
                        stack.append((neighbor, path + [node], max(min_power, total_power)))
        return None
    #complexité en O(V+E)


    def connected_components(self):
        visited = set()
        components = []
        for node in self.nodes:
            if node not in visited:
                component = []
                self._dfs(node, visited, component)
                components.append(component)
        return components

    def _dfs(self, node, visited, component):
        """
        Depth-first search implementation used by the connected_components method.
        As indicated in the guideline
        """
        visited.add(node)
        component.append(node)
        for neighbor, _, _ in self.graph[node]:
            if neighbor not in visited:
                self._dfs(neighbor, visited, component)


    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
    
    def min_power(self, src, dest):
        """
        This function should return path, min_power. 

        The aim of this function is to use binary research in order to return the minimum power
        to travel a traject.
        If the two nodes are not in the same connected components, the function return an error

        The complexity of this function is O(V+E).

        Parameters:
        -----------
        src : NodeType
            Source :A node of the graph
        dest : NodeType
            Destination : Another node of the graph
        
        Outputs:
        -----------
        path : list
            The path between src and dest that costs the minimum power
        power : int
            The minimum power required to travel the traject between src and dest
        """
        #Using binary research

        #Find min and max of edges' weight 
        _list_edges = [i[0] for i in g.graph.values() if len(i)>0]
        a = min([j[1] for j in _list_edges])
        b = max([j[1] for j in _list_edges])
        #From this point it is the real function
        while (b-a) >= 1:
            if self.get_path_with_power(src, dest, (a+b)/2) != None:
                b = (a+b)/2
            else : 
                a = (a+b)/2
        if self.get_path_with_power(src, dest, int(b)) != None:
            return self.get_path_with_power(src, dest, int(b)), int(b)    #assumed here that power is always an integer 
        raise ValueError("The two given nodes are not in the same connected component.")

    def view(self, node1 = None, node2 = None):
        """
        This function allow a visualisation of a graph

        Actually this function takes 2 nodes of the graph and display the entire graph with
        the shortest (meaning the least weight-costly) path between the two nodes in red.
        If the function does not recieve two nodes it will simply display the graph.
        The function automatically save the Graph in the file ../graph_viz_output

        Parameters:
        -----------
        node1 : NodeType
            A node of the graph
        node2 : NodeType
            Another node of the graph
        
        Outputs:
        -----------
        None
        """
        import graphviz
        dot = graphviz.Graph('Graph', comment='Graph visualisation', graph_attr = {"concentrate" : 'True'})
        verified_edge = [] #list of the already implemented edges

        #Initially, we create all the nodes
        for i in self.graph:
            dot.node('{}'.format(i))   

        cpt = 0

        if ((node1 != None) and (node2 != None)): #then we have to print the grap and the path
            path, _ = self.min_power(node1, node2)
            for i in self.graph:
                
                #we will colorize the path's nodes in red
                if i in path:
                    dot.node('{}'.format(i), color = 'red', fontcolor = 'red')
                    cpt = path.index(i)+1 # type: ignore
                    cpt = np.min([cpt, len(path)-1]) # type: ignore
                
                for j in self.graph[i]: #check all the i's neighbors
                    #now, we implement the edges
                    if ({i, j[0]} not in verified_edge) and (i in path) and (j[0] == path[cpt]): # type: ignore
                        #the following if is to avoid colorizing the edge between Node1 and Node2
                        #if the path is [Node1, ..., Node2]
                        if (i == path[0]) and (j[0]== path[-1]) and (len(path) != 2): # type: ignore
                            #implementing in BLACK the edge between path[0] and path[-1]
                            #avoiding the case where the path is [node1, node2]
                            dot.edge('{}'.format(i), '{}'.format(j[0]), weight = "{}".format(j[1]), label = "weight = {}\n length = {}".format(j[1], j[2]))
                            verified_edge.append({i, j[0]})
                        else:
                            #implementing in RED all the edges of the path
                            dot.edge('{}'.format(i), '{}'.format(j[0]), weight = "{}".format(j[1]), label = "weight = {}\n length = {}".format(j[1], j[2]), color = 'red')
                            verified_edge.append({i, j[0]})

            #implementing all the other edges of the graph
            for i in self.graph:
                for j in self.graph[i]:
                    if {i, j[0]} not in verified_edge:
                        dot.edge('{}'.format(i), '{}'.format(j[0]), weight = "{}".format(j[1]), label = "weight = {}\n length = {}".format(j[1], j[2]))
                        verified_edge.append({i, j[0]})

            dot.render(directory='graph_viz_output', view=True) #this is to print the graph


        else: #then we have to simply print the graph
            for i in self.graph:
                for j in self.graph[i]: 
                    if {i, j[0]} not in verified_edge:
                        dot.edge('{}'.format(i), '{}'.format(j[0]), weight = "{}".format(j[1]), label = "weight = {}\n length = {}".format(j[1], j[2]))
                        verified_edge.append({i, j[0]})
            dot.render(directory='graph_viz_output', view=True) #this is to print the graph



def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters:
    -----------
    filename: str
        The name of the file

    Outputs:
    -----------
    g: Graph
        An object of the class Graph with the graph from file_name.
    """
    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())
        g = Graph(range(1, n+1))
        for _ in range(m):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min) # will add dist=1 by default
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
    return g


def kruskal(g):
    """
    The aim of this function is to use the kruskal algorithm
    to find the minimum spanning tree of a given graph.
    
    Parameters:
    -----------
    g: Graph
        An object of the class Graph

    Outputs:
    -----------
    g_mst: Graph
        An object of the class Graph : the minimum spanning tree of g
    """
    #tri des arêtes par ordre croissant de poids
    set_edges = []
    for a in g.graph:
        for j in g.graph[a]:
            set_edges.append([a, j[0], j[1]])
    edges=sorted(set_edges,key=lambda x:x[2])
    #Initialisation of the Union Find Structure. 
    parent = list(g.nodes)
    
    def find(x):
        #print(x)
        if parent[x-1]==x:
            return x
        parent[x-1]=find(parent[x-1])
        return parent[x-1]

    def union(x,y):
        parent[find(x)-1]=find(y)
    
    #Minimum weight spanning tree construction
    g_mst=Graph(list(g.nodes))
    for u,v,w in edges:
        if find(u)!=find(v):
            g_mst.add_edge(u,v,w)
            union(u,v)
    return g_mst


def min_power_for_path(g, source, destination):
    """
    Reads a tree and a traject and return the minimal power to do this traject.
    The input graph has to be a minimum spanning tree.

    The complixity is in O(Nlog(N)) N is the number of edges

    Parameters:
    -----------
    g: Graph
        An object of the class Graph
    source: NodeType
        A node
    destination: NodeType
        The destination node

    Outputs:
    -----------
    min_power: int
        The minimal power required to travel the traject from source to destination
    """
    # verify that the given graph is a tree (a minimum spanning tree)
    """ assert g == kruskal(g), "Warning ! The graph given is not a minimum spanning tree" """
    #this lign is not working for now we will fix this in the futur

    # initialize the stack of nodes to visit
    stack = [1]

    # initialize parent dictionary and minimum power
    dico = dict([(i, [0,0]) for i in g.nodes]) #(parent, profondeur)
    dico[1] = [None, 0] # type: ignore

    verified = {1}
    # traverse the spanning tree from the source node (DFS)
    while stack:
        node = stack.pop()
        for neighbor, _, _ in g.graph[node]:
            if ((dico[neighbor][0] != node) and (dico[neighbor][0] != None) and (neighbor not in verified)):
                verified.add(neighbor)
                stack.append(neighbor)
                dico[neighbor] = [node, dico[node][1]+1]
                


    def find_path(src_, dest_):
        assert dico[src_][1] == dico[dest_][1]
        path = []
        curr1, curr2 = src_, dest_
        while 1 not in path:
            path.append(curr1)
            path.append(curr2)
            curr1, curr2 = dico[curr1][0], dico[curr2][0]
        return path

    if dico[source][1] == dico[destination][1]:
        path = find_path(source, destination)
    elif dico[source][1]>dico[destination][1]:
        path_ = []
        curr = source
        while dico[curr][1] != dico[destination][1]:
            path_.append(curr)
            curr = dico[curr][0]
        path = path_+find_path(curr, destination)
    else:
        path_ = []
        curr = destination
        while dico[curr][1] != dico[source][1]:
            path_.append(curr)
            curr = dico[curr][0]
        path = path_+find_path(source, curr)

    min_power = 0

    for i in range(len(path)-1):
        for j in g.graph[path[i]]:
            if j[0] in path:
                if j[1] > min_power:
                    min_power = j[1]
    
    return min_power


from typing import Any, List
def route_from_file(filename) -> List[List[int]]:
    """
    This function transform a text file in a list of road

    Parameters:
    -----------
    filename : txt file
        A text file with a list of road

    Outputs:
    -----------
    route : List[List[int]]
        A list of roads : city1 city2 utility
    """

    route = []
    with open(filename, "r") as file:
        n = list(map(int, file.readline().split()))[0]
        for _ in range(n):
            _tmp = list(map(int, file.readline().split()))
            route.append(_tmp)
    return route


def truck_from_file(filename) -> List[List[int]]:
    """
    This function transform a text file in a list of truck

    Parameters:
    -----------
    filename : txt file
        A text file with a list of trucks

    Outputs:
    -----------
    route : List[List[int]]
        A list of trucks : power cost
    """

    truck = []
    with open(filename, "r") as file:
        n = list(map(int, file.readline().split()))[0]
        for _ in range(n):
            _tmp = list(map(int, file.readline().split()))
            truck.append(_tmp)
    return truck


def assign_trucks_to_routes(graph, route_file, trucks_file):
    """
    This function assign a truck to a road in the optimal (heuristical) solution

    Parameters:
    -----------
    graph : a Graph
        A graph
    
    route_file : txt file
        A text file with a list of road

    trucks_file : txt file
        A text file with a list of trucks

    Outputs:
    -----------
    truck_assignments : List
        A list of tuples (truck (= power and cost), road)
    total_profit : Float
        A float which is the total of the profit
    """

    routes = route_from_file(route_file)
    trucks = truck_from_file(trucks_file)
    mst = kruskal(graph)

    min_powers = []
    for src, dest, profit in routes:
        min_power = min_power_for_path(mst, src, dest)
        min_powers.append((src, dest, profit, min_power))

    truck_assignments, total_profit = greedy_knapsack(trucks, min_powers)

    return truck_assignments, total_profit

def greedy_knapsack(trucks, min_powers):
    """
    This is the implementation of a greedy method in order to solve the knapsack problem
    (adapted to our subject)

    Parameters:
    -----------    
    trucks : list
        A list of trucks : power cost

    min_power : List[tuples]
        A list of tuples with 
        (city1, city2, profit, minimal power to travel the road)

    Outputs:
    -----------
    truck_assignments : List
        A list of tuples (truck (= power and cost), road)
    total_profit : Float
        A float which is the total of profit
    """
    
    sorted_min_powers = sorted(min_powers, key=lambda x: x[2] / x[3], reverse=True)
    sorted_trucks = sorted(trucks, key=lambda x: x[1], reverse=True)
    Bu = 25e9

    truck_assignments = []
    total_profit = 0

    for src, dest, profit, min_power in sorted_min_powers:
        for idx, truck in enumerate(sorted_trucks):
            if (truck[0] >= min_power) and (Bu - truck[1]>=0):
                Bu -= truck[1]
                truck_assignments.append((truck, (src, dest)))
                total_profit += profit
                sorted_trucks.pop(idx)
                break

    return truck_assignments, total_profit


#We will now build an exact method in order to find the exact optimum
# The name of the method is Branch&Bounds
import numpy as np

def bound(node, n, W, items):
    """
    This function compute for each node a bound for the further branch.
    This allows us to dramatically reduce the compute time

    Parameters:
    -----------
    node : NodeType
        A node of the graph
    
    n : int
        number of items
    
    W : int
        maximum weight

    items : list
        A list of items that we can put in the knapsack : 
        for each road we took the less costly truck that can travel the road
        An item is each time the utility and the cost

    Outputs:
    -----------
    profit_bound: Float
        the highest profit we can get
    """
    if node[1] > W:
        return 0

    # initialize profit bound to profit of current node
    profit_bound = node[2]

    # start from the next item index
    j = node[0] + 1

    # keep adding items until weight limit is reached or all items are added
    while j < n and node[1] + items[j][0] <= W:
        node = [j, node[1] + items[j][0], node[2] + items[j][1], node[3]]
        profit_bound += items[j][1]
        j += 1

    # if not all items are added, calculate the fractional profit of the next item
    if j < n:
        # calculate the remaining weight
        remaining_weight = W - node[1]
        # add the fraction of profit based on the remaining weight and the next item's value-to-weight ratio
        profit_bound += remaining_weight * items[j][1] / items[j][0]

    return profit_bound

def knapsack(budget, items):
    """
    This is an implementation of the branch and bounds algorithm in order to solve the 
    knapsack problem (adapted for our problem)

    Parameters:
    -----------
    budget : float
        the total budget
    
    items : list
        A list of items that we can put in the knapsack : 
        for each road we took the less costly truck that can travel the road
        An item is each time the utility and the cost

    Outputs:
    -----------
    max_profit: Float
        the highest profit we can get
    """

    n = len(items)
    items = sorted(items, key=lambda x: x[1] / x[0], reverse=True)
    queue = []
    #print(items)

    node = (-1, 0, 0, 0)
    queue.append(node)

    max_profit = 0

    while queue:
        node = queue.pop(0)
        node2 = [0, 0, 0, 0]

        if node[0] == -1:
            node2 = [0, 0, 0, 0]
            #v_level = 0
        elif node[0] == n-1:
            continue
        else:
            node2[0] = node[0] + 1

        
        node2 = [node2[0], node[1] + items[node2[0]][0], node[2] + items[node2[0]][1], 0]

        if node2[1] <= budget and node2[2] > max_profit:
            max_profit = node2[2]

        node2_bound = bound(node2, n, budget, items)

        if node2_bound > max_profit:
            node2 = [node2[0], node2[1], node2[2], node2_bound]
            queue.append(node2)

        node2 = (node[0] + 1, node[1], node[2], bound((node[0] + 1, node[1], node[2], 0), n, budget, items))
        if node2[3] > max_profit:
            queue.append(node2)

    return max_profit


def wrapper(graph: Graph, route_file, trucks_file):
    """
    This is a wrapp function, no need to explain
    """

    g = kruskal(graph)

    routes = route_from_file(route_file)
    trucks = truck_from_file(trucks_file)

    budget = 25*(10**9)
    summary_of_pb = []
    for road in routes:
        power_min = min_power_for_path(g, road[0], road[1])
        summary_of_pb.append([sorted([a for a in trucks if a[0] >= power_min], key=lambda x: x[1], reverse = False)[0][1], road[2]])
    
    n = len(summary_of_pb)
    #print(summary_of_pb)

    return knapsack(budget, summary_of_pb)




####################################################################################################################################################################################
##                   test (this section is to execute all the functions)
####################################################################################################################################################################################
g = graph_from_file("input/network.1.in")
route = route_from_file("input/routes.1.in")
truck = truck_from_file("input/trucks.0.in")
#g = kruskal(g)

#print(assign_trucks_to_routes(g, "input/routes.1_2.in", "input/trucks.0.in"))
#g = kruskal(g)
#assign_trucks_to_routes(g, )
#print(min_power_for_path(g, 5, 4))
#print(g.min_power(20, 19))
#print(wrapper(g, "input/routes.1_2.in", "input/trucks.0.in"))
g.view(1, 3)