import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
from translator_core import (
    translate_xml_file, 
    translate_text, 
    append_to_xml_file, 
    translate_texts_batch, 
    translate_and_append_batch
)
import queue
import threading

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XML Translator")
        
        # Đặt kích thước cửa sổ cố định thay vì full screen
        window_width = 1024  # Chiều rộng cửa sổ
        window_height = 768  # Chiều cao cửa sổ
        
        # Lấy kích thước màn hình
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Tính toán vị trí để cửa sổ nằm giữa màn hình
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        # Đặt kích thước và vị trí cửa sổ
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        # Cho phép resize cửa sổ
        self.root.resizable(True, True)
        
        # Đặt kích thước tối thiểu để UI không bị vỡ
        self.root.minsize(800, 600)
        
        # Xử lý sự kiện cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Unmap>", self.on_minimize)
        self.root.bind("<Map>", self.on_restore)
        
        # Biến để theo dõi trạng thái
        self.is_processing = False
        self.is_minimized = False
        
        # Thêm queue để xử lý cập nhật UI
        self.ui_queue = queue.Queue()
        
        # Thiết lập UI
        self.setup_ui()
        
    def on_minimize(self, event):
        """Xử lý khi cửa sổ bị thu nhỏ"""
        self.is_minimized = True
        # Tạm dừng cập nhật UI nếu đang xử lý
        if self.is_processing:
            self.pause_ui_updates()
    
    def on_restore(self, event):
        """Xử lý khi cửa sổ được khôi phục"""
        self.is_minimized = False
        # Tiếp tục cập nhật UI nếu đang xử lý
        if self.is_processing:
            self.resume_ui_updates()
    
    def on_closing(self):
        """Xử lý khi đóng cửa sổ"""
        if self.is_processing:
            if messagebox.askokcancel("Quit", "Translation is in progress. Do you want to quit?"):
                self.root.quit()
        else:
            self.root.quit()
            
    def pause_ui_updates(self):
        """Tạm dừng cập nhật UI"""
        if hasattr(self, 'text_status'):
            self.text_status.config(state='disabled')
        if hasattr(self, 'status_text'):
            self.status_text.config(state='disabled')
            
    def resume_ui_updates(self):
        """Tiếp tục cập nhật UI"""
        if hasattr(self, 'text_status'):
            self.text_status.config(state='normal')
        if hasattr(self, 'status_text'):
            self.status_text.config(state='normal')
            
    def setup_ui(self):
        # Tạo frame chính để chứa tất cả các elements
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        
        # Tạo notebook để chứa các tab
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Tab 1: Dịch file XML
        self.file_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.file_frame, text='Translate XML File')
        
        # Tab 2: Dịch và thêm chuỗi
        self.text_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.text_frame, text='Add New String')
        
        # Thiết lập các tab
        self.setup_file_translation_tab(self.file_frame)
        self.setup_text_translation_tab(self.text_frame)
        
        # Xử lý sự kiện chuyển tab
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        
    def on_tab_changed(self, event):
        """Xử lý sự kiện khi chuyển tab"""
        if self.is_processing:
            return
            
        try:
            current_tab = self.notebook.select()
            tab_id = self.notebook.index(current_tab)
            
            # Cập nhật UI của tab mới
            self.main_frame.update_idletasks()
            
            # Nếu chuyển sang tab Add New String
            if tab_id == 1:
                # Cập nhật danh sách values folders nếu có đường dẫn
                if hasattr(self, 'text_output_path') and self.text_output_path.get():
                    self.main_frame.after(100, lambda: self.update_values_folders(self.text_output_path.get()))
                    
        except Exception as e:
            print(f"Error switching tabs: {str(e)}")

    def on_window_resize(self, event):
        """Xử lý sự kiện khi cửa sổ bị resize"""
        if event.widget == self.root:
            # Cập nhật lại kích thước các elements nếu cần
            self.main_frame.update_idletasks()

    def add_common_language_buttons(self, parent_frame, add_callback):
        """Thêm các nút cho ngôn ngữ phổ biến"""
        common_langs_frame = ttk.Frame(parent_frame)
        common_langs_frame.pack(side='left', padx=10, pady=5)

        common_langs = [
            ("Vietnamese - vi", "vi"), ("Chinese - zh", "zh"),
            ("Korean - ko", "ko"), ("Japanese - ja", "ja"),
            ("Italian - it", "it"), ("French - fr", "fr"),
            ("German - de", "de"), ("Spanish - es", "es"),
            ("Arabic - ar", "ar"), ("Bengali - bn", "bn"), ("Greek - el", "el"),
            ("Hindi - hi", "hi"), ("Indonesian - in", "in"), ("Marathi - mr", "mr"),
            ("Malay - ms", "ms"), ("Portuguese - pt", "pt"), ("Portuguese (Brazil) - pt-rBR", "pt-rBR"),
            ("Russian - ru", "ru"), ("Tamil - ta", "ta"), ("Telugu - te", "te"),
            ("Thai - th", "th"), ("Turkish - tr", "tr"),
            ("Filipino - tl", "tl")
        ]

        for i, (name, code) in enumerate(common_langs):
            btn = ttk.Button(common_langs_frame, text=name, 
                           command=lambda c=code: add_callback(c))
            btn.grid(row=i//4, column=i%4, padx=2, pady=2)

    def setup_file_translation_tab(self, parent):
        """Thiết lập giao diện cho tab dịch file"""
        # Input file selection
        ttk.Label(parent, text="Input XML file:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_path = tk.StringVar()
        ttk.Entry(parent, textvariable=self.input_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(parent, text="Browse", command=self.browse_input).grid(row=0, column=2)
        
        # Output directory selection
        ttk.Label(parent, text="Output directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_path = tk.StringVar()
        ttk.Entry(parent, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(parent, text="Browse", command=self.browse_output).grid(row=1, column=2)
        
        # Language codes frame
        lang_frame = ttk.LabelFrame(parent, text="Target Languages", padding="5")
        lang_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Language codes list
        self.langs_listbox = tk.Listbox(lang_frame, height=5, width=20)
        self.langs_listbox.pack(side='left', padx=5)
        
        # Language input and buttons
        lang_input_frame = ttk.Frame(lang_frame)
        lang_input_frame.pack(side='left', padx=10)
        
        self.lang_code = tk.StringVar()
        ttk.Entry(lang_input_frame, textvariable=self.lang_code, width=10).pack(side='left', padx=5)
        ttk.Button(lang_input_frame, text="Add", command=self.add_language).pack(side='left', padx=2)
        ttk.Button(lang_input_frame, text="Remove", command=self.remove_language).pack(side='left', padx=2)
        
        # Common language buttons
        self.add_common_language_buttons(lang_frame, self.add_language)
        
        # Status text
        self.status_text = tk.Text(parent, height=10, width=70)
        self.status_text.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Translate button
        ttk.Button(parent, text="Translate All", command=self.translate_all).grid(row=4, column=0, columnspan=3, pady=10)

    def setup_text_translation_tab(self, parent):
        """Thiết lập giao diện cho tab dịch chuỗi"""
        # Frame chứa danh sách các chuỗi cần dịch
        strings_frame = ttk.LabelFrame(parent, text="Strings to translate", padding="5")
        strings_frame.pack(fill='x', padx=5, pady=5)

        # Frame cho việc nhập liệu
        input_frame = ttk.Frame(strings_frame)
        input_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(input_frame, text="String name:").pack(side='left')
        self.string_name = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.string_name, width=30).pack(side='left', padx=5)

        ttk.Label(input_frame, text="Text:").pack(side='left')
        self.input_text = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.input_text, width=40).pack(side='left', padx=5)

        ttk.Button(input_frame, text="Add to List", command=self.add_to_list).pack(side='left', padx=5)

        # Listbox để hiển thị các chuỗi đã thêm
        list_frame = ttk.Frame(strings_frame)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.strings_listbox = tk.Listbox(list_frame, height=6, width=70)
        self.strings_listbox.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.strings_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.strings_listbox.configure(yscrollcommand=scrollbar.set)

        # Buttons để quản lý danh sách
        btn_frame = ttk.Frame(strings_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(btn_frame, text="Remove Selected", command=self.remove_from_list).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_list).pack(side='left', padx=5)

        # Output directory selection and values folders
        dir_frame = ttk.LabelFrame(parent, text="Output Directory", padding="5")
        dir_frame.pack(fill='x', padx=5, pady=5)
        
        # Directory selection
        select_frame = ttk.Frame(dir_frame)
        select_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(select_frame, text="Resource directory:").pack(side='left')
        self.text_output_path = tk.StringVar()
        ttk.Entry(select_frame, textvariable=self.text_output_path, width=50).pack(side='left', padx=5)
        ttk.Button(select_frame, text="Browse", command=self.browse_text_output).pack(side='left')

        # Values folders selection
        values_frame = ttk.Frame(dir_frame)
        values_frame.pack(fill='x', padx=5, pady=5)
        
        # Left side: Available values folders
        left_frame = ttk.Frame(values_frame)
        left_frame.pack(side='left', fill='both', expand=True)
        ttk.Label(left_frame, text="Available values folders:").pack()
        self.available_values = tk.Listbox(left_frame, height=5, width=30, selectmode='multiple')
        self.available_values.pack(side='left', fill='both', expand=True)
        left_scroll = ttk.Scrollbar(left_frame, orient="vertical", command=self.available_values.yview)
        left_scroll.pack(side='right', fill='y')
        self.available_values.configure(yscrollcommand=left_scroll.set)

        # Middle: Buttons
        mid_frame = ttk.Frame(values_frame)
        mid_frame.pack(side='left', padx=10)
        ttk.Button(mid_frame, text=">>", command=self.add_selected_values).pack(pady=2)
        ttk.Button(mid_frame, text="<<", command=self.remove_selected_values).pack(pady=2)

        # Right side: Selected values folders
        right_frame = ttk.Frame(values_frame)
        right_frame.pack(side='left', fill='both', expand=True)
        ttk.Label(right_frame, text="Selected target folders:").pack()
        self.selected_values = tk.Listbox(right_frame, height=5, width=30, selectmode='multiple')
        self.selected_values.pack(side='left', fill='both', expand=True)
        right_scroll = ttk.Scrollbar(right_frame, orient="vertical", command=self.selected_values.yview)
        right_scroll.pack(side='right', fill='y')
        self.selected_values.configure(yscrollcommand=right_scroll.set)

        # Status text
        self.text_status = tk.Text(parent, height=10, width=70)
        self.text_status.pack(padx=5, pady=5)

        # Add Translation button
        ttk.Button(parent, text="Translate All", command=self.translate_multiple_texts).pack(pady=10)

    def browse_input(self):
        filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if filename:
            self.input_path.set(filename)

    def browse_output(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_path.set(directory)

    def browse_text_output(self):
        """Chọn thư mục và cập nhật danh sách values folders"""
        directory = filedialog.askdirectory()
        if directory:
            self.text_output_path.set(directory)
            self.update_values_folders(directory)

    def update_values_folders(self, directory):
        """Cập nhật danh sách các thư mục values"""
        if self.is_processing:
            return
            
        try:
            # Xóa danh sách cũ
            self.available_values.delete(0, tk.END)
            self.selected_values.delete(0, tk.END)
            
            # Tìm tất cả thư mục values và values-*
            values_dirs = [d for d in os.listdir(directory) 
                          if os.path.isdir(os.path.join(directory, d)) 
                          and (d == 'values' or d.startswith('values-'))]
            
            # Tạo thư mục values nếu chưa tồn tại
            if 'values' not in values_dirs:
                os.makedirs(os.path.join(directory, 'values'), exist_ok=True)
                values_dirs.append('values')
            
            # Tạo các thư mục values-{lang} cho các ngôn ngữ phổ biến nếu chưa tồn tại
            common_langs = ['vi', 'zh', 'ko', 'ja', 'it', 'fr', 'de', 'es']
            for lang in common_langs:
                values_dir = f'values-{lang}'
                if values_dir not in values_dirs:
                    os.makedirs(os.path.join(directory, values_dir), exist_ok=True)
                    values_dirs.append(values_dir)
            
            # Đảm bảo 'values' luôn ở đầu danh sách
            if 'values' in values_dirs:
                values_dirs.remove('values')
                values_dirs = ['values'] + sorted(values_dirs)
            else:
                values_dirs = sorted(values_dirs)
            
            # Thêm vào available_values
            for d in values_dirs:
                self.available_values.insert(tk.END, d)
            
            self.log_text(f"Found/Created values folders: {', '.join(values_dirs)}")
            
        except Exception as e:
            self.log_text(f"Error updating values folders: {str(e)}")

    def add_language(self, lang_code=None):
        if lang_code is None:
            lang_code = self.lang_code.get().strip()
        
        if lang_code and lang_code not in self.langs_listbox.get(0, tk.END):
            self.langs_listbox.insert(tk.END, lang_code)
            self.lang_code.set("")  # Clear input after adding

    def remove_language(self):
        selection = self.langs_listbox.curselection()
        if selection:
            self.langs_listbox.delete(selection)

    def log_text(self, message):
        """Cập nhật log an toàn từ bất kỳ thread nào"""
        if hasattr(self, 'text_status'):
            self.ui_queue.put(("text_status", message))
            self.root.after(10, self.process_ui_queue)
        if hasattr(self, 'status_text'):
            self.ui_queue.put(("status_text", message))
            self.root.after(10, self.process_ui_queue)

    def process_ui_queue(self):
        """Xử lý các cập nhật UI từ queue"""
        try:
            while True:
                try:
                    target, message = self.ui_queue.get_nowait()
                    if target == "text_status":
                        self.text_status.insert(tk.END, message + "\n")
                        self.text_status.see(tk.END)
                    elif target == "status_text":
                        self.status_text.insert(tk.END, message + "\n")
                        self.status_text.see(tk.END)
                    self.root.update_idletasks()
                except queue.Empty:
                    break
        except Exception as e:
            print(f"Error processing UI queue: {str(e)}")
        finally:
            # Tiếp tục kiểm tra queue nếu đang xử lý
            if self.is_processing:
                self.root.after(100, self.process_ui_queue)

    def translate_all(self):
        input_file = self.input_path.get()
        output_dir = self.output_path.get()
        languages = list(self.langs_listbox.get(0, tk.END))
        
        if not all([input_file, output_dir, languages]):
            self.log_text("Please select input file, output directory and add target languages!")
            return
            
        if self.is_processing:
            return
            
        try:
            # Đánh dấu đang xử lý
            self.is_processing = True
            
            # Disable các controls
            self.disable_controls()
            
            def translation_thread():
                try:
                    for lang in languages:
                        try:
                            lang_dir = os.path.join(output_dir, f"values-{lang}")
                            os.makedirs(lang_dir, exist_ok=True)
                            output_file = os.path.join(lang_dir, "strings.xml")
                            
                            self.log_text(f"\nStarting translation to {lang}...")
                            translate_xml_file(input_file, output_file, "en", lang, callback=self.log_text)
                            
                        except Exception as e:
                            self.log_text(f"Error translating {lang}: {str(e)}")
                finally:
                    # Đảm bảo luôn enable lại controls khi hoàn thành
                    self.root.after(0, self.on_translation_complete)
            
            # Bắt đầu thread dịch
            threading.Thread(target=translation_thread, daemon=True).start()
            
            # Bắt đầu xử lý UI queue
            self.process_ui_queue()
            
        except Exception as e:
            self.log_text(f"Error: {str(e)}")
            self.on_translation_complete()

    def add_to_list(self):
        """Thêm chuỗi vào danh sách"""
        name = self.string_name.get().strip()
        text = self.input_text.get().strip()
        
        if name and text:
            # Lưu theo format để dễ trích xuất sau này
            item = f"{name} :: {text}"
            self.strings_listbox.insert(tk.END, item)
            # Clear input fields
            self.string_name.set("")
            self.input_text.set("")
        else:
            self.log_text("Please enter both string name and text!")

    def remove_from_list(self):
        """Xóa chuỗi được chọn khỏi danh sách"""
        selection = self.strings_listbox.curselection()
        if selection:
            self.strings_listbox.delete(selection)

    def clear_list(self):
        """Xóa toàn bộ danh sách"""
        self.strings_listbox.delete(0, tk.END)

    def add_selected_values(self):
        """Chuyển các thư mục được chọn từ available sang selected"""
        selections = self.available_values.curselection()
        for i in reversed(selections):
            value = self.available_values.get(i)
            if value not in self.selected_values.get(0, tk.END):
                self.selected_values.insert(tk.END, value)
                self.available_values.delete(i)

    def remove_selected_values(self):
        """Chuyển các thư mục được chọn từ selected về available"""
        selections = self.selected_values.curselection()
        for i in reversed(selections):
            value = self.selected_values.get(i)
            if value not in self.available_values.get(0, tk.END):
                self.available_values.insert(tk.END, value)
                self.selected_values.delete(i)

    def translate_multiple_texts(self):
        """Dịch tất cả các chuỗi trong danh sách"""
        if self.is_processing:
            return
            
        output_dir = self.text_output_path.get()
        selected_folders = list(self.selected_values.get(0, tk.END))
        
        if not output_dir:
            self.log_text("Please select output directory!")
            return
        
        if not selected_folders:
            self.log_text("Please select target values folders!")
            return
        
        if self.strings_listbox.size() == 0:
            self.log_text("Please add some strings to translate!")
            return
        
        try:
            # Đánh dấu đang xử lý
            self.is_processing = True
            
            # Disable các controls
            self.disable_controls()
            
            # Lấy tất cả các items
            items = self.strings_listbox.get(0, tk.END)
            string_texts = [tuple(item.split(" :: ")) for item in items]
            
            def translation_callback(message):
                """Callback để cập nhật tiến trình từ thread dịch"""
                self.ui_queue.put(("text_status", message))
                self.root.after(10, self.process_ui_queue)
                
                if "completed" in message.lower():
                    self.root.after(0, self.on_translation_complete)

            def translation_thread():
                """Thread riêng để xử lý dịch"""
                try:
                    translate_and_append_batch(
                        string_texts,
                        output_dir,
                        selected_folders=selected_folders,
                        callback=translation_callback,
                        root=self.root
                    )
                except Exception as e:
                    self.ui_queue.put(("text_status", f"Error: {str(e)}"))
                    self.root.after(0, self.on_translation_complete)

            # Bắt đầu thread dịch
            threading.Thread(target=translation_thread, daemon=True).start()
            
            # Bắt đầu xử lý UI queue
            self.process_ui_queue()
            
        except Exception as e:
            self.log_text(f"Error: {str(e)}")
            self.on_translation_complete()

    def on_translation_complete(self):
        """Xử lý khi hoàn thành dịch"""
        self.enable_controls()
        self.clear_list()
        self.is_processing = False

    def disable_controls(self):
        """Disable các controls khi đang xử lý"""
        if hasattr(self, 'translate_button'):
            self.translate_button.configure(state='disabled')
        self.strings_listbox.configure(state='disabled')
        self.available_values.configure(state='disabled')
        self.selected_values.configure(state='disabled')

    def enable_controls(self):
        """Enable lại các controls sau khi xử lý xong"""
        if hasattr(self, 'translate_button'):
            self.translate_button.configure(state='normal')
        self.strings_listbox.configure(state='normal')
        self.available_values.configure(state='normal')
        self.selected_values.configure(state='normal')

def main():
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 