import io

def get_cell_inputs(file_path):
    from nbformat import current
    with io.open(file_path) as f:
        nb = current.read(f, 'json')

        ip = get_ipython()
        ret = []
        for cell in nb.worksheets[0].cells:
            if cell.cell_type != 'code':
                continue
            ret.append(cell.input)
    return ret

def get_colab_cells():

    # Load the notebook JSON.
    from google.colab import _message
    nb = _message.blocking_request('get_ipynb')

    # Search for the markdown cell with the particular contents.
    return ["".join(cell['source']) for cell in nb['ipynb']['cells']]


def get_cells():
    if 'google.colab' in str(get_ipython()):
        cells = get_colab_cells()
    else:
        print('Source code upload not support!')
        cells = []

    return cells
