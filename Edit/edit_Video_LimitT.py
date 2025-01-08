import os
import random
import uuid

import cv2
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips
from GetActionFile import getActionFile


def editVideo_Background_MinTime(resolution, flip, audio_choice, folder_video1_path, folder_video2_path,
                                 folder_output_path, folder_background_image_path, min_time):
    list_video1 = getActionFile.get_file_list(folder_video1_path)
    list_video2 = getActionFile.get_file_list(folder_video2_path)
    background_image_path = random.choice(getActionFile.get_file_list(folder_background_image_path))

    clips1 = []
    clips2 = []

    # Kiểm tra danh sách video
    if not list_video1 or not list_video2:
        print("Không có video nào trong danh sách.")
        return

    # Xử lý danh sách video 1
    sum_time1 = 0
    while sum_time1 < min_time and list_video1:
        video1 = random.choice(list_video1)
        list_video1.remove(video1)
        clip1 = VideoFileClip(video1)
        clips1.append(clip1)
        sum_time1 += clip1.duration

    # Xử lý danh sách video 2
    sum_time2 = 0
    while sum_time2 < min_time and list_video2:
        video2 = random.choice(list_video2)
        list_video2.remove(video2)
        clip2 = VideoFileClip(video2)
        clips2.append(clip2)
        sum_time2 += clip2.duration

    # Kiểm tra danh sách clip
    if not clips1 or not clips2:
        print("Không có clip nào để nối.")
        return

    # Nối video
    cap1 = concatenate_videoclips(clips1)
    cap2 = concatenate_videoclips(clips2)

    # Độ phân giải đầu ra
    output_height = resolution
    output_width = int(output_height * (9 / 16))

    # Tính tỷ lệ thu nhỏ
    scale1 = min(output_width // 2 / cap1.w, output_height / cap1.h)
    scale2 = min(output_width // 2 / cap2.w, output_height / cap2.h)

    # Tạo tên video tạm thời
    max_video = len(getActionFile.get_file_list(folder_output_path))
    unique_id = str(uuid.uuid4())
    temp_output_filename = os.path.join(
        "temp_video",
        f"video_{max_video + 1}_{unique_id}_noBg_minT_temp.mp4"
    )

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_output_filename, fourcc, cap1.fps, (output_width, output_height))

    # Lấy âm thanh từ video đã ghép
    audio_source = cap1.audio if audio_choice == 1 else cap2.audio

    # Kiểm tra ảnh nền và xử lý không gian màu nếu cần
    if background_image_path:
        background = cv2.imread(background_image_path, cv2.IMREAD_UNCHANGED)  # Đọc ảnh với tất cả các kênh
        if background is not None:
            background = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)  # Chuyển sang không gian RGB nếu cần
            bg_height, bg_width = background.shape[:2]

            # Cắt phần trung tâm nếu ảnh nền lớn hơn kích thước mong muốn
            if bg_width > output_width or bg_height > output_height:
                x_start = (bg_width - output_width) // 2
                y_start = (bg_height - output_height) // 2
                background = background[y_start:y_start + output_height, x_start:x_start + output_width]
    else:
        # Nền đen mặc định nếu không có ảnh nền
        background = np.zeros((output_height, output_width, 3), dtype=np.uint8)

    # Khởi tạo iterator cho từng frame
    frame_iter1 = cap1.iter_frames()
    frame_iter2 = cap2.iter_frames()

    try:
        while True:
            # Lấy frame của video bên trái
            frame1 = next(frame_iter1, None)
            if frame1 is None:
                break  # Nếu video bên trái kết thúc, dừng hẳn

            # Lấy frame của video bên phải, nếu video bên phải kết thúc, lặp lại từ đầu
            frame2 = next(frame_iter2, None)
            if frame2 is None:
                frame_iter2 = cap2.iter_frames()
                frame2 = next(frame_iter2, None)

            # Điều chỉnh kích thước frame
            frame1 = cv2.resize(frame1, None, fx=scale1, fy=scale1, interpolation=cv2.INTER_AREA)
            frame2 = cv2.resize(frame2, None, fx=scale2, fy=scale2, interpolation=cv2.INTER_AREA)

            # Sao chép ảnh nền cho từng khung hình
            final_frame = background.copy()
            left_x, right_x = 0, output_width // 2

            # Đặt frame
            final_frame[(output_height - frame1.shape[0]) // 2:(output_height + frame1.shape[0]) // 2,
            left_x:left_x + frame1.shape[1]] = frame1
            final_frame[(output_height - frame2.shape[0]) // 2:(output_height + frame2.shape[0]) // 2,
            right_x:right_x + frame2.shape[1]] = frame2

            if flip:
                final_frame = cv2.flip(final_frame, 1)

            out.write(cv2.cvtColor(final_frame, cv2.COLOR_RGB2BGR))

    finally:
        # Kết thúc ghi video
        out.release()
        cv2.destroyAllWindows()

    # Kết hợp âm thanh và lưu video cuối
    video_clip = VideoFileClip(temp_output_filename)
    final_clip = video_clip.set_audio(audio_source)

    # Tạo tên file video cuối
    final_output_filename = os.path.join(
        folder_output_path,
        f"video_{max_video + 1}_{unique_id}_noBg_minT_output.mp4"
    )
    final_clip.write_videofile(final_output_filename, codec="libx264", audio_codec="aac")
    print("Video đã được lưu:", final_output_filename)

    # Giải phóng tài nguyên và xóa file tạm
    final_clip.close()
    video_clip.close()
    if os.path.exists(temp_output_filename):
        os.remove(temp_output_filename)


