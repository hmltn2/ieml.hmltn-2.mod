from ieml.AST.terms import Term
from ieml.script.tables import generate_tables
from ieml.operator import sc
from collections import namedtuple
from ieml.script.constants import AUXILIARY_CLASS, VERB_CLASS, NOUN_CLASS
from models.terms import TermsConnector
import numpy as np

ScoreNode = namedtuple('ScoreNode', ['script', 'score'])


def rank_paradigms(paradigms_list, usl_list):
    """

    :param paradigms_list: list of all the root paradigms in our database
    :param usl_list: the usl collection we want to analyse
    :return:the ordered list of the root paradigms the most cited by the usl_list,
    first element of the list is the most cited root paradigm, and the dictionary of paradigms which associates a list
    list[0] : score of thr root paradigm, list[1] : number of noun citing the root paradigm
    list[2] : number of aux citing the root paradigm, list[3] : number of verb citing the root paradigm
    """
    paradigms = {p:[0,0,0,0] for p in paradigms_list}
    #paradigms = {p:0 for p in paradigms_list}
    # value is a list of 4 elements which correspond to :
    # a- how many times the root paradigm p is cited
    # b- number of noun citing p
    # c- number of auxiliary citing p
    # d- number of verb citing p
    # so a = b + c + d

    for usl in usl_list:
        term_list = [term for term in usl.tree_iter() if isinstance(term, Term)]
        for term in term_list:
            for paradigm in paradigms_list:
                p_term = Term(sc(paradigm))
                if set(term.script.singular_sequences) <= set(p_term.script.singular_sequences):
                    paradigms[paradigm][0] += 1
                    # verifify the grammatical of the term citing the root paradigm
                    if term.grammatical_class == NOUN_CLASS:
                        paradigms[paradigm][1] += 1
                    elif term.grammatical_class == AUXILIARY_CLASS:
                        paradigms[paradigm][2] += 1
                    elif term.grammatical_class == VERB_CLASS:
                        paradigms[paradigm][3] += 1


    # we remove the root paradigms which are not cited by usl_list
    for p in paradigms_list:
        if paradigms[p][0] == 0:
       # if paradigms[p] == 0:
            del paradigms[p]

    return sorted(paradigms, key= lambda e: paradigms[e][0], reverse=True), paradigms


# 3 Pour chaque paradigme-racine, une liste ordonnée des USLs qui le citent le plus
def rank_usls(paradigms_list, usl_list):
    """

    :param paradigms_list: list of the root paradigms we want to analyse
    :param usl_list: list of the uls (a collection) we want to analyse
    :return:a dictionary whose keys are the paradigms of paradigms_list
    and the values : an ordered list of the usls (of usl_list) which most quote the paradigm
     (first element is usl which quotes the most the paradigm in key), the usls are converted into strings
     if in usl_list there is the same usl twice, in the returned dictionary this usl will appear only once
    """
    paradigm_dico = {p:[] for p in paradigms_list}
    for p in paradigms_list:
        p_term = Term(sc(p))
        usl_dico = {str(usl):0 for usl in usl_list}  # convert usl to string, to use a dictionary
        for usl in usl_list:
            term_list = [term for term in usl.tree_iter() if isinstance(term, Term)]
            for term in term_list:
                if set(term.script.singular_sequences) <= set(p_term.script.singular_sequences):
                    usl_dico[str(usl)] += 1

        # we remove the usls which do not quote the paradigm p
        for usl in usl_list:
            if str(usl) in usl_dico and usl_dico[str(usl)] == 0:
                del usl_dico[str(usl)]

        sorted_usls = sorted(usl_dico, key= lambda e: usl_dico[e], reverse=True)  #  this is a list
        for e in sorted_usls:
            paradigm_dico[p].append(e)

    return paradigm_dico


def rank_usl_terms(term_list, usl_list):

    usl_id_map = {usl: i for i, usl in enumerate(usl_list)}
    # IMPORTANT: dictionary keys must be Term objects not Script objects
    term_citations = {term: [0 for i in range(len(usl_list))] for term in term_list}

    for i, usl in enumerate(usl_list):
        for elem in usl.tree_iter():
            if isinstance(elem, Term):
                term_citations[elem][i] += 1

    return {term: sorted(usl_list, key=lambda e: term_citations[term][usl_id_map[e]]) for term in term_list}


def paradigm_usl_distribution(paradigm, usl_collection):
    """

    Parameters
    ----------
    paradigm
    usl_collection

    Returns
    -------
    Distribution of number of terms (contained in 'paradigm') cited overlayed on the paradigms table
    """

    TermLocation = namedtuple('TermLocation', ['table', 'coords'])
    if isinstance(paradigm, str):
        paradigm = sc(paradigm)

    tbls = generate_tables(paradigm)
    term_coordinates = {}
    dist_tables = [np.zeros(table.cells.shape, dtype=int) for table in tbls]

    for term in paradigm.singular_sequences:
        for i, table in enumerate(tbls):
            if term in table.paradigm.singular_sequences:
                table_idx = i
                coord = np.where(table == term)
        term_coordinates[term] = TermLocation(table=table_idx, coords=coord)

    for usl in usl_collection:
        for elem in usl.tree_iter():
            if isinstance(elem, Term) and elem.script in term_coordinates:
                term_loc = term_coordinates[elem.script]
                if dist_tables[term_loc.table].ndim == 1:
                    dist_tables[term_loc.table][term_loc.coords[0][0]] += 1
                elif dist_tables[term_loc.table].ndim == 2:
                    dist_tables[term_loc.table][term_loc.coords[0][0]][term_loc.coords[1][0]] += 1
                elif dist_tables[term_loc.table].ndim == 3:
                    dist_tables[term_loc.table][term_loc.coords[0][0]][term_loc.coords[1][0]][term_loc.coords[2][0]] += 1

    return dist_tables

if __name__ == '__main__':

    paradigms_list = ["E:E:F:.", "E:F:.M:M:.-", "E:F:.O:O:.-"]

    #These 2 terms have the same root paradigm : E:E:F:.
    term_1 = Term(sc("E:E:F:."))
    term_2 = Term(sc("E:E:M:."))

    #The root paradigm of term_3 is E:F:.M:M:.-
    term_3 = Term(sc("E:M:.k.-"))

    usl_list1 = [term_1, term_2]
    usl_list2 = [term_3, term_1, term_3]
    usl_list3 = [term_1, term_3, term_2]

    term_1.check()
    term_2.check()
    term_3.check()

    paradigm_dico = rank_usls(paradigms_list,usl_list1)
    tc = TermsConnector()
    full_root_paradigms = tc.root_paradigms(ieml_only = True) # list of the 53 strings of the root paradigms

    paradigm_dico2 = rank_usls(paradigms_list, usl_list2)
    #self.assertTrue(len(paradigm_dico2) == len(full_root_paradigms))
    #self.assertTrue(len(paradigm_dico2["E:E:F:."]) == 1)
    #self.assertTrue(paradigm_dico2["E:F:.M:M:.-"] == 2)