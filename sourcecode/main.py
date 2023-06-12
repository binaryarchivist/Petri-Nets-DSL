from logic import code2AST
from graph_renderer import GraphRenderer
from os import getcwd
import sys, getopt

help = """
PETRINET DSL HELP MENU

python main.py <inputfile> -args...

-h                          help
-n                          name file, default: petrinet
-d                          directory to put in the files from relative terminal
-i                          input relative path from terminal
-g                          generate outcome tree
args:                       cluster, separated

-f                          file format
args:                       png, svg, pdf...

--graphviz                  generate .gv file
--reocurring-tokens         not ignore already occuring tokens
"""

try:
    filepath = sys.argv[1]
except:
    raise ValueError("No arguments given")

if len(sys.argv) > 1:
    opts, args = getopt.getopt(sys.argv[2:] ,'hn:o:i:g:f:', ['graphviz','view','reoccuring-tokens'])

name = 'petrinet'
outpath = getcwd()
file_format = 'png'
graphviz = False
view = False
reoccuring_tokens = False
token_tree_type = None

for opt, arg in opts:
    if opt == '-h':
        print(help)
        sys.exit()
    elif opt == '-n':
        name = arg
    elif opt == '-o':
        outpath = arg
    elif opt == '-i':
        filepath = arg
    elif opt == '-g':
        token_tree_type = arg
    elif opt == '-f':
        file_format = arg
    elif opt == '--graphviz':
        graphviz = True
    elif opt == '--view':
        view = True
    elif opt == '--reoccuring-tokens':
        reoccuring_tokens = True

input = open(filepath, 'r').read()

AST = code2AST(input)
gr = GraphRenderer(AST)
if token_tree_type:
    gr.TokenTree2Graph(token_tree_type=token_tree_type, 
                    name=name, 
                    path=outpath, 
                    format=file_format, 
                    allow_reoccuring_tokens=reoccuring_tokens)
else:
    gr.AST2Graph(name=name,
                 path=outpath,
                 format=file_format)