# training new models for spacy

### init model
`python -m spacy init-model sk /mnt/data/data/sk-vectors-fasttext-new/ --model-name sk_experimental_md --vectors-loc /mnt/data/data/models-fasttext/cc.sk.300-slim.vec --prune-vectors 200000`

--prune-vectors was throwing an error - maybe an old spaCy? (currently 2.2.3)


```
python -m spacy info

============================== Info about spaCy ==============================

spaCy version    2.2.1                         
Location         /home/dzon/env/lib/python3.6/site-packages/spacy
Platform         Linux-5.0.0-37-generic-x86_64-with-Ubuntu-18.04-bionic
Python version   3.6.9                         
Models           en                            
```

this worked (maybe a smaller number of target vectors is needed): `python -m spacy init-model sk /mnt/data/data/sk-vectors-fasttext-prune10000/ --model-name sk_experimental_prune10000 --vectors-loc /mnt/data/data/models-fasttext/cc.sk.300-slim.vec --prune-vectors 10000`

### universaldependencies data:
https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-3131

#### convert any data toconll with udpipe
`./udpipe --tokenize --tag --parse ~/kajo/spacy_multilang/udpipe-models/slovak-snk-ud-2.5-191206.udpipe ~/kajo/sk-texts/pleso.txt > pleso.conllu`

### convert to spacy format:
```
python -m spacy convert UD_Slovak-SNK/sk_snk-ud-train.conllu sk-json
python -m spacy convert UD_Slovak-SNK/sk_snk-ud-dev.conllu sk-json 
```
CONLLu to text (80 char per line)
`perl conllu_to_text.pl --lang=sk sk_snk-ud-dev.conllu > sk_snk-ud-dev.txt`

from: https://github.com/UniversalDependencies/tools

#### training
`python -m spacy train sk sk-models sk-json/sk_snk-ud-train.json sk-json/sk_snk-ud-dev.json`

`python -m spacy train sk /mnt/data/data/sk-vectors-fasttext2 /home/dzon/kajo/spacy_multilang/sk-json/sk_snk-ud-train.json /home/dzon/kajo/spacy_multilang/sk-json/sk_snk-ud-dev.json -v /mnt/data/data/sk-vectors-fasttext -n 10 --pipeline 'tagger,parser'`

`python -m spacy train sk /mnt/data/data/sk-vectors-fasttext-new-tagger-parser/ /home/dzon/kajo/spacy_multilang/sk-json/sk_snk-ud-train.json /home/dzon/kajo/spacy_multilang/sk-json/sk_snk-ud-dev.json -v /mnt/data/data/sk-vectors-fasttext-new/ -n 30 --pipeline 'tagger,parser'`
```
Itn  Tag Loss    Tag %    Dep Loss    UAS     LAS    Token %  CPU WPS
---  ---------  --------  ---------  ------  ------  -------  -------
  1  40816.843    71.342  71608.192  77.848  66.485  100.000    13176                                                                                                                                    
  2  23199.345    76.632  42468.942  82.936  73.798  100.000    14216                                                                                                                                       
  3  18346.534    78.376  33842.235  84.312  76.499  100.000    15183                                                                                                                                       
  4  15445.116    79.180  28411.796  85.151  77.658  100.000    14092                                                                                                                                       
  5  13300.054    79.670  24212.541  85.701  78.594  100.000    13601                                                                                                                                       
  6  11680.581    80.096  22020.810  86.071  79.067  100.000    13469                                                                                                                                       
  7  10389.259    80.322  19426.287  86.193  79.433  100.000    13089                                                                                                                                       
  8   9416.304    80.281  17598.654  86.188  79.493  100.000    13432                                                                                                                                       
  9   8551.520    80.386  15577.038  85.938  79.328  100.000    13295                                                                                                                                       
 10   8063.918    80.539  14824.776  86.005  79.499  100.000    12890                                                                                                                                       
 11   7386.846    80.603  13874.678  86.062  79.555  100.000    13105                                                                                                                                       
 12   6836.119    80.651  12410.340  86.243  79.634  100.000    13209                                                                                                                                       
 13   6359.059    80.539  11937.040  86.327  79.756  100.000    12394                                                                                                                                       
 14   6277.507    80.466  11308.739  86.472  79.938  100.000    12954                                                                                                                                       
 15   6031.368    80.394  10177.886  86.598  80.101  100.000     9833                                                                                                                                       
 16   5708.063    80.289   9839.208  86.619  80.058  100.000    11261                                                                                                                                       
 17   5411.634    80.338   9628.633  86.755  80.081  100.000    13323                                                                                                                                       
 18   5276.591    80.434   9225.565  86.712  80.141  100.000    13340                                                                                                                                       
 19   5122.746    80.297   8953.934  86.557  79.947  100.000    13281                                                                                                                                       
 20   4941.154    80.257   8380.837  86.603  80.079  100.000    13307                                                                                                                                       
 21   4749.657    80.193   8127.219  86.459  80.075  100.000    12945                                                                                                                                       
 22   4581.765    80.185   7701.288  86.520  80.062  100.000    12684                                                                                                                                       
 23   4446.615    80.048   7723.409  86.507  80.077  100.000    13775                                                                                                                                       
✔ Saved model to output directory                                                                                                                                                                          
/mnt/data/data/sk-vectors-fasttext-new-tagger-parser/model-final
...
OSError: [Errno 12] Cannot allocate memory
```

