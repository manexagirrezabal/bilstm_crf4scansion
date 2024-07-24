#./scan_file.sh input.txt output.txt

scansion_env/bin/python2.7 tagger/tagger.py -i $1 -o $2 -m tagger/models/tag_scheme=iobes,lower=False,zeros=False,char_dim=25,char_lstm_dim=25,char_bidirect=True,word_dim=100,word_lstm_dim=100,word_bidirect=True,pre_emb=,all_emb=False,cap_dim=0,crf=True,dropout=0.5,lr_method=sgd-lr_.005
python3 clean.py $2

