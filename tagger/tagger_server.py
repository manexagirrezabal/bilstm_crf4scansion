#!/usr/bin/env python

import os
import time
import codecs
import optparse
import json
import numpy as np

import re

from loader import prepare_sentence
from utils import create_input, iobes_iob, iob_ranges, zero_digits
from model import Model

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import urllib
from urlparse import urlparse, parse_qs

import clean

optparser = optparse.OptionParser()
#optparser.add_option(
#    "-m", "--model", default="",
#    help="Model location"
#)
#optparser.add_option(
#    "-i", "--input", default="",
#    help="Input file location"
#)
#optparser.add_option(
#    "-o", "--output", default="",
#    help="Output file location"
#)
optparser.add_option(
    "-d", "--delimiter", default="__",
    help="Delimiter to separate words from their tags"
)
optparser.add_option(
    "--outputFormat", default="",
    help="Output file format"
)
opts = optparser.parse_args()[0]

# Check parameters validity
assert opts.delimiter

# Load existing model
print "Loading model..."
modeldir = "/Users/jbt694/project_bilstm4scansion/bilstm_crf4scansion/tagger/models/tag_scheme=iobes,lower=False,zeros=False,char_dim=25,char_lstm_dim=25,char_bidirect=True,word_dim=100,word_lstm_dim=100,word_bidirect=True,pre_emb=,all_emb=False,cap_dim=0,crf=True,dropout=0.5,lr_method=sgd-lr_.005/"
model = Model(model_path=modeldir)
parameters = model.parameters

# Load reverse mappings
word_to_id, char_to_id, tag_to_id = [
    {v: k for k, v in x.items()}
    for x in [model.id_to_word, model.id_to_char, model.id_to_tag]
]

# Load the model
_, f_eval = model.build(training=False, **parameters)
model.reload()

#f_output = codecs.open(opts.output, 'w', 'utf-8')
start = time.time()

print 'Tagging...'

def analyze_line(line):
    count = 0

    line = re.sub("[^a-zA-Z\ ]","",line) #Cleanup

    words_ini = line.rstrip().split()
    result = ""
    if line:
        # Lowercase sentence
        if parameters['lower']:
            line = line.lower()
        # Replace all digits with zeros
        if parameters['zeros']:
            line = zero_digits(line)
        words = line.rstrip().split()
        # Prepare input
        sentence = prepare_sentence(words, word_to_id, char_to_id,
                                    lower=parameters['lower'])
        input = create_input(sentence, parameters, False)
        # Decoding
        if parameters['crf']:
            y_preds = np.array(f_eval(*input))[1:-1]
        else:
            y_preds = f_eval(*input).argmax(axis=1)
        y_preds = [model.id_to_tag[y_pred] for y_pred in y_preds]
        # Output tags in the IOB2 format
        if parameters['tag_scheme'] == 'iobes':
            y_preds = iobes_iob(y_preds)
        # Write tags
        assert len(y_preds) == len(words)
        
        result = ('%s\n' % ' '.join('%s%s%s' % (w, opts.delimiter, y)
                                             for w, y in zip(words_ini, y_preds)))

    return result

res = analyze_line("to be or not to be that is the question")
print (res)



class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)
        print (parsed_url)
        print (params)
        inp = params['inp']
        print ("Let's analyze this input: <"+str(inp[0].strip())+">")
        result = analyze_line(inp[0].strip())
        print ("This is the result: <"+result+">")
        l = clean.divide_wan(result)
        cleanresult = " ".join(clean.reformatline(l))
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(cleanresult)

def run(server_class=HTTPServer, server_port=8000):
    server_address = ('', server_port)
    httpd = server_class(server_address, RequestHandler)
    print("Starting server on port", server_port)
    httpd.serve_forever()

if __name__ == "__main__":
    run()

