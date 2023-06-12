from logic import AST2PetriNet
from graphviz import Digraph
from os import remove, rename, getcwd
from tree import Node

def format_ammount(amm: int):
    if amm == 0:
        return ""
    else:
        return str(amm)

def format_weight(weight: int):
    if weight == 1:
        return None
    else:
        return str(weight)

def format_var(var:str, cap=""):
    if cap == float("inf"):
        cap = ""
    if "_" in var:
        vars = var.split('_')
        return f"<<B>{vars[0]}<sub>{vars[1]}</sub></B> {cap}>"
    else:
        return f"<<B>{var}</B> {cap}>"

def graph_render(G: Digraph, directory, engine, format,  graphviz=False):
    G.render(directory=directory, engine=engine, format=format)
    if not graphviz:
        remove(f"{directory}/{G.name}.gv")
    rename(f"{directory}/{G.name}.gv.png", f"{directory}/{G.name}.png")


class GraphRenderer:

    def __init__(self, AST):
        self.AST = AST
        self.petrinet = AST2PetriNet(AST)

    def AST2Graph(self, name='petrinet', format='png', engine='dot', path=getcwd()):

        G = Digraph(name)
        G.graph_attr.update({'rankdir': 'LR'})
        for place, attr in self.AST["place"].items():
            G.node(place,
                    label=format_ammount(attr["amm"]), 
                    xlabel=format_var(place,attr["cap"]), 
                    shape="circle")

        for tran in self.AST["tran"]:
            G.node(tran, 
                    label=format_var(tran), 
                    shape="box")

        for arc in self.AST["arc_in"]:
            G.edge(arc["source"]["var"],
                    arc["destination"]["var"], 
                    label=format_weight(arc["weight"]))

        for arc in self.AST["arc_out"]:
            G.edge(arc["source"]["var"], 
                    arc["destination"]["var"], 
                    label=format_weight(arc["weight"]))
        
        graph_render(G, directory=path, format=format, engine=engine)
        return G

    def TokenTree2Graph(self, token_tree_type, name='petrinet', path=getcwd(), engine='dot', format='png', allow_reoccuring_tokens=False) -> None:

        token_tree = self.petrinet.build_token_tree(allow_reoccuring_tokens=allow_reoccuring_tokens)

        if token_tree_type == 'separated':

            G_list = []
            def preorder_traversal(node: Node, number=0):
                node.tree_index = number

                G = Digraph(name=f"{name}{number}")
                G.attr(label=f"{name}{number}")
                G.graph_attr.update({'rankdir': 'LR'})
                for place, attr in self.AST["place"].items():
                    G.node(f"{number}{place}",
                            label=format_ammount(node.M.item(attr["ID"])), 
                            xlabel=format_var(place,attr["cap"]), 
                            shape="circle")

                for tran in self.AST["tran"]:
                    G.node(f"{number}{tran}", 
                            label=format_var(tran), 
                            shape="box")

                for arc in self.AST["arc_in"]:
                    G.edge(f'{number}{arc["source"]["var"]}',
                            f'{number}{arc["destination"]["var"]}', 
                            label=format_weight(arc["weight"]))

                for arc in self.AST["arc_out"]:
                    G.edge(f'{number}{arc["source"]["var"]}', 
                            f'{number}{arc["destination"]["var"]}', 
                            label=format_weight(arc["weight"]))                

                G_list.append(G)

                for subnode in node.subnodes:
                    number += 1
                    number = preorder_traversal(subnode, number)

                return number
            
            preorder_traversal(token_tree)
            for graph in G_list:
                graph_render(graph, directory=path, engine=engine, format=format) 
                     
        elif token_tree_type == 'cluster':

            def preorder_traversal(node: Node, parent:Digraph=None, parent_no:int=0, number=0):
                node.tree_index = number

                with g.subgraph(name=f"cluster{name}{number}") as c:
                    
                    c.graph_attr.update({'rankdir': 'LR'})
                    c.attr(label=f"{name}{number}")
                    for place, attr in self.AST["place"].items():
                        c.node(f"{number}{place}",
                                label=format_ammount(node.M.item(attr["ID"])), 
                                xlabel=format_var(place,attr["cap"]), 
                                shape="circle")

                    for tran in self.AST["tran"]:
                        c.node(f"{number}{tran}", 
                                label=format_var(tran), 
                                shape="box")

                    for arc in self.AST["arc_in"]:
                        c.edge(f'{number}{arc["source"]["var"]}',
                                f'{number}{arc["destination"]["var"]}', 
                                label=format_weight(arc["weight"]))

                    for arc in self.AST["arc_out"]:
                        c.edge(f'{number}{arc["source"]["var"]}', 
                                f'{number}{arc["destination"]["var"]}', 
                                label=format_weight(arc["weight"]))                
                    if parent:
                        g.edge(f"{parent_no}{self.AST['places'][0]}", f"{number}{self.AST['places'][0]}", ltail=parent.name, lhead=c.name)

                    temp = number
                    for subnode in node.subnodes:
                        number += 1
                        number = preorder_traversal(subnode, c, temp, number)

                return number
            
            g = Digraph(name=name)
            g.attr(compound="true")
            g.graph_attr.update({'rankdir': 'LR'})
            preorder_traversal(token_tree)
            graph_render(g, directory=path, engine=engine, format=format)
        else:
            raise ValueError(f"{token_tree_type} from argument -g is not a valid token tree representation type.")