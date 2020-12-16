from flask import current_app


def add_to_index(index, model):
    """
    For each record going to be added in index, its id will be equal to the id of Post.
    """
    if not current_app.elasticsearch:
        return
    payload = dict()
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    """
    :param index:
    :param query:
    :param page:
    :param per_page:
    :return: ids of matched index records, count of matched records

    The query_index() function takes the index name and a text to search for, along with pagination controls,
    so that search results can be paginated like Flask-SQLAlchemy results are.
    The qyery type used here is multi_match, which can search across multiple fields.
    By passing a field name of *, we are telling elasticsearch to look in all the fields,  so basically searching the entire index.
    This is useful to make this function generic, since different models can have  different field names in the index.

    The body argument to es.search() includes pagination arguments in addition to the query itself.
    The from and size arguments control what subset of the entire result set needs to be returned.
    elasticsearch does not provide a nice Pagination object like the one from Flask-SQLAlchemy, so we have to do the pagination math
    to calculate the from value.

    """
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
