
from collections import defaultdict
import tensorflow as tf
import numpy as np
from time import time
from tqdm import tqdm


from WordEmbed.correlation import spearman_cor


# Building model

# Building layer

class Embed(tf.keras.layers.Layer):
    '''
    Define Embedding layer derived from keras layer. This layer will map words to ord embedding
    '''

    def __init__(self, vocab, units, name=None):
        super(Embed, self).__init__(name=name)
        self.units = units
        self.vocab = vocab

    def build(self, input_shape):
        w_init = tf.random_normal_initializer(seed=22)
        self.w = tf.Variable(initial_value=w_init(shape=[self.vocab, self.units], dtype=tf.float32),
                             trainable=True, name='kernel')

    def call(self, input):
        x = tf.one_hot(input, depth=self.vocab)
        return tf.matmul(x, self.w)


# Buiding Bias
class Bias(tf.keras.layers.Layer):
    '''
    Define Bias layer to train embeddings
    '''


    def __init__(self, vocab):
        super(Bias, self).__init__()
        self.vocab = vocab

    def build(self, input_shape):
        w_init = tf.random_normal_initializer(seed=20)
        self.w = tf.Variable(initial_value=w_init(shape=[self.vocab, 1], dtype=tf.float32),
                             trainable=True, name='kernel1')

    def call(self, input):
        x = tf.one_hot(input, depth=self.vocab)
        return tf.matmul(x, self.w)


# Define Model

class Model(tf.keras.Model):
    def __init__(self, vocab, embed_dim, Embed, Bias):
        super(Model, self).__init__()
        self.emb1 = Embed(vocab, embed_dim, name='embed')
        self.emb2 = Embed(vocab, embed_dim)
        self.b1 = Bias(vocab)
        self.b2 = Bias(vocab)
        self.dot = tf.keras.layers.Dot((1, 1))
        self.a = tf.keras.layers.Add()

    def call(self, inputs):
        i1 = inputs[0]
        i2 = inputs[1]
        o1 = self.emb1(i1)
        o2 = self.b1(i1)
        o3 = self.emb2(i2)
        o4 = self.b2(i2)
        o1 = self.dot([o1, o3])
        o = self.a([o1, o2, o4])
        return o


def train(model, d):
    opt = tf.keras.optimizers.Adam()
    x1, x2, y = d

    def data_gen(x1, x2, y):
        n = len(x1)
        for i in range(0, n, 1024):
            e = i + 1024
            if e < n:
                yield [x1[i:e], x2[i:e]], y[i:e]
            else:
                yield [x1[i:], x2[i:]], y[i:]

    # loss function
    @tf.function
    def loss_fn(a, y):
        a = tf.squeeze(a, axis=-1)
        # a=tf.cast(a,tf.float64)
        y = tf.convert_to_tensor(y)
        y = tf.cast(y, tf.float32)
        iszero = y <= 1.0
        f = tf.where(iszero, 0.25, 1.0)
        # f=tf.cast(f,tf.float64)
        # y=tf.cast(y,tf.float64)
        l = tf.math.square((a - tf.math.log(y + 0.1)))
        l = tf.multiply(f, l)
        loss = tf.reduce_sum(l)
        return loss

    @tf.function
    def train_step(input, y):
        with tf.GradientTape() as t:
            out = model(input)
            loss = loss_fn(out, y)
        var = model.trainable_variables
        grads = t.gradient(loss, var)
        opt.apply_gradients(zip(grads, var))
        return loss

    epochs = 20
    print('\nTraining starts...\n')
    for j in tqdm(range(epochs)):
        #print('\n\nEpochs : {}'.format(j + 1))
        t = time()
        l = 0
        i = 0
        l_ = []
        for inp, y1 in data_gen(x1, x2, y):
            ls = train_step(inp, y1)
            l = l + ls
            # print(ls)
            i = i + 1
        l = l / i
        #print('Loss: {}\nTime: {}'.format(l, time() - t))
        l_.append(l)




class Glove():
    def __init__(self,
                 data,
                 embedding_dim=None,
                 window=2,
                 trainable=True,
                 ):
        self.window = window
        self.trainable = trainable
        self.model = None
        self.data = data
        self.vocab_size = None
        self.embedding_dim = embedding_dim
        self.embeddings = {}
        self.tokenizer = None
        self.score = None
        self.TfAPI = None

    def process_data(self, data):

        # Tokenize the data
        tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=None,
                                                          oov_token='<oov>',
                                                          filters='!"#$%&()*+.,-/:;=?@[\]^_`{|}~ ')
        tokenizer.fit_on_texts(data)
        proc_data = tokenizer.texts_to_sequences(data)

        self.vocab_size = len(tokenizer.index_word) + 1
        self.tokenizer = tokenizer
        return proc_data

    # Defining matrix
    def build_mtrx(self, sentences, vocab, win):
        n = len(vocab) + 1
        mtrx = defaultdict(lambda: defaultdict(int))
        print('\ncreating matrix...\n')
        for i in tqdm(sentences):
            for j in range(len(i)):
                for d in range(1, win + 1):
                    if (j + d) < len(i):
                        w = 1 / d
                        x, y = sorted([i[j], i[j + d]])
                        mtrx[x][y] = mtrx[x][y] + w
        return mtrx

    def extr(self, dic):
        x = []
        y = []
        w = []
        for i in dic.keys():
            for j in dic[i].keys():
                x.append(i)
                y.append(j)
                w.append(dic[i][j])
        return np.array(x), np.array(y), np.array(w)

    def train(self):
        # Process the data
        data = self.process_data(self.data)

        # Build matrix
        vocab = self.tokenizer.word_index
        mtrx = self.build_mtrx(data, vocab, self.window)
        x1, x2, y = self.extr(mtrx)

        # Define the model
        self.model = Model(self.vocab_size, self.embedding_dim, Embed, Bias)

        # Train the model
        train(self.model, [x1, x2, y])

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
""" Test the class"""

# Loading shakespear data for our analysis
path_to_file = tf.keras.utils.get_file('shakespeare.txt',
                                       'https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')

with open(path_to_file) as f:
    data = f.read().splitlines()

emb = Glove(data, 512)

emb.train()

'''

