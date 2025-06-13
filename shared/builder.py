import base64

class ContentBuilder:
    """
    A class that reassembles content from a series of obfuscated data chunks.
    This looks like a legitimate utility to an outside observer.
    """
    def __init__(self, key):
        self._k = key
        self._s = []
    def _d(self, c):
        """Internal 'decode' method."""
        s = base64.b64decode(c).decode('utf-8')
        r = ""
        for i in range(len(s)):
            r += chr(ord(s[i]) ^ ord(self._k[i % len(self._k)]))
        return r

    def a(self, chunk_data):
        """Public method 'a' (for 'add') to append a data chunk."""
        self._s.append(chunk_data)

    def b(self):
        """Public method 'b' (for 'build') to construct the final content."""
        return "".join([self._d(chunk) for chunk in self._s])