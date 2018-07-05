#!/usr/bin/env python3
"""It's a simple program for searching words by regular expressions 
	in the file. """

import re
import click
import collections

# There we declare class of filename
class Filename():
	data = None
	error = None

	def __init__(self, filename):
		if filename:
			try:
				self.data = filename.readlines()
			except:
				print("Error: there are error in opening file %s." % filename)	
		else:
			self.error = "Error: there are not any filename."
	
	def __str__(self):
		print(self.data)


# There we declare class of pattern
class Pattern():
	reg_exp = None
	error = None

	def __init__(self, pattern):
		if pattern:
			self.reg_exp = re.compile(pattern)
		else:
			self.error = "Error: there are not any pattern."

	def __str__(self):
		print(self.reg_exp)


# There we declare class of options
class Options():
	dictionary = None

	def __init__(self, dictionary):
		self.dictionary = dictionary


# There we declare class of Searcher.
# There we will be solve the main task.
class Searcher():
	options = None
	pattern = None
	filename = None
	result = None
	error = None

	# The main buisness logic will be there.
	def __init__(self, options, pattern, filename):
		self.options = options
		self.pattern = pattern
		self.filename = filename

		if self.pattern.error or self.filename.error:
			self.error = "Error: there are some errors in initialization" \
			+ " of searcher instance. Check input parameters. Try: ./searcher" \
			+ " --help for help."
		else:
			# There we take the result wich be modified by options
			if self.pattern and self.filename:
				result = [re.findall(self.pattern.reg_exp, d) \
					for d in self.filename.data \
					if re.findall(self.pattern.reg_exp, d)
				]
				# # We translate result to flat list
				flat_result = [item for sublist in result for item in sublist]
				
				# This is default returned result when options is ommited
				self.result = flat_result
				# For count in options
			
				counts = collections.Counter(self.result)
				res = list(counts)
			
				# For frequency in options
				N = len(flat_result)
				freq = dict(counts)
				for i,k in counts.items():
					freq[i] = round(float(k) / N, 3)

				if result is None:
					print("There aren't any matches.")
			else:
				self.error = "Error: there aren't PATTERN or FILENAME." \
				+ "Usage: searcher.py [OPTIONS] PATTERN [FILENAME]."

			# Taking into account options
			if self.options.dictionary:
				# print(sorted(self.options.dictionary.items(), reverse=True))
				for key, value in sorted(self.options.dictionary.items(), \
				reverse=True):
					if value:
						print("There are options: {} : {}".format(key, value))
						# Python analog of switch - case operators
						if key is 'unique':
							self.result = list(set(flat_result))
						elif key is 'count':
							self.result = len(self.result)
						elif key is 'lines':
							self.result = len(result)
						elif key == 'sort' and value == 'abc':
							self.result = sorted(self.result)
						elif key == 'sort' and value == 'freq':
							self.result = sorted(self.result, key=lambda x: \
								counts[x]
							)
						elif key == 'order' and value == 'asc':
							pass
						elif key == 'order' and value == 'desc':
							self.result = self.result[::-1]
						elif key is 'number':
							self.result = self.result[0:int(value)]
						elif key == 'stat' and value == 'count':
							self.result = sorted(counts.items(), key=lambda x: \
								counts[x]
							)
						elif key == 'stat' and value == 'freq':
							tabs = "\t\t| "
							for i, k in enumerate(sorted(counts.items())):
								res[i] = str(k[0]) + tabs + str(k[1])
							self.result = res
						else:
							self.error \
								="This options {}: {}".format(key, value) \
								+ " doesn't exist."

	def print_result(self):
		if self.error:
			print(self.error)
		else:
			try:
				_ = iter(self.result)
			except TypeError:
				print(self.result)
			else:
				if isinstance(self.result, dict):
					print(self.result)	
				elif isinstance(self.result, list):
					print(self.result)	
				else:
					for i in self.result:
						print(i)

@click.command()
@click.option('--unique', '-u', is_flag=True, help='List unique matches only')
@click.option('--count', '-c', is_flag=True, help='Get total count of found \
matches')
@click.option('--lines', '-l', is_flag=True, help='Get total count of lines, \
where at least one match was found')
@click.option('--sort', '-s', default='abc', help='Sorting of found matches \
by alphabet and frequency (related to all found matches).')
@click.option('--order', '-o', default='asc', help='Sorting order can be \
specified (ascending, descending).')
@click.option('--number', '-n', help='List first N matches')
@click.option('--stat', help='List unique matches with statistic (count or \
frequency in percents)')
@click.argument('pattern', required=True)
@click.argument('filename', type=click.File('r'), required=False)
def searcher(unique, count, lines, sort, order, number, stat, pattern, filename):

	# print(filename)
	# print(pattern)
	# There we forms options as dictionary
	options = {'unique': unique, 'count': count, 'lines': lines, 'sort': sort,\
		'order': order, 'number': number, 'stat': stat
	}

	options_instance = Options(options)
	pattern_instance = Pattern(pattern)
	filename_instance = Filename(filename)
	
	searcher_instance = Searcher(options_instance, pattern_instance, \
		filename_instance
	)
	
	searcher_instance.print_result()


if __name__ == '__main__':
	searcher()
