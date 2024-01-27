import os


# Generates a "log" file. Designed to be run once from the command line.
def create_large_text_file(file_path, file_size_gb):
    file_size_bytes = file_size_gb * (1024 ** 3)
    index_format = "{:09d}"  # 9-digit zero-padded index

    with open(file_path, 'w') as file:
        index = 1
        while os.path.getsize(file_path) < file_size_bytes:
            line = f"{index_format.format(index)} This is line {index}\n"
            file.write(line)
            index += 1


if __name__ == "__main__":
    file_path = "/var/log/bigboy.log"
    file_size_gb = 2

    create_large_text_file(file_path, file_size_gb)
    print(f"File '{file_path}' created with size over 1GB.")
