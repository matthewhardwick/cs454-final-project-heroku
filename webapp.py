from flask import Flask, jsonify, render_template
from os import listdir
import re

app = Flask(__name__)

@app.route('/example/pass/<example_id>')
def example_pass(example_id):
	return render_lattice_template(u'pass', example_id)


@app.route('/example/fail/<example_id>')
def example_fail(example_id):
	return render_lattice_template(u'fail', example_id)


@app.route('/')
def index():
	regex = re.compile(u'(pass|fail)(\d+).in')
	files = { 'pass_files': [], 'fail_files': [] }
	for item in listdir('inputfiles/'):
		match = regex.match(item)
		if match and match.group(1) == 'pass':
			files['pass_files'].append({ 'filename' :item, 'id': match.group(2) })
		elif match and match.group(1) == 'fail':
			files['fail_files'].append({ 'filename' :item, 'id': match.group(2) }) 
	return render_template('index.html', viewModel=files)


def render_lattice_template(input_type, example_id):
	filename = 'inputfiles/' + input_type + example_id + '.in'
	infile = open(filename).readlines()
	if infile:
		return render_template('example.html', viewModel=infile)
	else:
		return filename

if __name__ == "__main__":
	app.run(use_debugger=True, use_reloader=True, debug=True, host='0.0.0.0')