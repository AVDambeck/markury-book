'''
find target dir.
ensure an empty dir.
look for manual list of files
    otherwise make a list.
make the html.
make the pdfs.
combine the pdfs.
    index.html first, then the rest alphabetically.
save the final pdf
'''

# set up

import argparse
import os
import shutil

parser = argparse.ArgumentParser(description='book rendering tool.')

parser.add_argument('-v', '--verbose', action='store_true', help='increase verbosity.')
parser.add_argument('-f', '--force', action='store_true', help='delete files in the way.')
parser.add_argument('-i', '--input-dir', type=str, help='dir of input files. defaults to ..')
parser.add_argument('-o', '--output-dir', type=str, help='output dir. defaults to input_dir/export')

args = parser.parse_args()

if args.input_dir is None:
    input_dir = '..'
else:
    input_dir = args.input_dir

if args.output_dir is None:
    output_dir = f'{input_dir}/export'
else: 
    output_dir = args.output_dir

if args.verbose is not None:
    pass
    
# define 
def is_dir_empty(dir):
    if os.path.exists(dir):
        if os.path.isdir(dir):
            return len(os.listdir(dir)) == 0
        else:
            raise NotADirectoryError(f"{dir} is not a dir.")
    else:
        raise FileNotFoundError(f"{dir} does not exist.")

def ensure_dir_exists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)  
        print(f'made {dir}')

def ensure_dir_empty(dir):
    ensure_dir_exists(dir)
    if is_dir_empty(dir):
        print('yippee!')
    else:
        if args.force == False:
            print(f'{dir} is not empty. Empty it or use -f')
            exit()
        else:
            try:
                shutil.rmtree(dir)  
                os.makedirs(dir)  
                print(f"Contents of '{dir}' deleted.")
            except Exception as e:
                print(f"An error occurred while clearing the dir: {e}")
                exit()

# main
ensure_dir_empty(output_dir)
