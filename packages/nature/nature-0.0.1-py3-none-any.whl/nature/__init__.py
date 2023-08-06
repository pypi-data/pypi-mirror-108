__name__ = 'nature'
__version__ = "0.0.1"
__author__ = "Kyle Erwin"
__license__ = "MIT License"


def greeting(name=None):
    """
    Greet someone.
    :param name: who you want to greet.
    :return: A string with the greeting.
    """

    if name is None:
        return "Hello!"

    return f"Hello {name}!"
