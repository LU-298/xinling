"""
心灵伙伴 - 治愈系心理健康数字人 🌱
"""
import streamlit as st
import time

st.set_page_config(page_title="心灵伙伴", page_icon="🌱", layout="wide")

API_KEY = "sk-eb28d368d6054551bad7e34daac57efd"
API_URL = "https://api.deepseek.com"

ROBOT_URL = "https://coze-coding-project.tos.coze.site/coze_storage_7625532895788105770/xinling-robot-v3_d3a96781.png?sign=1778082926-5227363965-0-fa71766199f5eb7764b262bfbd1579ef8ce81999b856f7a3c4675f29a181598d"

def get_ai_response(user_msg):
    """调用DeepSeek API，带重试"""
    for attempt in range(3):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=API_KEY, base_url=API_URL, timeout=60)
            system_prompt = "你是心灵伙伴，温暖的AI心理健康陪伴助手。像朋友一样聊天，善于倾听，回复简洁，用emoji。"
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg}
                ],
                max_tokens=80,
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt < 2:
                time.sleep(1)
                continue
            return "连接有点问题呢... 💭 请稍后再试"
    return "连接有点问题呢... 💭 请稍后再试"

def clean_for_js(text):
    return text.replace("\n", " ").replace('"', "'").replace("\\", "")

EMOTIONS = {
    "happy": {"name": "开心", "emoji": "😊"},
    "sad": {"name": "难过", "emoji": "😢"},
    "surprised": {"name": "惊讶", "emoji": "😲"},
    "confused": {"name": "困惑", "emoji": "🤔"},
    "thinking": {"name": "思考", "emoji": "🤨"},
    "angry": {"name": "生气", "emoji": "😤"},
    "loving": {"name": "温暖", "emoji": "🥰"},
    "neutral": {"name": "平静", "emoji": "🤗"}
}

EMOTION_MAP = {
    "happy": ["开心", "高兴", "快乐", "棒", "太好了", "幸福", "哈哈"],
    "sad": ["难过", "伤心", "痛苦", "哭", "累", "悲伤", "郁闷", "不开心"],
    "surprised": ["惊讶", "哇", "什么", "不会吧", "真的"],
    "confused": ["困惑", "不懂", "不知道", "迷茫", "怎么办"],
    "thinking": ["想", "思考", "考虑"],
    "angry": ["生气", "愤怒", "烦", "气死了"],
    "loving": ["爱", "喜欢", "想你", "谢谢", "温暖", "感动"]
}

def detect_emotion(text):
    for emotion, keywords in EMOTION_MAP.items():
        for kw in keywords:
            if kw in text:
                return emotion
    return "neutral"

st.components.v1.html("""
<script>
function speakText(text) {
    if ('speechSynthesis' in window) {
        speechSynthesis.cancel();
        var u = new SpeechSynthesisUtterance(text);
        u.lang = 'zh-CN';
        u.rate = 0.95;
        u.pitch = 1.1;
        speechSynthesis.speak(u);
    }
}
</script>
""", height=0)

st.components.v1.html("""
<script>
setInterval(function() {
    var robot = window.parent.document.querySelector('.avatar-box');
    if (robot) {
        robot.classList.add('blink');
        setTimeout(function() { robot.classList.remove('blink'); }, 250);
    }
}, 4000);
</script>
""", height=0)

