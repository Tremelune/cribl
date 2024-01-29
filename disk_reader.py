import os

BUFFER_SIZE = 8192


def reverseRead(path: str) -> list:
    """Reads from the local disk.

    Files are assumed to be plaintext with a fixed byte size per character.

    It turns out it's surprisingly difficult to read a file backwards in Python. It must be done sequentially in chunks
    using the file size to scroll to the end and read from there.

    Pulled largely from: https://stackoverflow.com/questions/2301789/how-to-read-a-file-in-reverse-order

    :param path: Absolute path to the file.
    :returns: Generator that iterates over each line of text in the file (separated by a newline character).
    """
    with open(path, 'rb') as file:
        segment = None
        offset = 0
        file.seek(0, os.SEEK_END)
        size = remainingSize = file.tell()
        while remainingSize > 0:
            offset = min(size, offset + BUFFER_SIZE)
            file.seek(size - offset)
            buffer = file.read(min(remainingSize, BUFFER_SIZE))

            # remove file's last "\n" if it exists, only for the first buffer
            if remainingSize == size and buffer[-1] == ord('\n'):
                buffer = buffer[:-1]
            remainingSize -= BUFFER_SIZE
            lines = buffer.split('\n'.encode())

            # append last chunk's segment to this chunk's last line
            if segment is not None:
                lines[-1] += segment
            segment = lines[0]
            lines = lines[1:]

            # yield lines in this chunk except the segment
            for line in reversed(lines):
                # only decode on a parsed line, to avoid utf-8 decode error
                yield line.decode()
                
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment.decode()
