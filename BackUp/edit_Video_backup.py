import cv2
from moviepy.editor import VideoFileClip
import os


def editVideo_noBackground_noTime(resolution, flip, audio_choice, video1_path, video2_path, folder_output_path):
    print(f"Đang edit 2 video không background và không giới hạn thời gian : {video1_path} , {video2_path}")

    # Đường dẫn đến 2 video
    video_path1 = video1_path
    video_path2 = video2_path

    # Tải 2 video
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)

    # Kiểm tra xem có mở được video hay không
    if not cap1.isOpened() or not cap2.isOpened():
        print('Không thể mở được video')
        return

    # Độ phân giải video đầu ra
    output_height = resolution
    output_width = int(output_height * (9 / 16))

    # Tính toán tỷ lệ thu nhỏ để vừa kích thước TikTok
    scale1 = min(output_width // 2 / cap1.get(cv2.CAP_PROP_FRAME_WIDTH),
                 output_height / cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scale2 = min(output_width // 2 / cap2.get(cv2.CAP_PROP_FRAME_WIDTH),
                 output_height / cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Tạo tên video tạm thời
    temp_output_filename = os.path.join(folder_output_path,
                                        f"{os.path.basename(video1_path)}_{os.path.basename(video2_path)}_nobackground_temp.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(temp_output_filename, fourcc, cap1.get(cv2.CAP_PROP_FPS), (output_width, output_height))

    # Thời gian video và thời gian âm thanh
    total_audio_duration = VideoFileClip(video1_path if audio_choice == 1 else video2_path).duration
    current_audio_time = 0

    # Vòng lặp xử lý từng frame
    while current_audio_time < total_audio_duration:
        # Đọc frame từ 2 video
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        # Nếu video1 hết thì reset về đầu
        if not ret1:
            cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret1, frame1 = cap1.read()

        # Nếu video2 hết thì reset về đầu
        if not ret2:
            cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret2, frame2 = cap2.read()

        # Kiểm tra xem có đọc được frame hay không
        if not ret1 or not ret2:
            break

        # Thay đổi kích thước frame cho phù hợp với TikTok
        frame1 = cv2.resize(frame1, None, fx=scale1, fy=scale1, interpolation=cv2.INTER_AREA)
        frame2 = cv2.resize(frame2, None, fx=scale2, fy=scale2, interpolation=cv2.INTER_AREA)

        # Tính toán kích thước trống để thêm vào
        empty_width1 = output_width // 2 - frame1.shape[1]
        empty_width2 = output_width // 2 - frame2.shape[1]
        empty_height1 = output_height - frame1.shape[0]
        empty_height2 = output_height - frame2.shape[0]

        # Tính toán kích thước cho frame đầu tiên
        top_padding1 = empty_height1 // 2
        bottom_padding1 = empty_height1 - top_padding1
        frame1 = cv2.copyMakeBorder(
            frame1, top_padding1, bottom_padding1, 0, empty_width1, cv2.BORDER_CONSTANT, value=(0, 0, 0)
        )

        # Tính toán kích thước cho frame thứ hai
        top_padding2 = empty_height2 // 2
        bottom_padding2 = empty_height2 - top_padding2
        frame2 = cv2.copyMakeBorder(
            frame2, top_padding2, bottom_padding2, 0, empty_width2, cv2.BORDER_CONSTANT, value=(0, 0, 0)
        )

        # Ghép 2 frame theo chiều ngang
        merged_frame = cv2.hconcat([frame1, frame2])

        # Nếu flip = True thì lật video
        if flip:
            merged_frame = cv2.flip(merged_frame, 1)  # Lật theo chiều ngang

        # Ghi frame kết quả vào video đầu ra tạm thời
        out.write(merged_frame)

        # Cập nhật thời gian âm thanh
        current_audio_time += 1 / cap1.get(cv2.CAP_PROP_FPS)

    # Giải phóng tài nguyên
    cap1.release()
    cap2.release()
    out.release()
    cv2.destroyAllWindows()

    # Chọn video làm nguồn âm thanh
    audio_source = VideoFileClip(video1_path if audio_choice == 1 else video2_path).audio

    # Tạo video đầu ra với âm thanh
    video_clip = VideoFileClip(temp_output_filename)
    final_clip = video_clip.set_audio(audio_source)

    # Tạo tên file video cuối cùng
    final_output_filename = os.path.join(folder_output_path, os.path.basename(video1_path).split('.')[0] + '_' +
                                         os.path.basename(video2_path).split('.')[0] + '_final_output.mp4')

    # Lưu video cuối cùng
    final_clip.write_videofile(final_output_filename, codec="libx264", audio_codec="aac")
    print(f"Video đã được lưu: {final_output_filename}")

    # Giải phóng tài nguyên
    final_clip.close()
    video_clip.close()

    # Xóa video tạm thời
    if os.path.exists(temp_output_filename):
        os.remove(temp_output_filename)

    print(f"Đã edit xong 2 video : {video_path1}, {video_path2}")


def editVideo_Background_noTime(resolution, flip, audio_choice, video1_path, video2_path,
                                background_image_path, folder_output_path):
    print(f"Đang edit 2 video có background và không giới hạn thời gian : {video1_path} , {video2_path}")

    # Đường dẫn đến 2 video
    video_path1 = r"{}".format(video1_path)
    video_path2 = r"{}".format(video2_path)

    # Tải 2 video
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)

    # Kiểm tra xem có mở được video hay không
    if not cap1.isOpened() or not cap2.isOpened():
        print('Không thể mở được video')
        return

    # Độ phân giải video đầu ra
    output_height = resolution
    output_width = int(output_height * (9 / 16))

    # Tải ảnh nền và thay đổi kích thước phù hợp với video đầu ra
    background_image = cv2.imread(background_image_path)
    background_image = cv2.resize(background_image, (output_width, output_height))

    # Tính toán tỷ lệ thu nhỏ để vừa kích thước TikTok
    scale1 = min(output_width // 2 / cap1.get(cv2.CAP_PROP_FRAME_WIDTH),
                 output_height / cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scale2 = min(output_width // 2 / cap2.get(cv2.CAP_PROP_FRAME_WIDTH),
                 output_height / cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Tạo tên video tạm thời
    temp_output_filename = os.path.join(folder_output_path,
                                        f"{os.path.basename(video1_path)}_{os.path.basename(video2_path)}_background_temp.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(temp_output_filename, fourcc, cap1.get(cv2.CAP_PROP_FPS), (output_width, output_height))

    # Thời gian video và thời gian âm thanh
    total_audio_duration = VideoFileClip(video1_path if audio_choice == 1 else video2_path).duration
    current_audio_time = 0

    # Vòng lặp xử lý từng frame
    while current_audio_time < total_audio_duration:
        # Đọc frame từ 2 video
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        # Nếu video1 hết thì reset về đầu
        if not ret1:
            cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret1, frame1 = cap1.read()

        # Nếu video2 hết thì reset về đầu
        if not ret2:
            cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret2, frame2 = cap2.read()

        # Kiểm tra xem có đọc được frame hay không
        if not ret1 or not ret2:
            break

        # Thay đổi kích thước frame cho phù hợp với TikTok
        frame1 = cv2.resize(frame1, None, fx=scale1, fy=scale1, interpolation=cv2.INTER_AREA)
        frame2 = cv2.resize(frame2, None, fx=scale2, fy=scale2, interpolation=cv2.INTER_AREA)

        # Tính toán vị trí của từng video trên ảnh nền
        left_x = 0
        right_x = output_width // 2
        top_y1 = (output_height - frame1.shape[0]) // 2
        top_y2 = (output_height - frame2.shape[0]) // 2

        # Tạo bản sao của ảnh nền
        final_frame = background_image.copy()

        # Đặt frame1 vào phía bên trái của ảnh nền
        final_frame[top_y1:top_y1 + frame1.shape[0], left_x:left_x + frame1.shape[1]] = frame1

        # Đặt frame2 vào phía bên phải của ảnh nền
        final_frame[top_y2:top_y2 + frame2.shape[0], right_x:right_x + frame2.shape[1]] = frame2

        # Nếu flip = True thì lật video
        if flip:
            final_frame = cv2.flip(final_frame, 1)  # Lật theo chiều ngang

        # Ghi frame kết quả vào video đầu ra tạm thời
        out.write(final_frame)

        # Cập nhật thời gian âm thanh
        current_audio_time += 1 / cap1.get(cv2.CAP_PROP_FPS)

    # Giải phóng tài nguyên
    cap1.release()
    cap2.release()
    out.release()
    cv2.destroyAllWindows()

    # Chọn video làm nguồn âm thanh
    audio_source = VideoFileClip(video1_path if audio_choice == 1 else video2_path).audio

    # Tạo video đầu ra với âm thanh
    video_clip = VideoFileClip(temp_output_filename)
    final_clip = video_clip.set_audio(audio_source)

    # Tạo tên file video cuối cùng
    final_output_filename = os.path.join(folder_output_path, os.path.basename(video1_path).split('.')[0] + '_' +
                                         os.path.basename(video2_path).split('.')[0] + '_final_output.mp4')

    # Lưu video cuối cùng
    final_clip.write_videofile(final_output_filename, codec="libx264", audio_codec="aac")
    print(f"Video đã được lưu: {final_output_filename}")

    # Giải phóng tài nguyên
    final_clip.close()
    video_clip.close()

    # Xóa video tạm thời
    if os.path.exists(temp_output_filename):
        os.remove(temp_output_filename)

    print(f"Đã edit xong 2 video : {video_path1}, {video_path2}")

# editVideo_Background_noTime(720, True, 1, r"E:\video_1\Download (1).mp4", r"E:\video_1\Download (3).mp4",
#                            r"C:\Users\LAPTOP\Pictures\Screenshots\Screenshot 2024-06-23 231524.png", r"E:\outputVideo")