st.markdown("""
<style>
.stApp { background: linear-gradient(180deg, #e8f5e9 0%, #c8e6c9 100%); font-family: 'Noto Sans SC', sans-serif; }
.top-area { text-align: center; padding: 20px; background: linear-gradient(135deg, #4CAF50, #66BB6A); border-radius: 0 0 40px 40px; margin-bottom: 20px; }
.avatar-box { width: 180px; height: 180px; margin: 0 auto; border-radius: 50%; overflow: hidden; border: 6px solid white; box-shadow: 0 12px 48px rgba(0,0,0,0.25); }
.avatar-img { width: 100%; height: 100%; object-fit: cover; animation: idle 4s ease-in-out infinite; }
@keyframes idle { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.04); } }
.avatar-box.blink .avatar-img { animation: blink-anim 0.25s ease-in-out; }
@keyframes blink-anim { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }
.robot-title { color: white; font-size: 28px; font-weight: bold; margin-top: 15px; }
.emotion-tag { display: inline-block; padding: 8px 20px; background: rgba(255,255,255,0.3); border-radius: 25px; color: white; font-size: 15px; margin-top: 12px; }
.chat-box { max-width: 550px; margin: 0 auto; background: white; border-radius: 30px; box-shadow: 0 15px 60px rgba(0,0,0,0.12); overflow: hidden; }
.chat-title { background: linear-gradient(135deg, #4CAF50, #66BB6A); color: white; padding: 15px; text-align: center; font-size: 18px; font-weight: bold; }
.chat-msgs { height: 380px; overflow-y: auto; padding: 20px; background: #f8faf8; }
.chat-msg { margin-bottom: 15px; animation: msg-in 0.3s ease; }
@keyframes msg-in { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
.chat-msg.user { text-align: right; }
.msg-text { display: inline-block; max-width: 78%; padding: 12px 18px; border-radius: 20px; font-size: 15px; line-height: 1.6; }
.chat-msg.user .msg-text { background: linear-gradient(135deg, #4CAF50, #45a049); color: white; border-bottom-right-radius: 6px; }
.chat-msg.bot .msg-text { background: white; color: #333; border-bottom-left-radius: 6px; box-shadow: 0 3px 12px rgba(0,0,0,0.08); }
.mini-avatar { width: 32px; height: 32px; border-radius: 50%; vertical-align: middle; margin-right: 8px; }
.input-area { padding: 15px 20px; background: white; border-top: 1px solid #f0f0f0; display: flex; gap: 12px; align-items: center; }
.chat-input { flex: 1; border: none !important; border-radius: 30px !important; padding: 15px 22px !important; background: #f5f5f5 !important; font-size: 15px !important; }
.send-btn { background: linear-gradient(135deg, #4CAF50, #45a049) !important; color: white !important; border: none !important; border-radius: 50% !important; width: 52px !important; height: 52px !important; font-size: 22px !important; }
.clear-btn { background: #f0f0f0 !important; color: #888 !important; border: none !important; border-radius: 50% !important; width: 45px !important; height: 45px !important; font-size: 18px !important; }
</style>
""", unsafe_allow_html=True)

if "msgs" not in st.session_state:
    st.session_state.msgs = [{"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n很高兴认识你~有什么想和我聊聊的吗？"}]
if "cur_emotion" not in st.session_state:
    st.session_state.cur_emotion = "neutral"

e = EMOTIONS[st.session_state.cur_emotion]

st.markdown(f"""
<div class="top-area">
    <div class="avatar-box">
        <img src="{ROBOT_URL}" class="avatar-img" />
    </div>
    <div class="robot-title">🌱 心灵伙伴</div>
    <div class="emotion-tag">{e["emoji"]} {e["name"]}</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-box">', unsafe_allow_html=True)
st.markdown('<div class="chat-title">💬 对话</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-msgs">', unsafe_allow_html=True)

for msg in st.session_state.msgs:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-msg user"><div class="msg-text">👤 {msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-msg bot"><img src="{ROBOT_URL}" class="mini-avatar" /><div class="msg-text">🤖 {msg["content"]}</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="input-area">', unsafe_allow_html=True)

user_input = st.text_input("", placeholder="说点什么吧...", label_visibility="collapsed", key="chat_input")

col_clear, col_input, col_send = st.columns([1, 5, 1])
with col_clear:
    clear_btn = st.button("🗑️", key="clear_btn")
with col_input:
    pass
with col_send:
    send_btn = st.button("➤", key="send_btn")

st.markdown('</div></div>', unsafe_allow_html=True)

if send_btn and user_input.strip():
    user_text = user_input.strip()
    st.session_state.msgs.append({"role": "user", "content": user_text})
    
    emotion = detect_emotion(user_text)
    st.session_state.cur_emotion = emotion
    
    with st.spinner("🤔 思考中..."):
        response = get_ai_response(user_text)
    
    st.session_state.msgs.append({"role": "bot", "content": response})
    
    clean_text = clean_for_js(response)
    js_code = '<script>speakText("%s");</script>' % clean_text
    st.markdown(js_code, unsafe_allow_html=True)
    
    st.rerun()

if clear_btn:
    st.session_state.msgs = [{"role": "bot", "content": "好的，我们重新开始吧！🌱\n\n有什么想和我聊聊的吗？"}]
    st.session_state.cur_emotion = "neutral"
    st.rerun()
