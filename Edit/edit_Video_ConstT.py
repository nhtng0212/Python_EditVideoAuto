import os
import random
import uuid
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips
from GetActionFile import getActionFile


def editVideo_Background_ConstTime(resolution, flip, audio_choice, folder_video1_path, folder_video2_path,
                                   folder_output_path, folder_background_image_path, const_time):
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
    while (sum_time1 < const_time):
        video1 = random.choice(list_video1)
        list_video1.remove(video1)
        clip1 = VideoFileClip(video1)
        if clip1.duration > const_time:
            clips1.append(clip1)
            break
        else:
            clips1.append(clip1)
            sum_time1 += clip1.duration

    # Xử lý danh sách video 2
    sum_time2 = 0
    while (sum_time2 < const_time):
        video2 = random.choice(list_video2)
        list_video2.remove(video2)
        clip2 = VideoFileClip(video2)
        if clip2.duration > const_time:
            clips2.append(clip2)
            break
        else:
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
    final_duration = min(audio_source.duration, const_time)

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

    # Đặt biến đếm frame
    frame_index1 = 0
    frame_index2 = 0

    # Lặp qua các frame và duy trì độ dài video
    while True:
        try:
            # Lấy frame từ video 1
            frame1 = cap1.get_frame(frame_index1 / cap1.fps)
            frame_index1 += 1
        except:
            break  # Nếu video 1 hết, dừng video tổng

        # Lấy frame từ video 2, lặp lại nếu hết video
        try:
            frame2 = cap2.get_frame(frame_index2 / cap2.fps)
            frame_index2 += 1
        except:
            frame_index2 = 0  # Nếu video 2 hết, quay lại từ đầu

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

    # Kết thúc ghi video
    out.release()
    cv2.destroyAllWindows()

    # Kết hợp âm thanh và lưu video cuối
    video_clip = VideoFileClip(temp_output_filename).subclip(0, final_duration)
    final_clip = video_clip.set_audio(audio_source.subclip(0, final_duration))

    # Tạo tên file video cuối
    final_output_filename = os.path.join(
        folder_output_path,
        f"video_{max_video + 1}_{unique_id}_noBg_constT_output.mp4"
    )
    final_clip.write_videofile(final_output_filename, codec="libx264", audio_codec="aac")
    print("Video đã được lưu:", final_output_filename)

    # Giải phóng tài nguyên và xóa file tạm
    final_clip.close()
    video_clip.close()
    if os.path.exists(temp_output_filename):
        os.remove(temp_output_filename)


def editVideo_noBackground_ConstTime(resolution, flip, audio_choice, folder_video1_path, folder_video2_path,
                                     folder_output_path, const_time):
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
    while (sum_time1 < const_time):
        video1 = random.choice(list_video1)
        list_video1.remove(video1)
        clip1 = VideoFileClip(video1)
        if clip1.duration > const_time:
            clips1.append(clip1)
            break
        else:
            clips1.append(clip1)
            sum_time1 += clip1.duration

    # Xử lý danh sách video 2
    sum_time2 = 0
    while (sum_time2 < const_time):
        video2 = random.choice(list_video2)
        list_video2.remove(video2)
        clip2 = VideoFileClip(video2)
        if clip2.duration > const_time:
            clips2.append(clip2)
            break
        else:
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
    final_duration = min(audio_source.duration, const_time)

    # Nếu có ảnh nền, tải ảnh nền và điều chỉnh kích thước
    background = np.zeros((output_height, output_width, 3), dtype=np.uint8)  # Nền đen mặc định nếu không có ảnh nền

    # Đặt biến đếm frame
    frame_index1 = 0
    frame_index2 = 0

    # Lặp qua các frame và duy trì độ dài video
    while True:
        try:
            # Lấy frame từ video 1
            frame1 = cap1.get_frame(frame_index1 / cap1.fps)
            frame_index1 += 1
        except:
            break  # Nếu video 1 hết, dừng video tổng

        # Lấy frame từ video 2, lặp lại nếu hết video
        try:
            frame2 = cap2.get_frame(frame_index2 / cap2.fps)
            frame_index2 += 1
        except:
            frame_index2 = 0  # Nếu video 2 hết, quay lại từ đầu

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

    # Kết thúc ghi video
    out.release()
    cv2.destroyAllWindows()

    # Kết hợp âm thanh và lưu video cuối
    video_clip = VideoFileClip(temp_output_filename).subclip(0, final_duration)
    final_clip = video_clip.set_audio(audio_source.subclip(0, final_duration))

    # Tạo tên file video cuối
    final_output_filename = os.path.join(
        folder_output_path,
        f"video_{max_video + 1}_{unique_id}_noBg_constT_output.mp4"
    )
    final_clip.write_videofile(final_output_filename, codec="libx264", audio_codec="aac")
    print("Video đã được lưu:", final_output_filename)

    # Giải phóng tài nguyên và xóa file tạm
    final_clip.close()
    video_clip.close()
    if os.path.exists(temp_output_filename):
        os.remove(temp_output_filename)
