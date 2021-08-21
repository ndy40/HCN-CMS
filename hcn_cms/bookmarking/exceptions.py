class BookmarksError(Exception):
    """
    base exception class for Bookmarks
    """
    pass


class AlreadyExists(BookmarksError):
    """
    Bookmark you trying to create already exists.
    """


class DoesNotExists(BookmarksError):
    """
    Bookmark you are trying to remove does not exists
    """


class AlreadyHandled(BookmarksError):
    pass


class NotHandled(BookmarksError):
    pass
