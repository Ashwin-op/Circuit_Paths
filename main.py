import re
import networkx as nx
from pathlib import Path
import matplotlib.pyplot as plt


def printInfo():
    """
    Prints general information about working of this script
    :return: None
    """
    print('\t' * 6 + 'Combinational Circuit Paths')

    print('-' * 75)

    print('Input: Verilog file with Gate Level Modelling')
    print('Output: All paths from input to output of the circuit described by the Verilog file')
    print('(Optional: Graph of the circuit can also be exported)')

    print('-' * 75, end='\n\n')


def parse_line(data, line, keyword):
    """
    Parse the given line to extract required the information
    :param data: A dictionary to store the parsed information
    :param line: The line to parse
    :param keyword: The type of keyword
    :return: None
    """
    if '[' in line:
        pos = re.search(r'\[(.*)\]', line).group(1).split(':')
        pos = sorted([int(i.strip()) for i in pos])
        for i in range(pos[0], pos[1]):
            for j in re.search(r'\](.*);', line).group(1).split(','):
                data[keyword].append(j.strip() + f'[{i}]')
    else:
        for i in re.search(rf'{keyword}(.*);', line).group(1).split(','):
            data[keyword].append(i.strip())


def parse(filename):
    """
    Parses the Verilog file with the given name to extract details about the Combinational circuit
    :param filename: Name of the file to be parsed
    :return: Dictionary containing information about the Verilog file
    """

    # Copy the content from given file to a local list
    with open(filename, 'r') as fp:
        content = [line for line in (line.strip() for line in fp) if line]

    # Initialize a dictionary to store the parsed data
    data = {
        'module_name': '',
        'input': [],
        'output': [],
        'wire': [],
        'reg': [],
        'connections': []
    }

    # Get module name
    if 'module' in content[0][:7]:
        data['module_name'] = re.search(r'e.*\(', content[0]).group()[1:-1].strip()
    else:
        print("Module name not present!")
        exit(0)

    try:
        for line in content[1:-1]:
            # Get module parameters
            keywords = ['input', 'output', 'wire', 'reg']
            for key in keywords:
                if key in line[:len(key) + 1]:
                    parse_line(data, line, key)

            # Get connections
            if any(x in line[:5] for x in ['nand', 'nor', 'not', 'xor', 'and', 'or', 'xnor']):
                gate = re.search(r' (.*)\(', line).group(1).strip()
                inputs = [s.strip() for s in re.search(r'\((.*)\)', line).group(1).split(',')]
                for i in inputs[1:]:
                    data['connections'].append((i, gate))
                data['connections'].append((gate, inputs[0]))
    except:
        print("Not supported!")
        exit(0)

    return data


def printPaths(graph, data):
    """
    Prints both the meta data of the circuit and all the paths from input to output in the graphical version of the
    circuit
    :param graph: The Graph object of the circuit
    :param data: The data relating to the circuit
    :return: None
    """

    # Printing data related to the circuit
    print(f'Module name: {data["module_name"]}')
    print('Input: ', end='')
    print(*data['input'], sep=', ')
    print('Output: ', end='')
    print(*data['output'], sep=', ')
    print('Wire: ', end='')
    print(*data['wire'], sep=', ', end='\n\n')

    # Printing the paths in the graphical version of the circuit
    print('All paths from input to output')
    for io in [[i, o] for i in data['input'] for o in data['output']]:
        for path in nx.all_simple_paths(graph, source=io[0], target=io[1]):
            print(*path, sep=' --> ')


if __name__ == '__main__':
    printInfo()

    files = Path('tests').glob('*.v')
    for filename in files:
        data = parse(filename)

        # Initializing graph
        G = nx.DiGraph()
        G.add_edges_from(data['connections'])

        # Printing all the paths from input to output
        printPaths(G, data)

        # Draw Graph
        # plt.subplots(tight_layout=False)
        # nx.draw(G, with_labels=True)
        # plt.savefig(f'{str(filename).split(".")[0]}.png')

        print('-' * 75, end='\n\n')
