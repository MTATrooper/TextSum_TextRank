from graph import Graph
from nltk.cluster.util import cosine_distance

THRESHOLD = 0.0001

def init_graph(list_Sentences_Index):   #Xây dựng đồ thị với mỗi node là chỉ số của các câu ban đầu
    g = Graph()
    for item in list_Sentences_Index:
        if len(g.nodes()) == 0:
            g.add_node(item)
        else:
            if not g.has_node(item):
                g.add_node(item)
    return g

def similar_sent(s1, s2):               #Tính độ tương tự giữa 2 câu theo khoảng cách cosine
    return 1 - cosine_distance(s1, s2)

def set_edge_weight(graph, list_Sentences_Vecto): #Tạo cách cạnh của đồ thị dựa trên sự tương đồng các câu
    for i in graph.nodes():
        for j in graph.nodes():
            edge = (i, j)
            weight = similar_sent(list_Sentences_Vecto[i], list_Sentences_Vecto[j])
            if (i != j and not graph.has_edge(edge) and weight != 0.0):
                graph.add_edge(edge, weight)
    
def textrank_weight(graph, d = 0.85):   #xây dựng rank cho các node
    scores = dict.fromkeys(graph.nodes(), 1)
    while True:
        count = 0
        for i in graph.nodes():
            rank = 1 - d
            
            for j in graph.neighbors(i):
                neighbor_sum = sum([graph.edge_weight((j,k)) for k in graph.neighbors(j)])
                rank += d * scores[j] * graph.edge_weight((i,j)) / neighbor_sum
            if abs(scores[i] - rank) <= THRESHOLD:  #Kiểm tra điều kiện thỏa mãn rank
                count += 1
            scores[i] = rank
        if count == len(graph.nodes()):
            return scores
    return scores

