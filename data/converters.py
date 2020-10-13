from collections import defaultdict
from typing import List, Mapping, Optional, Set, Tuple

from .constants import Unit
from .models import UnitConversion


class UnitConverter:
    _graph: Mapping[Unit, Set[Unit]]
    _conversions: Mapping[Tuple[Unit, Unit], float]

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

    def search_conversion(self, from_unit: Unit, to_unit: Unit) -> Optional[List[Unit]]:
        """
        Depth first search algorithm to find a path between units
        """
        stack = [(from_unit, [from_unit])]
        visited = set()
        while stack:
            (vertex, path) = stack.pop()
            if vertex not in visited:
                if vertex == to_unit:
                    return path
                visited.add(vertex)
                for neighbor in self._graph[vertex]:
                    stack.append((neighbor, path + [neighbor]))

    def has_conversion(self, from_unit: Unit, to_unit: Unit) -> bool:
        return self.search_conversion(from_unit, to_unit) is not None

    def scale(self, from_unit: Unit, to_unit: Unit) -> float:
        if from_unit == to_unit:
            return 1

        path = self.search_conversion(from_unit, to_unit)

        if not path:
            return None

        scale: float = 1
        for conversion in zip(path, path[1:]):
            scale *= self._conversions.get(conversion, 1)

        return scale