def editVideo_noBackground_MinTime(resolution, flip, audio_choice, folder_video1_path, folder_video2_path,
                                   folder_output_path, min_time):
    list_video1 = getActionFile.get_file_list(folder_video1_path)
    list_video2 = getActionFile.get_file_list(folder_video2_path)

    clips1 = []
    clips2 = []

    # Kiểm tra danh sách video
    if not list_video1 or not list_video2:
        print("Không có video nào trong danh sách.")
        return

    # Xử lý danh sách video 1
    sum_time1 = 0
    while sum_time1 < min_time and list_video1:
        video1 = random.choice(list_video1)
        list_video1.remove(video1)
        clip1 = VideoFileClip(video1)
        clips1.append(clip1)
        sum_time1 += clip1.duration

    # Xử lý danh sách video 2
    sum_time2 = 0
    while sum_time2 < min_time and list_video2:
        video2 = random.choice(list_video2)
        list_video2.remove(video2)
        clip2 = VideoFileClip(video2)
        clips2.append(clip2)
        sum_time2 += clip2.duration

    # Kiểm tra danh sách clip
    if not clips1 or not clips2:
        print("Không có clip nào để nối.")
        return

    # Nối video
    cap1 = concatenate_videoclips(clips1)
    cap2 = concatenate_videoclips(clips2)

    # Độ phân giải đầu ra
    output_height = resolution
    output_width = int(output_height * (9 / 16))

    # Tính tỷ lệ thu nhỏ
    scale1 = min(output_width // 2 / cap1.w, output_height / cap1.h)
    scale2 = min(output_width // 2 / cap2.w, output_height / cap2.h)

    # Tạo tên video tạm thời
    max_video = len(getActionFile.get_file_list(folder_output_path))
    unique_id = str(uuid.uuid4())
    temp_output_filename = os.path.join(
        "temp_video",
        f"video_{max_video + 1}_{unique_id}_noBg_minT_temp.mp4"
    )

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_output_filename, fourcc, cap1.fps, (output_width, output_height))

    # Lấy âm thanh từ video đã ghép
    audio_source = cap1.audio if audio_choice == 1 else cap2.audio

    # Nếu có ảnh nền, tải ảnh nền và điều chỉnh kích thước
    background = np.zeros((output_height, output_width, 3), dtype=np.uint8)  # Nền đen mặc định nếu không có ảnh nền

    # Khởi tạo iterator cho từng frame
    frame_iter1 = cap1.iter_frames()
    frame_iter2 = cap2.iter_frames()

    try:
        while True:
            # Lấy frame của video bên trái
            frame1 = next(frame_iter1, None)
            if frame1 is None:
                break  # Nếu video bên trái kết thúc, dừng hẳn

            # Lấy frame của video bên phải, nếu video bên phải kết thúc, lặp lại từ đầu
            frame2 = next(frame_iter2, None)
            if frame2 is None:
                frame_iter2 = cap2.iter_frames()
                frame2 = next(frame_iter2, None)

            # Điều chỉnh kích thước frame
            frame1 = cv2.resize(frame1, None, fx=scale1, fy=scale1, interpolation=cv2.INTER_AREA)
            frame2 = cv2.resize(frame2, None, fx=scale2, fy=scale2, interpolation=cv2.INTER_AREA)

            # Sao chép ảnh nền cho từng khung hình
            final_frame = background.copy()
            left_x, right_x = 0, output_width // 2

            # Đặt frame
            final_frame[(output_height - frame1.shape[0]) // 2:(output_height + frame1.shape[0]) // 2,
            left_x:left_x + frame1.shape[1]] = frame1
            final_frame[(output_height - frame2.shape[0]) // 2:(output_height + frame2.shape[0]) // 2,
            right_x:right_x + frame2.shape[1]] = frame2

            if flip:
                final_frame = cv2.flip(final_frame, 1)

            out.write(cv2.cvtColor(final_frame, cv2.COLOR_RGB2BGR))

    finally:
        # Kết thúc ghi video
        out.release()
        cv2.destroyAllWindows()

    # Kết hợp âm thanh và lưu video cuối
    video_clip = VideoFileClip(temp_output_filename)
    final_clip = video_clip.set_audio(audio_source)

    # Tạo tên file video cuối
    final_output_filename = os.path.join(
        folder_output_path,
        f"video_{max_video + 1}_{unique_id}_noBg_minT_output.mp4"
    )
    final_clip.write_videofile(final_output_filename, codec="libx264", audio_codec="aac")
    print("Video đã được lưu:", final_output_filename)

    # Giải phóng tài nguyên và xóa file tạm
    final_clip.close()
    video_clip.close()
    if os.path.exists(temp_output_filename):
        os.remove(temp_output_filename)
