# -*- coding: utf-8 -*-

"""
cues.select
===========

A module that contains the Select class.
"""

from typing import Deque, Iterable, List

from . import constants, cursor, utils
from .cue import Cue


class Select(Cue):
    """Construct a Select object to retrieve a single response from a user.

    A Select object will display a menu-like prompt to the user
    and ask the user to select one option. The user can use the
    Up and Down arrow keys to navigate the prompt and select an
    option by pressing Enter.

    Attributes
    ----------
    _num_options : int
        The number of options
    _markers : Deque of str
        Contains an arrow marker and empty spaces to indicate to 
        the user which option is currently selected.
    _select_marker_len : int
        The length of the arrow marker being used.
    _init_fmt : str
        The format for the initial statement.
    _list_fmt : str
        The format for list items.
    _list_fmt_if_active : str
        The format for active list items.
    """

    __name__ = 'Select'
    __module__ = 'cues'

    def __init__(self, name: str, message: str, options: Iterable[str]):
        """

        Parameters
        ----------
        name
            The name of the Select instance.
        message
            Instructions or useful information regarding the prompt for the user.
        options
            Available options for the user to pick from.
        """

        super().__init__(name, message)

        if hasattr(options, '__iter__'):
            self._options = list(options)
            self._num_options = len(self._options)
        else:
            raise TypeError(f"'{type(options)}' object is not iterable")

        # Create the deque that will contain the arrow markers and
        # allocate an appropriate number of arrow marker spaces depending
        # on the number of options:
        self._markers = self.create_deque(
            [constants.SELECT_MARKER], length=self._num_options)

        self._select_marker_len = len(constants.SELECT_MARKER)

        for _ in range(self._num_options - 1):
            self._markers.append(' ' * self._select_marker_len)

        self._init_fmt = '[pink][?][/pink] {message}\n'
        self._list_fmt = '[skyblue]{marker}[/skyblue] {option}'
        self._list_fmt_if_active = '[skyblue]{marker}[/skyblue] [underline skyblue]{option}[/underline skyblue]'

    @property
    def options(self) -> List[str]:
        return self._options

    @property
    def markers(self) -> Deque[str]:
        return self._markers

    @markers.setter
    def markers(self, pos: int):
        # If the keystroke was the up arrow:
        if pos:
            # If the LIST_MARKER is the first element in the deque:
            if not self._markers.index(constants.LIST_MARKER):
                self._markers.append(constants.LIST_MARKER)
            else:
                self._markers.append(' ' * self._select_marker_len)

        # Otherwise, if the keystroke was the down arrow:
        else:
            # If the LIST_MARKER is the last element in the deque:
            if self._markers.index(constants.LIST_MARKER) == self._num_options - 1:
                self._markers.appendleft(constants.LIST_MARKER)
            else:
                self._markers.appendleft(' ' * self._select_marker_len)

    def send(self) -> dict:
        """Returns a dict object containing user's response to the prompt.

        Returns
        -------
        dict
            Contains the user's response to the prompt.
        """

        try:
            cursor.hide()

            self._draw()
            return self.answer
        finally:
            cursor.show()

    def _draw(self):
        """Prints the prompt to console and sets user's response.
        """

        cursor.write(self._init_fmt.format(message=self._message), color=True)

        up = self.keys.get('up')
        down = self.keys.get('down')
        enter = self.keys.get('enter')

        while True:
            for marker, option in zip(self.markers, self.options):
                fmt = (self._list_fmt if marker !=
                       constants.LIST_MARKER else self._list_fmt_if_active)

                cursor.write(fmt.format(
                    marker=marker, option=option), color=True, newlines=1)

            key = self.listen_for_key()

            if key == up:
                self.markers = 1
            elif key == down:
                self.markers = 0
            elif key == enter:
                cursor.clear(self._num_options)
                break

            cursor.move(y=self._num_options)

        list_marker_pos = self._markers.index(constants.LIST_MARKER)
        self.answer = {self._name: self.options[list_marker_pos]}

    @classmethod
    def from_dict(cls, prompt: dict):
        """Creates and instantiates a Select object from a dict object.

        Parameters
        ----------
        prompt : dict
            A dict object that contains a name key, a message key, and an
            options key.

        Returns
        -------
        cues.Select
            A Select object to retrieve a single response from a user.
        """

        name = prompt['name']
        message = prompt['message']
        options = prompt['options']
        return cls(name, message, options)


def main(test=0):
    name = 'programming_language'
    message = 'Which of these is your favorite programming language?'
    options = ['Python', 'JavaScript', 'C++', 'C#']

    if not test:
        prompt = Select(name, message, options)
        answer = prompt.send()
        print(answer)


if __name__ == '__main__':
    main()
