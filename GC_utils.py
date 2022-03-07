import igraph as ig
import numpy as np
import copy

# sort array-like data by frequency
def sortbyfreq(arr):
    if arr == []:
        return []
    counts = {n: list(arr).count(n) for n in set(arr)}
    return sorted(list(set(arr)), key=lambda n: -counts[n])

# an iteration for sort the variable as minimum remaining values
class Vairables_iter:
    def __init__(self, state, edges):

        # Sort variable by minimum remaining values
        variables = [variable for variable in state if len(state[variable]) > 1]
        num_colors = {n: len(state[n]) for n in set(variables)}
        self.variables = sorted(variables, key=lambda n: num_colors[n])

        # # dictionary for number of minimum remaining values (MRV)
        # variables = [variable for variable in state if len(state[variable]) > 1]
        # num_colors = {n: len(state[n]) for n in set(variables)}
        #
        # # dictionary for number of involved constrains
        # graph = ig.Graph(edges)
        # degrees = {v.index: v.degree() for v in graph.vs}
        #
        # # Sorted variables by two dictionary (MRV has more weight)
        # self.variables = sorted(variables, key=lambda n: (100 * num_colors[n]) - degrees[n])

    def __iter__(self):
        self.index = 0
        return self
    def __next__(self):
        if self.index < len(self.variables):
            x = self.index
            self.index += 1
            return self.variables[x]
        else:
            return -1

# the node class, each node contains a graph
class Node:
    def __init__(self, state=None, edges = None):
        self.used_colors = sortbyfreq([state[variable][0] for variable in state if len(state[variable]) == 1]) # sorted used colors list by frequency

        self.state = self.sort_colors(state) # sort colors traversing priority for each variable
        self.color_count = 0 # current traversing color index
        self.iter_variables = iter(Vairables_iter(state, edges))
        self.current_variable = next(self.iter_variables)
        self.parent = None
        self.children = []
        self.graph = ig.Graph(edges)
        self.AC_3(edges)

    def AC_3(self, edges):
        edges_check = copy.deepcopy(edges)
        while len(edges_check) != 0:
            X_i, X_j = edges_check.pop(0)
            if self.remove_inconsistent_values(X_i, X_j):
                for X_k in self.graph.neighbors(X_i):
                    if not ((X_k, X_i) in edges_check or (X_i, X_k) in edges_check):
                        edges_check.append((X_k, X_i))
            if self.remove_inconsistent_values(X_j, X_i):
                for X_k in self.graph.neighbors(X_j):
                    if not ((X_k, X_j) in edges_check or (X_j, X_k) in edges_check):
                        edges_check.append((X_k, X_j))

    def remove_inconsistent_values(self, X_i, X_j):
        removed = False
        for index, x in enumerate(self.state[X_i]):
            if len(self.state[X_j]) == 1 and self.state[X_j][0] == x:
                self.state[X_i] = np.delete(self.state[X_i], index)
                removed = True
        return removed

    def sort_colors(self, state):
        for variable in state:
            if len(state[variable]) <= 1:
                continue
            else:
                state[variable] = np.unique(np.append([color for color in self.used_colors if color in state[variable]], state[variable]))
        return state

    def check_failed(self):
        for value in self.state.values():
            if len(value) == 0:
                return True
        return False
    def can_expand(self):
        if self.current_variable == -1:
            return False
        if self.color_count >= len(self.state[self.current_variable]):
            self.current_variable = next(self.iter_variables)
            self.color_count = 0
        if self.current_variable != -1:
            return True
        return False
    def check_success(self):
        if np.sum([True for value in self.state.values() if len(value) != 1])>0:
            return False
        return True


# the constrained search tree for backtracking, the finished node contained the solution
class CStree:
    def __init__(self, edges, num_color):
        colors = np.array(range(num_color))
        variables = np.unique(edges)
        root_state ={var: colors for var in variables}

        self.variables = variables
        self.edges = edges
        self.colors = np.array(range(num_color))
        self.root_node = Node(state=root_state, edges=self.edges)
        self.finished_node = None
        try:
            self.expanding_tree(self.root_node)
        except RecursionError as error:
            print(error)

    # recursive function to expand the tree
    def expanding_tree(self, node):
        if node.check_failed():
            if node.parent == None:
                return
            self.expanding_tree(node.parent)
        if node.check_success():
            for variable in node.state:
                node.state[variable] = node.state[variable][0]
            self.finished_node = node
            return
        if node.can_expand():
            new_state = copy.deepcopy(node.state)
            new_state[node.current_variable] = [new_state[node.current_variable][node.color_count]]
            node.color_count += 1
            new_node = Node(state=new_state, edges=self.edges)
            node.children.append(new_node)
            new_node.parent = node
            self.expanding_tree(new_node)
        else:
            if node.parent == None:
                return
            self.expanding_tree(node.parent)

    # a visualization function to visualize the finished node's graph.
    def visualization(self):
        if self.finished_node == None:
            print('Can not visualize the graph')
        else:
            result_state = self.finished_node.state

            graph = self.finished_node.graph
            colors = ['blue', 'red', 'green', 'yellow', 'purple', 'grey', 'orange']
            for vert in graph.vs:
                if vert.index not in result_state.keys():
                    graph.delete_vertices(vert.index)
                    continue
                index_color = int(result_state[vert.index])
                vert['color'] = colors[index_color]
            layout = graph.layout("auto")
            visual_style = {}
            visual_style["vertex_size"] = 80
            visual_style["layout"] = layout
            visual_style["bbox"] = (2000, 2000)
            visual_style["margin"] = 200
            ig.plot(graph, **visual_style)



