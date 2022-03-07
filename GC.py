from GC_utils import CStree

# Read the file and extract the num of color and edges for the graph.
num_color = 0
edges = []
with open("data.txt", "r") as f:
    data = f.readlines()
    for line in data:
        try:
            if line[0] == '#':
                continue
            if '=' in line:
                num_color = int(line.split('=')[1])
            if ',' in line:
                edge = (int(line.split(',')[0]), int(line.split(',')[1]))
                edges.append(edge)
        except IOError:
            print("Error: invalid input")

# Set the constrained search tree by the file's information
cstree = CStree(edges, num_color)
if cstree.finished_node != None:
    result_state = cstree.finished_node.state
    print('The coloring dictionary is: {}.'.format(result_state))
    cstree.visualization()
else:
    print('Can not solve this puzzle.')