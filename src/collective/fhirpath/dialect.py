# _*_ coding: utf-8 _*_
from fhirpath.dialects.elasticsearch import ElasticSearchDialect as BaseDialect
from fhirpath.dialects.elasticsearch import ES_PY_OPERATOR_MAP
from fhirpath.interfaces import IFhirPrimitiveType

import operator


__author__ = "Md Nazrul Islam<email2nazrul@gmail.com>"


class ElasticSearchDialect(BaseDialect):
    """ """

    def apply_security(self, securities, body_structure):
        """ """
        if "allowedRolesAndUsers" in securities:
            values = securities["allowedRolesAndUsers"]
            if isinstance(values, (str, bytes)):
                values = [values]
            terms = {"terms": {"allowedRolesAndUsers": values}}
            body_structure["query"]["bool"]["filter"].append(terms)

        if "effectiveRange" in securities:
            value = IFhirPrimitiveType(securities["effectiveRange"])
            # just validation
            value.to_python()
            range_ = [
                {
                    "range": {
                        "effectiveRange.effectiveRange1": {
                            ES_PY_OPERATOR_MAP[operator.le]: value
                        }
                    }
                },
                {
                    "range": {
                        "effectiveRange.effectiveRange2": {
                            ES_PY_OPERATOR_MAP[operator.ge]: value
                        }
                    }
                },
            ]

            body_structure["query"]["bool"]["filter"].extend(range_)