```
python -m spacy train sk /mnt/data/data/sk-no_vectors-tagger-parser_n30-continue/ /home/dzon/kajo/spacy_multilang/sk-json/sk_snk-ud-train.json /home/dzon/kajo/spacy_multilang/sk-json/sk_snk-ud-dev.json -n 30 --pipeline 'tagger,parser' -b /mnt/data/data/sk-no_vectors-tagger-parser_n30/model-best
Training pipeline: ['tagger', 'parser']
Starting with base model
'/mnt/data/data/sk-no_vectors-tagger-parser_n30/model-best'
Counting training words (limit=0)

Itn  Tag Loss    Tag %    Dep Loss    UAS     LAS    Token %  CPU WPS
---  ---------  --------  ---------  ------  ------  -------  -------
  1  10074.149    71.937  14536.531  80.562  72.110  100.000    13568                                                                                                                                       
  2   9495.046    72.267  14955.041  80.751  72.393  100.000    14027                                                                                                                                       
  3   8351.152    72.677  13354.041  81.279  73.306  100.000    13320                                                                                                                                       
  4   7634.332    72.669  11886.834  81.653  73.718  100.000    13339                                                                                                                                       
  5   6903.432    72.677  11090.139  81.155  73.305  100.000    13388                                                                                                                                       
  6   6437.976    72.717  10003.167  81.362  73.408  100.000    13324                                                                                                                                       
  7   6024.474    72.950   8997.056  81.822  73.784  100.000    13223                                                                                                                                       
  8   5627.351    72.934   8289.231  81.658  73.630  100.000    11889                                                                                                                                       
  9   5450.853    73.103   8240.859  81.508  73.649  100.000    11639                                                                                                                                       
 10   5054.848    73.320   7771.452  81.765  73.878  100.000    12026                                                                                                                                       
 11   4846.820    73.344   7338.102  81.883  73.950  100.000    12493                                                                                                                                       
 12   4614.055    73.320   6982.586  81.874  73.940  100.000    12764                                                                                                                                       
 13   4421.964    73.336   6813.821  81.921  73.893  100.000    13001                                                                                                                                       
 14   4439.935    73.336   6487.863  81.786  73.786  100.000    10956                                                                                                                                       
 15   4299.348    73.352   6164.833  81.833  73.824  100.000    13001                                                                                                                                       
 16   4083.502    73.328   6228.855  81.878  73.934  100.000    12973                                                                                                                                       
 17   4143.936    73.368   5928.025  82.034  74.081  100.000    13258                                                                                                                                       
 18   4017.809    73.400   5939.173  81.936  73.862  100.000    13000                                                                                                                                       
 19   4013.800    73.400   5865.661  81.964  73.871  100.000    13125                                                                                                                                       
 20   3884.929    73.432   5550.468  82.002  74.049  100.000    12922                                                                                                                                       
 21   3880.478    73.481   5412.136  82.094  74.216  100.000    13233                                                                                                                                       
 22   4009.261    73.368   5551.153  82.182  74.285  100.000    13205                                                                                                                                       
 23   3685.712    73.424   5208.539  82.145  74.266  100.000    13153                                                                                                                                       
 24   3868.782    73.328   5135.722  81.948  74.229  100.000    13215                                                                                                                                       
 25   3637.032    73.296   5358.575  82.117  74.417  100.000    13211                                                                                                                                       
 26   3681.935    73.400   5236.828  82.192  74.492  100.000    13187                                                                                                                                       
 27   3533.713    73.521   5072.871  82.276  74.576  100.000    13172                                                                                                                                       
 28   3576.996    73.577   5096.057  82.107  74.435  100.000    12722                                                                                                                                       
 29   3439.270    73.682   4717.179  82.113  74.592  100.000    11892                                                                                                                                       
 30   3421.553    73.770   4871.475  82.323  74.745  100.000    12608                                                                                                                                       
✔ Saved model to output directory
/mnt/data/data/sk-no_vectors-tagger-parser_n30-continue/model-final
✔ Created best model
/mnt/data/data/sk-no_vectors-tagger-parser_n30-continue/model-best
```

