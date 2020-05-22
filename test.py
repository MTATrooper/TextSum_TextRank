from gensim.models import KeyedVectors 

w2v = KeyedVectors.load_word2vec_format("../Word2vec_Model/wiki.vi.model.bin", binary=True)
vocab = w2v.vocab
print(vocab['chỉ_đạo'])