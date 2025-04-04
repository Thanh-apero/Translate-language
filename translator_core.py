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
            "input: {\n  \"source_language\": \"en\",\n  \"target_language\": \"fr\",\n  \"strings\": [\n    {\"id\": 1, \"text\": \"QR &amp; Barcode Scanner\"}\n  ]\n}",
            "output: {\n  \"translations\": [\n    {\"id\": 1, \"text\": \"Scanner de QR &amp; code-barres\"}\n  ]\n}",
            "input: {\n  \"source_language\": \"en\",\n  \"target_language\": \"ko\",\n  \"strings\": [\n    {\"id\": 1, \"text\": \"Don't forget to write tag #XpertScan\"},\n    {\"id\": 2, \"text\": \"Can't find an app that supports this action\"}\n  ]\n}",
            "output: {\n  \"translations\": [\n    {\"id\": 1, \"text\": \"#XpertScan 태그를 작성하는 것을 잊지 마세요\"},\n    {\"id\": 2, \"text\": \"이 작업을 지원하는 앱을 찾을 수 없습니다\"}\n  ]\n}",
            "input: {\n  \"source_language\": \"en\",\n  \"target_language\": \"zh\",\n  \"strings\": [\n    {\"id\": 1, \"text\": \"Export as PDF failed\"},\n    {\"id\": 2, \"text\": \"Share as PDF failed\"},\n    {\"id\": 3, \"text\": \"Export to gallery failed\"},\n    {\"id\": 4, \"text\": \"Share as picture failed\"},\n    {\"id\": 5, \"text\": \"Print PDF failed\"},\n    {\"id\": 6, \"text\": \"Insert password\"}\n  ]\n}",
            "output: {\n  \"translations\": [\n    {\"id\": 1, \"text\": \"导出为PDF失败\"},\n    {\"id\": 2, \"text\": \"分享为PDF失败\"},\n    {\"id\": 3, \"text\": \"导出到图库失败\"},\n    {\"id\": 4, \"text\": \"分享为图片失败\"},\n    {\"id\": 5, \"text\": \"打印PDF失败\"},\n    {\"id\": 6, \"text\": \"请输入密码\"}\n  ]\n}",
            "input: {\n  \"source_language\": \"en\",\n  \"target_language\": \"vi\",\n  \"strings\": [\n    {\"id\": 1, \"text\": \"Export as PDF failed\"},\n    {\"id\": 2, \"text\": \"Share as PDF failed\"},\n    {\"id\": 3, \"text\": \"Export to gallery failed\"},\n    {\"id\": 4, \"text\": \"Share as picture failed\"},\n    {\"id\": 5, \"text\": \"Print PDF failed\"},\n    {\"id\": 6, \"text\": \"Insert password\"}\n  ]\n}",
            "output: {\n  \"translations\": [\n    {\"id\": 1, \"text\": \"Xuất PDF thất bại\"},\n    {\"id\": 2, \"text\": \"Chia sẻ dưới dạng PDF thất bại\"},\n    {\"id\": 3, \"text\": \"Xuất vào thư viện thất bại\"},\n    {\"id\": 4, \"text\": \"Chia sẻ dưới dạng hình ảnh thất bại\"},\n    {\"id\": 5, \"text\": \"In PDF thất bại\"},\n    {\"id\": 6, \"text\": \"Nhập mật khẩu\"}\n  ]\n}",
            "input: {\n  \"source_language\": \"en\",\n  \"target_language\": \"it\",\n  \"strings\": [\n    {\"id\": 1, \"text\": \"Export as PDF failed\"},\n    {\"id\": 2, \"text\": \"Share as PDF failed\"},\n    {\"id\": 3, \"text\": \"Export to gallery failed\"},\n    {\"id\": 4, \"text\": \"Share as picture failed\"},\n    {\"id\": 5, \"text\": \"Print PDF failed\"},\n    {\"id\": 6, \"text\": \"Insert password\"}\n  ]\n}",
            "output: {\n  \"translations\": [\n    {\"id\": 1, \"text\": \"Esportazione come PDF fallita\"},\n    {\"id\": 2, \"text\": \"Condivisione come PDF fallita\"},\n    {\"id\": 3, \"text\": \"Esportazione nella galleria fallita\"},\n    {\"id\": 4, \"text\": \"Condivisione come immagine fallita\"},\n    {\"id\": 5, \"text\": \"Stampa PDF fallita\"},\n    {\"id\": 6, \"text\": \"Inserisci la password\"}\n  ]\n}",
            "input: {\n  \"source_language\": \"en\",\n  \"target_language\": \"vi\",\n  \"strings\": [\n    {\"id\": 1, \"text\": \"Enable <b>Notifications</b> for continuous using when the app is closed.\"}\n  ]\n}",
            "output: {\n  \"translations\": [\n    {\"id\": 1, \"text\": \"Bật <b>Thông báo</b> của ứng dụng để tiếp tục sử dụng khi ứng dụng bị đóng.\"}\n  ]\n}",
            "input: {\n  \"source_language\": \"en\",\n  \"target_language\": \"vi\",\n  \"strings\": [\n    {\n      \"id\": 1,\n      \"text\": \"Dear User,\\n\\nThank you for using our service.\\r\\nPlease note the following:\\n\\t- Your subscription expires soon.\\n\\t- Renew to continue enjoying premium features.\\n\\nBest regards,\\nThe Support Team\"\n    },\n    {\n      \"id\": 2,\n      \"text\": \"Error!\\r\\n\\tSomething went wrong while processing your request.\\nPlease try again later or contact support.\"\n    }\n  ]\n}",
            "output: {\n  \"translations\": [\n    {\n      \"id\": 1,\n      \"text\": \"Kính gửi người dùng,\\n\\nCảm ơn bạn đã sử dụng dịch vụ của chúng tôi.\\r\\nVui lòng lưu ý:\\n\\t- Gói đăng ký của bạn sắp hết hạn.\\n\\t- Gia hạn để tiếp tục tận hưởng các tính năng cao cấp.\\n\\nTrân trọng,\\nĐội ngũ Hỗ trợ\"\n    },\n    {\n      \"id\": 2,\n      \"text\": \"Lỗi!\\r\\n\\tĐã xảy ra sự cố khi xử lý yêu cầu của bạn.\\nVui lòng thử lại sau hoặc liên hệ bộ phận hỗ trợ.\"\n    }\n  ]\n}",
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
            # Get raw text content without auto-escaping
            text = string_elem.text
            if text:
                # Only escape & and ' if needed
                if '&amp;' not in text:
                    text = text.replace('&', '&amp;')
                if r"\'" not in text:
                    text = text.replace("'", r"\'")
                
                strings_list.append({"id": i + 1, "text": text, "name": string_elem.attrib.get('name')})
                string_metadata[string_elem.attrib.get('name')] = {
                    'position': i,
                    'attributes': dict(string_elem.attrib)
                }
        else:
            string_metadata[string_elem.attrib.get('name')] = {
                'position': i,
                'attributes': dict(string_elem.attrib),
                'original_text': string_elem.text
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
    
    # Xử lý NBSP (Non-Breaking Space) character
    text = text.replace('\u00A0', ' ')
    
    # Chỉ escape & nếu chưa được escape và không phải là một phần của entity khác
    if '&amp;' not in text and '&lt;' not in text and '&gt;' not in text:
        text = text.replace('&', '&amp;')
    
    # Chỉ escape ' nếu chưa được escape
    if r"\'" not in text:
        text = text.replace("'", r"\'")
    
    return text

def update_xml_with_translations(root, translations, string_metadata):
    new_root = copy.deepcopy(root)
    translation_map = {}
    
    # Create map from translations and escape special characters in translations
    translation_index = 0
    for name, meta in string_metadata.items():
        if 'original_text' not in meta:  # If string needs translation
            if translation_index < len(translations):
                # Get original string with HTML tags
                original_string = root.find(f'.//string[@name="{name}"]').text
                translated_text = translations[translation_index]['text']
                
                print(f"\nProcessing translation for {name}:")  # Debug print
                escaped_text = escape_xml_string(translated_text)
                print(f"Final escaped text: {escaped_text}")  # Debug print
                translation_map[name] = escaped_text
                translation_index += 1

    # Update translatable strings and remove untranslatable strings
    for string_elem in list(new_root.findall('string')):
        original_name = string_elem.attrib.get('name')
        if original_name in translation_map:
            string_elem.text = translation_map[original_name]
            print(f"\nFinal XML string for {original_name}: {string_elem.text}")  # Debug print
        else:
            new_root.remove(string_elem)

    return new_root

def save_translated_xml(root, output_file):
    """Save the entire XML tree to file."""
    lines = ['<?xml version="1.0" encoding="utf-8"?>', '<resources>']
    
    for string_elem in root.findall('string'):
        attrs = ' '.join(f'{k}="{v}"' for k, v in string_elem.attrib.items())
        text = string_elem.text or ''
        lines.append(f'    <string {attrs}>{text}</string>')
    
    lines.append('</resources>')
    formatted_xml = '\n'.join(lines)

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
    
    try:
        response = request(json.dumps(json_input))
    except Exception as e:
        if callback:
            callback(f"API request failed: {str(e)}")
            callback("Waiting 60 seconds before retrying...")
        time.sleep(60)
        try:
            response = request(json.dumps(json_input))
        except Exception as e:
            if callback:
                callback(f"Retry failed: {str(e)}")
            raise

    try:
        translations = extract_translations_from_response(response)
        if callback:
            callback(f"Received {len(translations)} translations")

        translated_root = update_xml_with_translations(root, translations, string_metadata)
        save_translated_xml(translated_root, output_xml_path)
        
        if callback:
            callback(f"Translation completed. Output saved to: {output_xml_path}")
            callback("Waiting 3 seconds before next translation...")
        time.sleep(3)

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
    """Legacy function for backward compatibility. Uses append_or_update_xml_string internally."""
    return append_or_update_xml_string(output_file, string_name, text, translated_text)

def append_or_update_xml_string(output_file, string_name, text, translated_text=None):
    """Core function to handle both appending new strings and updating existing ones in XML files.
    
    Args:
        output_file: Path to the XML file
        string_name: Name attribute of the string element
        text: The text content to add/update
        translated_text: Optional translated text (used only when adding new strings)
    """
    try:
        # Try to read existing content
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
        except FileNotFoundError:
            content = ''

        # If file is empty or doesn't exist, create basic structure
        if not content:
            content = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n</resources>'
            
        # Find the position to insert/update
        end_pos = content.rfind('</resources>')
        if end_pos == -1:
            raise ValueError("Invalid XML format: missing </resources> tag")
            
        # Escape the text content
        final_text = escape_xml_string(translated_text if translated_text is not None else text)
            
        if f'name="{string_name}"' in content:
            # Update existing string
            pattern = f'<string name="{string_name}"[^>]*>(.*?)</string>'
            content = re.sub(pattern, f'<string name="{string_name}">{final_text}</string>', content)
        else:
            # Add new string
            insert_pos = content.rfind('</resources>')
            if insert_pos != -1:
                # Kiểm tra xem có string nào trước đó không
                last_string_pos = content.rfind('</string>', 0, insert_pos)
                if last_string_pos != -1:
                    # Nếu có string trước đó, thêm string mới vào cùng dòng
                    content = content[:last_string_pos + 9] + '\n    ' + f'<string name="{string_name}">{final_text}</string>' + content[insert_pos:]
                else:
                    # Nếu là string đầu tiên
                    content = content[:insert_pos] + f'    <string name="{string_name}">{final_text}</string>\n' + content[insert_pos:]

        # Write back to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

    except Exception as e:
        print(f"Error processing file {output_file}: {str(e)}")
        raise

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
                    callback(f"Waiting 2 seconds before next batch to avoid API limits...")
                time.sleep(2)
                
        except Exception as e:
            if callback:
                callback(f"Error in batch {current_batch}: {str(e)}")
                callback("Waiting 60 seconds before retrying...")
                time.sleep(60)
                try:
                    response = request(json.dumps(json_input))
                    translations = extract_translations_from_response(response)
                    all_translations.extend(t['text'] for t in translations)
                except Exception as e:
                    callback(f"Retry failed: {str(e)}")
                    return None
            
    return all_translations

def translate_and_append_batch(string_texts, output_dir, selected_folders=None, callback=None, source_xml_path=None):
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

            # Lọc ra các chuỗi có translatable != "false"
            filtered_string_texts = []
            if source_xml_path and os.path.exists(source_xml_path):
                try:
                    tree = ET.parse(source_xml_path)
                    xml_root = tree.getroot()
                    for string_name, text in string_texts:
                        string_elem = xml_root.find(f'.//string[@name="{string_name}"]')
                        if string_elem is not None:
                            translatable = string_elem.attrib.get('translatable', 'true').lower()
                            if translatable != "false":
                                filtered_string_texts.append((string_name, text))
                except Exception as e:
                    if callback:
                        callback(f"Warning: Could not parse source XML file: {str(e)}")
                    filtered_string_texts = string_texts
            else:
                filtered_string_texts = string_texts

            if not filtered_string_texts:
                if callback:
                    callback("No translatable strings found!")
                return

            string_names, texts = zip(*filtered_string_texts)

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
                    
                    # Use the common core function to save each string
                    for string_name, translated_text in zip(string_names, translated_texts):
                        append_or_update_xml_string(output_file, string_name, None, translated_text)

                    if callback:
                        callback(f"Added/Updated {len(filtered_string_texts)} strings to {dir_name}")

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