### training NER
data downloaded from here: https://sites.google.com/site/rmyeid/projects/polylgot-ner

split NER data to train and dev:
```
wc -l sk_wiki.conl
split -l 8000000 sk_wiki_train.conll 
mv xaa sk_wiki_train.conll
mv xab sk_wiki_dev.conll
```
```
split -l 5000000 sk_wiki_conv.conll
mv xaa sk_wiki_train_5m_conv.iob
split -l 500000 tmp_dev
mv xaa sk_wiki_dev_5k_conv.iob
```

#### convert to spacy format:
`python -m spacy convert --converter ner /mnt/data/data/emnlp_datasets/acl_datasets/sk/data/sk_wiki_train_5m_conv.iob sk-json`

`python -m spacy convert --converter ner /mnt/data/data/emnlp_datasets/acl_datasets/sk/data/sk_wiki_dev_5k_conv.iob sk-json`


??? To generate better training data, you may want to group sentences into documents with `-n 10`.
`python -m spacy convert -n 10 --converter ner /mnt/data/data/emnlp_datasets/acl_datasets/sk/data/sk_wiki_train_5m_conv.iob sk-json-n10`
`python -m spacy convert -n 10 --converter ner /mnt/data/data/emnlp_datasets/acl_datasets/sk/data/sk_wiki_dev_5k_conv.iob sk-json-n10`

```
python -m spacy convert -n 10 --converter ner /mnt/data/data/ner/en_train.iob /mnt/data/data/ner/json
python -m spacy convert -n 10 --converter ner /mnt/data/data/ner/en_dev.iob /mnt/data/data/ner/json
```

training script

`python -m spacy train sk sk-models-ner sk-json/sk_wiki_train.json sk-json/sk_wiki_dev.json -v sk-models/model-final --pipeline 'ner' -n 5 -VV`

```
Itn  NER Loss   NER P   NER R   NER F   Token %  CPU WPS
---  ---------  ------  ------  ------  -------  -------
  1  303875.131  73.386  62.795  67.678  100.000    36383                                                                     
  2  253842.690  74.461  67.541  70.832  100.000    37325                                                                     
  3  234320.873  75.349  70.135  72.648  100.000    33710 
```

`python -m spacy train sk /mnt/data/data/sk-vectors-fasttext2-ner /home/dzon/kajo/spacy_multilang/sk-json/sk_wiki_train.json /home/dzon/kajo/spacy_multilang/sk-json/sk_wiki_dev.json -v /mnt/data/data/sk-vectors-fasttext2/model-final --pipeline 'ner' -n 3`

`python -m spacy train sk /mnt/data/data/sk-vectors-fasttext-new-ner/ /home/dzon/kajo/spacy_multilang/sk-json-n10/sk_wiki_train_5m_conv.json /home/dzon/kajo/spacy_multilang/sk-json-n10/sk_wiki_dev_5k_conv.json -v /mnt/data/data/sk-vectors-fasttext-new/ --pipeline 'ner' -n 5`

```
Itn  NER Loss   NER P   NER R   NER F   Token %  CPU WPS
---  ---------  ------  ------  ------  -------  -------
  1  161354.435  68.133  65.673  66.880  100.000    22830                                                                                                                                                   
  2  132375.623  69.665  68.260  68.955  100.000    38035                                                                                                                                                   
  3  123075.057  70.993  69.203  70.086  100.000    32415                                                                                                                                                   
  4  115662.235  71.700  71.103  71.400  100.000    34854                                                                                                                                                   
  5  110348.270  72.330  71.278  71.800  100.000    34240   
```

