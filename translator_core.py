import json
import google.generativeai as genai
import xml.etree.ElementTree as ET
import copy
import os
import re
import time
from tenacity import retry, wait_exponential, stop_after_attempt
import threading
import queue

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

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(2))
def request(input_data):
    try:
        # Ensure input_data is properly formatted JSON
        if isinstance(input_data, str):
            try:
                # Parse and re-serialize to ensure proper JSON formatting
                data = json.loads(input_data)
                input_data = json.dumps(data, ensure_ascii=False)
            except json.JSONDecodeError as e:
                print(f"Invalid JSON input: {str(e)}")
                raise
        
        print("\nDebug - Input data:", input_data)  # Debug print
        
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
        
        print("\nDebug - Response:", response.text)  # Debug print
        return response
        
    except Exception as e:
        print(f"\nDebug - Error details: {str(e)}")  # Debug print
        raise

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

def escape_xml_string(text):
    if not isinstance(text, str):
        return text
        
    replacements = {
        '&': '&amp;',
        "'": "\\'",
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def update_xml_with_translations(root, translations, string_metadata):
    new_root = copy.deepcopy(root)
    translation_map = {}
    for orig, trans in zip(string_metadata.keys(), translations):
        translation_map[orig] = trans['text']

    for string_elem in new_root.findall('string'):
        original_name = string_elem.attrib.get('name')
        if original_name in translation_map:
            string_elem.text = escape_xml_string(translation_map[original_name])

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
    json_input = {
        "source_language": source_lang,
        "target_language": target_lang,
        "strings": [{"id": 1, "text": text}]
    }
    
    response = request(json.dumps(json_input))
    translations = extract_translations_from_response(response)
    return translations[0]['text']

def append_to_xml_file(output_file, string_name, text, translated_text):
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if not content.strip():
            content = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n</resources>'
            
        end_pos = content.rfind('</resources>')
        if end_pos == -1:
            raise ValueError("Invalid XML format: missing </resources> tag")
            
        if f'name="{string_name}"' in content:
            pattern = f'<string name="{string_name}"[^>]*>(.*?)</string>'
            content = re.sub(pattern, f'<string name="{string_name}">{translated_text}</string>', content)
        else:
            last_newline = content.rfind('\n', 0, end_pos)
            if last_newline != -1:
                indent = content[last_newline + 1:end_pos].replace('</resources>', '')
            else:
                indent = '    '
                
            new_string = f'{indent}<string name="{string_name}">{translated_text}</string>\n{indent}'
            content = content[:end_pos] + new_string + content[end_pos:]

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

    except FileNotFoundError:
        content = f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="{string_name}">{translated_text}</string>
</resources>'''
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

def translate_texts_batch(texts, source_lang, target_lang, batch_size=20, callback=None):
    all_translations = []
    total_batches = (len(texts) + batch_size - 1) // batch_size
    
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        current_batch = (i // batch_size) + 1
        
        if callback:
            callback(f"Processing batch {current_batch}/{total_batches}")
        
        try:
            json_input = {
                "source_language": source_lang,
                "target_language": target_lang,
                "strings": [{"id": j+1, "text": text} for j, text in enumerate(batch_texts)]
            }
            
            response = request(json.dumps(json_input))
            translations = extract_translations_from_response(response)
            all_translations.extend(t['text'] for t in translations)
            
            if current_batch < total_batches:
                if callback:
                    callback(f"Waiting 5 seconds before next batch...")
                time.sleep(5)
                
        except Exception as e:
            if callback:
                callback(f"Error in batch {current_batch}: {str(e)}")
            return None
            
    return all_translations

def translate_and_append_batch(string_texts, output_dir, selected_folders=None, callback=None, root=None):
    def io_task():
        try:
            if selected_folders is None:
                dirs = [d for d in os.listdir(output_dir) 
                       if os.path.isdir(os.path.join(output_dir, d)) 
                       and d.startswith('values')]
            else:
                dirs = selected_folders

            if not dirs:
                if callback:
                    callback("No values directories selected!")
                return

            string_names, texts = zip(*string_texts)

            for dir_name in dirs:
                try:
                    if dir_name == 'values':
                        translated_texts = texts
                    else:
                        lang = dir_name.split('-')[1]
                        if callback:
                            callback(f"\nTranslating to {lang}...")
                        
                        def translate():
                            return translate_texts_batch(
                                texts, 
                                'en', 
                                lang, 
                                batch_size=20,
                                callback=callback
                            )
                        translated_texts = translate()
                        
                        if translated_texts is None:
                            if callback:
                                callback(f"Failed to translate to {lang}")
                            continue

                    output_file = os.path.join(output_dir, dir_name, 'strings.xml')
                    if callback:
                        callback(f"Saving translations to {dir_name}...")
                    
                    try:
                        tree = ET.parse(output_file)
                        root_elem = tree.getroot()
                    except (FileNotFoundError, ET.ParseError):
                        root_elem = ET.Element("resources")
                        tree = ET.ElementTree(root_elem)

                    for string_name, translated_text in zip(string_names, translated_texts):
                        existing = root_elem.find(f".//string[@name='{string_name}']")
                        if existing is not None:
                            existing.text = escape_xml_string(translated_text)
                        else:
                            new_string = ET.SubElement(root_elem, "string")
                            new_string.set("name", string_name)
                            new_string.text = escape_xml_string(translated_text)

                    lines = ['<?xml version="1.0" encoding="utf-8"?>', '<resources>']
                    for string_elem in root_elem.findall('string'):
                        attrs = string_elem.attrib
                        attr_str = ' '.join(f'{k}="{v}"' for k, v in attrs.items())
                        value = string_elem.text or ""
                        lines.append(f'    <string {attr_str}>{value}</string>')
                    lines.append('</resources>')

                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(lines))

                    if callback:
                        callback(f"Added {len(string_texts)} strings to {dir_name}")

                except Exception as e:
                    if callback:
                        callback(f"Error processing {dir_name}: {str(e)}")
                    continue

            if callback:
                callback("All translations completed!")

        except Exception as e:
            if callback:
                callback(f"Error: {str(e)}")

    if callback:
        callback(f"Processing {len(string_texts)} strings...")

    io_thread = threading.Thread(target=io_task)
    io_thread.daemon = True
    io_thread.start()

def main():
    os.makedirs("source", exist_ok=True)
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found!")
        print("Please put your strings.xml file in the source folder.")
        return

    for lang in languages:
        try:
            lang_dir = os.path.join(output_dir, f"values-{lang}")
            os.makedirs(lang_dir, exist_ok=True)
            
            output_file = os.path.join(lang_dir, "strings.xml")
            
            print(f"\nStarting translation to {lang}...")
            translate_xml_file(input_file, output_file, "en", lang, request)
            
            if lang != languages[-1]:
                print("Waiting before next language...")
                for j in range(10, 0, -1):
                    print(f"Next language in {j} seconds...")
                    for _ in range(10):
                        time.sleep(0.1)
        except Exception as e:
            print(f"Error translating {lang}: {str(e)}")

if __name__ == "__main__":
    main() 