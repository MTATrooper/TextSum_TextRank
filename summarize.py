import sys
from LoadDataFromFile import LoadDataFrom
from nltk.tokenize import sent_tokenize
from preprocessing import get_vec_from_doc, computeTFIDF,computeVec
from buildTextRank import init_graph, set_edge_weight, textrank_weight
from graph import Graph
from rouge import Rouge

def summary(text):
    sentences = sent_tokenize(text)
    lstVec = computeVec(text)
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
        results += sentences[i] + '\n'
    return results
if __name__ == "__main__":
    source_path = str(sys.argv[1])
    reference_path = str(sys.argv[2])
    text = LoadDataFrom(source_path)
    sentences = sent_tokenize(text)
    # lstVec = get_vec_from_doc(text)
    # lstVec = computeTFIDF(lstVec)
    lstVec = computeVec(text)
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
    reference = LoadDataFrom(reference_path)
    rouge = Rouge()
    evalua = rouge.get_scores(results, reference, avg=True)
    #print(evalua)
    print("============")
    print("ROUGE-1-R: %s" % evalua['rouge-1']['r'])
    print("ROUGE-1-P: %s" % evalua['rouge-1']['p'])
    print("ROUGE-1-F: %s" % evalua['rouge-1']['f'])
    print("============")
    print("ROUGE-2-R: %s" % evalua['rouge-2']['r'])
    print("ROUGE-2-P: %s" % evalua['rouge-2']['p'])
    print("ROUGE-2-F: %s" % evalua['rouge-2']['f'])
    print("============")
    print("ROUGE-L-R: %s" % evalua['rouge-l']['r'])
    print("ROUGE-L-P: %s" % evalua['rouge-l']['p'])
    print("ROUGE-L-F: %s" % evalua['rouge-l']['f'])