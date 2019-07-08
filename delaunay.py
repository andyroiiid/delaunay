from __future__ import annotations

from typing import List
from math import isclose


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return isclose(self.x, other.x) and isclose(self.y, other.y)

    def distance_2(self, other: Point) -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return dx * dx + dy * dy

    def is_in_circumscribed_center_of(self, triangle: Triangle) -> bool:
        return self.distance_2(triangle.center) <= triangle.radius_2


class Edge:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b

    def __repr__(self):
        return f"Edge({self.a}, {self.b})"

    def __eq__(self, other: Edge):
        return ((self.a == other.a) and (self.b == other.b)) or ((self.a == other.b) and (self.b == other.a))


class Triangle:
    def __init__(self, a: Point, b: Point, c: Point):
        self.a = a
        self.b = b
        self.c = c

        self.edges = [Edge(a, b), Edge(b, c), Edge(c, a)]

        self.center = self.get_circumscribed_center()
        self.radius_2 = self.center.distance_2(self.a)

    def __repr__(self):
        return f"Triangle({self.a}, {self.b}, {self.c})"

    def get_circumscribed_center(self) -> Point:
        a, b, c = self.a, self.b, self.c
        d = (a.x * (b.y - c.y) +
             b.x * (c.y - a.y) +
             c.x * (a.y - b.y)) * 2
        x = ((a.x * a.x + a.y * a.y) * (b.y - c.y) +
             (b.x * b.x + b.y * b.y) * (c.y - a.y) +
             (c.x * c.x + c.y * c.y) * (a.y - b.y))
        y = ((a.x * a.x + a.y * a.y) * (c.x - b.x) +
             (b.x * b.x + b.y * b.y) * (a.x - c.x) +
             (c.x * c.x + c.y * c.y) * (b.x - a.x))
        return Point(x / d, y / d)

    def has_edge(self, edge: Edge) -> bool:
        return edge in self.edges

    def has_vertex(self, point: Point) -> bool:
        return (self.a == point) or (self.b == point) or (self.c == point)

    def has_vertex_from(self, other: Triangle) -> bool:
        return self.has_vertex(other.a) or self.has_vertex(other.b) or self.has_vertex(other.c)


def calc_super_triangle(points: List[Point]) -> Triangle:
    min_x = min(point.x for point in points)
    max_x = max(point.x for point in points)
    min_y = min(point.y for point in points)
    max_y = max(point.y for point in points)

    dx = (max_x - min_x) / 2

    p1 = Point(min_x - dx - 1, min_y - 1)
    p2 = Point(max_x + dx + 1, min_y - 1)
    p3 = Point(min_x + dx, max_y + (max_y - min_y) + 1)

    return Triangle(p1, p2, p3)


def bowyer_watson(points: List[Point]) -> List[Triangle]:
    super_tri = calc_super_triangle(points)
    tris: List[Triangle] = [super_tri]

    for point in points:
        bad_tris: List[Triangle] = [t for t in tris if point.is_in_circumscribed_center_of(t)]

        # Grand Master In Funkytional Programming
        # polygon: List[Edge] = reduce(add, [[e for e in bad_tri.edges if
        #                                     not reduce(or_, (t.has_edge(e) for t in bad_tris if id(bad_tri) != id(t)),
        #                                                False)] for bad_tri in bad_tris], [])

        polygon: List[Edge] = list()
        for bad_tri in bad_tris:
            for edge in bad_tri.edges:
                is_shared = False
                for other_triangle in bad_tris:
                    if id(bad_tri) == id(other_triangle):
                        continue
                    if other_triangle.has_edge(edge):
                        is_shared = True
                if not is_shared:
                    polygon.append(edge)

        tris = [t for t in tris if t not in bad_tris]
        tris += [Triangle(point, edge.a, edge.b) for edge in polygon]

    return [t for t in tris if not t.has_vertex_from(super_tri)]


if __name__ == '__main__':
    ps = [Point(6, 5), Point(5, 1), Point(3, 1), Point(3, 4), Point(0, 0), Point(5, 6)]
    print(ps)
    ts = bowyer_watson(ps)
    # [Triangle(Point(3, 4), Point(3, 1), Point(5, 1)), Triangle(Point(3, 4), Point(5, 1), Point(6, 5)),
    #  Triangle(Point(0, 0), Point(5, 1), Point(3, 1)), Triangle(Point(0, 0), Point(3, 1), Point(3, 4)),
    #  Triangle(Point(5, 6), Point(3, 4), Point(6, 5))]
    print(ts)
