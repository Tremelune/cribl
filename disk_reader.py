import os

BUFFER_SIZE = 8192


# generator for reading text files backwards.
# It relies on characters being UTF-8 and a fixed size.
# It also expects each line to end in a newline character.
def reverseRead(path: str, offset: int, limit: int) -> list:
    with open(path, 'rb') as file:
        segment = None
        current_offset = 0
        file.seek(0, os.SEEK_END)
        size = remainingSize = file.tell()
        while remainingSize > 0:
            current_offset = min(size, current_offset + BUFFER_SIZE)
            file.seek(size - current_offset)
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
            lineCount = 0
            for line in reversed(lines):
                # Limit lines; stop reading the file!
                if lineCount < limit:
                    lineCount += 1
                    # only decode on a parsed line, to avoid utf-8 decode error
                    yield line.decode()
                else:
                    # We can't just break, or we might include the lingering segment.
                    return
                
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment.decode()
