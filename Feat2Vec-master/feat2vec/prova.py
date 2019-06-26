import numpy as np
import pandas as pd
import tensorflow as tf
import keras
import model
from model import DeepFM
import implicitsampler
#reload(implicitsampler)
from implicitsampler import ImplicitSampler
#from past.builtins import xrange

np.random.seed(1)
samplesize = 100000 #number of records
batch_size=2000 #number of positive labels per batch
neg_samples=5 #number of negative labels per batch
embed_dim = 10 #dimensionality of embeddings to learn

attrs = np.random.multivariate_normal(mean = np.array([0.,0.]), cov = np.array([[1.,.1],[.1,1]]),size=samplesize)
data = pd.DataFrame({ 'item': np.random.randint(0,10,size=samplesize),
						  'id': np.random.randint(0,50,size=samplesize),
                          'attr1':attrs[:,0],
                          'attr2':attrs[:,1],
                          'attr3': np.random.uniform(size=samplesize),
						  'offset_':np.zeros(samplesize)
	})

data['latenty'] = ( (data.attr3)**4/600. + np.exp(data.attr1*data.attr2) \
                       + (data.item<=3)*np.pi - ((data.item==2) | (data.item==4))*data.attr3 \
                       + ((data.item==8) | (data.item==7) )*data.attr2 \
                       + (data.item>=6)*data.attr1 + (data.id%3)*data.attr3 \
                       + np.random.normal(size=samplesize) - 5 )
data.loc[np.abs(data['latenty']) >= 10,'latenty'] = 0
data['y'] = np.floor(data.latenty)
'''

Define what features we are going to use and how we are going to use them
Some important things to note here:
* Each item in the model_features list will be represented as a dense vector that learns similarities by interacting with all other model features
* Each item in the sampling_features list represents a unique feature of data that should be sampled together for the oversampling method . For example, one might want to sample car model and car manufacturer together because other combinations are not only not observed in the data, they are entirely nonsensical. sampling_features do not need to coincide with model features (i.e. a researcher might still feel its important to learn separate embeddings for make and model of a car)
* features is a list of what we call the model_features in the keras model layers
* We pass most arguments to feat2vec as a list of lists, and often each sub-list only has one element. this is necessary because it is possible to have multiple elements in a single "feature" 
* We aggregate attr1,attr2,attr3 into a single "feature" called attrs. The idea is these features all represent at a high level one characteristic of each observation, and so should be grouped together. One might imagine in a real world setting, instead aggregating city,county,state columns into a single "location" feature vector.
*


'''
features = ['item','id','attrs','y','offset']
model_features = [['item'],['id'],['attr1','attr2','attr3'],['y'],['offset_']]
sampling_features = model_features
'''

Define how we are going to use the features in the model; specifically, whether to learn biases or embeddings only. typically, we want do not want to learn bias terms since these are not straightforward to import to external applications. Here we only learn embeddings for everything except the intercept term (offset\_) which we keep to 
modify the average level of the score function. both bias_only and embeddings_only except an ordered boolean list where positionally they correspond to each feature listed in model_features

also pass a realvalued bool list which tells our model whether we should treat the inputs as discrete categories or real-valued scalar numbers

finally, feature\_dims refers to the dimensionality of each feature. for discrete categories, this is the total # of categories. for realvalued features, this is the number of columns (i.e. for attrs it is 3)


'''

bias_only = [False]*len(model_features)
bias_only[ features.index('offset') ] =True
embeddings_only = [True]*len(model_features)
embeddings_only[ features.index('offset') ] =False
realvalued = [False]*len(model_features)
realvalued[ features.index('attrs') ] =True
feature_dims = [10,50,3,2,1]
'''

build the feat2vec model in keras; note we specify noise contrastive estimation as the objective; negative sampling is also available but disencouraged


'''
# feat2vec_obj = DeepFM(feature_dims, embed_dim, obj='nce' ,
#                       feature_names=features,realval=realvalued)
feat2vec_obj = DeepFM(model_features, feature_dims, obj='nce',
                      feature_names=features, realval=realvalued)

feat2vec_fm = feat2vec_obj.build_model(embed_dim, deep_out=False,bias_only=bias_only,embeddings_only=embeddings_only)

step1_probs = implicitsampler.gen_step1_probs(feat2vec_fm,features,.5)


pct_train = .90
train_sample = np.random.uniform(size=samplesize)
train_sample = (train_sample <=np.percentile(train_sample,pct_train*100) ).astype('bool')
train_data = data[train_sample==True]
valid_data = data[train_sample==False]
'''

Create samplers from implicitsampler class . Here we pass the second main hyperparameter, $\alpha_2=.25$ (sampling_alpha) to determine how much we flatten our empirical distribution that samples values for negative labels.

* sampling_bias adds a minimum count to each unique value in the data to ensure very low frequency values get sampled enough

* negative_samples is the number of negative samples per observed record

* keep_noise_probs necessary if we use NCE, otherwise should not use.


'''
trainsampler = ImplicitSampler(train_data,model_features=model_features,sampling_features=sampling_features,
                          batch_size=batch_size,                 
                          sampling_alpha=.25,sampling_bias=10,
                          negative_samples=neg_samples,
                          init_probs = step1_probs,keep_noise_probs=feat2vec_obj.obj=='nce')
validsampler = ImplicitSampler(valid_data,model_features=model_features,sampling_features=sampling_features,
                          batch_size=batch_size,                 
                          sampling_alpha=.25,sampling_bias=10,
                          negative_samples=neg_samples,
                          init_probs = step1_probs,keep_noise_probs=feat2vec_obj.obj=='nce')

callbacks = [keras.callbacks.EarlyStopping(monitor='val_loss', patience=0)]
feat2vec_fm.compile(loss='binary_crossentropy', metrics=['accuracy'], optimizer=keras.optimizers.TFOptimizer(tf.train.AdamOptimizer()))

feat2vec_fm.fit_generator(generator = trainsampler.keras_generator(),
                          epochs=100, 
                          steps_per_epoch = len(train_data)/batch_size,
                          validation_data=validsampler.keras_generator(),
                          validation_steps =  len(valid_data)/batch_size,
                          callbacks=callbacks,
                          verbose=1,
                          max_queue_size=1,
                          workers=8,
                          use_multiprocessing=True)

#collect embeddings
embeddings = []
embed_names = ['dim_'+str(i) for i in range(1,embed_dim+1)]
for j in feat2vec_obj.feature_names:
    for l in feat2vec_fm.layers:
         if l.name=='factor_{}'.format(j) or l.name=='embedding_{}'.format(j):
                embedding = feat2vec_fm.get_layer(l.name).get_weights()[0]
                embedding = pd.DataFrame(embedding,columns=embed_names)
                embedding['value'] = [j +'_' + str(i) for i in embedding.index]
                embeddings.append(embedding)
embeddings = pd.concat(embeddings,ignore_index=True)