without vectors: `python -m spacy train sk /mnt/data/data/sk-vectors-fasttext-new-ner_only/ /home/dzon/kajo/spacy_multilang/sk-json-n10/sk_wiki_train_5m_conv.json /home/dzon/kajo/spacy_multilang/sk-json-n10/sk_wiki_dev_5k_conv.json  --pipeline 'ner' -n 5`
```
Itn  NER Loss   NER P   NER R   NER F   Token %  CPU WPS
---  ---------  ------  ------  ------  -------  -------
  1  180872.591  68.647  56.837  62.186  100.000    39840                                                                                                                                                   
  2  148378.688  68.762  61.324  64.830  100.000    38418                                                                                                                                                   
  3  136929.420  69.863  63.634  66.603  100.000    40931                                                                                                                                                   
  4  129603.306  70.011  65.687  67.780  100.000    37749                                                                                                                                                   
  5  123905.559  71.067  66.330  68.617  100.000    41704    
```

#### EN - NER training:
`python -m spacy train en /mnt/data/data/en-ner/ /mnt/data/data/ner/json/en_train.json /mnt/data/data/ner/json/en_dev.json  --pipeline 'ner' -n 20`

#### usage of polyglot to tag NER
`polyglot --lang sk tokenize --input ~/kajo/sk-texts/pleso.txt |  polyglot --lang sk ner > ~/kajo/spacy_multilang/sk_pleso_ner.txt`

repair wrong NER convert:
```
with open('/home/dzon/kajo/spacy_multilang/sk_pleso_ner.txt', 'rt') as f:
    for line in f.readlines():
        line = line.strip()
        #if line == "":
        #    continue
        line = re.sub("O$", " O", line)    
        line = re.sub("\s+", "\t", line)    
        
        lines.append(line)
```        

#### CLI training info
https://spacy.io/api/cli#train

### adding vectors to model
How to convert the vectors: https://spacy.io/usage/vectors-similarity#converting

`python -m spacy init-model sk /mnt/data/data/sk-vectors-fasttext/ --vectors-loc /mnt/data/data/models-fasttext/cc.sk.300.vec`

157 languages vectrors: https://fasttext.cc/docs/en/crawl-vectors.html


### lemma spacy-lookups
slovak lemma dictionary: https://korpus.sk/morphology_database.html

### reduce the dimension of Slovak fasttext model
https://github.com/facebookresearch/fastText/blob/master/docs/crawl-vectors.md

`python ./reduce_model.py ../sk_fasttext/cc.sk.300.bin 100`

### merge models
from: https://github.com/aajanki/spacy-fi/blob/master/tools/train.sh

`python mergemodels.py /mnt/data/data/sk-vectors-fasttext-new-tagger-parser/model-final /mnt/data/data/sk-vectors-fasttext-new-ner/model-final /mnt/data/data/sk-vectors-fasttext-new-merged` - it merges the the `model-best` (there are the accuracy data)

`python ~/kajo/spacy_multilang/mergemodels_custom.py /mnt/data/data/sk-no_vectors-tagger-parser_n30-continue/model-best /mnt/data/data/sk-ner_only_full_n20/model-best /mnt/data/data/sk-experimental_no_vectors`

### pretrain
`python -m spacy pretrain /home/dzon/kajo/spacy_multilang/sk-json-n10/sk_wiki_train_5m_conv.json en_core_web_sm /mnt/data/data/experiment-pretrain-sm`

## package model
from https://spacy.io/api/cli#package
```
import spacy
nlp = spacy.load("en_core_web_sm")
nlp.to_disk("/mnt/data/data/en_core_web_sm")
```
```
/mnt/data/data$ mkdir packages
python -m spacy package en_core_web_sm/ packages
cd /mnt/data/data/packages/en_core_web_sm-2.2.0
python setup.py sdist
TOTEST: pip install dist/en_core_web_sm-2.2.0.tar.gz
```

```
python -m spacy package sk-experimental_no_vectors/ packages/
cd packages/sk_sk_experimental_no_vectors-0.1a/
python setup.py sdist
pip install dist/sk_sk_experimental_no_vectors-0.1a0.tar.gz
```

use in python:
```
import spacy
nlp_orig = spacy.load("sk_sk_experimental_no_vectors")
```
