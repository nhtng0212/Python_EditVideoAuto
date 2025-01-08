from moviepy.editor import VideoFileClip

def get_video_duration(file_path):
    clip = VideoFileClip(file_path)
    duration = clip.duration  # Thời gian tính bằng giây
    clip.close()
    return duration