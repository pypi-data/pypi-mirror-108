#!/usr/bin/env python
# coding: utf-8
from contextvars import ContextVar, copy_context


ctxargs = (
    "patient",
    "doctor",
    "therapist",
    "employee",
    "assistant",
    "subjective",
    "objective",
    "assessment",
    "plan",
)


class ContextManager:
    def __init__(self, *args, **kwargs):
        for attr in [ x for x in [ *ctxargs, *args ] ]:
            setattr(self, attr, ContextVar(attr))
        self.kwargs = kwargs

    def set(self, attr, v):
        x = getattr(self, attr)
        setattr(self, f"_{attr}", x.set(v))

    def copy(self):
        ctx = copy_context()
        return {k.name: v for k, v in dict(ctx).items()}

    def get(self, attr):
        try:
            return self.copy()[ attr ]
        except KeyError:
            return None


