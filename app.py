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
import re

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XML Translator")
        
        window_width = 1024
        window_height = 768
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        self.root.resizable(True, True)
        
        self.root.minsize(800, 600)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Unmap>", self.on_minimize)
        self.root.bind("<Map>", self.on_restore)
        
        self.is_processing = False
        self.is_minimized = False
        
        self.ui_queue = queue.Queue()
        
        self.setup_ui()
        
    def on_minimize(self, event):
        self.is_minimized = True
        if self.is_processing:
            self.pause_ui_updates()
    
    def on_restore(self, event):
        self.is_minimized = False
        if self.is_processing:
            self.resume_ui_updates()
    
    def on_closing(self):
        if self.is_processing:
            if messagebox.askokcancel("Quit", "Translation is in progress. Do you want to quit?"):
                self.root.quit()
        else:
            self.root.quit()
            
    def pause_ui_updates(self):
        if hasattr(self, 'text_status'):
            self.text_status.config(state='disabled')
        if hasattr(self, 'status_text'):
            self.status_text.config(state='disabled')
            
    def resume_ui_updates(self):
        if hasattr(self, 'text_status'):
            self.text_status.config(state='normal')
        if hasattr(self, 'status_text'):
            self.status_text.config(state='normal')
            
    def setup_ui(self):
        # Create main scrollable frame
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(main_container)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Create window in canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Add mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Setup notebook in scrollable frame
        self.notebook = ttk.Notebook(self.scrollable_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.file_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.file_frame, text='Translate XML File')
        
        self.text_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.text_frame, text='Add New String')
        
        self.setup_file_translation_tab(self.file_frame)
        self.setup_text_translation_tab(self.text_frame)
        
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        
    def on_tab_changed(self, event):
        if self.is_processing:
            return
            
        try:
            current_tab = self.notebook.select()
            tab_id = self.notebook.index(current_tab)
            
            self.scrollable_frame.update_idletasks()
            
            if tab_id == 1:
                if hasattr(self, 'text_output_path') and self.text_output_path.get():
                    self.scrollable_frame.after(100, lambda: self.update_values_folders(self.text_output_path.get()))
                    
        except Exception as e:
            print(f"Error switching tabs: {str(e)}")

    def on_window_resize(self, event):
        if event.widget == self.root:
            self.scrollable_frame.update_idletasks()

    def add_common_language_buttons(self, parent_frame, add_callback):
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
        ttk.Label(parent, text="Input XML file:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_path = tk.StringVar()
        ttk.Entry(parent, textvariable=self.input_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(parent, text="Browse", command=self.browse_input).grid(row=0, column=2)
        
        ttk.Label(parent, text="Output directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_path = tk.StringVar()
        ttk.Entry(parent, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(parent, text="Browse", command=self.browse_output).grid(row=1, column=2)
        
        lang_frame = ttk.LabelFrame(parent, text="Target Languages", padding="5")
        lang_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.langs_listbox = tk.Listbox(lang_frame, height=5, width=20)
        self.langs_listbox.pack(side='left', padx=5)
        
        lang_input_frame = ttk.Frame(lang_frame)
        lang_input_frame.pack(side='left', padx=10)
        
        self.lang_code = tk.StringVar()
        ttk.Entry(lang_input_frame, textvariable=self.lang_code, width=10).pack(side='left', padx=5)
        ttk.Button(lang_input_frame, text="Add", command=self.add_language).pack(side='left', padx=2)
        ttk.Button(lang_input_frame, text="Remove", command=self.remove_language).pack(side='left', padx=2)
        
        self.add_common_language_buttons(lang_frame, self.add_language)
        
        self.status_text = tk.Text(parent, height=10, width=70)
        self.status_text.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(parent, text="Translate All", command=self.translate_all).grid(row=4, column=0, columnspan=3, pady=10)

    def setup_text_translation_tab(self, parent):
        strings_frame = ttk.LabelFrame(parent, text="Strings to translate", padding="5")
        strings_frame.pack(fill='x', padx=5, pady=5)

        # Add bulk input frame
        bulk_frame = ttk.LabelFrame(strings_frame, text="Bulk Input (XML format)", padding="5")
        bulk_frame.pack(fill='x', padx=5, pady=5)
        
        # Container for text area and scrollbar
        text_container = ttk.Frame(bulk_frame)
        text_container.pack(fill='x', padx=5, pady=5)
        
        # Text area for input
        self.bulk_text = tk.Text(text_container, height=6, width=70)
        self.bulk_text.pack(side='left', fill='both', expand=True)
        
        bulk_scroll = ttk.Scrollbar(text_container, orient="vertical", command=self.bulk_text.yview)
        bulk_scroll.pack(side='right', fill='y')
        self.bulk_text.configure(yscrollcommand=bulk_scroll.set)
        
        # Parse button in bulk frame
        ttk.Button(bulk_frame, text="Parse XML Strings", 
                  command=self.parse_bulk_input).pack(fill='x', padx=5, pady=5)

        # Existing single input frame
        input_frame = ttk.Frame(strings_frame)
        input_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(input_frame, text="String name:").pack(side='left')
        self.string_name = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.string_name, width=30).pack(side='left', padx=5)

        ttk.Label(input_frame, text="Text:").pack(side='left')
        self.input_text = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.input_text, width=40).pack(side='left', padx=5)

        ttk.Button(input_frame, text="Add to List", command=self.add_to_list).pack(side='left', padx=5)

        list_frame = ttk.Frame(strings_frame)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.strings_listbox = tk.Listbox(list_frame, height=6, width=70)
        self.strings_listbox.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.strings_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.strings_listbox.configure(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(strings_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(btn_frame, text="Remove Selected", command=self.remove_from_list).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_list).pack(side='left', padx=5)

        dir_frame = ttk.LabelFrame(parent, text="Output Directory", padding="5")
        dir_frame.pack(fill='x', padx=5, pady=5)
        
        select_frame = ttk.Frame(dir_frame)
        select_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(select_frame, text="Resource directory:").pack(side='left')
        self.text_output_path = tk.StringVar()
        ttk.Entry(select_frame, textvariable=self.text_output_path, width=50).pack(side='left', padx=5)
        ttk.Button(select_frame, text="Browse", command=self.browse_text_output).pack(side='left')

        values_frame = ttk.Frame(dir_frame)
        values_frame.pack(fill='x', padx=5, pady=5)
        
        left_frame = ttk.Frame(values_frame)
        left_frame.pack(side='left', fill='both', expand=True)
        ttk.Label(left_frame, text="Available values folders:").pack()
        self.available_values = tk.Listbox(left_frame, height=5, width=30, selectmode='multiple')
        self.available_values.pack(side='left', fill='both', expand=True)
        left_scroll = ttk.Scrollbar(left_frame, orient="vertical", command=self.available_values.yview)
        left_scroll.pack(side='right', fill='y')
        self.available_values.configure(yscrollcommand=left_scroll.set)

        mid_frame = ttk.Frame(values_frame)
        mid_frame.pack(side='left', padx=10)
        ttk.Button(mid_frame, text=">>", command=self.add_selected_values).pack(pady=2)
        ttk.Button(mid_frame, text="<<", command=self.remove_selected_values).pack(pady=2)

        right_frame = ttk.Frame(values_frame)
        right_frame.pack(side='left', fill='both', expand=True)
        ttk.Label(right_frame, text="Selected target folders:").pack()
        self.selected_values = tk.Listbox(right_frame, height=5, width=30, selectmode='multiple')
        self.selected_values.pack(side='left', fill='both', expand=True)
        right_scroll = ttk.Scrollbar(right_frame, orient="vertical", command=self.selected_values.yview)
        right_scroll.pack(side='right', fill='y')
        self.selected_values.configure(yscrollcommand=right_scroll.set)

        self.text_status = tk.Text(parent, height=10, width=70)
        self.text_status.pack(padx=5, pady=5)

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
        directory = filedialog.askdirectory()
        if directory:
            self.text_output_path.set(directory)
            self.update_values_folders(directory)

    def update_values_folders(self, directory):
        if self.is_processing:
            return
            
        try:
            self.available_values.delete(0, tk.END)
            self.selected_values.delete(0, tk.END)
            
            # Lấy tất cả các thư mục values hiện có (trừ values-night)
            values_dirs = [d for d in os.listdir(directory) 
                          if os.path.isdir(os.path.join(directory, d)) 
                          and (d == 'values' or d.startswith('values-'))
                          and d != 'values-night']
            
            # Đảm bảo có thư mục values gốc
            if 'values' not in values_dirs:
                os.makedirs(os.path.join(directory, 'values'), exist_ok=True)
                values_dirs.append('values')
            
            # Sắp xếp với values đầu tiên
            if 'values' in values_dirs:
                values_dirs.remove('values')
                values_dirs = ['values'] + sorted(values_dirs)
            else:
                values_dirs = sorted(values_dirs)
            
            # Thêm trực tiếp vào selected_values
            for d in values_dirs:
                self.selected_values.insert(tk.END, d)
            
            self.log_text(f"Found values folders and auto-selected: {', '.join(values_dirs)}")
            
        except Exception as e:
            self.log_text(f"Error updating values folders: {str(e)}")

    def add_language(self, lang_code=None):
        if lang_code is None:
            lang_code = self.lang_code.get().strip()
        
        if lang_code and lang_code not in self.langs_listbox.get(0, tk.END):
            self.langs_listbox.insert(tk.END, lang_code)
            self.lang_code.set("")

    def remove_language(self):
        selection = self.langs_listbox.curselection()
        if selection:
            self.langs_listbox.delete(selection)

    def log_text(self, message):
        if hasattr(self, 'text_status'):
            self.ui_queue.put(("text_status", message))
            self.root.after(10, self.process_ui_queue)
        if hasattr(self, 'status_text'):
            self.ui_queue.put(("status_text", message))
            self.root.after(10, self.process_ui_queue)

    def process_ui_queue(self):
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
                    self.scrollable_frame.update_idletasks()
                except queue.Empty:
                    break
        except Exception as e:
            print(f"Error processing UI queue: {str(e)}")
        finally:
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
            self.is_processing = True
            
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
                    self.root.after(0, self.on_translation_complete)
            
            threading.Thread(target=translation_thread, daemon=True).start()
            
            self.process_ui_queue()
            
        except Exception as e:
            self.log_text(f"Error: {str(e)}")
            self.on_translation_complete()

    def add_to_list(self):
        name = self.string_name.get().strip()
        text = self.input_text.get().strip()
        
        if name and text:
            item = f"{name} :: {text}"
            self.strings_listbox.insert(tk.END, item)
            self.string_name.set("")
            self.input_text.set("")
        else:
            self.log_text("Please enter both string name and text!")

    def remove_from_list(self):
        selection = self.strings_listbox.curselection()
        if selection:
            self.strings_listbox.delete(selection)

    def clear_list(self):
        self.strings_listbox.delete(0, tk.END)

    def add_selected_values(self):
        selections = self.available_values.curselection()
        for i in reversed(selections):
            value = self.available_values.get(i)
            if value not in self.selected_values.get(0, tk.END):
                self.selected_values.insert(tk.END, value)
                self.available_values.delete(i)

    def remove_selected_values(self):
        selections = self.selected_values.curselection()
        for i in reversed(selections):
            value = self.selected_values.get(i)
            if value not in self.available_values.get(0, tk.END):
                self.available_values.insert(tk.END, value)
                self.selected_values.delete(i)

    def translate_multiple_texts(self):
        if self.is_processing:
            return
            
        output_dir = self.text_output_path.get()
        selected_folders = list(self.selected_values.get(0, tk.END))
        source_xml_path = self.input_path.get()  # Lấy đường dẫn file XML gốc
        
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
            self.is_processing = True
            
            self.disable_controls()
            
            items = self.strings_listbox.get(0, tk.END)
            string_texts = [tuple(item.split(" :: ")) for item in items]
            
            def translation_callback(message):
                self.ui_queue.put(("text_status", message))
                self.root.after(10, self.process_ui_queue)
                
                if "completed" in message.lower():
                    self.root.after(0, self.on_translation_complete)

            def translation_thread():
                try:
                    translate_and_append_batch(
                        string_texts,
                        output_dir,
                        selected_folders=selected_folders,
                        callback=translation_callback,
                        source_xml_path=source_xml_path  # Truyền đường dẫn file XML gốc
                    )
                except Exception as e:
                    self.ui_queue.put(("text_status", f"Error: {str(e)}"))
                    self.root.after(0, self.on_translation_complete)

            threading.Thread(target=translation_thread, daemon=True).start()
            
            self.process_ui_queue()
            
        except Exception as e:
            self.log_text(f"Error: {str(e)}")
            self.on_translation_complete()

    def on_translation_complete(self):
        self.enable_controls()
        self.clear_list()
        self.is_processing = False

    def disable_controls(self):
        if hasattr(self, 'translate_button'):
            self.translate_button.configure(state='disabled')
        self.strings_listbox.configure(state='disabled')
        self.available_values.configure(state='disabled')
        self.selected_values.configure(state='disabled')

    def enable_controls(self):
        if hasattr(self, 'translate_button'):
            self.translate_button.configure(state='normal')
        self.strings_listbox.configure(state='normal')
        self.available_values.configure(state='normal')
        self.selected_values.configure(state='normal')

    def parse_bulk_input(self):
        bulk_text = self.bulk_text.get("1.0", tk.END).strip()
        if not bulk_text:
            self.log_text("Please enter XML strings to parse!")
            return
            
        try:
            # Simple regex to match string elements
            pattern = r'<string\s+name="([^"]+)">(.*?)</string>'
            matches = re.findall(pattern, bulk_text, re.DOTALL)
            
            if not matches:
                self.log_text("No valid string elements found!")
                return
                
            # Add new strings (always append mode now)
            for name, text in matches:
                # Clean up the text (remove extra whitespace)
                text = ' '.join(text.split())
                item = f"{name} :: {text}"
                self.strings_listbox.insert(tk.END, item)
                
            self.log_text(f"Successfully parsed {len(matches)} strings")
            self.bulk_text.delete("1.0", tk.END)  # Clear the input area
            
        except Exception as e:
            self.log_text(f"Error parsing XML strings: {str(e)}")

def main():
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 