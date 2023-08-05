import nltk
import codecs
import string
import matplotlib.pyplot as plt


class Work:

    def __init__(self, name, particle, quantity):
        self.quantity = quantity
        self.particle = particle
        self.name = name
        try:
            self.doc = codecs.open(self.name, 'r', 'utf-8').read()
        except:
            self.doc = codecs.open(self.name, 'r', 'cp1251').read()

    def sentences_word_length(self):
        sentences = nltk.sent_tokenize(self.doc)
        sentences_word_length = [len(sent.split()) for sent in sentences]
        return sentences_word_length

    @staticmethod
    def text_sentences_length(sentences_word_length):
        average_sentences_word_length = (sum(sentences_word_length) / len(sentences_word_length))
        return average_sentences_word_length

    def tokenize(self):
        word = nltk.word_tokenize(self.doc)
        remove_punctuation = str.maketrans('', '', string.punctuation)
        tokens_ = [x for x in [t.translate(remove_punctuation).lower() for t in word] if len(x) > 0]
        return tokens_

    @staticmethod
    def words_length(tokens_):
        words = set(tokens_)
        word_chars = [len(word) for word in words]
        return word_chars

    @staticmethod
    def text_lexical(tokens_):
        lexical_diversity = (len(set(tokens_)) / len(tokens_)) * 100
        return lexical_diversity

    @staticmethod
    def word_mean_length(word_chars):
        mean_word_len = sum(word_chars) / float(len(word_chars))
        return mean_word_len

    def commas_in_text(self):
        tokens = nltk.word_tokenize(self.doc)
        dist = nltk.probability.FreqDist(nltk.Text(tokens))
        commas_per_quantity = (dist[self.particle] * self.quantity) / dist.N()
        return commas_per_quantity

    @staticmethod
    def visual_thinks(sentences_word_length):
        x_list = list(range(0, len(sentences_word_length)))
        y1_list = list(sentences_word_length)
        plt.plot(x_list, y1_list)
        plt.ylabel("Длина предложений", fontsize=14, fontweight="bold")
        plt.show()
