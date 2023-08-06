import tensorflow as tf
import random
from tqdm import tqdm


from WordEmbed.correlation import spearman_cor


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
        self.dot = z = tf.keras.layers.Dot((1, 2))

    @tf.function
    def call(self, inputs):
        i1 = inputs[0]
        i2 = inputs[1]
        x = self.target_embed(i1)
        y = self.context_embed(i2)
        x = tf.squeeze(x, axis=[1])
        z = self.dot([x, y])
        out = tf.keras.activations.softmax(z)
        return out




class Skipgram():
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

    def data_sampling(self, sequences, n_sampl, win):
        lab, tar, con = [], [], []
        print('\nSampling the data..\n')
        for seq in tqdm(sequences):
            if len(seq) > (win + n_sampl + 1):
                tar.append(seq[0])
                con.append([random.choice(seq[1:1 + win])] + random.sample(seq[win + 2:], n_sampl))
                lab.append([1] + [0] * n_sampl)
                tar.append(seq[-1])
                con.append([random.choice(seq[-(win + 1):-1])] + random.sample(seq[:-(win + 1)], n_sampl))
                lab.append([1] + [0] * n_sampl)
                for i in range(1, len(seq) - 1):
                    st = max(0, i - win)
                    ed = min(len(seq) - 1, i + win + 1)
                    c = seq[st:i] + seq[i + 1:ed]
                    ns = seq[:st] + seq[ed:]
                    if len(ns) > (n_sampl - 1):
                        con_ar = [random.choice(c)] + random.sample(ns, n_sampl)
                        tar.append(seq[i])
                        con.append(con_ar)
                        lab.append([1] + [0] * n_sampl)
        return tar, con, lab

    def train(self):
        # Process the data
        data = self.process_data(self.data)

        # Define the model
        self.model = Model(self.vocab_size, self.embedding_dim, self.negative_samples)

        # Get the data for training
        target, context, label = self.data_sampling(data, self.negative_samples, self.sampling_window)
        trn = tf.data.Dataset.from_tensor_slices(((target, context), label))
        trn = trn.batch(128).shuffle(buffer_size=20000).prefetch(buffer_size=tf.data.AUTOTUNE)

        # Train the model
        self.model.compile(optimizer='adam', loss="categorical_crossentropy", metrics=['accuracy'])
        self.model.fit(trn, epochs=1)

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

"""#Test the class"""

# Loading shakespear data for our analysis
path_to_file = tf.keras.utils.get_file('shakespeare.txt',
                                       'https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')

with open(path_to_file) as f:
    data = f.read().splitlines()

w2v = Skipgram(data, 512)

w2v.train()

print(w2v.score)

l = w2v.TfAPI

'''

