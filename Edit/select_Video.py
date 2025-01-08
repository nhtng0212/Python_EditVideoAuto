import random
from moviepy.editor import VideoFileClip, concatenate_videoclips
from GetActionVideo import getActionVideo
from GetActionFile import getActionFile


def getListVideoLeft(folder_video_left_path, limit_time):
    list_video_left = getActionFile.get_file_list(folder_video_left_path)
    list_video_left_after = []

    time = 0
    while (time < int(limit_time)):
        video_left = random.choice(list_video_left)
        if video_left not in list_video_left_after:
            list_video_left_after.append(video_left)
            time = time + getActionVideo.get_video_duration(video_left)

    return list_video_left_after


def getListVideoRight(folder_video_right_path, limit_time):
    list_video_right = getActionFile.get_file_list(folder_video_right_path)
    list_video_right_after = []

    time = 0
    while (time < int(limit_time)):
        video_right = random.choice(list_video_right)
        if video_right not in list_video_right_after:
            list_video_right_after.append(video_right)
            time = time + getActionVideo.get_video_duration(video_right)

    return list_video_right_after


def video_Concatenation_Left(list_video, limit_time):
    clips = []
    print(list_video, limit_time)

    # Lấy danh sách video
    video_files = list_video

    # Kiểm tra xem danh sách video có rỗng không
    if not video_files:
        print("Không có video nào trong danh sách.")
        return

    for video in video_files:
        clip = VideoFileClip(video)

        # Cắt clip nếu nó dài hơn limit_time
        if clip.duration > limit_time:
            clips.append(clip)
            break
        else:
            clips.append(clip)

    # Kiểm tra xem danh sách clips có rỗng không
    if not clips:
        print("Không có clip nào để nối.")
        return

    # Nối các video lại với nhau
    final_video = concatenate_videoclips(clips)

    # Xuất video đã ghép
    final_video.write_videofile("video_concatenation_left.mp4", codec="libx264", audio_codec="aac")


def video_Concatenation_Right(list_video, limit_time):
    clips = []
    print(list_video, limit_time)

    for video in list_video:
        clip = VideoFileClip(video)

        # Cắt clip nếu nó dài hơn limit_time
        if clip.duration > limit_time:
            clips.append(clip)
            break
        else:
            clips.append(clip)

    # Nối các video lại với nhau
    final_video = concatenate_videoclips(clips)

    # Xuất video đã ghép
    final_video.write_videofile("video_concatenation_right.mp4", codec="libx264", audio_codec="aac")
