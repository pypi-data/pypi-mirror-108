import tensorflow as tf
import numpy as np
import random
from tqdm.notebook import tqdm
import tensorflow.keras.backend as K

from WordEmbed.correlation import spearman_cor


# create the model
class Model(tf.keras.Model):
    def __init__(self, vocab_size, embed_dim, neg_sample):
        super(Model, self).__init__()
        self.target_embed = tf.keras.layers.Embedding(vocab_size,
                                                      embed_dim,
                                                      input_length=1,
                                                      name='embed')
        self.context_embed = tf.keras.layers.Embedding(vocab_size,
                                                       embed_dim,
                                                       input_length=neg_sample)

        self.lambd = tf.keras.layers.Lambda(lambda x: K.mean(x, axis=1))
        self.dot = tf.keras.layers.Dot((1, 2))

    def call(self, inputs):
        t = inputs[0]
        c = inputs[1]
        x = self.context_embed(t)
        y = self.target_embed(c)
        x = self.lambd(x)
        z = self.dot([x, y])
        out = tf.keras.activations.softmax(z)
        return out


class CBOW():
    def __init__(self,
                 data,
                 embedding_dim=None,
                 sampling_window=2,
                 negative_samples=4,
                 trainable=True,
                 ):
        self.trainable = trainable
        self.model = None
        self.sampling_window = sampling_window
        self.negative_samples = negative_samples
        self.data = data
        self.vocab_size = None
        self.embedding_dim = embedding_dim
        self.embeddings = {}
        self.tokenizer = None
        self.score = None
        self.TfAPI = None

    def process_data(self, data):

        # To create training data minimum sentence length=window+neg_sample
        n = self.negative_samples + self.sampling_window
        data = [i for i in data if len(i.split()) >= n]

        # Tokenize the data
        tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=None,
                                                          oov_token='<oov>',
                                                          filters='!"#$%&()*+.,-/:;=?@[\]^_`{|}~ ')
        tokenizer.fit_on_texts(data)
        proc_data = tokenizer.texts_to_sequences(data)

        self.vocab_size = len(tokenizer.index_word) + 1
        self.tokenizer = tokenizer
        return proc_data

    def data_sampling(self, data, win, n):
        context = []
        label = []
        target = []
        print('\nSampling the data..\n')
        for a in tqdm(data):
            for i in range(len(a)):
                if len(a) > (win + n + 1):
                    if i == 0:
                        con = a[1:win + 1]
                        n_sample = a[win + 1:]
                        ns = random.sample(n_sample, n)
                        target.append([a[i]] + ns)
                        context.append(con)
                        label.append([1] + [0] * n)
                    elif i == len(a):
                        con = a[n - win - 1:-1]
                        n_samle = a[:len(a) - win - 1]
                        ns = random.sample(n_sample, n)
                        target.append([a[i]] + ns)
                        context.append(con)
                        label.append([1] + [0] * n)
                    else:
                        st = max(0, i - win)
                        ed = min(len(a), i + win + 1)
                        con = a[st:i] + a[i + 1:ed]
                        n_sample = a[:st] + a[ed:]
                        if len(n_sample) > (n - 1):
                            ns = random.sample(n_sample, n)
                            target.append([a[i]] + ns)
                            context.append(con)
                            label.append([1] + [0] * n)
                        elif len(a) > 6:
                            context.append([a[i - 1], a[i + 1]])
                            n_sample = a[:i - 1] + a[i + 2:]
                            ns = random.sample(n_sample, n)
                            target.append([a[i]] + ns)
                            label.append([1] + [0] * n)
        return context, target, label

    def train(self):
        # Process the data
        data = self.process_data(self.data)

        # Define the model
        self.model = Model(self.vocab_size, self.embedding_dim, self.negative_samples)

        # Get the data for training
        context, target, label = self.data_sampling(data, self.sampling_window, self.negative_samples)
        a = np.array([context, target, label], dtype=object)
        a3 = np.array([[a[0][i], a[1][i], a[2][i]] for i in range(len(a[0])) if len(a[0][i]) == self.negative_samples],
                      dtype=object)
        con = list(a3[:, 0])
        tar = list(a3[:, 1])
        lab = list(a3[:, 2])

        trn = tf.data.Dataset.from_tensor_slices(((con, tar), lab))
        trn = trn.batch(128).shuffle(buffer_size=20000).prefetch(buffer_size=tf.data.AUTOTUNE)

        # Train the model
        print('\nTraining starts ...')
        self.model.compile(optimizer='adam', loss="categorical_crossentropy", metrics=['accuracy'])
        self.model.fit(trn, epochs=10, verbose=1)

        # Save the embeddings
        weights = self.model.get_layer(name='embed').get_weights()[0]
        layer = self.model.get_layer(name='embed')
        vocab = self.tokenizer.index_word
        for i in range(1, len(weights)):
            self.embeddings[vocab[i]] = weights[i]

        # Calculating score/quality of embeddings
        self.score = spearman_cor(self.embeddings)

        # forming TF API
        if self.trainable == False:
            layer.trainable = False
        self.TfAPI = layer



'''
"""# Test the class"""

# Loading shakespear data for our analysis
path_to_file = tf.keras.utils.get_file('shakespeare.txt',
                                       'https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')

with open(path_to_file) as f:
    data = f.read().splitlines()

w2v = CBOW(data, 512)

w2v.train()

print(w2v.score)

print(w2v.TfAPI)

# w2v.embeddings

'''