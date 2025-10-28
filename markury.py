'''
find target dir.
ensure an empty dir.
make a list of files.
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
import fnmatch
import markdown

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

def convert_md_to_html(md_content):
    return markdown.markdown(md_content)

# AI Slop
def copy_md_structure_and_convert(source_directory, target_directory):
    """Copy directory structure and convert .md files to .html in the target directory."""
    for root, dirs, files in os.walk(source_directory):
        # Create corresponding directory in target
        target_root = root.replace(source_directory, target_directory, 1)
        os.makedirs(target_root, exist_ok=True)

        for filename in fnmatch.filter(files, '*.md'):
            md_file_path = os.path.join(root, filename)
            # Read the .md file
            with open(md_file_path, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()

            # Convert to HTML
            html_content = convert_md_to_html(md_content)
            html_filename = filename.replace('.md', '.html')
            html_file_path = os.path.join(target_root, html_filename)

            # Write the HTML to the new file
            with open(html_file_path, 'w', encoding='utf-8') as html_file:
                html_file.write(html_content)

# main
def get_parent_directory():
    """Return the parent directory of the directory where this script is located."""
    # Get the current script's directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Get the parent directory
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    
    return parent_directory

# Usage example
parent_dir = get_parent_directory()
print(f"The parent directory is: {parent_dir}")

# ensure_dir_empty(output_dir)
# copy_md_structure_and_convert(input_dir, output_dir)
