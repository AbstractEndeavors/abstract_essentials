import os
import shutil
import json


def create_directory_map(folder_path):
    """
    Creates a map of the directory structure, file sizes, and token counts for a given folder.

    Args:
        folder_path (str): The path to the folder.

    Returns:
        dict: The directory map containing file information.
    """
    directory_map = {}
    replica_folder_path = folder_path + "_replica"

    # Remove the replica folder if it exists, and create a new one
    if os.path.exists(replica_folder_path):
        shutil.rmtree(replica_folder_path)
    shutil.copytree(folder_path, replica_folder_path, ignore=shutil.ignore_patterns('*.*'))  # Copy the folder structure only, excluding all files

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            replica_file_path = file_path.replace(folder_path, replica_folder_path)

            size = os.path.getsize(file_path)
            tokens = 0
            content = read_file_if_not_image(file_path)
            if content is not None:
                tokens = tokenize(content)

            # Create a blank file in the replica folder
            if not imgTF(file_path):
                with open(replica_file_path, "w", encoding="utf-8"):
                    pass

            directory_map[file_path] = {"size": size, "tokens": tokens, 'image': imgTF(file_path)}
    print(json.dumps(directory_map, indent=2))
    return directory_map

def get_size(path):
    """
    Calculates the total size of a file or directory.

    Args:
        path (str): The path to the file or directory.

    Returns:
        int: The total size in bytes.
    """
    if os.path.isfile(path):
        return os.path.getsize(path)
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            fp = os.path.join(dirpath, file)
            total_size += os.path.getsize(fp)
    return total_size

def process_file_content(content, resp, file_path):
    """
    Processes the content of a file and performs section-wise revision using OpenAI.

    Args:
        content (str): The content of the file.
        resp (str): The response from OpenAI.
        file_path (str): The path to the file.

    Returns:
        str: The updated content after revision.
    """
    updated = ''
    resp = loadIt(resp)
    sections = [content[i:i + token_size['desiredTokenSize']] for i in range(0, len(content), token_size['desiredTokenSize'])]

    for index, section in enumerate(sections):
        section_prompt = f'\n\nThis is section {index + 1} of {len(sections)} for {file_path}:\n'
        send_it = {"botNotation": resp["botNotation"], "revision": resp["revision"], "section_prompt": section_prompt, "section": section}
        tokens = tokenize(str(send_it))

        if token_size['maxTokenSize'] < tokens:
            subsections = [section[i:i + token_size['desiredTokenSize']] for i in range(0, len(section), token_size['maxTokenSize'])]
            for sub_index, subsection in enumerate(subsections):
                subsection_prompt = f'\n\nThis is subsection {sub_index + 1} of {len(subsections)} for section {index + 1} of {len(sections)} for {file_path}:\n'
                send_it["subsection_prompt"] = subsection_prompt
                send_it["subsection"] = subsection
                resp = send_to_openai(send_it)
                updated += ifrRev(send_it["subsection"], resp)['revision']
        else:
            resp = send_to_openai(send_it)
            updated += ifrRev(send_it["section"], resp)['revision']
    print(updated)
    return resp

def imgTF(file_path):
    """
    Checks if a file is an image based on its file extension.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file is an image, False otherwise.
    """
    if not imghdr.what(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return False
        except (UnicodeDecodeError, IOError) as e:
            print(f"Error reading file: {file_path}. {e}")
            return False
    else:
        return True
