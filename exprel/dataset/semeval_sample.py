import networkx as nx
from bs4 import BeautifulSoup
from exprel.dataset.sample import Sample
from stanza.models.common.doc import Document


class SemevalSample(Sample):
    def __init__(self, sen_id, sentence, label, nlp, docs):
        super().__init__()
        self.sen_id = int(sen_id)
        self.e1 = None
        self.e2 = None
        self.e1_lemma = None
        self.e2_lemma = None
        self.prepare_sentence(sentence)
        self.label = label
        self.nlp = nlp
        self.graph = None
        self.docs = docs
        self._doc = None
        self.prepare_doc()

    @property
    def sentence(self):
        return self._sentence

    @sentence.setter
    def sentence(self, sen):
        self.prepare_sentence(sen)

    def prepare_sentence(self, sen):
        soup = BeautifulSoup(sen)
        self._sentence = soup.text.strip('"')
        self.e1 = soup.e1.text.split()[-1]
        self.e2 = soup.e2.text.split()[-1]

    def _postprocess(self, graph):
        for node, attr in graph.nodes(data=True):
            if self.e1_lemma:
                if (
                    attr["name"] == self.e1_lemma
                    or attr["name"] == self.e1_lemma.split()[-1]
                ):
                    attr["name"] = "entity1"
            else:
                if attr["name"] == self.e1 or attr["name"] == self.e1.split()[-1]:
                    attr["name"] = "entity1"
            if self.e2_lemma:
                if (
                    attr["name"] == self.e2_lemma
                    or attr["name"] == self.e2_lemma.split()[-1]
                ):
                    attr["name"] = "entity2"
            else:
                if attr["name"] == self.e2 or attr["name"] == self.e2.split()[-1]:
                    attr["name"] = "entity2"

        return graph

    def set_graph(self, graph):
        self.graph = self._postprocess(graph)

    def prepare_doc(self):
        doc = self.nlp(self._sentence)
        self._doc = doc

        for token in self._doc.sentences[0].words:
            if token.text == self.e1:
                self.e1_lemma = token.lemma
            if token.text == self.e2:
                self.e2_lemma = token.lemma
