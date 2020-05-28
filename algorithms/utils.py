import os

BASE_PATH = os.path.dirname(os.path.abspath(__name__))

DATA_PATH = os.path.join(BASE_PATH, 'data')

def explorer(file_name):
    """A simple defintion for getting files from the
    data directory
    """
    if not file_name.endswith('.csv'):
        file_name = file_name + '.csv'
        
    path_to_return = {'result': 'Not found'}
    files = list(os.walk(DATA_PATH))
    for file in files:
        current_files = file[2]
        if file_name in current_files:
            path_to_return = os.path.join(DATA_PATH, file_name)
            break
    return path_to_return        
