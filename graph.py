class Graph(object):
    def __init__(self):
        self.edge_properties = {} #ví dụ {(u,v) : 12}
        self.node_neighbors = {}  #ví dụ {u : [v,w]}

    def has_edge(self, edge):     #Kiểm tra xem có cạnh chưa
        u,v = edge
        return (u,v) in self.edge_properties and (v,u) in self.edge_properties

    def edge_weight(self, edge):  #lấy thuộc tính của 1 cạnh
        return self.get_edge_properties(edge)

    def neighbors(self, node):    #lấy lân cận của node
        return self.node_neighbors[node]

    def has_node(self,node):      #kiểm tra xem có node chưa
        #print(node)
        return node in self.node_neighbors

    def add_edge(self, edge, weight = 1): #Thêm 1 cạnh
        u, v = edge
        if u != v and u not in self.node_neighbors[v] and v not in self.node_neighbors[u]:
            self.node_neighbors[u].append(v)
            self.node_neighbors[v].append(u)
            self.set_edge_properties((u,v), weight = weight)
            self.set_edge_properties((v,u), weight = weight)
        else:
            raise ValueError("Edge (%s, %s) already in graph" % (u, v))

    def add_node(self, node):     #Thêm node
        if len(self.node_neighbors) == 0:
            self.node_neighbors[node] = []
        elif node not in self.node_neighbors:
            self.node_neighbors[node] = []
        else:
            raise ValueError("Edge %s already in graph" % node)

    def get_edge_properties(self, edge):
        return self.edge_properties[edge]

    def set_edge_properties(self, edge, weight = 1):
        self.edge_properties[edge] = weight 

    def nodes(self):
        return self.node_neighbors

    def del_node(self, node):
        del(self.node_neighbors[node])

    def validate_graph(self):
        dictNode = self.node_neighbors.copy()
        for node in dictNode:
            if len(self.node_neighbors[node]) == 0:
                self.del_node(node)