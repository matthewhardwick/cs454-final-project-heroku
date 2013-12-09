from flask import Flask, jsonify, render_template
from os import listdir
import re
from delta import *
from dfa import makeDFA

app = Flask(__name__)
example_types = ['pass', 'fail']

@app.route('/example/<example_type>/<example_id>')
def example_pass(example_type, example_id):
	if example_type in example_types:
		infile = get_infile(example_type, example_id)
		state_info = []
		state = 'start'
		for i in infile:
			current_state_info = { 'start': state, 'symbol': i }
			state = delta(state, i)
			current_state_info['end'] = state
			state_info.append(current_state_info)
		return render_template('example.html', viewModel={ 'states': infile, 'state_info': state_info })


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


def get_infile(input_type, example_id):
	filename = 'inputfiles/' + input_type + example_id + '.in'
	infile = [ s.rstrip() for s in open(filename).readlines() ]
	return infile

