import json
import google.generativeai as genai
import xml.etree.ElementTree as ET
import copy
import os

api_keys = [
    "AIzaSyB_59fjCUN_vGW8FnPf5CZdl267_yfiOBs",
    "AIzaSyCN7x2uMvL2cHq0jdBq9aMJ9ijJYct4QJ0"
]
current_key_index = 0

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def get_next_api_key():
    global current_key_index
    key = api_keys[current_key_index]
    current_key_index = (current_key_index + 1) % len(api_keys)
    return key

def request(input_data):
    genai.configure(api_key=get_next_api_key())
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
    )
    response = model.generate_content([
        "input: {\n  \"source_language\": \"en\",\n  \"target_language\": \"ko\",\n  \"strings\": [\n    {\"id\": 1, \"text\": \"Your document has been saved successfully.\"},\n    {\"id\": 2, \"text\": \"Please check your internet connection and try again.\"},\n    {\"id\": 3, \"text\": \"This feature is not available in the free version.\"}\n  ]\n}",
        "output: {\n  \"translations\": [\n    {\"id\": 1, \"text\": \"문서가 성공적으로 저장되었습니다.\"},\n    {\"id\": 2, \"text\": \"인터넷 연결을 확인하고 다시 시도하세요.\"},\n    {\"id\": 3, \"text\": \"이 기능은 무료 버전에서 사용할 수 없습니다.\"}\n  ]\n}",
        "input: {\n  \"source_language\": \"en\",\n  \"target_language\": \"ko\",\n  \"strings\": [\n    {\"id\": 1, \"text\": \"Don't forget to write tag #XpertScan\"},\n    {\"id\": 2, \"text\": \"Can't find an app that supports this action\"}\n  ]\n}",
        "output: {\n  \"translations\": [\n    {\"id\": 1, \"text\": \"#XpertScan 태그를 작성하는 것을 잊지 마세요\"},\n    {\"id\": 2, \"text\": \"이 작업을 지원하는 앱을 찾을 수 없습니다\"}\n  ]\n}",
        "input: {\n  \"source_language\": \"en\",\n  \"target_language\": \"zh\",\n  \"strings\": [\n    {\"id\": 1, \"text\": \"Export as PDF failed\"},\n    {\"id\": 2, \"text\": \"Share as PDF failed\"},\n    {\"id\": 3, \"text\": \"Export to gallery failed\"},\n    {\"id\": 4, \"text\": \"Share as picture failed\"},\n    {\"id\": 5, \"text\": \"Print PDF failed\"},\n    {\"id\": 6, \"text\": \"Insert password\"}\n  ]\n}",
        "output: {\n  \"translations\": [\n    {\"id\": 1, \"text\": \"导出为PDF失败\"},\n    {\"id\": 2, \"text\": \"分享为PDF失败\"},\n    {\"id\": 3, \"text\": \"导出到图库失败\"},\n    {\"id\": 4, \"text\": \"分享为图片失败\"},\n    {\"id\": 5, \"text\": \"打印PDF失败\"},\n    {\"id\": 6, \"text\": \"请输入密码\"}\n  ]\n}",
        "input: {\n  \"source_language\": \"en\",\n  \"target_language\": \"vi\",\n  \"strings\": [\n    {\"id\": 1, \"text\": \"Export as PDF failed\"},\n    {\"id\": 2, \"text\": \"Share as PDF failed\"},\n    {\"id\": 3, \"text\": \"Export to gallery failed\"},\n    {\"id\": 4, \"text\": \"Share as picture failed\"},\n    {\"id\": 5, \"text\": \"Print PDF failed\"},\n    {\"id\": 6, \"text\": \"Insert password\"}\n  ]\n}",
        "output: {\n  \"translations\": [\n    {\"id\": 1, \"text\": \"Xuất PDF thất bại\"},\n    {\"id\": 2, \"text\": \"Chia sẻ dưới dạng PDF thất bại\"},\n    {\"id\": 3, \"text\": \"Xuất vào thư viện thất bại\"},\n    {\"id\": 4, \"text\": \"Chia sẻ dưới dạng hình ảnh thất bại\"},\n    {\"id\": 5, \"text\": \"In PDF thất bại\"},\n    {\"id\": 6, \"text\": \"Nhập mật khẩu\"}\n  ]\n}",
        "input: {\n  \"source_language\": \"en\",\n  \"target_language\": \"it\",\n  \"strings\": [\n    {\"id\": 1, \"text\": \"Export as PDF failed\"},\n    {\"id\": 2, \"text\": \"Share as PDF failed\"},\n    {\"id\": 3, \"text\": \"Export to gallery failed\"},\n    {\"id\": 4, \"text\": \"Share as picture failed\"},\n    {\"id\": 5, \"text\": \"Print PDF failed\"},\n    {\"id\": 6, \"text\": \"Insert password\"}\n  ]\n}",
        "output: {\n  \"translations\": [\n    {\"id\": 1, \"text\": \"Esportazione come PDF fallita\"},\n    {\"id\": 2, \"text\": \"Condivisione come PDF fallita\"},\n    {\"id\": 3, \"text\": \"Esportazione nella galleria fallita\"},\n    {\"id\": 4, \"text\": \"Condivisione come immagine fallita\"},\n    {\"id\": 5, \"text\": \"Stampa PDF fallita\"},\n    {\"id\": 6, \"text\": \"Inserisci la password\"}\n  ]\n}",
        "input: {\n  \"source_language\": \"en\",\n  \"target_language\": \"it\",\n  \"strings\": [\n    {\"id\": 1, \"text\": \"Export as PDF failed\"},\n    {\"id\": 2, \"text\": \"Share as PDF failed\"},\n    {\"id\": 3, \"text\": \"Export to gallery failed\"},\n    {\"id\": 4, \"text\": \"Share as picture failed\"},\n    {\"id\": 5, \"text\": \"Print PDF failed\"},\n    {\"id\": 6, \"text\": \"Insert password\"}\n  ]\n}",
        "output: {\n  \"translations\": [\n    {\"id\": 1, \"text\": \"Esportazione come PDF fallita\"},\n    {\"id\": 2, \"text\": \"Condivisione come PDF fallita\"},\n    {\"id\": 3, \"text\": \"Esportazione nella galleria fallita\"},\n    {\"id\": 4, \"text\": \"Condivisione come immagine fallita\"},\n    {\"id\": 5, \"text\": \"Stampa PDF fallita\"},\n    {\"id\": 6, \"text\": \"Inserisci la password\"}\n  ]\n}",
        f"input 2: {input_data}",
        "output 2: ",
    ])
    return response

