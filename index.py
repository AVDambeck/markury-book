
"""
get the target dir.
see if an index exists
    1. create
    2. append
    3. overwrite
look for everything that would get a link
put it in the index.
"""

target_dir = '/path/to/fir/'
mode = 1

def check_for_index(dir):
    index_path = f'{dir}/index.md'
    if os.path.exists(index_path):
        if mode == 1:
            print(f'{index_path} already exists.')
            exit()
        if mode == 3:
            try:
                os.remove(index_path)
            except Exception as e:
                print(f"An error occurred while deleting: {e}")
                exit()
    else:
        return False


