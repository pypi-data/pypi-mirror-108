from enum import Enum
from typing import Type, cast, Iterable

from collections_extended import RangeMap
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.formatter import FormatterParameters, FormatterBase
from pymultirole_plugins.v1.schema import Document, Annotation
from starlette.responses import Response, JSONResponse


class ConsolidationType(str, Enum):
    linker = 'linker'
    unknown = 'unknown'
    unknown_only = 'unknown_only'


class ConsolidateParameters(FormatterParameters):
    type: ConsolidationType = Field(ConsolidationType.unknown, description="""Type of consolidation, use
    - *linker* to retain only known entities
    - *unkown* to retain all but prepending `unknown_` to the label name of unknwon entities
    - *unkown_only* to retain only unknown entities prepending `unknown_` to their label name""")


class ConsolidateFormatter(FormatterBase):
    """Consolidate formatter .
    """

    def format(self, document: Document, parameters: FormatterParameters) \
            -> Response:
        params: ConsolidateParameters = cast(ConsolidateParameters, parameters)
        if document.annotations:
            anns = self.filter_annotations(document)
            if params.type in [ConsolidationType.unknown_only, ConsolidationType.unknown]:
                for a in anns:
                    if a.terms is None:
                        a.labelName = "unknown_" + a.labelName
                        if a.label:
                            a.label = "Unknown " + a.label
                if params.type == ConsolidationType.unknown_only:
                    anns = [a for a in anns if a.terms is None]
            elif params.type == ConsolidationType.linker:
                anns = [a for a in anns if a.terms is not None]
            document.annotations = anns
        return JSONResponse(content=jsonable_encoder(document))

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return ConsolidateParameters

    def filter_annotations(self, input: Document):
        """Filter a sequence of annotations and remove duplicates or overlaps. When spans overlap, the (first)
        longest span is preferred over shorter spans.
        annotations (iterable): The annotations to filter.
        RETURNS (list): The filtered annotations.
        """

        def get_sort_key(a: Annotation):
            return a.end - a.start, -a.start, a.labelName is None

        sorted_annotations: Iterable[Annotation] = sorted(input.annotations, key=get_sort_key, reverse=True)
        result = []
        seen_offsets = RangeMap()
        for ann in sorted_annotations:
            # Check for end - 1 here because boundaries are inclusive
            if seen_offsets.get(ann.start) is None and seen_offsets.get(ann.end - 1) is None:
                result.append(ann)
                seen_offsets[ann.start:ann.end] = ann
            else:
                target = seen_offsets.get(ann.start) or seen_offsets.get(ann.end - 1)
                # if target.labelName in kb_labels and ann.labelName in white_labels and (target.start-ann.start != 0 or target.end-ann.end != 0):
                if (target.start - ann.start == 0 or target.end - ann.end == 0) and (ann.end - ann.start) / (
                        target.end - target.start) > 0.8:
                    if ann.terms:
                        terms = set(target.terms or [])
                        terms.update(ann.terms)
                        target.terms = list(terms)
                    if ann.properties:
                        props = target.properties or {}
                        props.update(ann.properties)
                        target.properties = props
        result = sorted(result, key=lambda ann: ann.start)
        return result