def generate_json_from_xml(source_language, target_language, xml_content):
    root = ET.fromstring(xml_content)
    strings_list = []
    string_metadata = {}

    for i, string_elem in enumerate(root.findall('string')):
        translatable = string_elem.attrib.get('translatable', 'true').lower()
        if translatable != "false":
            text = string_elem.text
            if text:
                strings_list.append({"id": i + 1, "text": text, "name": string_elem.attrib.get('name')})
                string_metadata[string_elem.attrib.get('name')] = {
                    'position': i,
                    'attributes': dict(string_elem.attrib)
                }

    json_structure = {
        "source_language": source_language,
        "target_language": target_language,
        "strings": strings_list
    }

    return json_structure, string_metadata, root

def update_xml_with_translations(root, translations, string_metadata):
    new_root = copy.deepcopy(root)
    translation_map = {}
    for orig, trans in zip(string_metadata.keys(), translations):
        translation_map[orig] = trans['text']

    for string_elem in new_root.findall('string'):
        original_name = string_elem.attrib.get('name')
        if original_name in translation_map:
            string_elem.text = translation_map[original_name]

    return new_root

def save_translated_xml(root, output_file):
    xml_str = ET.tostring(root, encoding='unicode', method='xml')
    formatted_xml = '<?xml version="1.0" encoding="utf-8"?>\n' + xml_str

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_xml)

def extract_translations_from_response(response):
    response_text = response.candidates[0].content.parts[0].text
    response_text = response_text.replace('```json\n', '').replace('\n```', '')
    response_json = json.loads(response_text)
    return response_json['translations']

