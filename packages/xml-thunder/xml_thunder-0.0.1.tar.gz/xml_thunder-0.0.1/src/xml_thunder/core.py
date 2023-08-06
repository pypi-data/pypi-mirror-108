import xml.etree.ElementTree as ElementTree

from io import TextIOWrapper
from typing import *
from collections.abc import Callable

"""
The xml_lightning library is designed to make creating XML parsers an
easier and more efficient process
"""


RoutesDictionary = Dict[str, Callable]


class Lightning(object):
    """
    Used for creating an XML parser
    """

    def __init__(self):
        self.__routes: RoutesDictionary = {}

    def __getitem__(self, route: AnyStr):
        return self.__routes[route]

    def __len__(self):
        return len(self.__routes)

    def __bool__(self):
        return self.__routes == {}

    def get_route(self, route: str) -> Callable:
        """ Returns a registered route if there is one at 'route' """
        return self[route]

    def get_all_routes(self) -> RoutesDictionary:
        """ Returns all registered routes """
        return self.__routes

    def add_route(self, path: AnyStr, function: Callable) -> None:
        """ Adds a route at 'path' with 'function' as the value """
        self.__routes[path] = function

    def route(self, path: AnyStr):
        """
        Creates a route for the provided 'path'

        Note that 'path' is any valid xPath
        """

        def inner(function_: Callable):
            self.add_route(path, function_)

        return inner

    def parse(self, xml_like_document: Union[AnyStr, TextIOWrapper]) -> None:
        """ The entrypoint for parsing documents """

        document_root = ElementTree.parse(xml_like_document).getroot()

        for path_as_string, function_ in self.__routes.items():
            for element in document_root.findall(path_as_string):
                if function_.__code__.co_argcount != 1:
                    raise ValueError(
                        f"{function_.__name__} must have 1 argument")
                function_(element)
