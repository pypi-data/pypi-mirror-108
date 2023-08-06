from typing import Optional, Sequence, TypeVar
from django.db.models import (
    Q, Case, When, Func, Value, BooleanField, F, QuerySet, IntegerField
)
from django.db.models.fields import BigIntegerField
from pxd_tree.adjacency_list import TreeQuerySet as Base

from .const import FieldsConfig, DEFAULT_FIELDS_CONFIG
from .db import ArrayPosition, ArrayConcat

__all__ = (
    'rough_valid_path',
    'path_descendants_Q',
    'AncestorsFunc',
    # 'RootFunc',
    'ancestors_list',
    'roots_list',
    'TreeQuerySet',
)

QT = TypeVar('QT', bound='TreeQuerySet')
NQS = Optional[QT]


def rough_valid_path(
    qs: QuerySet,
    validity_field: str = 'is_roughly_valid_element',
    id_field: str = DEFAULT_FIELDS_CONFIG.id,
    parent_id_field: str = DEFAULT_FIELDS_CONFIG.parent_id,
    path_field: str = DEFAULT_FIELDS_CONFIG.path
) -> QuerySet:
    # CREATE OR REPLACE FUNCTION px_tree.is_valid_path(
    #     id ANYELEMENT,
    #     parent ANYELEMENT,
    #     path ANYARRAY
    # ) RETURNS BOOL AS $$
    #     SELECT
    #         CASE WHEN (
    #             array_length(path, 1) > 0
    #             AND
    #             array_ndims(path) = 1
    #             AND
    #             path[array_upper(path, 1)] = id
    #             AND
    #             (
    #                 parent IS NULL
    #                 OR
    #                 path[array_upper(path, 1) - 1] = parent
    #             )
    #         ) THEN true ELSE false END
    # $$ LANGUAGE sql IMMUTABLE;
    path = F(path_field)

    return (
        qs
        .annotate(path_field_array_length=Func(path, Value(1), function='array_length', output_field=BigIntegerField()))
        # .annotate(path_field_array_ndims=Func(path, Cast(Value(1), output_field=BigIntegerField()), function='array_ndims', output_field=BigIntegerField()))
        .annotate(**{validity_field: Case(
            When(
                (
                    Q(path_field_array_length__gt=Value(0))
                    # TODO: Rewrite to be more similar to SQL above. Now it's to be less accurate.
                    # &
                    # Q(path_field_array_ndims=Value(1))
                    # &
                    # Q(**{id_field: ArrayPosition(path, Func(path, Value(1), function='array_upper'))})
                    &
                    # (
                    #     Q(**{f'{parent_id_field}__isnull': True})
                    #     |
                    #     Q(**{parent_id_field: ArrayPosition(path, index=Func(path, Value(1), function='array_upper') - Value(1), output_field=IntegerField())})
                    # )
                    (
                        (
                            Q(**{f'{parent_id_field}__isnull': True})
                            &
                            Q(path_field_array_length=Value(1))
                            &
                            Q(**{f'{path_field}__contains': [F(id_field)]})
                        )
                        |
                        (
                            Q(**{f'{parent_id_field}__isnull': False})
                            &
                            Q(path_field_array_length__gte=Value(2))
                            &
                            Q(**{f'{path_field}__contains': [F(parent_id_field), F(id_field)]})
                        )
                    )
                ),
                then=Value(True)
            ),
            default=Value(False),
            output_field=BooleanField()
        )})
    )


def path_descendants_Q(
    paths: Sequence[Sequence[int]] = [],
    path_field: str = DEFAULT_FIELDS_CONFIG.path
) -> Q:
    q = Q()

    for path in paths:
        q |= Q(**{f'{path_field}__contains': path})

    return q


def id_descendants_Q(
    ids: Sequence[int] = [],
    path_field: str = DEFAULT_FIELDS_CONFIG.path
) -> Q:
    q = Q()

    for id in ids:
        q |= Q(**{f'{path_field}__contains': [id]})

    return q


def AncestorsFunc(path_field: str = DEFAULT_FIELDS_CONFIG.path):
    return Func(path_field, function='unnest')


def RootFunc(path_field: str = DEFAULT_FIELDS_CONFIG.path):
    return Func(path_field, 1, function='array_lower', output_field=IntegerField())


def ancestors_list(
    qs: QuerySet,
    within: QuerySet,
    id_field: str = DEFAULT_FIELDS_CONFIG.id,
    path_field: str = DEFAULT_FIELDS_CONFIG.path
) -> Q:
    return within.filter(**{f'{id_field}__in': (
        qs
        .annotate(_ancestors_identifier=AncestorsFunc(path_field))
        .values_list('_ancestors_identifier', flat=True)
        .distinct('_ancestors_identifier')
    )})


def roots_list(
    qs: QuerySet,
    within: QuerySet,
    id_field: str = DEFAULT_FIELDS_CONFIG.id,
    path_field: str = DEFAULT_FIELDS_CONFIG.path
) -> Q:
    f = f'{path_field}__0'

    return within.filter(**{f'{id_field}__in': (
        qs
        .values_list(f, flat=True)
        .distinct(f)
    )})
    # return within.filter(**{f'{id_field}__in': (
    #     qs
    #     .annotate(_root_identifier=RootFunc(path_field))
    #     .values_list('_root_identifier', flat=True)
    #     .distinct('_root_identifier')
    # )})


class TreeQuerySet(Base):
    fields: FieldsConfig = DEFAULT_FIELDS_CONFIG

    def descendants(self: QT, within: NQS = None) -> QT:
        return self._get_tree_within(within).descendants_of(ids=self.ids())

    def descendants_of(
        self: QT,
        ids: Sequence[Sequence[int]] = [],
        paths: Sequence[Sequence[int]] = []
    ) -> QT:
        if ids and len(ids) > 0:
            return self.filter(id_descendants_Q(ids))

        return self.filter(path_descendants_Q(paths))

    def ancestors(self: QT, within: NQS = None) -> QT:
        return ancestors_list(self, self._get_tree_within(within))

    def roots(self: QT, within: NQS = None) -> QT:
        return roots_list(self, self._get_tree_within(within))

    def roughly_valid_elements(self, validity=True):
        return (
            rough_valid_path(self, 'is_roughly_valid_element')
            .filter(is_roughly_valid_element=validity)
        )

    def update_roughly_invalid_tree(self):
        return (
            self.roughly_valid_elements(validity=False)
            .update(path=ArrayConcat(F('parent__path'), F('id')))
        )

    def update_deeply_invalid_tree(self):
        raise NotImplementedError(
            'Not yet implemented. Use `.update_roughly_invalid_tree`.'
        )
