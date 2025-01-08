import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from Render import RENDER
from GetActionFile import getActionFile
import datetime
import time


class VideoToolApp:
    def __init__(self, root):
        root.title("Dowload & Edit Video Tiktok _ DEMO 15/12/2024 _ Ver 0.2")
        root.geometry("1000x650")

        # Cấu hình lưới để căn giữa và giãn đều các ô vuông
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # Khung nguồn bên trái
        left_frame = ttk.LabelFrame(root, text="Dowload - Update sau", width=300, height=200)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Khung nguồn bên phải
        right_frame = ttk.LabelFrame(root, text="Dowload - Update sau", width=300, height=200)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Khung nguồn nền
        bg_frame = ttk.LabelFrame(root, text="Chon nguồn", width=300, height=200)
        bg_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.left_source_entry, self.right_source_entry, self.bg_source_entry = self.create_file_frame(bg_frame)

        # Khung hành động (cho thư mục nguồn và độ dài ngắn nhất)
        action_frame = ttk.LabelFrame(root, text="Dowload - Update sau", width=300, height=200)
        action_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Khung hành động kết xuất
        render_frame = ttk.LabelFrame(root, text="Cấu hình render", width=300, height=200)
        render_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.create_render_frame(render_frame)

        # Khung hiển thị đầu ra
        output_frame = ttk.LabelFrame(root, text="Thông báo lỗi", width=300, height=200)
        output_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        # Widget Text để hiển thị đầu ra
        self.output_text = tk.Text(output_frame, wrap="word", height=10, width=40)
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)

    def create_source_frame(self, frame, source_type):
        """Hàm trợ giúp để tạo các khung nguồn với ô nhập và nút chọn"""
        entry = ttk.Entry(frame, width=30)
        entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Nút để chọn thư mục nguồn
        select_button = ttk.Button(frame, text="Chọn", command=lambda: self.select_source(entry, source_type))
        select_button.grid(row=0, column=1, padx=5, pady=5)

        return entry  # Trả về ô nhập để có thể sử dụng sau này

    def create_file_frame(self, frame):
        """Hàm trợ giúp để tạo khung cho các thư mục: video trái, video phải và ảnh nền."""

        # Ô nhập và nút chọn cho thư mục video trái
        left_video_folder_entry = ttk.Entry(frame, width=30)
        left_video_folder_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        left_video_folder_button = ttk.Button(frame, text="Video Trái",
                                              command=lambda: self.select_folder(left_video_folder_entry))
        left_video_folder_button.grid(row=0, column=1, padx=5, pady=5)

        # Ô nhập và nút chọn cho thư mục video phải
        right_video_folder_entry = ttk.Entry(frame, width=30)
        right_video_folder_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        right_video_folder_button = ttk.Button(frame, text="Video Phải",
                                               command=lambda: self.select_folder(right_video_folder_entry))
        right_video_folder_button.grid(row=1, column=1, padx=5, pady=5)

        # Ô nhập và nút chọn cho thư mục ảnh nền
        background_folder_entry = ttk.Entry(frame, width=30)
        background_folder_entry.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        background_folder_button = ttk.Button(frame, text="Ảnh Nền",
                                              command=lambda: self.select_folder(background_folder_entry))
        background_folder_button.grid(row=2, column=1, padx=5, pady=5)

        # Trả về các ô nhập để có thể sử dụng sau này nếu cần
        return left_video_folder_entry, right_video_folder_entry, background_folder_entry

    def select_folder(self, entry):
        """Hàm để mở hộp thoại chọn thư mục và điền đường dẫn vào ô nhập."""
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry.delete(0, tk.END)
            entry.insert(0, folder_path)

    def create_render_frame(self, frame):
        """Hàm trợ giúp để tạo khung kết xuất với số luồng và nút kết xuất"""
        self.render_entry = ttk.Entry(frame, width=30)  # Thêm trường nhập cho thư mục kết xuất
        self.render_entry.grid(row=0, column=0, padx=5, pady=5)

        # Nút để chọn thư mục xuất
        select_button = ttk.Button(frame, text="Video đầu ra", command=self.select_render_folder)
        select_button.grid(row=0, column=1, padx=5, pady=5)

        # Chọn số luồng chạy
        ttk.Label(frame, text="Số Luồng").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.thread_combobox = ttk.Combobox(frame, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], width=5)
        self.thread_combobox.current(0)  # Mặc định chọn 5 luồng
        self.thread_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Checkbox cho việc sử dụng nền
        self.use_background_var = tk.BooleanVar()
        use_background_checkbox = ttk.Checkbutton(frame, text="Sử Dụng Nền", variable=self.use_background_var)
        use_background_checkbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Checkbox cho việc sử dụng thời gian tối thiểu
        self.use_min_time_var = tk.BooleanVar()
        use_min_time_checkbox = ttk.Checkbutton(frame, text="Sử Dụng Thời Gian Tối Thiểu",
                                                variable=self.use_min_time_var)
        use_min_time_checkbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Sử dụng thời gian tối thiểu
        self.shortest_length_entry = ttk.Entry(frame, width=10)  # Thêm ô nhập cho độ dài ngắn nhất
        self.shortest_length_entry.insert(0, "62")  # Gán giá trị mặc định là 62 giây
        self.shortest_length_entry.grid(row=3, column=1, padx=5, pady=5)

        # Checkbox cho việc sử dụng thời gian cố định
        self.use_const_time_var = tk.BooleanVar()
        use_const_time_checkbox = ttk.Checkbutton(frame, text="Sử Dụng Thời Gian Cố định",
                                                  variable=self.use_const_time_var)
        use_const_time_checkbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Sử dụng thời gian cố định
        self.shortest_const_entry = ttk.Entry(frame, width=10)  # Thêm ô nhập cho độ dài ngắn nhất
        self.shortest_const_entry.insert(0, "62")  # Gán giá trị mặc định là 62 giây
        self.shortest_const_entry.grid(row=4, column=1, padx=5, pady=5)

        # Checkbox cho việc lật video
        self.flip_video_var = tk.BooleanVar()
        flip_video_checkbox = ttk.Checkbutton(frame, text="Lật Video", variable=self.flip_video_var)
        flip_video_checkbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # ComboBox cho việc chọn video nào giữ âm thanh
        ttk.Label(frame, text="Chọn video chính").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.keep_sound_combobox = ttk.Combobox(frame, values=["Video trái", "Video phải"], width=10)
        self.keep_sound_combobox.current(0)  # Mặc định chọn Video 1
        self.keep_sound_combobox.grid(row=6, column=1, padx=5, pady=5)

        # ComboBox cho lựa chọn độ phân giải video
        ttk.Label(frame, text="Độ Phân Giải Video").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.resolution_combobox = ttk.Combobox(frame, values=[144, 360, 480, 720, 1080, 1440, 2160], width=10)
        self.resolution_combobox.current(3)  # Mặc định chọn 720p
        self.resolution_combobox.grid(row=7, column=1, padx=5, pady=5)

        # Checkbox cho việc giới hạn tạo video
        self.limit_video_var = tk.BooleanVar()  # Tạo biến mới cho checkbox này
        limit_video_checkbox = ttk.Checkbutton(frame, text="Giới hạn tạo video", variable=self.limit_video_var)
        self.limit_video_var.set(True)
        limit_video_checkbox.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Ô nhập cho độ dài video giới hạn
        self.limitvideo_length_entry = ttk.Entry(frame, width=10)  # Thêm ô nhập cho độ dài video giới hạn
        self.limitvideo_length_entry.insert(0, "10")  # Gán giá trị mặc định là 10
        self.limitvideo_length_entry.grid(row=8, column=1, padx=5, pady=5)

        # Nút thực hiện để bắt đầu kết xuất đơn folder với kích thước cố định
        render_button_single = ttk.Button(frame, text="Render đơn folder", command=self.render_action, width=20)
        render_button_single.grid(row=10, column=0, padx=(15, 0), pady=5, sticky="w")

        # Nút thực hiện để bắt đầu kết xuất đa folder với kích thước cố định
        render_button_multi = ttk.Button(frame, text="Render đa folder", command=self.render_action_multi_folder,
                                         width=20)
        render_button_multi.grid(row=10, column=1, padx=(0, 40), pady=5, sticky="w")

        # Thanh tiến trình
        self.progress_bar = ttk.Progressbar(frame, mode='determinate')
        self.progress_bar.grid(row=11, column=0, columnspan=2, padx=(5, 30), pady=5, sticky="ew")

    def select_source(self, entry, source_type):
        """Chọn thư mục nguồn"""
        folder_path = filedialog.askdirectory()  # Chọn thư mục
        if folder_path:
            entry.delete(0, tk.END)
            entry.insert(0, folder_path)

    def select_file(self, entry):
        """Chọn tệp nguồn nền"""
        file_path = filedialog.askopenfilename()  # Chọn tệp
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    def select_render_folder(self):
        """Chọn thư mục kết xuất"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.render_entry.delete(0, tk.END)
            self.render_entry.insert(0, folder_path)

    def render_action(self):
        # Lấy ngày hiện tại
        current_date = datetime.datetime.now()
        # Định nghĩa ngày giới hạn
        limit_date = datetime.datetime(2024, 12, 15)
        # Kiểm tra xem ngày hiện tại có lớn hơn ngày giới hạn hay không
        if current_date > limit_date:
            messagebox.showwarning("Hết hạn", "Đã quá hạn dùng thử. Liên hệ zalo 0869045270 để được unlock")
            return

        """Thực hiện hành động xuất"""
        left_source = self.left_source_entry.get()
        right_source = self.right_source_entry.get()
        background_source = self.bg_source_entry.get()
        render_folder_source = self.render_entry.get()
        resolution = int(self.resolution_combobox.get())

        if left_source == "" or right_source == "" or background_source == "" or render_folder_source == "":
            message = "Vui lòng nhập đủ các đường dẫn trước khi tiếp tục."
            messagebox.showwarning("Chưa nhập đủ các đường dẫn", message)
            return
        else:
            self.progress_bar["value"] = 10

        audio_choice = 2 if str(self.keep_sound_combobox.get()) == "Video phải" else 1
        limit_video = int(self.limitvideo_length_entry.get()) if self.limit_video_var.get() else -1
        min_time = int(self.shortest_length_entry.get()) if self.use_min_time_var.get() else 62
        const_time = int(self.shortest_const_entry.get()) if self.use_const_time_var.get() else 62
        thread_sum = int(self.thread_combobox.get())

        # Lấy số luồng từ ComboBox
        number_of_threads = int(self.thread_combobox.get())

        def update_progress():
            while any(thread.is_alive() for thread in render_threads):
                # Lấy danh sách các file trong thư mục đầu ra
                current_count = len(getActionFile.get_file_list(render_folder_source))
                progress_value = (current_count / limit_video) * 100 if limit_video != -1 else 100
                self.progress_bar["value"] = min(progress_value, 100)
                time.sleep(1)  # Cập nhật tiến trình mỗi giây

            # Hiển thị thông báo hoàn thành khi tất cả luồng render kết thúc
            self.progress_bar["value"] = 100
            messagebox.showinfo("Thông Báo", "Render thành công!")
            self.progress_bar["value"] = 0

        def render_video():
            if self.use_background_var.get():
                if self.use_const_time_var.get():
                    print(f"EDIT với thời gian cố định {const_time}s và có nền")
                    RENDER.renderOutputVideo_Background_ConstT(
                        resolution=resolution,
                        flip=self.flip_video_var.get(),
                        folder_video1_path=left_source,
                        folder_video2_path=right_source,
                        audio_choice=audio_choice,
                        folder_video_output=render_folder_source,
                        folder_background_image_path=background_source,
                        limit_video=(limit_video + 1) - thread_sum,
                        const_time=const_time
                    )
                elif self.use_min_time_var.get():
                    print(f"EDIT với thời gian nhỏ nhất {const_time}s và có nền")
                    RENDER.renderOutputVideo_Background_MinT(
                        resolution=resolution,
                        flip=self.flip_video_var.get(),
                        folder_video1_path=left_source,
                        folder_video2_path=right_source,
                        audio_choice=audio_choice,
                        folder_video_output=render_folder_source,
                        folder_background_image_path=background_source,
                        limit_video=(limit_video + 1) - thread_sum,
                        min_time=min_time
                    )
                else:
                    print("EDIT tự động có nền")
                    RENDER.renderOutputVideo_Background_noConstT_noLimitT(
                        resolution=resolution,
                        flip=self.flip_video_var.get(),
                        folder_video1_path=left_source,
                        folder_video2_path=right_source,
                        audio_choice=audio_choice,
                        folder_video_output=render_folder_source,
                        folder_background_image_path=background_source,
                        limit_video=(limit_video + 1) - thread_sum,
                    )
            else:
                if self.use_const_time_var.get():
                    print(f"EDIT với thời gian cố định {const_time}s và không có nền")
                    RENDER.renderOutputVideo_noBackground_ConstT(
                        resolution=resolution,
                        flip=self.flip_video_var.get(),
                        folder_video1_path=left_source,
                        folder_video2_path=right_source,
                        audio_choice=audio_choice,
                        folder_video_output=render_folder_source,
                        limit_video=(limit_video + 1) - thread_sum,
                        const_time=const_time
                    )
                elif self.use_min_time_var.get():
                    print(f"EDIT với thời gian nhỏ nhất {const_time}s và không có nền")
                    RENDER.renderOutputVideo_noBackground_MinT(
                        resolution=resolution,
                        flip=self.flip_video_var.get(),
                        folder_video1_path=left_source,
                        folder_video2_path=right_source,
                        audio_choice=audio_choice,
                        folder_video_output=render_folder_source,
                        limit_video=(limit_video + 1) - thread_sum,
                        min_time=min_time
                    )
                else:
                    print("EDIT tự động không nền")
                    RENDER.renderOutputVideo_noBackground_noConstT_noLimitT(
                        resolution=resolution,
                        flip=self.flip_video_var.get(),
                        folder_video1_path=left_source,
                        folder_video2_path=right_source,
                        audio_choice=audio_choice,
                        folder_video_output=render_folder_source,
                        limit_video=(limit_video + 1) - thread_sum,
                    )

        # Tạo và chạy luồng
        render_threads = []
        print(f"TỔNG SỐ LUỒNG CÀI ĐẶT : {self.thread_combobox.get()}")
        for i in range(number_of_threads):
            print(f"Khởi động luồng : {i + 1}")
            render_thread = threading.Thread(target=render_video)
            render_thread.start()
            render_threads.append(render_thread)

        # Tạo và chạy luồng cập nhật tiến trình
        progress_thread = threading.Thread(target=update_progress)
        progress_thread.start()

    def render_action_multi_folder(self):
        # Lấy ngày hiện tại
        current_date = datetime.datetime.now()
        # Định nghĩa ngày giới hạn
        limit_date = datetime.datetime(2024, 12, 15)
        # Kiểm tra xem ngày hiện tại có lớn hơn ngày giới hạn hay không
        if current_date > limit_date:
            messagebox.showwarning("Hết hạn", "Đã quá hạn dùng thử. Liên hệ zalo 0869045270 để được unlock")
            return

        """Thực hiện hành động xuất"""
        left_source = self.left_source_entry.get()
        right_source = self.right_source_entry.get()
        background_source = self.bg_source_entry.get()
        render_folder_source = self.render_entry.get()
        resolution = int(self.resolution_combobox.get())

        if left_source == "" or right_source == "" or background_source == "" or render_folder_source == "":
            message = "Vui lòng nhập đủ các đường dẫn trước khi tiếp tục."
            messagebox.showwarning("Chưa nhập đủ các đường dẫn", message)
            return
        elif len(left_source) == 0 or len(right_source) == 0:
            message = "Folder trái chưa đúng định dạng với chế độ"
            messagebox.showwarning("Sai định dạng", message)
            return
        else:
            self.progress_bar["value"] = 10

        # Lấy đường dẫn các folder
        list_folder_main = getActionFile.get_subfolders(left_source)
        list_folder_right = getActionFile.get_subfolders(right_source)

        # Kiểm tra để taọ các folder kết quả
        list_folder_output = getActionFile.create_folder_structure(left_source, render_folder_source)
        if len(list_folder_main) == len(list_folder_right):
            list_folder_output = getActionFile.create_folder_structure(left_source, render_folder_source)
        elif len(list_folder_main) > len(list_folder_right):
            list_folder_output = getActionFile.create_folder_structure(right_source, render_folder_source)
        elif len(list_folder_main) < len(list_folder_right):
            list_folder_output = getActionFile.create_folder_structure(left_source, render_folder_source)

        if left_source == "" or right_source == "" or background_source == "" or render_folder_source == "":
            message = "Vui lòng nhập đủ các đường dẫn trước khi tiếp tục."
            messagebox.showwarning("Chưa nhập đủ các đường dẫn", message)
            return
        else:
            self.progress_bar["value"] = 10

        audio_choice = 2 if str(self.keep_sound_combobox.get()) == "Video phải" else 1
        limit_video = int(self.limitvideo_length_entry.get()) if self.limit_video_var.get() else -1
        min_time = int(self.shortest_length_entry.get()) if self.use_min_time_var.get() else 62
        const_time = int(self.shortest_const_entry.get()) if self.use_const_time_var.get() else 62
        thread_sum = int(self.thread_combobox.get())

        # Lấy số luồng từ ComboBox
        number_of_threads = int(self.thread_combobox.get())

        def update_progress():
            while any(thread.is_alive() for thread in render_threads):
                # Lấy danh sách các file trong thư mục đầu ra
                current_count = 0
                for i in range(len(list_folder_output)):
                    current_count = current_count + len(getActionFile.get_file_list(list_folder_output[i]))
                progress_value = (current_count / (
                        limit_video * len(list_folder_output))) * 100 if limit_video != -1 else 100
                self.progress_bar["value"] = min(progress_value, 100)
                time.sleep(1)  # Cập nhật tiến trình mỗi giây

                # Hiển thị thông báo hoàn thành khi tất cả luồng render kết thúc
            self.progress_bar["value"] = 100
            messagebox.showinfo("Thông Báo", "Render thành công!")
            self.progress_bar["value"] = 0

        def render_video(folder_left_path, folder_right_path, folder_output_path):
            if self.use_background_var.get():
                if self.use_const_time_var.get():
                    print(f"EDIT với thời gian cố định {const_time}s và có nền")
                    RENDER.renderOutputVideo_Background_ConstT(
                        resolution=resolution,
                        flip=self.flip_video_var.get(),
                        folder_video1_path=folder_left_path,
                        folder_video2_path=folder_right_path,
                        audio_choice=audio_choice,
                        folder_video_output=folder_output_path,
                        folder_background_image_path=background_source,
                        limit_video=(limit_video + 1) - thread_sum,
                        const_time=const_time
                    )
                elif self.use_min_time_var.get():
                    print(f"EDIT với thời gian nhỏ nhất {const_time}s và có nền")
                    RENDER.renderOutputVideo_Background_MinT(
                        resolution=resolution,
                        flip=self.flip_video_var.get(),
                        folder_video1_path=folder_left_path,
                        folder_video2_path=folder_right_path,
                        audio_choice=audio_choice,
                        folder_video_output=folder_output_path,
                        folder_background_image_path=background_source,
                        limit_video=(limit_video + 1) - thread_sum,
                        min_time=min_time
                    )
                else:
                    print("EDIT tự động có nền")
                    RENDER.renderOutputVideo_Background_noConstT_noLimitT(
                        resolution=resolution,
                        flip=self.flip_video_var.get(),
                        folder_video1_path=folder_left_path,
                        folder_video2_path=folder_right_path,
                        audio_choice=audio_choice,
                        folder_video_output=folder_output_path,
                        folder_background_image_path=background_source,
                        limit_video=(limit_video + 1) - thread_sum,
                    )
            else:
                if self.use_const_time_var.get():
                    print(f"EDIT với thời gian cố định {const_time}s và không có nền")
                    RENDER.renderOutputVideo_noBackground_ConstT(
                        resolution=resolution,
                        flip=self.flip_video_var.get(),
                        folder_video1_path=folder_left_path,
                        folder_video2_path=folder_right_path,
                        audio_choice=audio_choice,
                        folder_video_output=folder_output_path,
                        limit_video=(limit_video + 1) - thread_sum,
                        const_time=const_time
                    )
                elif self.use_min_time_var.get():
                    print(f"EDIT với thời gian nhỏ nhất {const_time}s và không có nền")
                    RENDER.renderOutputVideo_noBackground_MinT(
                        resolution=resolution,
                        flip=self.flip_video_var.get(),
                        folder_video1_path=folder_left_path,
                        folder_video2_path=folder_right_path,
                        audio_choice=audio_choice,
                        folder_video_output=folder_output_path,
                        limit_video=(limit_video + 1) - thread_sum,
                        min_time=min_time
                    )
                else:
                    print("EDIT tự động không nền")
                    RENDER.renderOutputVideo_noBackground_noConstT_noLimitT(
                        resolution=resolution,
                        flip=self.flip_video_var.get(),
                        folder_video1_path=folder_left_path,
                        folder_video2_path=folder_right_path,
                        audio_choice=audio_choice,
                        folder_video_output=folder_output_path,
                        limit_video=(limit_video + 1) - thread_sum,
                    )

        # Tạo và chạy luồng
        render_threads = []
        print(f"TỔNG SỐ LUỒNG CÀI ĐẶT : {self.thread_combobox.get()}")
        for i in range(number_of_threads):
            print(f"Khởi động luồng : {i + 1}")
            if len(list_folder_output) > i:
                print(list_folder_main[i])
                print(list_folder_right[i])
                render_thread = threading.Thread(target=render_video,
                                                 args=(
                                                     list_folder_main[i], list_folder_right[i], list_folder_output[i]))
                render_thread.start()
                render_threads.append(render_thread)
            else:
                print("Luồng thừa so với số lượng folder")

        # Tạo và chạy luồng cập nhật tiến trình
        progress_thread = threading.Thread(target=update_progress)
        progress_thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToolApp(root)
    root.mainloop()
