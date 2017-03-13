from twisted.web.template import (
    TagLoader, Element, XMLString, renderer)
from twisted.python.filepath import FilePath


class HomeElement(Element):
    loader = XMLString(FilePath('templates/index.xml').open().read())

    def __init__(self, movies):
        self._movies = movies

    @renderer
    def content(self, request, tag):
        yield MoviesElement(TagLoader(tag), self._movies)

    @renderer
    def header(self, request, tag):
        return tag('Header.')

    @renderer
    def footer(self, request, tag):
        return tag('Footer.')


class MoviesElement(Element):
    loader = XMLString(FilePath('templates/movies.xml').open().read())

    def __init__(self, loader, movies):
        self._movies = movies

    @renderer
    def movies(self, request, tag):
        for movie in self._movies:
            yield tag.clone().fillSlots(
                image=movie.get('image'),
                title=movie.get('title'),
                genre=movie.get('genre'))
