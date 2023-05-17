# linebot_english_teacher

This is a system for Japanese users who are learning English vocabulary. The system processes English words and their components, such as prefixes, roots, and suffixes. Then it outputs useful information for the user to memorize the English words.

## Getting Started

To use this system, you need to have the following credentials:

・OpenAI API key
・Line Channel Access Token
・Line Channel Secret

After obtaining these credentials, you can clone this repository and run the code.

Bash
git clone https://github.com/username/repository.git
cd repository
python app.py

## Dependencies

This code uses the following dependencies:

・FastAPI
・OpenAI API
・Linebot

## Usage

To use this system, you need to send an array of English words to the system. The system will break down each word into prefixes, roots, and suffixes. If a corresponding prefix, root, or suffix is not found, it will be labeled as N/A. Then the system outputs the information in a specified format.

 ## Input Example

Bash
construction reserve

## Output Example

Bash
WORD_1 : construction
PREFIX_1 : con- ... 一緒に
ROOT_1 : struct ... 建てる
SUFFIX_1 : -ion ... 名詞化の接尾辞
MEANINGS_1 : 建設
ETYMOLOGY_1 : construct（一緒に建てる）に、名詞化の接尾辞がついたもの
TIPS_1 : 
[例] ... construction site (建設現場), 
[名詞] ... construction (建設),
[動詞] ... construct (建設する), 
[形容詞] ... constructive (建設的な),
[類義語] ... building (建物),
[重要表現] ... under construction (建設中),
[使用例] ... The construction of the new building is almost complete. (新しい建物の建設はほぼ完了しています。)

WORD_2 : reserve
PREFIX_2 : re- ... 再び
ROOT_2 : serv ... 保つ
SUFFIX_2 : -e ... 動詞化の接尾辞
MEANINGS_2 : 予約する、蓄える、備える
ETYMOLOGY_2 : re-（再び）、serve（保つ）。後ろに取っておくという意味。
TIPS_2 : 
[例] ... to reserve a room (部屋を予約する), 
[名詞] ... reservation (予約),
[動詞] ... reserve (予約する),
[形容詞] ... reserved (控えめな),
[類義語] ... book (予約する), save (蓄える), store (蓄える),
[重要表現] ... reserve the right to do (～する権利を有する),
[使用例] ... I will reserve a table for two for tonight. (今夜の二人分のテーブルを予約します。)

## Note
Please note that the provided URL is being used as a database for personal use only. Do not share the code or data obtained from this URL with others without permission.

https://www.readingrockets.org/article/root-words-roots-and-affixes
