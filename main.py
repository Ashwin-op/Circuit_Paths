import re
import networkx as nx
from pathlib import Path
import matplotlib.pyplot as plt


def printInfo():
    """
    Prints general information about working of this script
    :return: None
    """
    print('\t\t\tCombinational Circuit Paths')

    print('-' * 75)

    print('Input: Verilog file with Gate Level Modelling')
    print('Output: All paths from input to output of the circuit described by the Verilog file')
    print('(Optional: Graph of the circuit can also be exported)')

    print('-' * 75, end='\n')


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
        'wires': [],
        'reg': [],
        'connections': []
    }

    # Get module name
    for line in content:
        if 'module' in line[:7]:
            data['module_name'] = re.search(r'e.*\(', line).group()[1:-1].strip()
            break

    for line in content:
        # Get input terminals
        if 'input' in line[:6]:
            for i in re.search(r't.*;', line).group()[1:-1].strip().split(','):
                data['input'].append(i.strip())

        # Get output terminals
        if 'output' in line[:7]:
            for i in re.search(r't.*;', line).group()[4:-1].strip().split(','):
                data['output'].append(i.strip())

        # Get intermediate wires
        if 'wire' in line[:5]:
            for i in re.search(r'e.*;', line).group()[1:-1].strip().split(','):
                data['wires'].append(i.strip())

        # Get intermediate reg
        if 'reg' in line[:4]:
            for i in re.search(r'g.*;', line).group()[1:-1].strip().split(','):
                data['wires'].append(i.strip())

        # Get connections
        if any(x in line[:5] for x in ['nand', 'nor', 'not', 'xor', 'and', 'or']):
            output = re.search(r' .*\(', line).group()[:-1].strip().split()[0]
            inputs = [s.strip() for s in re.search(r'\(.*\)', line).group()[1:-1].split(',')]
            data['connections'].append((inputs[1], output))
            data['connections'].append((inputs[2], output))
            data['connections'].append((output, inputs[0]))

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
    print(*data['output'], sep=', ', end='\n')

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
