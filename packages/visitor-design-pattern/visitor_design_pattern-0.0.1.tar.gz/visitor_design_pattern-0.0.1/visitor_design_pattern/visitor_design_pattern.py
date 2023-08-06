"""Main module."""

import enum
from abc import ABC, abstractmethod


class Visitor(ABC):
    
    @abstractmethod
    def visit_prefix(self, element, **kwargs):
        ...

    @abstractmethod
    def visit_infix(self, element, **kwargs):
        ...
    
    @abstractmethod
    def visit_postfix(self, element, **kwaargs):
        ...


class PostfixVisitor(Visitor):
    @dispatch(object)
    def visit_prefix(self, element, parent_res=None):
        pass
    @dispatch(object)
    def visit_infix(self, element, parent_res=None):
        pass


class PrefixVisitor(Visitor):
    @dispatch(object)
    def visit_infix(self, element, parent_res=None):
        pass
    @dispatch(object)
    def visit_postfix(self, element, parent_res=None, prefix_res=None, visited_attrs=None):
        pass


class InfixVisitor(Visitor):
    @dispatch(object)
    def visit_prefix(self, element, parent_res=None):
        pass
    @dispatch(object)
    def visit_postfix(self, element, parent_res=None, prefix_res=None, visited_attrs=None):
        pass


class VisitableInterface():

    DATA_TYPES = [
        str, 
        float, 
        int, 
        type(None), 
        dict,
        enum.EnumMeta,
    ]
    
    def accept(self, visitor: Visitor, parent_res=None):
        prefix_res = visitor.visit_prefix(self, parent_res=parent_res)
        visited_attrs = {}
        for i, (key, value) in enumerate(self.__dict__.items()):
            if type(value) not in self.DATA_TYPES:
                visited = None
                if isinstance(value, list):
                    visited = []
                    for j, x in enumerate(value):
                        visited.append(x.accept(visitor, parent_res=prefix_res))
                        if j < len(value) - 1:
                            visitor.visit_infix(self, parent_res=parent_res)
                else:
                    visited = value.accept(visitor, parent_res=prefix_res)
                    if i < len(self.__dict__.keys()) - 1:
                        visitor.visit_infix(self, parent_res=parent_res)
                visited_attrs[key] = visited
        postfix_res = visitor.visit_postfix(self, parent_res=parent_res, prefix_res=prefix_res, visited_attrs=visited_attrs)
        return prefix_res, visited_attrs, postfix_res