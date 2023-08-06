# WordEmbed

## About 
This project allows you to train word embedding on your own data set. It incorporates embedding methods such as 'Glove','Skip-gram' or 'CBOW' and train word embeddings specific to dataset. Morever, this word embeddings can be used as tensorflow layer API too.  

If you want to build a NLP model, word embeddings are the building blocks for most of the NLP model. Current trend give us two option:  
1. Train word embedding along with your final NLP model from the scratch. It is generally used in small and simple models. In this case, as model stacks huge no of layers, vanishing gradients become significant and cause poor training of word embedding.  Example- Tensorflow's Embedding API   
2. Use pre-trained embedding, trained on different dataset. Most of the industrial and real world soltions use this option. It has minor drawback. i.e when our dataset contains words which aren't present in pre-trained embeddings, embedding quality degrades.  Example FastText,GloVe,Word2vec.  

This work addresses this issue by allowing us to train word embedding on specific data and then use this trained embedding as tensorflow layer API and train along with model.   

  
  
  



![](embedding.gif)  

 


## Installation  

LINUX:  
python -m pip install WordEmbed  

WINDOWS:  
py -m pip install WordEmbed  

## Usage  

class Embed(data,embidding_dim,embedding='glove',sampling_window=2, negative_samples=4,Trainable=True)  

Parameters:  

**data**= string, path to raw data file.  

**embedding_dim**= integer, Vector dimension e.g 512  

**embeding**=string,{'glove','skipgram','cbow'} embedding method to be used default to 'glove'  

**sampling_window**= integer, {1<sampling_window<10} Size of sampling window default = 2  

**negative_samples**= integer, {2<negative_samples<15} Size of negative samples default=4  

**Trainable**= bool, if TRUE, Tensorflow layer API is trainable else Freezed if False. Default=True  

**Returns Embed object**  

### Methods  

1. **train()**:  
    Preprocess the raw data and trains the embedding  

### Attributes  

1. **score:**  
   Returns a float value, spearmen correlation w.r.t simlex999. It can be used to compare embeddings from different method.  
   
2. **TfAPI:**  
   Returns tensorflow's layer object. It can be used in tensorflow model building, just like teensorflow's Embedding layer API.  
   
3. **embeddings:**  
   Returns a dictonary with word-embedding pair.  
   
4. **tokenizer:**  
   Returns tensorflow's tokenizer object.  
   
### Example  

![image](https://user-images.githubusercontent.com/39105103/120958342-29b8a580-c775-11eb-9ebd-16dbd477b98e.png)
  
  

  
  








