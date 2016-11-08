import random

import itertools

import functools

from ieml.ieml_objects.commons import IEMLObjects
from ieml.ieml_objects.exceptions import InvalidIEMLObjectArgument
from ieml.ieml_objects.parser.parser import IEMLParser
from ieml.ieml_objects.paths import IEMLPath
from ieml.ieml_objects.terms import Term
from ieml.script.operator import script

from ieml.ieml_objects.sentences import Sentence, Clause, SuperSentence, SuperClause
from ieml.ieml_objects.texts import Text
from ieml.ieml_objects.words import Word, Morpheme
from ieml.ieml_objects.exceptions import CantGenerateElement


def ieml(arg):
    if isinstance(arg, IEMLObjects):
        return arg

    if isinstance(arg, str):
        return IEMLParser().parse(arg)

    raise ValueError("Invalid argument, c'ant instantiate an IEMLObject from %s."%str(arg))


def _loop_result(max_try):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ex = None
            for i in range(max_try):
                try:
                    return func(*args, **kwargs)
                except InvalidIEMLObjectArgument as e:
                    ex = e
                    continue

            raise CantGenerateElement(str(ex))
        return wrapper
    return decorator


class RandomPoolIEMLObjectGenerator:
    def __init__(self, level=Text, pool_size=20):
        self.level = level
        self.pool_size = pool_size

        if level > Text:
            raise ValueError('Cannot generate object higher than a Text.')

        self._build_pools()

        self.type_to_method = {
            Term: self.term,
            Word: self.word,
            Sentence: self.sentence,
            SuperSentence: self.super_sentence,
            Text: self.text
        }

    def _build_pools(self):
        """
        Slow method, retrieve all the terms from the database.
        :return:
        """
        from models.terms.terms import TermsConnector as tc
        self.terms_pool = set(Term(script(t['_id'])) for t in tc().get_all_terms()[:self.pool_size])

        if self.level >= Word:
            # words
            self.words_pool = set(self.word() for i in range(self.pool_size))

        if self.level >= Sentence:
            # sentences
            self.sentences_pool = set(self.sentence() for i in range(self.pool_size))

        if self.level >= SuperSentence:
            self.super_sentences_pool = set(self.super_sentence() for i in range(self.pool_size))

        if self.level >= Text:
            self.propositions_pool = set(itertools.chain.from_iterable((self.words_pool, self.sentences_pool, self.super_sentences_pool)))

        # self.hypertext_pool = set(self.hypertext() for i in range(self.pool_size))

    @_loop_result(10)
    def term(self):
        return random.sample(self.terms_pool, 1)[0]

    @_loop_result(10)
    def word(self):
        return Word(Morpheme(random.sample(self.terms_pool, 3)), Morpheme(random.sample(self.terms_pool, 2)))

    def _build_graph_object(self, primitive, mode, object, max_nodes=6):
        nodes = {primitive()}
        modes = set()

        if max_nodes < 2:
            raise ValueError('Max nodes >= 2.')

        result = set()

        for i in range(random.randint(2, max_nodes)):
            while True:
                s, a, m = random.sample(nodes, 1)[0], primitive(), mode()
                if a in nodes or m in nodes or a in modes:
                    continue

                nodes.add(a)
                modes.add(m)

                result.add(object(s, a, m))
                break
        return result

    @_loop_result(10)
    def sentence(self, max_clause=6):
        def p():
            return random.sample(self.words_pool, 1)[0]

        return Sentence(self._build_graph_object(p, p, Clause, max_nodes=max_clause))

    @_loop_result(10)
    def super_sentence(self, max_clause=4):
        def p():
            return random.sample(self.sentences_pool, 1)[0]

        return SuperSentence(self._build_graph_object(p, p, SuperClause, max_nodes=max_clause))

    @_loop_result(10)
    def text(self):
        return Text(random.sample(self.propositions_pool, random.randint(1, 8)))

    # def hypertext(self):
    #     def text():
    #         return random.sample(self.text_pool, 1)[1]
    #
    #
    #
    #     return Hypertext(self._build_graph_object(text, , SuperSentence))


    def from_type(self, type):
        try:
            return self.type_to_method[type]()
        except KeyError:
            raise ValueError("Can't generate that type or not an IEMLObject : %s"%str(type))


def replace_from_paths(ieml_obj, paths, elements):
    """
    Replace the elements in the argument ieml_obj at the given paths with the
    elements in argument.
    Each path will be replaced with the corresponding ieml_object in elements, then the two index-able collections
    must be the same length.
    This function return a new ieml_object as the ieml_object are immutable.
    :param ieml_obj: the ieml object to replace
    :param paths: the paths in ieml_obj pointing to the elements to replace
    :param elements: the new ieml_object to put in ieml_obj
    :return: A new ieml-object if there are replacement, otherwise the same
    """

    if not isinstance(ieml_obj, IEMLObjects):
        raise ValueError('The ieml_obj argument must be a ieml_obj or a path is not pointing to an ieml_object '
                         'instance.')

    if len(elements) != len(paths):
        raise ValueError('The list of path argument and the list of element to replace '
                         'must be the same length (%d != %d)'%(len(paths), len(elements)))

    if not paths:
        return ieml_obj

    if any(len(p) == 0 for p in paths):
        index = [i for i, v in enumerate(paths) if len(v) == 0]
        if len(index) > 1:
            raise ValueError("Multiple paths are pointing to the same elements %s."%str(ieml_obj))
        return elements[index[0]]

    if isinstance(ieml_obj, Term):
        return ieml_obj

    def clamp(paths, elems, child):
        # get the paths, elems that are involving this child (paths[0] == child)
        result = list(zip(*[[p[1:], elems[i]] for i, p in enumerate(paths) if str(p[0]) == str(child)]))

        return result if result else [[], []]

    try:
        return ieml_obj.__class__(children=[replace_from_paths(c, *clamp(paths, elements, c)) for c in ieml_obj.children])
    except InvalidIEMLObjectArgument as e:
        raise ValueError('Invalid replacement, the resulting ieml is not valid.') from e

def build_paths(paths):
    if not isinstance(paths, IEMLPath):
        raise ValueError("Paths must be an IEMLPath instances.")



if __name__ == '__main__':
    r = RandomPoolIEMLObjectGenerator(Text)
    print(str(r.sentence()))