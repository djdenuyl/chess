"""
SVG Parser

author: David den Uyl (djdenuyl@gmail.com)
date: 2023-05-10
"""
from dash.development.base_component import Component
from dash_svg import Circle, Ellipse, Line, Path, Polygon, Polyline, Rect, Svg, G
from enum import Enum
# noinspection PyProtectedMember
from lxml.etree import fromstring, _Element, QName
from pathlib import Path as FilePath
from re import search
from typing import Optional
from uuid import uuid4


class SVGShape(Enum):
    CIRCLE = 'circle'
    ELLIPSE = 'ellipse'
    G = 'g'
    IMAGE = 'image'
    LINE = 'line'
    PATH = 'path'
    POLYGON = 'polygon'
    POLYLINE = 'polyline'
    RECTANGLE = 'rect'


class SVGParser:
    ns = {
        'svg': 'http://www.w3.org/2000/svg',
        'sodipodi': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
        'inkscape': 'http://www.inkscape.org/namespaces/inkscape'
    }

    _fill = 'white'
    _stroke = 'black'
    _stroke_width = '1'

    def __init__(self, tree, fill: str = _fill, stroke: str = _stroke, stroke_width: float = _stroke_width):
        self.tree = tree
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width

    @classmethod
    def from_file(cls, file: FilePath, **kwargs):
        with open(file, 'r') as f:
            data = f.read()

        return SVGParser(tree=fromstring(bytes(data, 'utf-8')), **kwargs)

    @property
    def mapper(self) -> dict:
        return {
            SVGShape.CIRCLE: self.parse_circle,
            SVGShape.ELLIPSE: self.parse_ellipse,
            SVGShape.IMAGE: lambda _: None,
            SVGShape.LINE: self.parse_line,
            SVGShape.PATH: self.parse_path,
            SVGShape.POLYGON: self.parse_polygon,
            SVGShape.POLYLINE: self.parse_polyline,
            SVGShape.RECTANGLE: self.parse_rect
        }

    def parse_shapes(self, with_color: bool = False) -> list[Component]:
        gs = self.tree.xpath('./svg:g', namespaces=self.ns)

        shapes = []
        for g in gs:
            shapes.extend(self.parse_g(g, with_color))

        return shapes

    def parse_g(self, g: _Element, with_color: bool = False) -> list[Component]:
        shapes = []
        for shape in g.getchildren():
            if QName(shape).localname == SVGShape.G.value:
                shapes.extend(self.parse_g(shape, with_color))

            else:
                shapes.append(
                    self.mapper.get(
                        SVGShape(
                            QName(shape).localname
                        )
                    )(shape, with_color)
                )

        return shapes

    def parse_circle(self, shape: _Element, with_color: bool = False) -> Circle:
        return Circle(
            id={'type': 'shape', 'id': str(uuid4())},
            r=shape.attrib.get('r'),
            cx=shape.attrib.get('cx'),
            cy=shape.attrib.get('cy'),
            transform=shape.attrib.get('transform'),
            stroke=self.stroke,
            strokeWidth=self.stroke_width,
            fill=self.get_fill(shape, with_color)
        )

    def parse_ellipse(self, shape: _Element, with_color: bool = False) -> Ellipse:
        return Ellipse(
            id={'type': 'shape', 'id': str(uuid4())},
            rx=shape.attrib.get('rx'),
            ry=shape.attrib.get('ry'),
            cx=shape.attrib.get('cx'),
            cy=shape.attrib.get('cy'),
            transform=shape.attrib.get('transform'),
            stroke=self.stroke,
            strokeWidth=self.stroke_width,
            fill=self.get_fill(shape, with_color)
        )

    def parse_line(self, shape: _Element, with_color: bool = False) -> Line:
        return Line(
            id={'type': 'shape', 'id': str(uuid4())},
            x1=shape.attrib.get('x1'),
            y1=shape.attrib.get('y1'),
            x2=shape.attrib.get('x2'),
            y2=shape.attrib.get('y2'),
            transform=shape.attrib.get('transform'),
            stroke=self.stroke,
            strokeWidth=self.stroke_width,
            fill=self.get_fill(shape, with_color)
        )

    def parse_path(self, shape: _Element, with_color: bool = False) -> Path:
        return Path(
            id={'type': 'shape', 'id': str(uuid4())},
            d=shape.attrib.get('d'),
            transform=shape.attrib.get('transform'),
            stroke=self.stroke,
            strokeWidth=self.stroke_width,
            fill=self.get_fill(shape, with_color)
        )

    def parse_polygon(self, shape: _Element, with_color: bool = False) -> Polygon:
        return Polygon(
            id={'type': 'shape', 'id': str(uuid4())},
            points=shape.attrib.get('points'),
            transform=shape.attrib.get('transform'),
            stroke=self.stroke,
            strokeWidth=self.stroke_width,
            fill=self.get_fill(shape, with_color)
        )

    def parse_polyline(self, shape: _Element, with_color: bool = False) -> Polyline:
        return Polyline(
            id={'type': 'shape', 'id': str(uuid4())},
            points=shape.attrib.get('points'),
            transform=shape.attrib.get('transform'),
            stroke=self.stroke,
            strokeWidth=self.stroke_width,
            fill=self.get_fill(shape, with_color)
        )

    def parse_rect(self, shape: _Element, with_color: bool = False) -> Rect:
        return Rect(
            id={'type': 'shape', 'id': str(uuid4())},
            width=shape.attrib.get('width'),
            height=shape.attrib.get('height'),
            x=shape.attrib.get('x'),
            y=shape.attrib.get('y'),
            rx=shape.attrib.get('rx'),
            ry=shape.attrib.get('ry'),
            transform=shape.attrib.get('transform'),
            stroke=self.stroke,
            strokeWidth=self.stroke_width,
            fill=self.get_fill(shape, with_color)
        )

    def get_fill(self, shape, with_color: bool = False) -> Optional[str]:
        if not with_color:
            return self.fill
        elif f := shape.attrib.get('fill'):
            return f
        else:
            return self.get_prop_from_style(shape.attrib.get('style'), 'fill')

    @staticmethod
    def get_prop_from_style(style: str, prop: str) -> Optional[str]:
        m = search(f'{prop}:', style)

        if not m:
            return

        value_start = m.span()[1]
        value_end = value_start + (n.span()[0] if (n := search(';', style[value_start:])) else len(style))

        return style[value_start: value_end]

    def parse_svg(
            self,
            classes: list[str] | None = None,
            with_color: bool = True,
            view_box: tuple[int, int, int, int] | None = None
    ) -> Svg:
        if view_box is None:
            view_box = (0, 0, 100, 100)

        if classes is None:
            classes = []

        view_box_str = " ".join([str(v) for v in view_box])

        return Svg(
            id=id,
            className=' '.join(classes),
            children=[
                G(
                    children=self.parse_shapes(with_color=with_color)
                )
            ],
            viewBox=view_box_str
        )
