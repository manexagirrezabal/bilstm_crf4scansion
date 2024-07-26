# BiLSTM+CRF model for poetry scansion
This is the model for English poetry scansion that was presented in Agirrezabal (2017) and in Agirrezabal, Alegria and Hulden (2017).

We used a corpus of English poetry for training and testing our models, called [For Better For Verse](https://github.com/manexagirrezabal/for_better_for_verse/tree/master/poems). The linked repository is a fork of the original repository. We made some changes so that our corpus reader reads the files properly. This corpus was developed by Herbert Tucker, from the Scholars' Lab at the University of Virginia especially for an [interactive website](http://prosody.lib.virginia.edu/) for learning how to scan English poetry.
Then, we can read the corpus files using the following [script](https://github.com/manexagirrezabal/herascansion/blob/master/script.sh) written for the [HeraScansion](https://github.com/manexagirrezabal/herascansion) project (discontinued). This script requires the English poetry corpus reader that we have in the [following repository](https://bitbucket.org/manexagirrezabal/poetrycorpusreader/src/master/).

The specific model that the user can use in this repository is the BiLSTM+CRF model that converts words to stress patterns (W2SP), as it does not require syllabification of words. For more information, please check section 4 of Agirrezabal, Alegria and Hulden (2017).

# Requirements

In order to make it easier to use, all requirements are included in the Python environment that is saved in the `scansion_env` directory.

# Usage
If we want to scan a poem, this should be in txt format, and there should be no empty lines in between. In its current form, if an empty line is found, the program will stop scanning. This is how you can scan a poem. 

`./scan_file.sh input.txt output.txt`

The output is saved in the file called `output.txt`. Watch out! If the file exists, its contents will be overwritten.

# Example:

Input from ``The voice`` by Thomas Hardy (Monroe 1917, p. 131):

```
Woman much missed, how you call to me, call to me,
Saying that now you are not as you were
When you had changed from the one who was all to me,
But as at first, when our day was fair.
```

The scansion model returns the following:

```
Woman much missed, how you call to me, call to me,   +- - + - - + - - + - + 
Saying that now you are not as you were  ___________ +- - + - - + - + - 
When you had changed from the one who was all to me,   - + - + - - + - - + - + 
But as at first, when our day was fair.  ___________ + - - + - - + - +
```

# Usage (server mode)
As the software requires python2.7, we can overcome this by running the scansion model as a server, and interact with it using a client from Python3.x. The server can be run using the `tagger_server.py` program:

`scansion_env/bin/python2.7 tagger/tagger_server.py`

And the client, is saved in this same directory:

`python3 client.py "Woman much missed, how you call to me, call to me,"`

Which performs scansion and cleanup, and therefore, it would return the following:

`+- - + - - + - - + - +`

# Citation

 - Agirrezabal, Manex, Iñaki Alegría, and Mans Hulden. ["A Comparison of Feature-Based and Neural Scansion of Poetry."](https://aclanthology.org/R17-1003/) Proceedings of the International Conference Recent Advances in Natural Language Processing, RANLP 2017. 2017.
 - Agirrezabal Zabaleta, Manex. ["Automatic scansion of poetry"](https://addi.ehu.es/handle/10810/29999). DIF-FISS. Universidad del País Vasco-Euskal Herriko Unibertsitatea, 2017.
