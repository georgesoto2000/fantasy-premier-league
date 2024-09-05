import unicodedata


class StringsUtils:
    def replace_special_character(name: str) -> str:
        """Takes a player's name and replaces any special characters with their 
        anglo-alphabetic equivalant

        Args:
            name (str): player's name

        Returns:
            str: player name with no special characters
        """

        if name is not None:
            name = name.lower()
            normalized_text = unicodedata.normalize('NFKD', name)
            ascii_text = ''.join(c for c in normalized_text if unicodedata.category(c) != 'Mn')
            return ascii_text
        else:
            return None
        
    def remove_full_stop(name: str) -> str:
        """removes the fullstop from a name and returns the longest part
        e.g. B.Fernandes -> Fernandes 

        Args:
            name (str): name to remove fullstop

        Returns:
            str: name without fullstop
        """
        sections = name.split('.')
        sections = [section.strip() for section in sections]
        longest = max(sections, key=len)
        return longest

    def remove_whitespace(name: str) -> str:
        """If a name has whitespace at the end it is removed

        Args:
            name (str): name to correct

        Returns:
            str: corrected name
        """
        if name and name[-1] == ' ':
            name = name[:-1]
        return name