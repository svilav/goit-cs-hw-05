import random
import string
from pathlib import Path


def generate_files(src_folder, num_files):
    Path(src_folder).mkdir(parents=True, exist_ok=True)
    extensions = ['txt', 'png', 'jpg', 'pdf', 'docx']
    for _ in range(num_files):
        ext = random.choice(extensions)
        file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + f'.{ext}'
        file_path = Path(src_folder) / file_name
        with open(file_path, 'w') as f:
            f.write('Test data content.')


def main():
    src_folder = 'test_src'
    num_files = 100
    generate_files(src_folder, num_files)
    print(f"Generated {num_files} files in {src_folder}")


if __name__ == '__main__':
    main()
