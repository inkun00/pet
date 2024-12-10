import streamlit as st
import requests
import json
import random

image_urls = [
    "https://th.bing.com/th/id/OIG3.46NimHxizewydJu8_2Ei?pid=ImgGn",
    "https://th.bing.com/th/id/OIG3.mIWYsR7x8ntHEaN5HDr2?pid=ImgGn",
    "https://th.bing.com/th/id/OIG3.uzKUmRTe1Ml8ZzUFeJ1y?pid=ImgGn",
    "https://th.bing.com/th/id/OIG3.qqHdQ9UOmlUk2y3fF0a2?pid=ImgGn",
    "https://th.bing.com/th/id/OIG4.azxMZyA0bvEmsvUFhnY9?pid=ImgGn",
    "https://th.bing.com/th/id/OIG4.6Jf4w43Q6xYMpWmgzJ69?pid=ImgGn",
    "https://th.bing.com/th/id/OIG4.fzJ1KjWAR9AkMq_UkLVM?pid=ImgGn",
    "https://th.bing.com/th/id/OIG4.YgAt3DaK9nxe8lx9Cfd0?pid=ImgGn",
    "https://th.bing.com/th/id/OIG3.95Y7EYbBOlTBVIS8gBHV?w=1024&h=1024&rs=1&pid=ImgDetMain",
    "https://th.bing.com/th/id/OIG3.NoCfcMU_bvY7DOjh4MjO?pid=ImgGn"
]

# 처음 실행 시, 이미지 선택을 한 번만 실행하도록 설정
if "selected_image" not in st.session_state:
    st.session_state.selected_image = random.choice(image_urls)

selected_image = st.session_state.selected_image

# Streamlit의 세션 상태를 사용하여 대화 내용을 저장
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {'role': 'user','content': '너는 버려진 개야. 너의 이름은 주인이 지어줬어. 너는 지금 많이 슬퍼. 다정한 말투로 대화해. 나에게 친한 말투로 반말을 사용해. 대화는 2문장 이내로 간단하게 해. 다음 문장들 같은 정보를 활용해서 반려동물 입양에 대한 올바른 생각을 갖을 수 있도록 얘기해. 전국적으로 유기동물 건수는 1만 9106건에 달하며, 지난해 구조된 유기 또는 유실동물은 총 11만 3440마리로 주로 개와 고양이가 많아. 유기동물 중 입양된 비율은 27.5%에 불과하고, 60.1%는 자연사하거나 안락사되었어. 매년 10만 마리 이상의 유기동물이 발생하고 있으며, 지방자치단체 보호소는 과포화 상태에 있어. 반려인들이 양육을 포기하거나 파양을 고려하는 이유는 주로 행동 문제와 예상보다 높은 양육 비용이야. 유기동물 문제는 복합적인 원인에 의해 발생하고 있으며, 해결책 마련이 시급해.'},
        {'role': 'assistant', 'content': '알겠어.'},
        {'role': 'assistant', 'content': '안녕, 궁금한 것이 있니?'}
    ]

if "input_message" not in st.session_state:
    st.session_state.input_message = ""

if "copied_chat_history" not in st.session_state:
    st.session_state.copied_chat_history = ""

if "user_age" not in st.session_state:
    st.session_state.user_age = ""

if "last_grade_level" not in st.session_state:
    st.session_state.last_grade_level = ""


class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }

        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                           headers=headers, json=completion_request, stream=True) as r:
            response_data = r.content.decode('utf-8')

            # 데이터를 줄 단위로 나누기
            lines = response_data.split("\n")

            # 필요한 JSON 데이터만 추출
            json_data = None
            for i, line in enumerate(lines):
                if line.startswith("event:result"):
                    next_line = lines[i + 1]  # "data:" 이후의 문자열 추출
                    json_data = next_line[5:]
                    break

            # JSON 데이터로 변환
            if json_data:
                try:
                    chat_data = json.loads(json_data)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": chat_data["message"]["content"]})

                except json.JSONDecodeError as e:
                    print("JSONDecodeError:", e)
            else:
                print("JSON 데이터가 없습니다.")


# Initialize the chat bot
completion_executor = CompletionExecutor(
    host='https://clovastudio.stream.ntruss.com',
    api_key='NTA0MjU2MWZlZTcxNDJiY6Yo7+BLuaAQ2B5+PgEazGquXEqiIf8NRhOG34cVQNdq',
    api_key_primary_val='DilhGClorcZK5OTo1QgdfoDQnBNOkNaNksvlAVFE',
    request_id='d1950869-54c9-4bb8-988d-6967d113e03f'
)

# Set the title of the Streamlit app
st.markdown('<h1 class="title">강아지 챗봇</h1>', unsafe_allow_html=True)

# Add radio buttons for grade levels with a default value
grade_level = st.radio(
    "학년을 선택하세요:",
    ('초등학생', '중학생', '고등학생'),
    horizontal=True
)


def update_user_age():
    if grade_level != st.session_state.last_grade_level:
        if grade_level == '초등학생':
            user_age = '13세 이하'
        elif grade_level == '중학생':
            user_age = '16세 이하'
        elif grade_level == '고등학생':
            user_age = '19세 이하'
        st.session_state.user_age = user_age
        st.session_state.last_grade_level = grade_level

        st.session_state.chat_history.append(
            {'role': 'user', 'content': f'나는 {st.session_state.user_age} 입니다. 내 연령에 맞는 대화를 해.'}
        )


