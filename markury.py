import argparse
import os
import shutil
import fnmatch
import markdown

# flags
flag_index = "%INDEX%"
flag_gallery = "%GALLERY%"
flags = [flag_index, flag_gallery]

# cli flags
parser = argparse.ArgumentParser(description='book rendering tool.')

parser.add_argument('-v', '--verbose', action='store_true', help='increase verbosity.')
parser.add_argument('-i', '--input-dir', type=str, help='dir of input files. defaults to parent directory of the script i.e. dir/dir/markuary-book/..')
parser.add_argument('-o', '--output-dir', type=str, help='output dir. defaults to input_dir/export')
parser.add_argument('-t', '--types', nargs='*', help='types to include. default is md, html, css, json, yaml, yml, jpg, jpeg, gif, webm, png. using this flag replaces the defaults')
parser.add_argument('-s', '--css', type=str, help='path to css file. it will be copied to the output dir, inplace of the default css')
parser.add_argument('-f', '--force', action='store_true', help='delete files in the way.')
parser.add_argument('--blacklist', nargs='*', help='skip these dirs. Automattically includes output dir and the current dir. automatically prepends inputdir/')

args = parser.parse_args()

## dirs
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

if args.input_dir is None:
    input_dir = parent_dir
else:
    input_dir = args.input_dir

if args.output_dir is None:
    output_dir = f'{input_dir}/export'
else: 
    output_dir = args.output_dir

blacklist = [output_dir, current_dir]
if args.blacklist is not None:
    for i in args.blacklist:
        blacklist += [f'{input_dir}/{i}']

## misc
if args.css is None:
    css_path = f'{current_dir}/default.css'
else:
    css_path = args.css

if args.types is None:
    target_types = ['md', 'html', 'css', 'json', 'yaml', 'yml', 'jpg', 'jpeg', 'webm', 'png']
else:
    target_types = []
    for i in args.types:
        target_types += i

if args.verbose is not None:
    pass
    


# define 
## dirs
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
        return True 
    else:
        if args.force == False:
            print(f'{dir} is not empty. Empty it or use -f')
            exit()
        else:
            try:
                shutil.rmtree(dir)  
                os.makedirs(dir)  
                print(f"Contents of '{dir}' deleted.")
                return True
            except Exception as e:
                print(f"An error occurred while clearing the dir: {e}")
                exit()

## Stream processing
def respond_flag(md_content, root):
    if flag_index in md_content:
        md_content = add_index(md_content, root)

    if flag_gallery in md_content:
        md_content = add_gallery(md_content, root)

    return md_content

def add_index(md_content, root):
    index_content = """
    - foo
    - bar
    - bap
    """

    md_content = md_content.replace(flag_index, index_content)
    
    return(md_content)

def add_gallery(md_content, dir):
    gallery_content = """
    - foo
    - bar
    - bap
    """

    md_content = md_content.replace(flag_gallery, gallery_content)
    
    return(md_content)

## Conversion
def convert_md_to_html(md_content, css_path):
    html_content = markdown.markdown(md_content, extensions=['tables'])
    css_link = f'<link rel="stylesheet" type="text/css" href="{css_path}">'
    return f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">{css_link}</head><body>{html_content}</body></html>'


def copy_md_structure_and_convert(source_directory, target_directory):
    """Copy directory structure and convert .md files to .html in the target directory."""

    # Copy the CSS file to the target directory
    css_filename = "style.css"
    target_css_path = os.path.join(target_directory, css_filename)
    shutil.copy(css_path, target_css_path)

    for root, dirs, files in os.walk(source_directory):
        # Skip blacklisted files
        if any(blacklisted_dir in root for blacklisted_dir in blacklist):
            continue  

        # Create corresponding directory in target
        target_root = root.replace(source_directory, target_directory, 1)
        os.makedirs(target_root, exist_ok=True)

        for filename in files:
            file_extension = os.path.splitext(filename)[1][1:]  
            if file_extension in target_types:
                source_file_path = os.path.join(root, filename)

                if file_extension == 'md':
                    # Read the .md file
                    with open(source_file_path, 'r', encoding='utf-8') as md_file:
                        md_content = md_file.read()

                    # Look for flags
                    for flag in flags:
                        if flag in md_content:
                            md_content = respond_flag(md_content, root)

                    # Convert to HTML
                    html_content = convert_md_to_html(md_content, css_filename)
                    html_filename = filename.replace('.md', '.html')
                    html_file_path = os.path.join(target_root, html_filename)

                    # Write the HTML to the new file
                    with open(html_file_path, 'w', encoding='utf-8') as html_file:
                        html_file.write(html_content)
                else:
                    # jpgs and all other types just get coppied.
                    target_file_path = os.path.join(target_root, filename)
                    shutil.copy(source_file_path, target_file_path)

# main
if __name__ == "__main__":
    ensure_dir_empty(output_dir)
    copy_md_structure_and_convert(input_dir, output_dir)
