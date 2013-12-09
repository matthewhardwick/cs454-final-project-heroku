from flask import Flask, jsonify, render_template
from os import listdir
import re
from delta import *
from dfa import makeDFA

app = Flask(__name__)
app.debug = True
example_types = ['pass', 'fail']

@app.route('/example/<example_type>/<example_id>')
def example_pass(example_type, example_id):
	if example_type in example_types:
		infile = get_infile(example_type, example_id)
		return render_template('example.html', viewModel=infile)


@app.route('/')
def index():
	regex = re.compile(u'(pass|fail)(\d+).in')
	files = { s: [] for s in example_types }
	for item in listdir('inputfiles/'):
		match = regex.match(item)
		if match and match.group(1) in example_types:
			files[match.group(1)].append({ 'filename' :item, 'id': match.group(2) })
	for s in files.keys():
		files[s].sort()
	return render_template('index.html', viewModel=files)

@app.route('/debug')
def debug():
	dfa = makeDFA()
	infile = get_infile('pass', '1')
	output = ""
	state = 'start'
	for i in infile:
		output += state + ' => ' + i + ' => '
		state = delta(state, i)
		output += state + '<br />'
	return output


def get_infile(input_type, example_id):
	filename = 'inputfiles/' + input_type + example_id + '.in'
	infile = [ s.rstrip() for s in open(filename).readlines() ]
	return infile

