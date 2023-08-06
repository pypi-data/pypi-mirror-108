#!/usr/bin/env python
# coding: utf-8
from abc import ABC
from dataclasses import dataclass
from typing import List, Union
from markupsafe import Markup

class BaseElement(ABC):

    @property
    def render(self):
        return Markup(self.__html__())

    def klass(self, v):
        setattr(self, 'element_class', v)
        return self

    def style(self, v):
        setattr(self, 'element_style', v)
        return self

    def _klass(self):
        return f' class="{self.element_class}"' if hasattr(self, 'element_class') else ''

    def _style(self):
        return f' style="{self.element_style}"' if hasattr(self, 'element_style') else ''

    @property
    def meta(self):
        return self._klass() + self._style()

    def __html__(self):
        raise NotImplemented


    def __call__(self, *args, **kwargs):
        return self.__html__()


    def __add__(self, other):
        assert isinstance(other, (BaseElement, str)), 'only can add BaseElement and str'
        if isinstance(other, BaseElement):
            return self.__html__() + other.__html__()
        elif isinstance(other, str):
            return self.__html__() + other



@dataclass
class Input(BaseElement):
    type: str = 'submit'

    def __html__(self):
        return f'\n<input{self.meta} type="{self.type}"/>\n'



@dataclass
class Form(BaseElement):
    text: str = ''
    method: str = 'GET'
    action: str = '/'
    input_type: str = 'submit'
    input_klass: str = 'bg-primary float-end'
    input_value: str = 'enviar'

    def _klass(self):
        return f' class="{self.element_class}"' if hasattr(self, 'element_class') else ' class="form-control form-group p-2"'



    @property
    def meta(self):
        return f'{self._klass() + self._style()} action="{self.action}" method="{self.method}"'

    def __html__(self):
        return f'\n<form{self.meta}>{self.text}<br><input type="{self.input_type}" class="{self.input_klass}" value="{self.input_value}"/></form>\n'

@dataclass
class Div(BaseElement):
    text: str = ''

    def __html__(self):
        return f'\n<div{self.meta}>{self.text}</div>\n'

@dataclass
class HR(BaseElement):
    def __html__(self):
        return f'<hr{self.meta} />'


@dataclass
class ListItem(BaseElement):
    text: str

    def __html__(self):
        return f'\n<li{self.meta}>{self.text}</li>\n'

@dataclass
class UnOlList(BaseElement):
    items: List[Union[BaseElement, str, None]]
    text: str = ''
    ol: bool = False

    def __html__(self):
        unol = 'ol' if self.ol else 'ul'
        items = []
        for item in self.items:
            if isinstance(item, BaseElement):
                items.append(item())
            else:
                items.append(item)
        return f'<{unol}{self.meta}>{"".join([ListItem(item)() for item in items])}<{unol}>'


@dataclass
class Paragraph(BaseElement):
    text: str

    def __html__(self):
        return f'<p{self.meta}>{self.text}</p>'

@dataclass
class Title(BaseElement):
    text: str
    level: int

    def __html__(self):
        return f'<h{self.level}{self.meta}>{self.text}</h{self.level}>'

@dataclass
class Link(BaseElement):
    text: str
    href: str

    def __html__(self):
        return f'<a href="{self.href}"{self.meta}>{self.text}</a>'

