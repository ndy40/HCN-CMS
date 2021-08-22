class BookmarksError(Exception):
    """
    base exception class for Bookmarks
    """
    pass


class AlreadyExist(BookmarksError):
    """
    Bookmark you trying to create already exists.
    """


class DoesNotExist(BookmarksError):
    """
    Bookmark you are trying to remove does not exists
    """


class AlreadyHandled(BookmarksError):
    pass


class NotHandled(BookmarksError):
    pass
