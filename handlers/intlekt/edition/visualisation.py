from functools import partial

from ieml.ieml_objects.hypertexts import Hyperlink, Hypertext
from ieml.ieml_objects.sentences import Clause, SuperClause
from ieml.ieml_objects.words import Word, Morpheme
from ieml.usl.tools import usl as _usl, usl
from handlers.commons import exception_handler
from ieml.ieml_objects import Term, Sentence, SuperSentence
from ieml.ieml_objects.texts import Text
from models.terms.terms import TermsConnector

word = "[([o.wa.-]+[x.t.-]+[t.a.-k.a.-'])*([c.b.-]+[t.o.-d.o.-s.u.-'])]"
sentence = "[([([E:A:.wu.-]+[o.h.-]+[b.u.-])*([c.b.-]+[t.e.-m.u.-'])]*[([wo.s.-]+[x.t.-]+[t.i.-s.i.-'])*([e.-o.-we.h.-']+[d.i.-m.i.-t.u.-'])]*[([S:M:.]+[x.t.-]+[t.o.-d.o.-s.u.-'])*([wo.s.-]+[n.j.-])])+([([wo.s.-]+[x.t.-]+[t.i.-s.i.-'])*([e.-o.-we.h.-']+[d.i.-m.i.-t.u.-'])]*[([M:O:.j.-]+[e.-o.-we.h.-']+[t.o.-d.o.-s.u.-'])*([c.b.-]+[t.e.-m.u.-'])]*[([b.u.-]+[n.j.-]+[b.e.-s.u.-'])*([t.o.-d.o.-s.u.-']+[n.o.-d.o.-'])])]"
supersentence = "[([([([S:M:.]+[c.b.-]+[t.i.-s.i.-'])*([S:M:.]+[t.a.-k.a.-'])]*[([M:O:.j.-]+[t.o.-d.o.-s.u.-']+[t.a.-k.a.-'])*([o.h.-]+[d.i.-m.i.-t.u.-'])]*[([E:A:.wu.-]+[t.i.-s.i.-']+[n.o.-d.o.-'])*([x.t.-]+[t.o.-d.o.-s.u.-'])])+([([M:O:.j.-]+[t.o.-d.o.-s.u.-']+[t.a.-k.a.-'])*([o.h.-]+[d.i.-m.i.-t.u.-'])]*[([S:M:.]+[c.b.-]+[b.e.-s.u.-'])*([E:B:.b.-]+[n.o.-d.o.-'])]*[([E:A:.wu.-]+[o.wa.-]+[c.b.-])*([t.a.-k.a.-']+[n.o.-d.o.-'])])+([([S:M:.]+[c.b.-]+[b.e.-s.u.-'])*([E:B:.b.-]+[n.o.-d.o.-'])]*[([wo.s.-]+[M:O:.j.-]+[d.i.-m.i.-t.u.-'])*([S:M:.]+[n.j.-])]*[([wo.s.-]+[M:O:.j.-]+[d.i.-m.i.-t.u.-'])*([S:M:.]+[n.j.-])])+([([S:M:.]+[c.b.-]+[b.e.-s.u.-'])*([E:B:.b.-]+[n.o.-d.o.-'])]*[([e.-o.-we.h.-']+[b.e.-s.u.-']+[t.e.-m.u.-'])*([t.o.-d.o.-s.u.-']+[d.i.-m.i.-t.u.-'])]*[([S:M:.]+[b.u.-]+[x.t.-])*([o.h.-]+[t.a.-k.a.-'])])]*[([([E:A:.wu.-]+[t.i.-s.i.-']+[n.o.-d.o.-'])*([x.t.-]+[t.o.-d.o.-s.u.-'])]*[([E:A:.wu.-]+[o.wa.-]+[c.b.-])*([t.a.-k.a.-']+[n.o.-d.o.-'])]*[([S:M:.]+[c.b.-]+[t.i.-s.i.-'])*([S:M:.]+[t.a.-k.a.-'])])+([([E:A:.wu.-]+[t.i.-s.i.-']+[n.o.-d.o.-'])*([x.t.-]+[t.o.-d.o.-s.u.-'])]*[([wo.s.-]+[M:O:.j.-]+[d.i.-m.i.-t.u.-'])*([S:M:.]+[n.j.-])]*[([E:A:.wu.-]+[wo.s.-]+[s.i.-b.i.-t.u.-'])*([E:A:.wu.-]+[o.h.-])])+([([E:A:.wu.-]+[o.wa.-]+[c.b.-])*([t.a.-k.a.-']+[n.o.-d.o.-'])]*[([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])]*[([S:M:.]+[b.u.-]+[x.t.-])*([o.h.-]+[t.a.-k.a.-'])])+([([wo.s.-]+[M:O:.j.-]+[d.i.-m.i.-t.u.-'])*([S:M:.]+[n.j.-])]*[([x.t.-]+[M:O:.j.-]+[d.i.-m.i.-t.u.-'])*([n.j.-]+[n.o.-d.o.-'])]*[([S:M:.]+[b.u.-]+[x.t.-])*([o.h.-]+[t.a.-k.a.-'])])+([([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])]*[([E:B:.b.-]+[wo.s.-]+[n.j.-])*([E:B:.b.-]+[t.i.-s.i.-'])]*[([S:M:.]+[t.e.-m.u.-']+[t.i.-s.i.-'])*([E:B:.b.-]+[b.u.-])])+([([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])]*[([o.wa.-]+[n.j.-]+[M:O:.j.-])*([S:M:.]+[d.i.-m.i.-t.u.-'])]*[([S:M:.]+[t.e.-m.u.-']+[t.i.-s.i.-'])*([E:B:.b.-]+[b.u.-])])]*[([([S:M:.]+[b.u.-]+[x.t.-])*([o.h.-]+[t.a.-k.a.-'])]*[([o.wa.-]+[n.j.-]+[M:O:.j.-])*([S:M:.]+[d.i.-m.i.-t.u.-'])]*[([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])])+([([o.wa.-]+[n.j.-]+[M:O:.j.-])*([S:M:.]+[d.i.-m.i.-t.u.-'])]*[([wo.s.-]+[M:O:.j.-]+[d.i.-m.i.-t.u.-'])*([S:M:.]+[n.j.-])]*[([t.o.-d.o.-s.u.-']+[t.e.-m.u.-']+[t.i.-s.i.-'])*([c.b.-]+[t.e.-m.u.-'])])])+([([([E:A:.wu.-]+[t.i.-s.i.-']+[n.o.-d.o.-'])*([x.t.-]+[t.o.-d.o.-s.u.-'])]*[([E:A:.wu.-]+[o.wa.-]+[c.b.-])*([t.a.-k.a.-']+[n.o.-d.o.-'])]*[([S:M:.]+[c.b.-]+[t.i.-s.i.-'])*([S:M:.]+[t.a.-k.a.-'])])+([([E:A:.wu.-]+[t.i.-s.i.-']+[n.o.-d.o.-'])*([x.t.-]+[t.o.-d.o.-s.u.-'])]*[([wo.s.-]+[M:O:.j.-]+[d.i.-m.i.-t.u.-'])*([S:M:.]+[n.j.-])]*[([E:A:.wu.-]+[wo.s.-]+[s.i.-b.i.-t.u.-'])*([E:A:.wu.-]+[o.h.-])])+([([E:A:.wu.-]+[o.wa.-]+[c.b.-])*([t.a.-k.a.-']+[n.o.-d.o.-'])]*[([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])]*[([S:M:.]+[b.u.-]+[x.t.-])*([o.h.-]+[t.a.-k.a.-'])])+([([wo.s.-]+[M:O:.j.-]+[d.i.-m.i.-t.u.-'])*([S:M:.]+[n.j.-])]*[([x.t.-]+[M:O:.j.-]+[d.i.-m.i.-t.u.-'])*([n.j.-]+[n.o.-d.o.-'])]*[([S:M:.]+[b.u.-]+[x.t.-])*([o.h.-]+[t.a.-k.a.-'])])+([([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])]*[([E:B:.b.-]+[wo.s.-]+[n.j.-])*([E:B:.b.-]+[t.i.-s.i.-'])]*[([S:M:.]+[t.e.-m.u.-']+[t.i.-s.i.-'])*([E:B:.b.-]+[b.u.-])])+([([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])]*[([o.wa.-]+[n.j.-]+[M:O:.j.-])*([S:M:.]+[d.i.-m.i.-t.u.-'])]*[([S:M:.]+[t.e.-m.u.-']+[t.i.-s.i.-'])*([E:B:.b.-]+[b.u.-])])]*[([([S:M:.]+[c.b.-]+[b.e.-s.u.-'])*([E:B:.b.-]+[n.o.-d.o.-'])]*[([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])]*[([o.wa.-]+[c.b.-]+[d.i.-m.i.-t.u.-'])*([o.h.-]+[b.u.-])])+([([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])]*[([E:B:.b.-]+[wo.s.-]+[n.j.-])*([E:B:.b.-]+[t.i.-s.i.-'])]*[([E:A:.wu.-]+[wo.s.-]+[s.i.-b.i.-t.u.-'])*([E:A:.wu.-]+[o.h.-])])+([([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])]*[([wo.s.-]+[M:O:.j.-]+[d.i.-m.i.-t.u.-'])*([S:M:.]+[n.j.-])]*[([t.o.-d.o.-s.u.-']+[t.a.-k.a.-']+[n.o.-d.o.-'])*([S:M:.]+[b.e.-s.u.-'])])+([([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])]*[([M:O:.j.-]+[t.o.-d.o.-s.u.-']+[t.a.-k.a.-'])*([o.h.-]+[d.i.-m.i.-t.u.-'])]*[([o.wa.-]+[c.b.-]+[d.i.-m.i.-t.u.-'])*([o.h.-]+[b.u.-])])]*[([([o.wa.-]+[n.j.-]+[M:O:.j.-])*([S:M:.]+[d.i.-m.i.-t.u.-'])]*[([S:M:.]+[t.e.-m.u.-']+[t.i.-s.i.-'])*([E:B:.b.-]+[b.u.-])]*[([S:M:.]+[c.b.-]+[b.e.-s.u.-'])*([E:B:.b.-]+[n.o.-d.o.-'])])+([([S:M:.]+[t.e.-m.u.-']+[t.i.-s.i.-'])*([E:B:.b.-]+[b.u.-])]*[([S:M:.]+[b.u.-]+[x.t.-])*([o.h.-]+[t.a.-k.a.-'])]*[([S:M:.]+[b.u.-]+[x.t.-])*([o.h.-]+[t.a.-k.a.-'])])])+([([([E:A:.wu.-]+[t.i.-s.i.-']+[n.o.-d.o.-'])*([x.t.-]+[t.o.-d.o.-s.u.-'])]*[([E:A:.wu.-]+[o.wa.-]+[c.b.-])*([t.a.-k.a.-']+[n.o.-d.o.-'])]*[([S:M:.]+[c.b.-]+[t.i.-s.i.-'])*([S:M:.]+[t.a.-k.a.-'])])+([([E:A:.wu.-]+[t.i.-s.i.-']+[n.o.-d.o.-'])*([x.t.-]+[t.o.-d.o.-s.u.-'])]*[([wo.s.-]+[M:O:.j.-]+[d.i.-m.i.-t.u.-'])*([S:M:.]+[n.j.-])]*[([E:A:.wu.-]+[wo.s.-]+[s.i.-b.i.-t.u.-'])*([E:A:.wu.-]+[o.h.-])])+([([E:A:.wu.-]+[o.wa.-]+[c.b.-])*([t.a.-k.a.-']+[n.o.-d.o.-'])]*[([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])]*[([S:M:.]+[b.u.-]+[x.t.-])*([o.h.-]+[t.a.-k.a.-'])])+([([wo.s.-]+[M:O:.j.-]+[d.i.-m.i.-t.u.-'])*([S:M:.]+[n.j.-])]*[([x.t.-]+[M:O:.j.-]+[d.i.-m.i.-t.u.-'])*([n.j.-]+[n.o.-d.o.-'])]*[([S:M:.]+[b.u.-]+[x.t.-])*([o.h.-]+[t.a.-k.a.-'])])+([([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])]*[([E:B:.b.-]+[wo.s.-]+[n.j.-])*([E:B:.b.-]+[t.i.-s.i.-'])]*[([S:M:.]+[t.e.-m.u.-']+[t.i.-s.i.-'])*([E:B:.b.-]+[b.u.-])])+([([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])]*[([o.wa.-]+[n.j.-]+[M:O:.j.-])*([S:M:.]+[d.i.-m.i.-t.u.-'])]*[([S:M:.]+[t.e.-m.u.-']+[t.i.-s.i.-'])*([E:B:.b.-]+[b.u.-])])]*[([([t.o.-d.o.-s.u.-']+[t.a.-k.a.-']+[n.o.-d.o.-'])*([S:M:.]+[b.e.-s.u.-'])]*[([S:M:.]+[c.b.-]+[b.e.-s.u.-'])*([E:B:.b.-]+[n.o.-d.o.-'])]*[([o.wa.-]+[c.b.-]+[d.i.-m.i.-t.u.-'])*([o.h.-]+[b.u.-])])+([([t.o.-d.o.-s.u.-']+[t.a.-k.a.-']+[n.o.-d.o.-'])*([S:M:.]+[b.e.-s.u.-'])]*[([S:M:.]+[t.e.-m.u.-']+[t.i.-s.i.-'])*([E:B:.b.-]+[b.u.-])]*[([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])])+([([t.o.-d.o.-s.u.-']+[t.a.-k.a.-']+[n.o.-d.o.-'])*([S:M:.]+[b.e.-s.u.-'])]*[([b.u.-]+[b.e.-s.u.-']+[t.e.-m.u.-'])*([o.wa.-]+[t.e.-m.u.-'])]*[([t.o.-d.o.-s.u.-']+[t.e.-m.u.-']+[t.i.-s.i.-'])*([c.b.-]+[t.e.-m.u.-'])])+([([t.o.-d.o.-s.u.-']+[t.a.-k.a.-']+[n.o.-d.o.-'])*([S:M:.]+[b.e.-s.u.-'])]*[([c.b.-]+[t.e.-m.u.-']+[t.i.-s.i.-'])*([S:M:.]+[M:O:.j.-])]*[([t.o.-d.o.-s.u.-']+[t.e.-m.u.-']+[t.i.-s.i.-'])*([c.b.-]+[t.e.-m.u.-'])])+([([S:M:.]+[c.b.-]+[b.e.-s.u.-'])*([E:B:.b.-]+[n.o.-d.o.-'])]*[([E:A:.wu.-]+[wo.s.-]+[s.i.-b.i.-t.u.-'])*([E:A:.wu.-]+[o.h.-])]*[([x.t.-]+[M:O:.j.-]+[d.i.-m.i.-t.u.-'])*([n.j.-]+[n.o.-d.o.-'])])]*[([([c.b.-]+[t.e.-m.u.-']+[t.i.-s.i.-'])*([S:M:.]+[M:O:.j.-])]*[([E:A:.wu.-]+[t.i.-s.i.-']+[n.o.-d.o.-'])*([x.t.-]+[t.o.-d.o.-s.u.-'])]*[([S:M:.]+[c.b.-]+[t.i.-s.i.-'])*([S:M:.]+[t.a.-k.a.-'])])+([([c.b.-]+[t.e.-m.u.-']+[t.i.-s.i.-'])*([S:M:.]+[M:O:.j.-])]*[([x.t.-]+[M:O:.j.-]+[d.i.-m.i.-t.u.-'])*([n.j.-]+[n.o.-d.o.-'])]*[([wo.s.-]+[n.j.-]+[d.i.-m.i.-t.u.-'])*([wo.s.-]+[o.h.-])])+([([c.b.-]+[t.e.-m.u.-']+[t.i.-s.i.-'])*([S:M:.]+[M:O:.j.-])]*[([M:O:.j.-]+[t.o.-d.o.-s.u.-']+[t.a.-k.a.-'])*([o.h.-]+[d.i.-m.i.-t.u.-'])]*[([t.o.-d.o.-s.u.-']+[t.a.-k.a.-']+[n.o.-d.o.-'])*([S:M:.]+[b.e.-s.u.-'])])+([([E:A:.wu.-]+[t.i.-s.i.-']+[n.o.-d.o.-'])*([x.t.-]+[t.o.-d.o.-s.u.-'])]*[([e.-o.-we.h.-']+[b.e.-s.u.-']+[t.e.-m.u.-'])*([t.o.-d.o.-s.u.-']+[d.i.-m.i.-t.u.-'])]*[([S:M:.]+[c.b.-]+[b.e.-s.u.-'])*([E:B:.b.-]+[n.o.-d.o.-'])])+([([e.-o.-we.h.-']+[b.e.-s.u.-']+[t.e.-m.u.-'])*([t.o.-d.o.-s.u.-']+[d.i.-m.i.-t.u.-'])]*[([E:A:.wu.-]+[wo.s.-]+[s.i.-b.i.-t.u.-'])*([E:A:.wu.-]+[o.h.-])]*[([t.o.-d.o.-s.u.-']+[t.a.-k.a.-']+[n.o.-d.o.-'])*([S:M:.]+[b.e.-s.u.-'])])])]"

