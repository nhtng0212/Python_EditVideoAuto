import os
from pathlib import Path


def get_file_list(folder_path):
    file_names = []
    try:
        # Lấy danh sách các file trong folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            # Chỉ thêm vào mảng nếu là file
            if os.path.isfile(file_path):
                # Thêm đường dẫn tuyệt đối vào mảng
                file_names.append(os.path.abspath(file_path))
    except Exception as e:
        print(f"Lỗi khi lấy danh sách file: {e}")
    return file_names


def get_subfolders(parent_folder):
    subfolders = [os.path.join(parent_folder, folder) for folder in os.listdir(parent_folder)
                  if os.path.isdir(os.path.join(parent_folder, folder))]
    return subfolders


def create_folder_structure(parent_folder, folder_output):
    list_folder = get_subfolders(parent_folder)

    for folder_child in list_folder:
        folder_child_name = f"{os.path.basename(folder_child)}_output"
        # Tạo đường dẫn cho folder mới bên trong folder_output
        new_folder_path = Path(folder_output) / folder_child_name
        # Tạo folder mới với cấu trúc như folder gốc
        new_folder_path.mkdir(parents=True, exist_ok=True)

    return get_subfolders(folder_output)
