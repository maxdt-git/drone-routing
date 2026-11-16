class Color:
    """
    Class color juste take chose color
    """
    def chose_color(self, color: str) -> str:
        """
        Func takes a color on parameter and return the ansi code of the color
        """
        if color == "green":
            return "\033[0;32m"
        elif color == "blue":
            return "\033[0;34m"
        elif color == "red":
            return "\033[0;31m"
        elif color == "yellow":
            return "\033[0;33m"
        elif color == "orange":
            return "\033[38;5;208m"
        elif color == "cyan":
            return "\033[0;36m"
        elif color == "purple":
            return "\033[0;35m"
        elif color == "brown":
            return "\033[38;5;131m"
        elif color == "lime":
            return "\033[38;5;46m"
        elif color == "magenta":
            return "\033[1;35m"
        elif color == "black":
            return "\033[0;30m"
        elif color == "maroon":
            return "\033[38;5;52m"
        elif color == "gold":
            return "\033[38;5;220m"
        elif color == "darkred":
            return "\033[38;5;88m"
        elif color == "violet":
            return "\033[38;5;177m"
        elif color == "crimson":
            return "\033[38;5;197m"
        elif color == "rainbow":
            return "\033[38;5;196m"
        else:
            return "\033[0m"