def sample_usls(n, language='EN'):
    return [
        {"ieml" : word, "title" : "Exemple de mot"},
        {"ieml" : sentence, "title" : "Exemple de phrase"},
        {"ieml" : supersentence, "title" : "Exemple de superphrase"}
    ]


def recent_usls(n, language='EN'):
    return []

@exception_handler
def usl_to_json(usl):
    u = _usl(usl["usl"])
    def _walk(u, start=True):
        if isinstance(u, Term):
            return {
                'type': u.__class__.__name__.lower(),
                'script': str(u.script),
                'singular_sequences': [str(s) for s in u.script.singular_sequences],
                'title': {'en':TermsConnector().get_term(u.script)['TAGS']['EN'],
                          'fr':TermsConnector().get_term(u.script)['TAGS']['FR']}
            }
        if start and len(u.children) == 1:
            return _walk(u.children[0])

        def _build_tree(transition, children_tree, supersentence=False):
            result = {
                'type': 'supersentence-node' if supersentence else 'sentence-node',
                'mode': _walk(transition[1].mode, start=False),
                'node': _walk(transition[0], start=False),
                'children': []
            }
            if transition[0] in children_tree:
                result['children'] = [_build_tree(c, children_tree, supersentence=supersentence) for c in children_tree[transition[0]]]
            return result

        if isinstance(u, Sentence):
            result = {
                'type': 'sentence-root-node',
                'node': _walk(u.tree_graph.root, start=False),
                'children': [
                    _build_tree(c, u.tree_graph.transitions) for c in u.tree_graph.transitions[u.tree_graph.root]
                ]
            }
        elif isinstance(u, SuperSentence):
            result = {
                'type': 'supersentence-root-node',
                'node': _walk(u.tree_graph.root, start=False),
                'children': [
                    _build_tree(c, u.tree_graph.transitions, supersentence=True) for c in u.tree_graph.transitions[u.tree_graph.root]
                    ]
            }
        else:
            result = {
                'type': u.__class__.__name__.lower(),
                'children': [_walk(c, start=False) for c in u]
            }

        return result

    return _walk(u.ieml_object)


