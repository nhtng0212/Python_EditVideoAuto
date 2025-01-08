from Edit import edit_Video_noConstT_noLimitT
from GetActionFile import getActionFile
import os
import random
from Edit import edit_Video_ConstT
from Edit import edit_Video_LimitT
import itertools


def renderOutputVideo_noBackground_noConstT_noLimitT(resolution, flip, folder_video1_path, folder_video2_path,
                                                     audio_choice,
                                                     folder_video_output, limit_video):
    # Lấy danh sách các file trong các folder video
    list_video_1 = getActionFile.get_file_list(os.path.normpath(folder_video1_path))
    list_video_2 = getActionFile.get_file_list(os.path.normpath(folder_video2_path))

    print(os.path.normpath(folder_video1_path))

    # Tạo tất cả các kết hợp có thể giữa video1 và video2
    possible_combinations = list(itertools.product(list_video_1, list_video_2))

    # Lặp qua tất cả các kết hợp có thể
    while possible_combinations:
        list_video_output = getActionFile.get_file_list(folder_video_output)

        # Chọn ngẫu nhiên một cặp video từ các kết hợp còn lại
        video1_path, video2_path = random.choice(possible_combinations)

        # Tạo tên file cho video đầu ra
        max_name = len(getActionFile.get_file_list(folder_video_output))
        final_output_filename = os.path.join(
            folder_video_output,
            f'video_{max_name + 1}_noBg_noT_output.mp4'
        )

        if final_output_filename.replace("\\", "\\\\") not in list_video_output:
            if limit_video != -1 and limit_video == len(list_video_output):
                break

            # Xử lý video nếu không bị trùng tên
            try:
                print(f"Processing videos: {video1_path} and {video2_path}")
                edit_Video_noConstT_noLimitT.editVideo_noBackground_noTime(
                    resolution=resolution,
                    flip=flip,
                    audio_choice=audio_choice,
                    video1_path=video1_path,
                    video2_path=video2_path,
                    folder_output_path=folder_video_output
                )
            except Exception as e:
                print(f"Có lỗi với video này: {e}")

        # Loại bỏ kết hợp đã thử khỏi danh sách các kết hợp có thể
        possible_combinations.remove((video1_path, video2_path))

    # Thông báo khi tất cả các kết hợp đã được xử lý
    print("Các video kết hợp đã vào hàng được xử lý.")


def renderOutputVideo_Background_noConstT_noLimitT(resolution, flip, folder_video1_path, folder_video2_path,
                                                   audio_choice,
                                                   folder_video_output, folder_background_image_path, limit_video):
    # Lấy danh sách các file trong các folder video
    list_video_1 = getActionFile.get_file_list(os.path.normpath(folder_video1_path))
    list_video_2 = getActionFile.get_file_list(os.path.normpath(folder_video2_path))

    # Tạo tất cả các kết hợp có thể giữa video1 và video2
    possible_combinations = list(itertools.product(list_video_1, list_video_2))

    # Lặp qua tất cả các kết hợp có thể
    while possible_combinations:
        list_video_output = getActionFile.get_file_list(folder_video_output)

        # Chọn ngẫu nhiên một cặp video từ các kết hợp còn lại
        video1_path, video2_path = random.choice(possible_combinations)

        # Tạo tên file cho video đầu ra
        max_name = len(getActionFile.get_file_list(folder_video_output))
        final_output_filename = os.path.join(
            folder_video_output,
            f"video_{max_name + 1}_Bg_noT_output.mp4"
        )
        print(final_output_filename)

        # Kiểm tra nếu tên video đã tồn tại trong thư mục đầu ra
        if final_output_filename.replace("\\", "\\\\") not in list_video_output:
            if limit_video != -1 and limit_video == len(list_video_output):
                break

            # Xử lý video nếu không bị trùng tên
            print(f"Processing videos: {video1_path} and {video2_path}")

            try:
                edit_Video_noConstT_noLimitT.editVideo_Background_noTime(
                    resolution=resolution,
                    flip=flip,
                    audio_choice=audio_choice,
                    video1_path=video1_path,
                    video2_path=video2_path,
                    folder_background_image_path=folder_background_image_path,
                    folder_output_path=folder_video_output
                )
            except Exception as e:
                print(f"Có lỗi với video này: {e}")

        # Loại bỏ kết hợp đã thử khỏi danh sách các kết hợp có thể
        possible_combinations.remove((video1_path, video2_path))

    # Thông báo khi tất cả các kết hợp đã được xử lý
    print("Các video kết hợp đã vào hàng được xử lý.")


