from collections import defaultdict
from functools import reduce
from operator import itemgetter, mul
from typing import Dict, List, Set, Tuple

from common.constants import Unit
from common.models import UnitConversion


class UnitConverter:
    _graph: Dict[Unit, Set[Unit]]

    def __init__(self, conversions: List[UnitConversion]):
        self._conversions = {}

        self._graph = defaultdict(set)

        for convert in conversions:
            from_unit = Unit(convert.from_unit)
            to_unit = Unit(convert.to_unit)
            self._graph[from_unit].add(to_unit)
            self._graph[to_unit].add(from_unit)

            self._conversions[(from_unit, to_unit)] = convert.scale
            self._conversions[(to_unit, from_unit)] = 1 / convert.scale

    def search_conversion(
        self, from_unit: Unit, to_unit: Unit
    ) -> List[Tuple[Unit, Unit]]:
        def dfs_paths(graph, start, goal):
            stack = [(start, [start])]
            visited = set()
            while stack:
                (vertex, path) = stack.pop()
                if vertex not in visited:
                    if vertex == goal:
                        return path
                    visited.add(vertex)
                    for neighbor in graph[vertex]:
                        stack.append((neighbor, path + [neighbor]))

        return dfs_paths(self._graph, from_unit, to_unit)

    def scale(self, from_unit: Unit, to_unit: Unit) -> float:
        if from_unit == to_unit:
            return 1

        path = self.search_conversion(from_unit, to_unit)

        if not path:
            return None

        scale = 1
        for conversion in zip(path, path[1:]):
            scale *= self._conversions.get(conversion, 1)

        return scale
