"""
This file contains the implementation of curve point calculation and efficient approximation using polygons
"""

"""
MIT License

Copyright (c) 2026 t-wy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from typing import *
Point = Tuple[float, float]


def lerp(start: float, end: float, progress: float) -> float:
    return start + (end - start) * progress

def unlerp(start: float, end: float, value: float) -> float:
    if start == end:
        return 0
    return (value - start) / (end - start)

def lerp_point(start: Point, end: Point, progress: float) -> Point:
    return (
        lerp(start[0], end[0], progress),
        lerp(start[1], end[1], progress)
    )
    
def quadratic_lerp(start: float, control: float, end: float, progress: float) -> Point:
    p01 = lerp(start, control, progress)
    p12 = lerp(control, end, progress)
    return lerp(p01, p12, progress)
    
def quadratic_lerp_point(points: List[Point], progress: float) -> Point:
    p01 = lerp_point(points[0], points[1], progress)
    p12 = lerp_point(points[1], points[2], progress)
    return lerp_point(p01, p12, progress)

def quadratic_unlerp(start: float, control: float, end: float, value: float) -> float:
    # assert monotonic increasing/decreasing in x
    span = end - start
    assert span != 0
    control_loc = unlerp(start, end, control)
    assert 0 <= control_loc <= 1
    target = unlerp(start, end, value)
    # x = (1 - t)^2 * p0 + 2 * (1 - t) * t * p1 + t^2 * p2
    # x = (1 - t)^2 * 0 + 2 * (1 - t) * t * point_1_percentage + t^2 * 1
    # x = 2 * (1 - t) * t * point_1_percentage + t^2
    a = 2 * control_loc - 1 # -1 ~ 1
    b = - 2 * control_loc # 0 ~ -2
    c = target
    if a == 0:
        # linear
        return -c / b
    else:
        delta = b * b - 4 * a * c # 0 ~ 4
        if delta < 0:
            delta = 0
        return (-b - delta ** 0.5) / (2 * a)

def quadratic_gradient_point_x(points: List[Point], x_target: float) -> float:
    # assert monotonic increasing/decreasing in x
    t = quadratic_unlerp(points[0][0], points[1][0], points[2][0], x_target)
    return quadratic_lerp_point(points, t)[1]

def quadratic_gradient_point_y(points: List[Point], y_target: float) -> float:
    # assert monotonic increasing in y
    t = quadratic_unlerp(points[0][1], points[1][1], points[2][1], y_target)
    return quadratic_lerp_point(points, t)[0]
    
def cubic_gradient_point(points: List[Point], progress: float) -> Point:
    p01 = lerp_point(points[0], points[1], progress)
    p12 = lerp_point(points[1], points[2], progress)
    p23 = lerp_point(points[2], points[3], progress)
    p012 = lerp_point(p01, p12, progress)
    p123 = lerp_point(p12, p23, progress)
    return lerp_point(p012, p123, progress)

def cubic_gradient_point_x(points: List[Point], x_target: float) -> float:
    # assert monotonic increasing in x
    if points[0][0] > points[3][0]:
        points = points[::-1]
    assert points[0][0] <= points[1][0] <= points[3][0]
    assert points[0][0] <= points[2][0] <= points[3][0]
    if x_target >= points[-1][0]:
        return points[-1][1]
    if x_target <= points[0][0]:
        return points[0][1]
    left = 0
    right = 1
    while True:
        mid = (left + right) / 2
        test = cubic_gradient_point(points, mid)
        if test[0] == x_target or left == mid or mid == right:
            # print(points, (x_target, test[1]))
            return test[1]
        elif x_target > test[0]:
            left = mid
        else:
            right = mid

def cubic_gradient_point_y(points: List[Point], y_target: float) -> float:
    # assert monotonic increasing in y
    return cubic_gradient_point_x([(point[1], point[0]) for point in points], y_target)

def triangle_area(p0: Point, p1: Point, p2: Point) -> float:
    """
    | 1   1   1 |
    |p0x p1x p2x| × 0.5
    |p0y p1y p2y|
    """
    # (p0x - p2x) * (p1y - p0y) - (p0x - p1x) * (p2y - p0y)
    # = p0x * (p1y - p2y) + p1x * (p2y - p0y) + p2x * (p0y - p1y)
    return 0.5 * abs((p0[0] - p2[0]) * (p1[1] - p0[1]) - (p0[0] - p1[0]) * (p2[1] - p0[1]))

def distance_from_point_to_line(point: Point, start: Point, end: Point) -> float:
    dist_start_end = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5
    if dist_start_end == 0:
        # point distance
        return (point[0] - start[0]) ** 2 + (point[1] - start[1]) ** 2
    return 2 * triangle_area(start, point, end) / dist_start_end

def quadratic_bezier_to_points(p0: Point, p1: Point, p2: Point, max_distance: float = 0.1) -> List[Point]:
    """
    Return a list of points that approximate the bezier curve with the maximum distance of max_distance using De Casteljau's algorithm
    """
    result = []
    def append_points(p0: Point, p1: Point, p2: Point):
        dist1 = distance_from_point_to_line(p1, p0, p2)
        if dist1 < max_distance:
            result.append(p0)
            result.append(p2)
            return
        progress = 0.5
        p01 = lerp_point(p0, p1, progress)
        p12 = lerp_point(p1, p2, progress)
        p012 = lerp_point(p01, p12, progress)
        append_points(p0, p01, p012)
        result.pop() # remove duplicated p012
        append_points(p012, p12, p2)
    append_points(p0, p1, p2)
    return result

def quadratic_trapezoid_to_points(p0l: Point, p0r: Point, p1: Point, p2l: Point, p2r: Point, max_distance: float = 0.1) -> List[Point]:
    """
    Return a list of points that approximate the bezier curve with the maximum distance of max_distance using De Casteljau's algorithm
    """
    # Same y-coord expected
    assert p0l[1] == p0r[1] and p2l[1] == p2r[1]
    left_result = []
    right_result = []
    p0w = p0r[0] - p0l[0]
    p2w = p2r[0] - p2l[0]
    p0m = (p0l[0] + p0r[0]) / 2, p0l[1]
    p1m = p1
    p2m = (p2l[0] + p2r[0]) / 2, p2l[1]
    def append_points(p0m: Point, p0w: float, p1m: Point, p2m: Point, p2w: float):
        p1w = (p0w + p2w) / 2
        p0l = (p0m[0] - p0w / 2, p0m[1])
        p0r = (p0m[0] + p0w / 2, p0m[1])
        p1l = (p1m[0] - p1w / 2, p1m[1])
        p1r = (p1m[0] + p1w / 2, p1m[1])
        p2l = (p2m[0] - p2w / 2, p2m[1])
        p2r = (p2m[0] + p2w / 2, p2m[1])
        dist1 = distance_from_point_to_line(p1l, p0l, p2l)
        dist2 = distance_from_point_to_line(p1r, p0r, p2r)
        if dist1 < max_distance and dist2 < max_distance:
            left_result.append(p0l)
            left_result.append(p2l)
            right_result.append(p0r)
            right_result.append(p2r)
            return
        p01m = lerp_point(p0m, p1m, 0.5)
        p12m = lerp_point(p1m, p2m, 0.5)
        p012m = lerp_point(p01m, p12m, 0.5)
        p012w = (p0w + p2w) / 2
        append_points(p0m, p0w, p01m, p012m, p012w)
        left_result.pop() # remove duplicated p012m
        right_result.pop() # remove duplicated p012m
        append_points(p012m, p012w, p12m, p2m, p2w)
    append_points(p0m, p0w, p1m, p2m, p2w)
    return left_result + right_result[::-1]

def cubic_bezier_to_points(p0: Point, p1: Point, p2: Point, p3: Point, max_distance: float = 0.1) -> List[Point]:
    """
    Return a list of points that approximate the bezier curve with the maximum distance of max_distance using De Casteljau's algorithm
    """
    result = []
    def append_points(p0: Point, p1: Point, p2: Point, p3: Point):
        dist1 = distance_from_point_to_line(p1, p0, p3)
        dist2 = distance_from_point_to_line(p2, p0, p3)
        if dist1 < max_distance and dist2 < max_distance:
            result.append(p0)
            result.append(p3)
            return
        progress = 0.5
        p01 = lerp_point(p0, p1, progress)
        p12 = lerp_point(p1, p2, progress)
        p23 = lerp_point(p2, p3, progress)
        p012 = lerp_point(p01, p12, progress)
        p123 = lerp_point(p12, p23, progress)
        p0123 = lerp_point(p012, p123, progress)
        append_points(p0, p01, p012, p0123)
        result.pop() # remove duplicated p0123
        append_points(p0123, p123, p23, p3)
    append_points(p0, p1, p2, p3)
    return result

def quadratic_to_points(a: float, b: float, c: float, x0: float, x1: float, max_distance: float = 0.1) -> List[Point]:
    """
    Return a list of points that approximate the quadratic curve y = ax^2 + bx + c with the maximum distance of max_distance
    """
    result = []
    def append_points(x0: float, x1: float):
        # m = (f(x1) - f(x0)) / (x1 - x0)
        #   = a ((x1^2 - x0^2) + b (x1 - x0)) / (x1 - x0)
        #   = a (x1 + x0) + b
        #             dy/dx = 2ax + b
        # 2 a x_max + b = m = a (x1 + x0) + b
        #             x_max = (x0 + x1) / 2
        m = a * (x0 + x1) + b
        # vdist = | f(x_max) - (f(x0) + f(x1)) / 2 |
        #       = 1/2 | (f(x_max) - f(x0)) + (f(x_max) - f(x1)) |
        #       = 1/2 | a (2 x_max^2 - x0^2 - x1^2) + b (2 x_max - x0 - x1) |
        #       = 1/2 | a ((x0 + x1)^2 / 2 - x0^2 - x1^2) |
        #       = | a ((x0 - x1)^2 / 4) |
        dist = (x0 - x1) ** 2 * abs(a) / (4 * (1 + m ** 2) ** 0.5)
        if dist < max_distance:
            result.append(x0)
            result.append(x1)
            return
        x_max = (x0 + x1) / 2
        append_points(x0, x_max)
        result.pop() # remove duplicated x_max
        append_points(x_max, x1)
    append_points(x0, x1)
    return [(x, a * x * x + b * x + c) for x in result]

if __name__ == "__main__":
    # print(quadratic_gradient_point_x([
    #     (0, 0), (23, 50), (100, 100)
    # ], 23))
    # points = quadratic_to_points(0.01, 3.5, 3, 0, 100)
    # print(len(points), points)
    points = quadratic_to_points(1/100, 0, 0, 0, 100, max_distance=0.01)
    print(len(points), points)
    points = [(0, 0), (100/3, 200/3), (200/3, 100), (100, 100)]
    bezier_points = cubic_bezier_to_points(*points, max_distance=0.01)
    print(len(bezier_points), bezier_points)
    # points = [(0, 0), (0, 50), (100, 100)]
    # bezier_points = quadratic_bezier_to_points(*points, max_distance=0.5)
    # print(len(bezier_points), bezier_points)
    # points = [(0, 0), (0, 50), (100, 100), (100, 100)]
    # bezier_points = cubic_bezier_to_points(*points, max_distance=0.01)
    # print(len(bezier_points), bezier_points)
    # points = [(0, 0), (0, 50), (100, 100), (100, 100)]
    # bezier_points = cubic_bezier_to_points(*points)
    # print(len(bezier_points), bezier_points)
    # points = [(0, 0), (0, 50), (100, 100), (100, 100)]
    # bezier_points = cubic_bezier_to_points(*points, max_distance=0.5)
    # print(len(bezier_points), bezier_points)
    # points = [(0, 0), (0, 50), (100, 100), (100, 100)]
    # bezier_points = cubic_bezier_to_points(*points, max_distance=1)
    # print(len(bezier_points), bezier_points)
    # points = [(0, 0), (0, 0), (100, 100), (100, 100)]
    # bezier_points = cubic_bezier_to_points(*points)
    # print(len(bezier_points))