def translate_xml_file(input_xml_path, output_xml_path, source_lang, target_lang, callback=None):
    if callback:
        callback("Reading input XML file...")
    
    with open(input_xml_path, 'r', encoding='utf-8') as f:
        xml_content = f.read()

    json_input, string_metadata, root = generate_json_from_xml(source_lang, target_lang, xml_content)
    
    if callback:
        callback(f"Found {len(json_input['strings'])} strings to translate")

    if not json_input["strings"]:
        if callback:
            callback("No strings to translate!")
        return

    if callback:
        callback("Calling translation API...")
    
    response = request(json.dumps(json_input))

    try:
        translations = extract_translations_from_response(response)
        if callback:
            callback(f"Received {len(translations)} translations")

        translated_root = update_xml_with_translations(root, translations, string_metadata)
        save_translated_xml(translated_root, output_xml_path)
        
        if callback:
            callback(f"Translation completed. Output saved to: {output_xml_path}")

    except Exception as e:
        if callback:
            callback(f"Error: {str(e)}")
        raise 

def translate_text(text, source_lang, target_lang):
    """Dịch một chuỗi văn bản đơn lẻ"""
    json_input = {
        "source_language": source_lang,
        "target_language": target_lang,
        "strings": [{"id": 1, "text": text}]
    }
    
    response = request(json.dumps(json_input))
    translations = extract_translations_from_response(response)
    return translations[0]['text']

def append_to_xml_file(output_file, string_name, text, translated_text):
    """Thêm cặp chuỗi mới vào file XML"""
    try:
        # Đọc file XML hiện có
        tree = ET.parse(output_file)
        root = tree.getroot()
    except (FileNotFoundError, ET.ParseError):
        # Nếu file không tồn tại hoặc không phải XML hợp lệ, tạo mới
        root = ET.Element("resources")
        tree = ET.ElementTree(root)

    # Kiểm tra xem string_name đã tồn tại chưa
    existing = root.find(f".//string[@name='{string_name}']")
    if existing is not None:
        # Nếu đã tồn tại, cập nhật giá trị
        existing.text = translated_text
    else:
        # Nếu chưa tồn tại, thêm mới
        new_string = ET.SubElement(root, "string")
        new_string.set("name", string_name)
        new_string.text = translated_text

    # Lưu file với định dạng đẹp
    xml_str = ET.tostring(root, encoding='unicode', method='xml')
    formatted_xml = '<?xml version="1.0" encoding="utf-8"?>\n' + xml_str

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_xml)

def translate_and_append(string_name, text, output_dir, callback=None):
    """Dịch một chuỗi và thêm vào các file XML trong thư mục values-*"""
    if callback:
        callback(f"Processing: {text}")
    
    # Tìm tất cả các thư mục values-* trong output_dir
    try:
        dirs = [d for d in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, d)) and d.startswith('values')]
    except FileNotFoundError:
        if callback:
            callback(f"Error: Directory {output_dir} not found!")
        return
    
    if not dirs:
        if callback:
            callback("No values directories found!")
        return

    for dir_name in dirs:
        try:
            # Xác định ngôn ngữ từ tên thư mục
            if dir_name == 'values':
                # Thư mục gốc chứa strings tiếng Anh
                lang = 'en'
                translated_text = text  # Không cần dịch
            else:
                # Lấy mã ngôn ngữ từ tên thư mục (values-ar -> ar)
                lang = dir_name.split('-')[1]
                # Dịch sang ngôn ngữ tương ứng
                translated_text = translate_text(text, 'en', lang)
            
            # Đường dẫn đến file strings.xml
            output_file = os.path.join(output_dir, dir_name, 'strings.xml')
            
            # Thêm vào file XML
            append_to_xml_file(output_file, string_name, text, translated_text)
            
            if callback:
                if lang == 'en':
                    callback(f"Added to {dir_name}: {text}")
                else:
                    callback(f"Added to {dir_name}: {translated_text}")
                
        except Exception as e:
            if callback:
                callback(f"Error processing {dir_name}: {str(e)}") 