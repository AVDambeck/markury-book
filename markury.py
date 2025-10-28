'''
find target directory.
ensure an empty dir.
look for manual list of files
    otherwise make a list.
make the html.
make the pdfs.
combine the pdfs.
    index.html first, then the rest alphabetically.
save the final pdf
'''

import argparse

parser = argparse.ArgumentParser(description='book rendering tool.')

parser.add_argument('-v', '--verbose', action='store_true', help='increase verbosity.')
parser.add_argument('-i', '--input-dir', type=str, help='directory of input files. defaults to ../')

args = parser.parse_args()

if args.input_dir is None:
    input_dir = '..'
else:
    input_dir = args.input_dir

if args.verbose is not None:
    pass
    
print(input_dir)

