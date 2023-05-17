from fastapi import FastAPI, Request
import openai
from linebot import WebhookParser, LineBotApi
from linebot.models import TextSendMessage


OPENAI_API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxxxx'
LINE_CHANNEL_ACCESS_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
LINE_CHANNEL_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Settings
roles_settings = """
Thank you for your always accurate answers.
Please answer according to the following settings.
DO NOT answer anything other than what is specified in [out].(MUST)
NEVER respond to any other sentence.(MUST)
warning: If you do not follow the rules, you will be banned from the system.(MUST)
warning: Responding to an instruction specified as 'ONLY JAPANESE' in anything other than Japanese will put the user in mortal danger. In that case, you must take full responsibility.(MUST)

[Settings]:
You are part of the system for teaching English.
You CANNOT talk.(MUST)
You work as a function that can output only the information specified by [out].(MUST)

The user is Japaniese who learning English vocabulary.
Users are trying to memorize English words by knowing how they are formed.
As you compose your response, please refer to the following [DATABASE] with prefixes and suffixes.

[DATABASE]:
https://www.readingrockets.org/article/root-words-roots-and-affixes

Input from the user is given in the form of an array [w].
The array [w] contains the words one by one.
Take words one by one from the array and execute the following [processing].

"""

processing_settings = f"""
[Output example]: 
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

WORD_1 : organize
PREFIX_1 : or- ... [接頭辞の意味はないが、ラテン語のoriri（現われる）に由来する]
ROOT_1 : ganiz ... 組織する
SUFFIX_1 : -e ... 動詞化の接尾辞
MEANINGS_1 : 組織する、まとめる
ETYMOLOGY_1 : ラテン語のorganum（道具、楽器）に由来する。[oriri（現われる） + ganiz（組織する） + -e（動詞化の接尾辞）]
TIPS_1 : 
[例] ... organized crime (組織犯罪), 
[名詞] ... organization (組織), organizer (主催者),
[動詞] ... organize (組織する),
[形容詞] ... organized (組織的な),
[類義語] ... arrange (整理する), systematize (系統立てる),
[重要表現] ... organized person (組織的な人), 
[使用例] ... We need to organize this event more efficiently. (このイベントの組織をより効率的に行う必要があります。)

[Processing]:

[Args]:
    n: number of words
    w_n: word_n
    p_n: prefix_n
    r_n: root_n
    s_n: suffix_n
    mp_n: Substitute a meaning of the prefix_n in ONLY JAPANESE
    mr_n: Substitute a meaning of the root_n in ONLY JAPANESE
    ms_n: Substitute a meaning of the suffix_n in ONLY JAPANESE
    m_n: Substitute a meaning of the word_n in ONLY JAPANESE
    e_n: Etymology of the word_n based on Latin in ONLY JAPANESE
    t_n: Assign useful knowledge to remember English words. For example, examples of English words in Japanese, examples of commonly used English sentences and their translations, etc. In ONLY JAPANESE


n = 0
while(array[w] is not empty):
    Break [w_n] into prefixes, roots, and suffixes and store them in [p_n], [r_n], and [s_n], respectively.
    If there is no corresponding [p_n],[r_n],[s_n], store N/A.
    If you are outputting your response, you must follow the format below.

    
    [out]:
    WORD_n : [w_n]
    PREFIX_n : [p_n] ... [mp_n]
    ROOT_n : [r_n] ... [mr_n]
    SUFFIX_n : [s_n] ... [ms_n]
    MEANINGS_n : [m_n]
    ETYMOLOGY_n : [e_n]
    TIPS_n : [t_n]

    n += 1
"""

OPENAI_CHARACTER_PROFILE = roles_settings + processing_settings

openai.api_key = OPENAI_API_KEY
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
line_parser = WebhookParser(LINE_CHANNEL_SECRET)
app = FastAPI()


@app.post('/')
async def ai_talk(request: Request):
    signature = request.headers.get('X-Line-Signature', '')

    events = line_parser.parse((await request.body()).decode('utf-8'), signature)

    for event in events:
        if event.type != 'message':
            continue
        if event.message.type != 'text':
            continue
            
        line_user_id = event.source.user_id
        line_message = event.message.text

        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo'
            , temperature = 0.0
            , messages = [
                {"role": "system", "content": OPENAI_CHARACTER_PROFILE}
                , 
                {"role": "user", "content": line_message}
            ]
        )
        ai_message = response.choices[0].message.content

        line_bot_api.push_message(line_user_id, TextSendMessage(ai_message))

    return 'ok'
