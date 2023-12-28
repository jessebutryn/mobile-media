import os

def format_size(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}

    while size >= power:
        size /= power
        n += 1

    return f"{size:.2f} {power_labels[n]}"

def get_file_size(file):
	size = os.path.getsize(file)
	formatted_size = format_size(size)
	return formatted_size

def is_directory_writable(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        test_file = os.path.join(directory, 'test_file.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True
    except Exception as e:
        return False

def get_file_path(file):
     directory_path = os.path.dirname(file)
     return directory_path

def get_basename(file):
	filename = os.path.basename(file)
	return filename
