from handlers.commons import exception_handler
from ieml.usl.tools import usl
from models.intlekt.edition.lexicon import LexiconConnector


@exception_handler
def get_lexicon_list(split=None):

    if split is not None:
        return {'success': True,
                'favorites': LexiconConnector().all_lexicons(favorite=True),
                'others': LexiconConnector().all_lexicons(favorite=False)}
    else:
        return {
            'success': True,
            'lexicons': sorted(LexiconConnector().all_lexicons(),
                            key=lambda g: g['favorite'] if g['favorite'] is not None else 10000)}



@exception_handler
def new_lexicon(body):
    name = body['name']
    id = LexiconConnector().add_lexicon(name)

    return {'success': True, 'id': id}


@exception_handler
def delete_lexicon(body):
    id = body['id']
    success = LexiconConnector().remove_lexicon(id=id)

    return {'success': success}


@exception_handler
def set_lexicon_favorite(body):
    names = body['names']
    LexiconConnector().set_favorites(names)
    return {'success': True}


@exception_handler
def add_word_to_lexicon(lexicon_id, body):
    word = body['word']

    modified = LexiconConnector().add_words([word], id=lexicon_id)
    if modified:
        return {'success': True}
    else:
        return {'success': False, 'message': 'Word "%s" already present in this lexicon.'%word}


@exception_handler
def remove_words_to_lexicon(lexicon_id, body):
    words = list(body['words'])

    LexiconConnector().remove_words(words, id=lexicon_id)
    return {'success': True}


@exception_handler
def get_words_of_lexicon(lexicon_id):
    lexicon = LexiconConnector().get(id=lexicon_id)

    return {'success': True,
            'words': [{
                'ieml': str(t['USL']['IEML']),
                'translations': {
                    **t['TRANSLATIONS'],
                    **{'default_%s'%k: v for k,v in usl(t['USL']['IEML']).auto_translation().items()}
                },
                'id': t['_id'],
                'last_modified': t['LAST_MODIFIED'] } for t in lexicon['words']],
            'id': lexicon['id'],
            'name': lexicon['name']}
