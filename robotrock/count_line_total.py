import os, fnmatch, sys

def all_files(root, patterns = '*', single_level=False, yield_folders=False):
	patterns = patterns.split(';')
	for path, subdirs, files in os.walk(root):
		if yield_folders:
			files.extend(subdirs)
		files.sort()
		for name in files:
			for pattern in patterns:
				if fnmatch.fnmatch(name, pattern):
					yield os.path.join(path, name)
					break
		if single_level:
			break

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'Usage: python count_line_total.py <root dir>'
		quit()
	files = all_files(sys.argv[1], '*.py', False, False)
	total = 0
	for name in files:
		length = len(open(name, 'rU').readlines()) 
		print name, ' is ', length, 'lines'
		total += length
	print 'Total line count: ', total 			
