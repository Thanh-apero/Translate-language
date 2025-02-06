import tkinter as tk
from tkinter import filedialog, ttk
import os
from translator_core import translate_xml_file, translate_text, append_to_xml_file, translate_and_append

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XML Translator")
        self.root.geometry("800x600")  # Tăng kích thước cửa sổ
        
        # Tạo notebook để chứa các tab
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Tab 1: Dịch file XML
        self.file_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.file_frame, text='Translate XML File')
        self.setup_file_translation_tab(self.file_frame)
        
        # Tab 2: Dịch và thêm chuỗi
        self.text_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.text_frame, text='Add New String')
        self.setup_text_translation_tab(self.text_frame)

    def add_common_language_buttons(self, parent_frame, add_callback):
        """Thêm các nút cho ngôn ngữ phổ biến"""
        common_langs_frame = ttk.Frame(parent_frame)
        common_langs_frame.pack(side='left', padx=10, pady=5)
        
        common_langs = [
            ("Vietnamese", "vi"), ("Chinese", "zh"), 
            ("Korean", "ko"), ("Japanese", "ja"),
            ("Italian", "it"), ("French", "fr"),
            ("German", "de"), ("Spanish", "es")
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
        # String name input
        name_frame = ttk.Frame(parent)
        name_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(name_frame, text="String name:").pack(side='left')
        self.string_name = tk.StringVar()
        ttk.Entry(name_frame, textvariable=self.string_name, width=50).pack(side='left', padx=5)
        
        # Text input
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(text_frame, text="Text to translate:").pack(side='left')
        self.input_text = tk.StringVar()
        ttk.Entry(text_frame, textvariable=self.input_text, width=50).pack(side='left', padx=5)
        
        # Output directory selection (res folder)
        dir_frame = ttk.Frame(parent)
        dir_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(dir_frame, text="Resource directory (containing values folders):").pack(side='left')
        self.text_output_path = tk.StringVar()
        ttk.Entry(dir_frame, textvariable=self.text_output_path, width=50).pack(side='left', padx=5)
        ttk.Button(dir_frame, text="Browse", command=self.browse_text_output).pack(side='left')
        
        # Status text
        self.text_status = tk.Text(parent, height=10, width=70)
        self.text_status.pack(padx=5, pady=5)
        
        # Add Translation button
        ttk.Button(parent, text="Add Translation", command=self.translate_text).pack(pady=10)

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

    def log(self, message):
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.root.update()

    def log_text(self, message):
        self.text_status.insert(tk.END, message + "\n")
        self.text_status.see(tk.END)
        self.root.update()

    def translate_all(self):
        input_file = self.input_path.get()
        output_dir = self.output_path.get()
        languages = list(self.langs_listbox.get(0, tk.END))
        
        if not all([input_file, output_dir, languages]):
            self.log("Please select input file, output directory and add target languages!")
            return
            
        for lang in languages:
            try:
                lang_dir = os.path.join(output_dir, f"values-{lang}")
                os.makedirs(lang_dir, exist_ok=True)
                output_file = os.path.join(lang_dir, "strings.xml")
                
                self.log(f"\nStarting translation to {lang}...")
                translate_xml_file(input_file, output_file, "en", lang, callback=self.log)
                
            except Exception as e:
                self.log(f"Error translating {lang}: {str(e)}")

    def translate_text(self):
        string_name = self.string_name.get()
        text = self.input_text.get()
        output_dir = self.text_output_path.get()
        
        if not all([string_name, text, output_dir]):
            self.log_text("Please fill in all fields!")
            return
            
        try:
            # Kiểm tra xem thư mục có tồn tại không
            if not os.path.isdir(output_dir):
                self.log_text(f"Error: Directory {output_dir} not found!")
                return
                
            # Kiểm tra xem có thư mục values nào không
            values_dirs = [d for d in os.listdir(output_dir) 
                         if os.path.isdir(os.path.join(output_dir, d)) 
                         and d.startswith('values')]
            
            if not values_dirs:
                self.log_text("No values directories found in the selected directory!")
                return
                
            self.log_text(f"Found directories: {', '.join(values_dirs)}")
            
            # Gọi hàm translate_and_append với thư mục gốc
            translate_and_append(
                string_name, 
                text, 
                output_dir,
                callback=self.log_text
            )
            
            # Clear input fields after successful addition
            self.string_name.set("")
            self.input_text.set("")
            
        except Exception as e:
            self.log_text(f"Error: {str(e)}")

def main():
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 