def renderOutputVideo_noBackground_ConstT(resolution, flip, folder_video1_path, folder_video2_path, audio_choice,
                                          folder_video_output, limit_video, const_time):
    # Lặp qua tất cả các kết hợp có thể
    while len(getActionFile.get_file_list(folder_video_output)) < limit_video:
        list_video_output = getActionFile.get_file_list(folder_video_output)

        # Tạo tên file cho video đầu ra
        max_name = len(list_video_output)
        final_output_filename = os.path.join(
            folder_video_output,
            f"video_{max_name + 1}_noBg_constT_output.mp4"
        )

        if final_output_filename.replace("\\", "\\\\") not in list_video_output:
            if limit_video != -1 and limit_video == len(list_video_output):
                break

            try:
                edit_Video_ConstT.editVideo_noBackground_ConstTime(
                    resolution=resolution,
                    flip=flip,
                    audio_choice=audio_choice,
                    folder_video1_path=folder_video1_path,
                    folder_video2_path=folder_video2_path,
                    folder_output_path=folder_video_output,
                    const_time=const_time
                )
            except Exception as e:
                print(f"Có lỗi với video này: {e}")

    # Thông báo khi tất cả các kết hợp đã được xử lý
    print("Các video kết hợp đã vào hàng được xử lý.")


def renderOutputVideo_Background_ConstT(resolution, flip, folder_video1_path, folder_video2_path, audio_choice,
                                        folder_video_output, folder_background_image_path, limit_video, const_time):
    # Lặp qua tất cả các kết hợp có thể
    while len(getActionFile.get_file_list(folder_video_output)) < limit_video:
        list_video_output = getActionFile.get_file_list(folder_video_output)

        # Tạo tên file cho video đầu ra
        max_name = len(list_video_output)
        final_output_filename = os.path.join(
            folder_video_output,
            f"video_{max_name + 1}_Bg_constT_output.mp4"
        )

        if final_output_filename.replace("\\", "\\\\") not in list_video_output:
            if limit_video != -1 and limit_video == len(list_video_output):
                break

            try:
                edit_Video_ConstT.editVideo_Background_ConstTime(
                    resolution=resolution,
                    flip=flip,
                    audio_choice=audio_choice,
                    folder_video1_path=folder_video1_path,
                    folder_video2_path=folder_video2_path,
                    folder_output_path=folder_video_output,
                    folder_background_image_path=folder_background_image_path,
                    const_time=const_time
                )
            except Exception as e:
                print(f"Có lỗi với video này: {e}")

    # Thông báo khi tất cả các kết hợp đã được xử lý
    print("Các video kết hợp đã vào hàng được xử lý.")


def renderOutputVideo_noBackground_MinT(resolution, flip, folder_video1_path, folder_video2_path, audio_choice,
                                        folder_video_output, limit_video, min_time):
    # Lặp qua tất cả các kết hợp có thể
    while len(getActionFile.get_file_list(folder_video_output)) < limit_video:
        list_video_output = getActionFile.get_file_list(folder_video_output)

        # Tạo tên file cho video đầu ra
        max_name = len(list_video_output)
        final_output_filename = os.path.join(
            folder_video_output,
            f"video_{max_name + 1}_noBg_minT_temp.mp4"
        )

        if final_output_filename.replace("\\", "\\\\") not in list_video_output:
            if limit_video != -1 and limit_video == len(list_video_output):
                break

            try:
                edit_Video_LimitT.editVideo_noBackground_MinTime(
                    resolution=resolution,
                    flip=flip,
                    audio_choice=audio_choice,
                    folder_video1_path=folder_video1_path,
                    folder_video2_path=folder_video2_path,
                    folder_output_path=folder_video_output,
                    min_time=min_time
                )
            except Exception as e:
                print(f"Có lỗi với video này: {e}")
    # Thông báo khi tất cả các kết hợp đã được xử lý
    print("Các video kết hợp đã vào hàng được xử lý.")


def renderOutputVideo_Background_MinT(resolution, flip, folder_video1_path, folder_video2_path, audio_choice,
                                      folder_video_output, folder_background_image_path, limit_video, min_time):
    # Lặp qua tất cả các kết hợp có thể
    while len(getActionFile.get_file_list(folder_video_output)) < limit_video:
        list_video_output = getActionFile.get_file_list(folder_video_output)

        # Tạo tên file cho video đầu ra
        max_name = len(list_video_output)
        final_output_filename = os.path.join(
            folder_video_output,
            f"video_{max_name + 1}_Bg_minT_temp.mp4"
        )

        if final_output_filename.replace("\\", "\\\\") not in list_video_output:
            if limit_video != -1 and limit_video == len(list_video_output):
                break

            try:
                edit_Video_LimitT.editVideo_Background_MinTime(
                    resolution=resolution,
                    flip=flip,
                    audio_choice=audio_choice,
                    folder_video1_path=folder_video1_path,
                    folder_video2_path=folder_video2_path,
                    folder_output_path=folder_video_output,
                    folder_background_image_path=folder_background_image_path,
                    min_time=min_time
                )
            except Exception as e:
                print(f"Có lỗi với video này:{e}")

    # Thông báo khi tất cả các kết hợp đã được xử lý
    print("Các video kết hợp đã vào hàng được xử lý.")