def _tree_node(json, constructor):
    result = []
    for child in json['children']:
        result.append(
            constructor(substance=_json_to_ieml(json['node']),
                        attribute=_json_to_ieml(child['node']),
                        mode=_json_to_ieml(child['mode'])))
        result.extend(_tree_node(child, constructor))
    return result


def _children_list(constructor, json):
    return constructor(children=list(_json_to_ieml(c) for c in json['children']))

type_to_action = {
    Term.__name__.lower(): lambda json: Term(json['script']),
    'sentence-root-node': lambda json: Sentence(_tree_node(json, Clause)),
    'supersentence-root-node': lambda json: SuperSentence(_tree_node(json, SuperClause)),
    'sentence-node': lambda json: Sentence(_tree_node(json, Clause)),
    'supersentence-node': lambda json: SuperSentence(_tree_node(json, SuperClause)),
}
for cls in (Morpheme, Word, Text, Hyperlink, Hypertext):
    type_to_action[cls.__name__.lower()] = partial(_children_list, cls)


def _json_to_ieml(json):
    try:
        return type_to_action[json['type']](json)
    except KeyError as k:
        raise ValueError("The node of type %s was unexpected. Invalid json structure."%str(k))

@exception_handler
def json_to_usl(json):
    """Convert a json representation of an usl to the usl object and return the ieml string."""
    return str(usl(_json_to_ieml(json['json'])))