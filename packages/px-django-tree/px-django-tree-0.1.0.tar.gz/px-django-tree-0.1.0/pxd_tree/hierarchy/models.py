from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GistIndex
from django.utils.translation import pgettext_lazy

from pxd_tree.adjacency_list import Tree as BaseTree


__all__ = 'Tree', 'tree_indexes',


def tree_indexes(name: str = '%(app_label)s_%(class)s'):
    return [
        GistIndex(
            name=name + '_path_index',
            fields=['path'],
            opclasses=('gist__int_ops',)
        )
    ]


class Tree(BaseTree):
    class Meta:
        abstract = True
        indexes = tree_indexes()

    path = ArrayField(
        models.BigIntegerField(),
        verbose_name=pgettext_lazy('pxd_tree', 'Hierarchy path'),
        null=False, blank=False, default=list, editable=False
    )