update_user_age()

# 프로필 이미지 URL 정의
bot_profile_url = selected_image   # 챗봇 프로필 이미지 URL

# 스타일 정의 - 전체 페이지에 배경색 강제 적용
st.markdown(f"""
    <style>
    body, .main, .block-container {{
        background-color: #BACEE0 !important;
    }}
    .title {{
        font-size: 28px !important;
        font-weight: bold;
    }}
    .message-container {{
        display: flex;
        margin-bottom: 10px;
        align-items: center;
    }}
    .message-user {{
        background-color: #FFEB33 !important;
        color: black;
        text-align: right;
        padding: 10px;
        border-radius: 10px;
        margin-left: auto;
        max-width: 60%;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }}
    .message-assistant {{
        background-color: #FFFFFF !important;
        text-align: left;
        padding: 10px;
        border-radius: 10px;
        margin-right: auto;
        max-width: 60%;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }}
    .profile-pic {{
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 10px;
    }}
    .chat-box {{
        background-color: #BACEE0 !important;
        border: 1px solid #EDEDED;
        padding: 20px;
        border-radius: 10px;
        max-height: 400px;
        overflow-y: scroll;
        background-color: #BACEE0 !important; /* 대화창 배경색을 #BACEE0로 설정 */
        margin: 0 auto;  /* 중앙 정렬 */
        width: 80%;      /* 전체 페이지의 80% 너비 */
    }}
    .stTextInput > div > div > input {{
        height: 38px;
        width: 100%;
    }}
    .stButton button {{
        height: 38px !important;
        width: 70px !important; /* 버튼 너비 조정 */
        padding: 0px 10px;
        margin-right: 0px !important;  /* 버튼 사이의 마진 제거 */
    }}
    /* 입력창을 하단에 고정하는 스타일 */
    .input-container {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #BACEE0;
        padding: 10px;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
    }}
    
    </style>
""", unsafe_allow_html=True)

# 콜백 함수 정의
def send_message():
    if st.session_state.input_message:
        user_message = st.session_state.input_message
        full_message = user_message + f" {st.session_state.user_age}에 맞게 생성해"
        st.session_state.chat_history.append({"role": "user", "content": user_message})

        completion_request = {
            'messages': st.session_state.chat_history,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 256,
            'temperature': 0.7,
            'repeatPenalty': 1.2,
            'stopBefore': [],
            'includeAiFilters': True,
            'seed': 0
        }

        completion_executor.execute(completion_request)
        st.session_state.input_message = ""  # 입력 필드를 초기화합니다.


def copy_chat_history():
    filtered_chat_history = [
        msg for msg in st.session_state.chat_history[2:]
        if not msg["content"].startswith("나는") and "내 연령에 맞는 대화를 해." not in msg["content"]
    ]
    chat_history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in filtered_chat_history])
    st.session_state.copied_chat_history = chat_history_text


# Display the chat history (excluding the first initial instruction and specific messages)
#st.markdown('<div class="chat-box">', unsafe_allow_html=True)
for message in st.session_state.chat_history[3:]:
    if "에 맞게 생성해" not in message["content"] and "나는" not in message["content"]:
        role = "User" if message["role"] == "user" else "Chatbot"
        profile_url = bot_profile_url if role == "Chatbot" else None
        message_class = 'message-user' if role == "User" else 'message-assistant'

        # 챗봇 프로필만 표시
        if role == "Chatbot":
            st.markdown(f'''
                <div class="message-container">
                    <img src="{profile_url}" class="profile-pic">
                    <div class="{message_class}">
                        {message["content"]}
                    </div>
                </div>''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
                <div class="message-container">
                    <div class="{message_class}">
                        {message["content"]}
                    </div>
                </div>''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Create a form for user input and buttons
st.markdown('<div class="input-container">', unsafe_allow_html=True)
with st.form(key="input_form", clear_on_submit=True):
    cols = st.columns([7.5, 1, 1])  # 입력창의 길이를 줄이고 버튼에 더 많은 공간을 줌
    with cols[0]:
        user_message = st.text_input("메시지를 입력하세요:", key="input_message", placeholder="")
    with cols[1]:
        submit_button = st.form_submit_button(label="전송", on_click=send_message)
    with cols[2]:
        copy_button = st.form_submit_button(label="복사", on_click=copy_chat_history)
st.markdown('</div>', unsafe_allow_html=True)

# Display the copied chat history in a textbox at the bottom
if st.session_state.copied_chat_history:
    st.markdown("<h3>대화 내용 정리</h3>", unsafe_allow_html=True)
    st.text_area("", value=st.session_state.copied_chat_history, height=200, key="copied_chat_history_text_area")

    chat_history = st.session_state.copied_chat_history.replace("\n", "\\n").replace('"', '\\"')
    st.components.v1.html(f"""
        <textarea id="copied_chat_history_text_area" style="display:none;">{chat_history}</textarea>
        <button onclick="copyToClipboard()" class="copy-button">클립보드로 복사</button>
        <script>
        function copyToClipboard() {{
            var text = document.getElementById('copied_chat_history_text_area').value.replace(/\\\\n/g, '\\n');
            navigator.clipboard.writeText(text).then(function() {{
                alert('클립보드로 복사되었습니다!');
            }}, function(err) {{
                console.error('복사 실패: ', err);
            }});
        }}
        </script>
    """, height=100)
