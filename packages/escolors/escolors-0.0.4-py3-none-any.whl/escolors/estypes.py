from termcolor import color_map


class esString(str):
    """esString object based on str, with methods to aid formatting and coloring"""

    def __init__(self, value):
        """
        Initialize the esString object (Based on string)
        :param value: The text for the object to hold
        """
        self.value = value

    def colparse(self) -> str:
        """
        Process the esString's value and convert placeholders into
        format sequences to colorify the value
        :return: Colorized and formatted string
        """
        if self.value != None and self.value != "":
            for col, fmt in color_map.items():
                self.value = self.value.replace(col, fmt)
            return self.value
        else:
            return None

    def __str__(self) -> str:
        """
        The objects str value
        :return: Returns the esString's value colorized
        """
        return self.colparse()

    def stripcols(self) -> str:
        """
        Processes the value of the esString and removes placeholders,
        also removes formatting sequences in the case of processing having
        already taken place
        :return: Value of esString with all formatting sequences and placeholders
        removed from the text
        """
        for col, fmt in color_map.items():
            self.value = self.value.replace(col, '')
            self.value = self.value.replace(fmt, '')
        return self.value
