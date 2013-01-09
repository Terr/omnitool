"""Functions for working with HTML entities."""

import re
import htmlentitydefs


def convert_htmlentities_to_unicode(text):
    """Removes HTML or XML character references and entities from a text string.

    @param text The HTML (or XML) source text.
    @return The plain text, as a Unicode string, if necessary.
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # Character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # Named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # Leave as is
    return re.sub("&#?\w+;", fixup, text)

def convert_unicode_to_htmlentities(text):
    """Replaces Unicode/special characters with HTML entities in a text string.

    @param text The source text.
    @return The originial text, possibily with added HTML entities.
    """
    #regex = '\s&|[\X\w]+\s'
    regex = '[^\s;]+\s'

    def convert_match(match):
        """Checks each character in regex match against codepoint
        table.
        """
        r = match.group(0)
        text = ''

        for s in r:
            char_code = ord(s)

            if char_code in htmlentitydefs.codepoint2name:
                text += '&%s;' % htmlentitydefs.codepoint2name[char_code]
            else:
                text += s

        return text

    return re.sub(regex, convert_match, text)
