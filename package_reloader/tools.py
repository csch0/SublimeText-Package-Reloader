import sublime, sublime_plugin

import json, os.path, re

if sublime.version()[0] == "2":
	from codecs import open

def load_resource(name):
	if hasattr(sublime, 'decode_value'):
		return sublime.load_resource(name)
	else:
		with open(os.path.join(sublime.packages_path(), name[9:]), encoding = "utf-8") as f:
			return f.read()

def save_resource(name, value):
	with open(os.path.join(sublime.packages_path(), name[9:]), "w", encoding = "utf-8") as f:
		f.write(value)

def decode_value(string):
	if hasattr(sublime, 'decode_value'):
		return sublime.decode_value(string)
	else:
		lines = [line for line in string.split("\n") if not re.search(r'//.*', line)]
		string = "\n".join(lines)
		if string:
			return json.loads(string)
		else:
			return None

def encode_value(value, pretty = False):
	if hasattr(sublime, 'encode_value'):
		return sublime.encode_value(value, pretty)
	else:
		return json.dumps(value, sort_keys = True if pretty else False, indent = 4 if pretty else 0)

def source_files(package_dir):
	items = []
	for root, dir_names, file_names in os.walk(package_dir):
		items += [os.path.relpath(os.path.join(root, file_name), package_dir).replace(os.sep, "/") for file_name in file_names if file_name[-3:] == ".py"]
	return items