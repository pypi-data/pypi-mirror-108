from WordEmbed.skipgram import Skipgram
from WordEmbed.cbow import CBOW
from WordEmbed.glove import Glove


def Embed(
        data,
        embedding_dim,
        embedding='glove',
        sampling_window=2,
        negative_samples=4,
        Trainable=True ):

    emb={'glove':Glove,'skipgram':Skipgram,'cbow':CBOW}
    if embedding not in emb.keys():
        raise Exception('embedding type is not from listed options')
    if sampling_window<1 and sampling_window>10:
        raise Exception('Sampling window is not in expected range')
    if negative_samples<2 and negative_samples>15:
        raise Exception('Negative samples are not in range')

    if embedding=='glove':
        return emb[embedding](data,embedding_dim,sampling_window,Trainable)
    if embedding=='skipgram':
        return emb[embedding](data,embedding_dim,sampling_window,negative_samples,Trainable)
    if embedding== 'cbow':
        return emb[embedding](data,embedding_dim,sampling_window,trainable)



