
import yaml
import os.path
import functools
import networkx as nx
import matplotlib.pyplot as plt
import networkx.drawing.layout as l
from collections import Counter

ingredients = yaml.load(open('ingredients.yml'), Loader=yaml.CLoader)

terminals = []
for part in ingredients:
    for subpart in ingredients[part]:
        if subpart not in ingredients and subpart not in terminals:
            terminals.append(subpart)
#print("Terminals: " + str(terminals))

frequency = []
for partname in ingredients:
    frequency += ingredients[partname]

f = open('histogram.txt', 'w')
counts = Counter(frequency)
for k, count in counts.most_common():
    print("%27s" % (k,), count * '*', file=f)
f.close()

f = open('non-ingredient-parts.yml', 'w')
non_ingredients = [ x for x in ingredients if not x in frequency ]
print(yaml.dump(non_ingredients, Dumper=yaml.CDumper), file=f)
f.close()

important = { x: ingredients[x] for x in ingredients if x not in non_ingredients }
#print(yaml.dump(important, Dumper=yaml.CDumper))

def _get_all_ingredients(part, ing):
    if part in ingredients:
        for subpart in ingredients[part]:
            if not subpart in ing:
                ing.append(subpart)
                _get_all_ingredients(subpart, ing)
    return ing

def get_all_ingredients(part):
    return _get_all_ingredients(part, [])

def partsort(a, b):
    aing = [a] + get_all_ingredients(a)
    bing = [b] + get_all_ingredients(b)
    v = 0
    for a in aing:
        v = v - 1 if a in bing else v + 1
    for b in bing:
        v = v + 1 if b in aing else v - 1
    #print(str(aing) + " <~> " + str(bing) + ": " + str(v))
    return v

def sortparts(a):
    return sorted(a, key=functools.cmp_to_key(partsort))

def sortedparts(part):
    return sortparts(get_all_ingredients(part))

def get_ingredients_recursive(part):
    ing = {}
    if part in ingredients:
        for subpart in ingredients[part]:
            sub = get_ingredients_recursive(subpart)
            ing[subpart] = sub
    if len(ing) == 0: ing = "<~"
    return ing

def dump(v):
    print(yaml.dump(v, Dumper=yaml.CDumper))

class Node:

    def __init__(self, part):
        self.input_types = [] if part in terminals else ingredients[part]
        self.output_type = part
        self.inputs = {}
        self.outputs = []

    def connect_input(self, node):
        assert node.output_type in self.input_types
        if node.output_type in self.inputs: return
        self.inputs[node.output_type] = node
        node.connect_output(self)

    def connect_output(self, node):
        assert self.output_type in node.input_types
        if node in self.outputs: return
        self.outputs.append(node)
        node.connect_input(self)

    def find(self, part):
        if self.output_type == part: return self
        for t in self.input_types:
            test = self.inputs[t].find(part) if t in self.inputs else None
            if test is not None: return test
        return None

    def connect(self, root):
        for inp in self.input_types:
            node = root.find(inp)
            if node is None:
                node = Node(inp)
                node.connect(root)
            self.connect_input(node)

    def tostr(self, depth=0):
        sval = (" " * (depth*2)) + "<- " + self.output_type
        for i in self.inputs:
            sval += "\n"
            sval += self.inputs[i].tostr(depth+1)
        return sval

    def __str__(self):
        return self.tostr()

    def _graph(self, output):
        for x in self.inputs:
            output.append((x, self.output_type))
            self.inputs[x]._graph(output)
        return output

    def graph(self):
        return self._graph([])

def makenode(part):
    n = Node(part)
    n.connect(n)
    return n

def printpartinfo(part):
    print("------------------- " + str(part) + " -------------------")
    #rec = get_ingredients_recursive(part)
    #print(yaml.dump({ "ingredients": rec }, Dumper=yaml.CDumper))
    print(str(sortedparts(part)))
    n = makenode(part)
    print(str(n))
    #parts = sortedparts(part)
    #forest = []
    #for p in parts:
    #    if p in terminals: forest.append(Node(p))
    #for root in forest:
    #    for p in parts:
    #        if not p in terminals: root.connect(p)
    #    root.connect(part)
    #for root in forest:
    #    for p in parts:
    #        if root in get_ingredients_recursive(p):
    #            forest[root][p] = {}       
    #dump(forest)

#printpartinfo("nuclear-reactor")

def plot(part):
    n = makenode(part)

    proc = n.graph()

    G = nx.Graph()
    G.add_edges_from(proc)

    # TODO: can this be done without reading and writing a file?
    nx.write_edgelist(G, path="grid.edgelist", delimiter=":")
    H = nx.read_edgelist(path="grid.edgelist", delimiter=":")
    os.unlink("grid.edgelist")
    layout = l.kamada_kawai_layout(G, pos=l.shell_layout(G))

    nx.draw(
      H,
      pos=layout,
      edge_color="#777777",
      node_color="#ffffff",
      with_labels=True,
      font_family="Arial",
      font_size=9,
      label=part,
    )
    #plt.show()
    if not os.path.isdir('output'): os.makedirs('output')
    path = os.path.join('output', part + '.svg')
    plt.savefig(path, format="svg")
    plt.close()

for part in important: plot(part)
