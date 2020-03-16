import sys
from LoadDataFromFile import LoadDataFrom
from nltk.tokenize import sent_tokenize
from preprocessing import get_vec_from_doc
from buildTextRank import init_graph, set_edge_weight, textrank_weight
from graph import Graph
from rouge import Rouge

if __name__ == "__main__":
    path = str(sys.argv[1])
    text = LoadDataFrom(path)
    sentences = sent_tokenize(text)
    lstVec = get_vec_from_doc(text)
    graph = init_graph([i for i in range(len(lstVec))])
    set_edge_weight(graph, lstVec)
    graph.validate_graph()
    scores = textrank_weight(graph, d=0.85)
    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    ratio = 0.2
    summarization_length = int(len(sentences) * ratio)
    results = ""
    index = []
    for key,value in scores:
        index.append(key)
        summarization_length -= 1
        if(summarization_length == 0): break
    index.sort()
    for i in index:
        results += sentences[i] + ' '
    print (results)
    rouge = Rouge()
    evalua = rouge.get_scores(results, text)
    print(evalua)
