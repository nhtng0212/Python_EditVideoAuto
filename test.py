import os
import cv2


def check_image_files(directory_path):
    """
    Kiểm tra tất cả các ảnh trong thư mục: Kích thước (chiều cao, chiều rộng), số kênh, và trạng thái ảnh.
    """
    # Lấy danh sách các tệp trong thư mục
    files = os.listdir(directory_path)

    # Duyệt qua tất cả các tệp
    for file_name in files:
        # Kiểm tra xem tệp có phải là ảnh không (dựa trên phần mở rộng)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            file_path = os.path.join(directory_path, file_name)

            # Đọc ảnh
            image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

            if image is None:
                print(f"Không thể đọc ảnh: {file_name}")
                continue

            # Lấy kích thước ảnh
            height, width = image.shape[:2]
            channels = image.shape[2] if len(
                image.shape) > 2 else 1  # Nếu có 3 kênh (RGB), lấy số kênh, nếu không lấy 1 (đen trắng)

            # In thông tin về ảnh
            print(f"Ảnh: {file_name}")
            print(f"  - Kích thước: {width}x{height}")
            print(f"  - Số kênh màu: {channels}")

            # Kiểm tra nếu ảnh có kích thước hợp lệ
            if width == 0 or height == 0:
                print(f"  - Cảnh báo: Ảnh có kích thước không hợp lệ (chiều rộng hoặc chiều cao bằng 0).")
            else:
                print(f"  - Ảnh hợp lệ.")
            print("-" * 40)

'''
# Ví dụ sử dụng hàm
directory_path = r"C:\Users\LAPTOP\Pictures\Screenshots"  # Thay đổi thành đường dẫn thư mục ảnh của bạn
check_image_files(directory_path)
'''
