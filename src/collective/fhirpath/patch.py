# -*- coding: utf-8 -*-
from .utils import uuidToObject
from collective.elasticsearch.hook import get_index_data
from collective.elasticsearch.hook import get_wrapped_object
from collective.elasticsearch.hook import logger as es_logger
from collective.elasticsearch.indexes import getIndex
from collective.elasticsearch.mapping import MappingAdapter
from plone import api
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.component.hooks import setSite

import warnings


__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


def MappingAdapter_get_index_creation_body(self):
    """Per index based settings
    https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html
    https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html#mapping-limit-settings
    """
    registry = getUtility(IRegistry)
    settings = dict()

    try:
        settings["index"] = {
            "mapping": {
                "total_fields": {
                    "limit": registry["fhirpath.es.index.mapping.total_fields.limit"]
                },
                "depth": {"limit": registry["fhirpath.es.index.mapping.depth.limit"]},
                "nested_fields": {
                    "limit": registry["fhirpath.es.index.mapping.nested_fields.limit"]
                },
            }
        }
        # removed from ES 7.1.x
        settings["index.mapper.dynamic"] = False

    except KeyError:
        msg = """
            Plone registry records ("
            fhirpath.es.index.mapping.total_fields.limit,
            fhirpath.es.index.mapping.depth.limit,
            fhirpath.es.index.mapping.nested_fields.limit")
            are not created.\n May be collective.fhirpath is not installed!\n
            Either install collective.fhirpath or create records from other addon.
        """
        warnings.warn(msg, UserWarning)

    settings["analysis"] = {
        "analyzer": {
            "fhir_reference_analyzer": {
                "tokenizer": "keyword",
                "filter": ["fhir_reference_filter"],
            },
        },
        "filter": {
            "fhir_reference_filter": {
                "type": "pattern_capture",
                "preserve_original": True,
                "patterns": [r"(?:\w+\/)?(https?\:\/\/.*|[a-zA-Z0-9_-]+)"],
            },
        },
        "char_filter": {},
        "tokenizer": {},
    }
    return dict(settings=settings)


def index_batch(remove, index, positions, es=None):  # noqa: C901
    """Issue: https://github.com/collective/collective.elasticsearch/issues/91
    Cannot access object (lack of permission) index_batch()->uuidToObject(uid).
    """
    if es is None:
        from collective.elasticsearch.es import ElasticSearchCatalog

        es = ElasticSearchCatalog(api.portal.get_tool("portal_catalog"))

    setSite(api.portal.get())
    conn = es.connection
    bulk_size = es.get_setting("bulk_size", 50)

    if len(remove) > 0:
        bulk_data = []
        for uid in remove:
            bulk_data.append(
                {"delete": {"_index": es.index_name, "_type": es.doc_type, "_id": uid}}
            )
        result = es.connection.bulk(
            index=es.index_name, doc_type=es.doc_type, body=bulk_data
        )

        if "errors" in result and result["errors"] is True:
            es_logger.error("Error in bulk indexing removal: %s" % result)

    if len(index) > 0:
        if type(index) in (list, tuple, set):
            # does not contain objects, must be async, convert to dict
            index = dict([(k, None) for k in index])
        bulk_data = []

        for uid, obj in index.items():
            # If content has been moved (ie by a contentrule) then the object
            # passed here is the original object, not the moved one.
            # So if there is a uuid, we use this to get the correct object.
            # See https://github.com/collective/collective.elasticsearch/issues/65 # noqa
            if uid is not None:
                obj = uuidToObject(uid, unrestricted=True)

            if obj is None:
                obj = uuidToObject(uid, unrestricted=True)
                if obj is None:
                    continue
            bulk_data.extend(
                [
                    {
                        "index": {
                            "_index": es.index_name,
                            "_type": es.doc_type,
                            "_id": uid,
                        }
                    },
                    get_index_data(obj, es),
                ]
            )
            if len(bulk_data) % bulk_size == 0:
                result = conn.bulk(
                    index=es.index_name, doc_type=es.doc_type, body=bulk_data
                )

                if "errors" in result and result["errors"] is True:
                    es_logger.error("Error in bulk indexing: %s" % result)

                bulk_data = []

        if len(bulk_data) > 0:
            result = conn.bulk(
                index=es.index_name, doc_type=es.doc_type, body=bulk_data
            )

            if "errors" in result and result["errors"] is True:
                es_logger.error("Error in bulk indexing: %s" % result)

    if len(positions) > 0:
        bulk_data = []
        index = getIndex(es.catalogtool._catalog, "getObjPositionInParent")
        for uid, ids in positions.items():
            if uid == "/":
                parent = getSite()
            else:
                parent = uuidToObject(uid, unrestricted=True)
            if parent is None:
                es_logger.warn("could not find object to index positions")
                continue
            for _id in ids:
                ob = parent[_id]
                wrapped_object = get_wrapped_object(ob, es)
                try:
                    value = index.get_value(wrapped_object)
                except Exception:
                    continue
                bulk_data.extend(
                    [
                        {
                            "update": {
                                "_index": es.index_name,
                                "_type": es.doc_type,
                                "_id": IUUID(ob),
                            }
                        },
                        {"doc": {"getObjPositionInParent": value}},
                    ]
                )
                if len(bulk_data) % bulk_size == 0:
                    conn.bulk(index=es.index_name, doc_type=es.doc_type, body=bulk_data)
                    bulk_data = []

        if len(bulk_data) > 0:
            conn.bulk(index=es.index_name, doc_type=es.doc_type, body=bulk_data)


# *** Monkey Patch ***
def do():
    """ """
    if getattr(MappingAdapter_get_index_creation_body, "__patched__", None) is None:

        setattr(MappingAdapter_get_index_creation_body, "__patched__", True)

        setattr(
            MappingAdapter,
            "get_index_creation_body",
            MappingAdapter_get_index_creation_body,
        )

    from collective.elasticsearch import hook

    if getattr(index_batch, "__patched__", None) is None:
        module_ = hook.index_batch.__module__
        qname_ = hook.index_batch.__qualname__
        setattr(index_batch, "__patched__", True)
        setattr(index_batch, "__module__", module_)
        setattr(index_batch, "__qualname__", qname_)
        setattr(
            hook,
            "index_batch",
            index_batch,
        )
