from collections import defaultdict
from functools import cached_property
from typing import List, Mapping, Optional, Set, Tuple

from .constants import Unit


class UnitConverter:
    _conversions: Mapping[Unit, Set[Unit]]
    _scaling: Mapping[Tuple[Unit, Unit], float]

    def __init__(self, conversions: List):
        self._scaling = {}

        self._conversions = defaultdict(set)

        for convert in conversions:
            from_unit = Unit(convert.from_unit)
            to_unit = Unit(convert.to_unit)
            self._conversions[from_unit].add(to_unit)
            self._conversions[to_unit].add(from_unit)

            self._scaling[(from_unit, to_unit)] = convert.scale
            self._scaling[(to_unit, from_unit)] = 1 / convert.scale

    def search_conversion(self, start: Unit, end: Unit) -> Optional[List[Unit]]:
        """
        Depth first search algorithm to find a path between units
        """
        stack = [(start, [start])]
        visited = set()
        while stack:
            (vertex, path) = stack.pop()
            if vertex not in visited:
                if vertex == end:
                    return path
                visited.add(vertex)
                for neighbor in self._conversions[vertex]:
                    stack.append((neighbor, path + [neighbor]))

    def has_conversion(self, from_unit: Unit, to_unit: Unit) -> bool:
        return self.search_conversion(from_unit, to_unit) is not None

    def scale(self, from_unit: Unit, to_unit: Unit) -> float:
        if from_unit == to_unit:
            return 1

        path = self.search_conversion(from_unit, to_unit)

        if path is None:
            raise ValueError(f"No conversion available from {from_unit} to {to_unit}")

        scale: float = 1
        for conversion in zip(path, path[1:]):
            scale *= self._scaling.get(conversion, 1)

        return scale

    @cached_property
    def conversion_matrix(self) -> Mapping[Unit, Mapping[Unit, Optional[float]]]:
        return {
            from_unit: {
                to_unit: self.scale(from_unit, to_unit)
                if self.has_conversion(from_unit, to_unit)
                else None
                for to_unit in Unit
            }
            for from_unit in Unit
        }
