"""
心灵伙伴 - 治愈系数字人 🌱
超级增强版 - 神态变化 + 语音 + 智能对话
"""
import streamlit as st
import time
import os

st.set_page_config(page_title="心灵伙伴", page_icon="🌱", layout="wide")

# DeepSeek API
DEEPSEEK_API_KEY = "sk-2334cff883c94f61a5dcd16d46baf550"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

def get_deepseek_response(user_message, emotion):
    """获取DeepSeek回复"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
        
        system_prompt = f"""你是"心灵伙伴"，一个温暖、专业、富有同理心的AI心理健康陪伴助手。

【你的特点】
- 温暖善良，像知心朋友一样
- 善于倾听，感知用户情绪
- 回复简短温馨，30-80字
- 会用emoji增加亲切感

【当前情绪】{emotion}

请像朋友聊天一样回复，自然温暖。"""
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
            temperature=0.85
        )
        return response.choices[0].message.content
    except Exception as e:
        return "抱歉，连接有点问题，再试一次好吗？💭"

# 情绪表情映射
EMOTION_FACES = {
    "happy": {"eyes": "😊", "mouth": "happy", "desc": "开心", "blink_speed": 2},
    "sad": {"eyes": "😢", "mouth": "sad", "desc": "难过", "blink_speed": 4},
    "stressed": {"eyes": "😰", "mouth": "neutral", "desc": "焦虑", "blink_speed": 1},
    "confused": {"eyes": "🤔", "mouth": "neutral", "desc": "困惑", "blink_speed": 3},
    "love": {"eyes": "🥰", "mouth": "happy", "desc": "温暖", "blink_speed": 3},
    "angry": {"eyes": "😤", "mouth": "sad", "desc": "生气", "blink_speed": 2},
    "tired": {"eyes": "😴", "mouth": "neutral", "desc": "疲惫", "blink_speed": 5},
    "neutral": {"eyes": "🤗", "mouth": "neutral", "desc": "平静", "blink_speed": 3}
}

EMOTION_KEYWORDS = {
    "happy": ["开心", "高兴", "快乐", "棒", "太好了", "幸福", "哈哈", "嘻嘻", "好开心", "兴奋", "激动"],
    "sad": ["难过", "伤心", "痛苦", "哭", "累", "疲惫", "心碎", "悲伤", "郁闷", "不开心", "沮丧"],
    "stressed": ["压力", "焦虑", "紧张", "害怕", "担心", "恐惧", "不安", "烦恼", "崩溃"],
    "confused": ["困惑", "不懂", "不知道", "迷茫", "怎么办", "疑问"],
    "love": ["爱", "喜欢", "想你", "谢谢", "温暖", "感动"],
    "angry": ["生气", "愤怒", "讨厌", "烦", "气死了", "怒"],
    "tired": ["累", "困", "疲惫", "疲倦", "没劲", "无力"]
}

def detect_emotion(text):
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return emotion
    return "neutral"

# 超级精美CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');

.stApp { 
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 50%, #a5d6a7 100%);
    font-family: 'Noto Sans SC', sans-serif;
}

h1 { 
    color: #1b5e20 !important; 
    text-align: center; 
    font-size: 2.8em !important; 
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.stButton > button { 
    background: linear-gradient(135deg, #4CAF50, #45a049); 
    color: white; 
    border-radius: 25px; 
    font-size: 16px; 
    padding: 12px 30px; 
    border: none;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}
.stButton > button:hover { 
    background: linear-gradient(135deg, #45a049, #3d8b40);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

/* 聊天气泡 */
.user-msg {
    background: linear-gradient(135deg, #4CAF50, #45a049);
    color: white;
    padding: 15px 20px;
    border-radius: 20px 20px 5px 20px;
    margin: 15px 0;
    max-width: 85%;
    margin-left: auto;
    box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.bot-msg {
    background: white;
    padding: 15px 20px;
    border-radius: 20px 20px 20px 5px;
    margin: 15px 0;
    max-width: 85%;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    white-space: pre-wrap;
}

/* 输入框 */
.stTextArea textarea {
    border-radius: 20px !important;
    border: 2px solid #e0e0e0 !important;
    padding: 15px !important;
    font-size: 16px !important;
    transition: all 0.3s;
}
.stTextArea textarea:focus {
    border-color: #4CAF50 !important;
    box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.2) !important;
}

/* 滚动条 */
.chat-container ::-webkit-scrollbar {
    width: 8px;
}
.chat-container ::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}
.chat-container ::-webkit-scrollbar-thumb {
    background: #4CAF50;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# 初始化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n我升级啦！现在我可以：\n• 像真人一样和你聊天 💬\n• 用表情回应你的心情 😊\n• 开口说话陪你倾诉 🗣️\n• 感知你的各种情绪 💕\n\n有什么想和我聊聊的吗？✨"}
    ]
    st.session_state.current_emotion = "neutral"
    st.session_state.is_speaking = False

# JS代码 - TTS和动画
tts_js = """
<script>
// TTS语音合成
function speakText(text) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'zh-CN';
        utterance.rate = 1;
        utterance.pitch = 1.1;
        utterance.volume = 1;
        
        // 动画嘴巴
        animateMouth();
        
        utterance.onend = function() {
            stopMouthAnimation();
        };
        
        window.speechSynthesis.speak(utterance);
    }
}

function animateMouth() {
    const mouth = document.getElementById('mouth-path');
    if (mouth) {
        mouth.dataset.animating = 'true';
        const interval = setInterval(() => {
            if (mouth.dataset.animating !== 'true') {
                clearInterval(interval);
                return;
            }
            const current = mouth.getAttribute('d');
            const isOpen = current.includes('20 25') || current.includes('22 25');
            if (isOpen) {
                mouth.setAttribute('d', 'M 5 12 Q 30 15 55 12');
            } else {
                mouth.setAttribute('d', 'M 5 12 Q 30 25 55 12');
            }
        }, 150);
    }
}

function stopMouthAnimation() {
    const mouth = document.getElementById('mouth-path');
    if (mouth) {
        mouth.dataset.animating = 'false';
        mouth.setAttribute('d', 'M 5 12 Q 30 18 55 12');
    }
}

// 眨眼
function blink() {
    const eyes = document.querySelectorAll('.eye-anim');
    eyes.forEach(eye => {
        eye.style.height = '4px';
        eye.style.borderRadius = '10px';
        setTimeout(() => {
            eye.style.height = '26px';
            eye.style.borderRadius = '50%';
        }, 150);
    });
}

// 随机眨眼
setInterval(() => {
    if (Math.random() > 0.6) blink();
}, 3000);

// 情绪变化
function updateEmotion(emotion) {
    const eyeElem = document.getElementById('emotion-eye');
    if (eyeElem) {
        const emojis = {'happy':'😊','sad':'😢','stressed':'😰','confused':'🤔','love':'🥰','angry':'😤','tired':'😴','neutral':'🤗'};
        eyeElem.textContent = emojis[emotion] || '🤗';
    }
}

// 点击数字人
function clickCharacter() {
    const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2teleQ4AIA==');
    audio.volume = 0.1;
    audio.play().catch(()=>{});
}
</script>
"""

st.components.v1.html(tts_js, height=0)

# 标题
st.markdown("# 🌱 心灵伙伴")
st.markdown("### 💚 **超级智能增强版** - 有表情 · 会说话 · 更懂你")

col_info, col_speak = st.columns([3, 1])
with col_info:
    st.success("✅ DeepSeek AI大脑已连接")
with col_speak:
    st.checkbox("🔊 自动朗读", value=True, key="auto_speak")

# 两列布局
col1, col2 = st.columns([1, 2])

with col1:
    # 超级精美的数字人
    emotion = st.session_state.current_emotion
    face = EMOTION_FACES.get(emotion, EMOTION_FACES["neutral"])
    
    st.markdown("""
    <style>
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    @keyframes breathe {
        0%, 100% { transform: translateX(-50%) scale(1); box-shadow: 0 0 30px rgba(76, 175, 80, 0.5); }
        50% { transform: translateX(-50%) scale(1.15); box-shadow: 0 0 50px rgba(76, 175, 80, 0.8); }
    }
    @keyframes wave {
        0%, 100% { transform: rotate(-10deg); }
        50% { transform: rotate(-40deg); }
    }
    .character-wrapper {
        animation: float 4s ease-in-out infinite;
    }
    .chest-glow {
        animation: breathe 3s ease-in-out infinite;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="character-wrapper" style="background:white; padding:30px; border-radius:30px; box-shadow:0 15px 50px rgba(0,0,0,0.15);">
        <div style="text-align:center; margin-bottom:15px;">
            <span style="font-size:40px;" id="emotion-eye">{face['eyes']}</span>
        </div>
        
        <!-- 数字人 -->
        <div style="width:180px; height:220px; margin:0 auto; position:relative;">
            <!-- 头 -->
            <div style="
                width:160px; height:180px; 
                background:linear-gradient(145deg, #f8f8f8 0%, #e8e8e8 50%, #d8d8d8 100%); 
                border-radius:80px; 
                position:absolute; top:0; left:50%; transform:translateX(-50%);
                box-shadow:0 10px 30px rgba(0,0,0,0.1), inset 0 -5px 20px rgba(0,0,0,0.05);
            ">
                <!-- 眼镜框 -->
                <div style="position:absolute; top:50px; left:50%; transform:translateX(-50%); display:flex; gap:12px;">
                    <div style="width:50px; height:40px; border:5px solid #2c2c2c; border-radius:12px; background:linear-gradient(135deg, rgba(200,230,255,0.4), rgba(180,210,240,0.3));"></div>
                    <div style="width:50px; height:40px; border:5px solid #2c2c2c; border-radius:12px; background:linear-gradient(135deg, rgba(200,230,255,0.4), rgba(180,210,240,0.3));"></div>
                </div>
                <!-- 眼镜桥 -->
                <div style="position:absolute; top:65px; left:50%; transform:translateX(-50%); width:20px; height:6px; background:#2c2c2c; border-radius:3px;"></div>
                
                <!-- 眼睛 -->
                <div style="position:absolute; top:55px; left:50%; transform:translateX(-50%); display:flex; gap:25px;">
                    <div class="eye-anim" style="width:26px; height:26px; background:linear-gradient(145deg, #2c2c2c, #1a1a1a); border-radius:50%; position:relative; transition:all 0.15s;">
                        <div style="position:absolute; top:5px; left:6px; width:10px; height:10px; background:white; border-radius:50%;"></div>
                    </div>
                    <div class="eye-anim" style="width:26px; height:26px; background:linear-gradient(145deg, #2c2c2c, #1a1a1a); border-radius:50%; position:relative; transition:all 0.15s;">
                        <div style="position:absolute; top:5px; left:6px; width:10px; height:10px; background:white; border-radius:50%;"></div>
                    </div>
                </div>
                
                <!-- 嘴巴 SVG -->
                <div style="position:absolute; top:105px; left:50%; transform:translateX(-50%); width:70px; height:35px;">
                    <svg viewBox="0 0 70 35" width="70" height="35">
                        <path id="mouth-path" d="M 5 12 Q 35 22 65 12" stroke="#2c2c2c" stroke-width="5" fill="none" stroke-linecap="round" style="transition:all 0.2s;"/>
                    </svg>
                </div>
            </div>
            
            <!-- 身体 -->
            <div style="
                width:150px; height:70px; 
                background:linear-gradient(145deg, #f5f5f5, #e0e0e0); 
                border-radius:35px 35px 25px 25px; 
                position:absolute; bottom:0; left:50%; transform:translateX(-50%);
                box-shadow:0 8px 25px rgba(0,0,0,0.1);
            ">
                <!-- 胸口发光 -->
                <div class="chest-glow" style="
                    position:absolute; top:10px; left:50%; 
                    width:45px; height:45px; 
                    background:radial-gradient(circle, #4CAF50 0%, #2E7D32 60%, transparent 100%);
                    border-radius:50%;
                "></div>
            </div>
            
            <!-- 手臂 -->
            <div style="position:absolute; bottom:20px; left:5px; width:25px; height:60px; background:linear-gradient(145deg,#e8e8e8,#d0d0d0); border-radius:12px; transform:rotate(15deg);"></div>
            <div style="position:absolute; bottom:20px; right:5px; width:25px; height:60px; background:linear-gradient(145deg,#e8e8e8,#d0d0d0); border-radius:12px; transform:rotate(-15deg);"></div>
        </div>
        
        <!-- 情绪显示 -->
        <div style="margin-top:20px; padding:15px; background:linear-gradient(135deg, #e8f5e9, #c8e6c9); border-radius:15px; text-align:center;">
            <div style="font-size:18px; font-weight:500; color:#2e7d32;">{face['desc']}</div>
            <div style="font-size:12px; color:#666; margin-top:5px;">点击数字人打招呼 👋</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    **✨ 我的超能力：**
    - 🧠 DeepSeek AI大脑
    - 😊 情绪表情变化  
    - 🗣️ 语音朗读回复
    - 💬 智能对话
    - 💡 暖心建议
    """)

with col2:
    st.markdown("### 💬 对话")
    
    # 聊天容器
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container" style="height:400px; overflow-y:auto; padding:10px; background:rgba(255,255,255,0.7); border-radius:20px; margin-bottom:15px;">', unsafe_allow_html=True)
        
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-msg">👤 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-msg">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 输入区域 - 支持回车换行
    st.markdown("""
    <div style="background:#f5f5f5; padding:15px; border-radius:20px; margin-bottom:15px;">
        <div style="font-size:12px; color:#888; margin-bottom:8px;">💡 按 Enter 发送，Shift+Enter 换行</div>
    </div>
    """, unsafe_allow_html=True)
    
    user_input = st.text_area(
        "输入消息...", 
        placeholder="说点什么吧... 😊\n可以换行输入长内容哦~",
        label_visibility="collapsed",
        height=100,
        key="input_area"
    )
    
    col_send, col_clear, col_speak_btn = st.columns([2, 1, 1])
    
    with col_send:
        if st.button("🚀 发送", use_container_width=True):
            if user_input.strip():
                st.session_state.messages.append({"role": "user", "content": user_input.strip()})
                emotion = detect_emotion(user_input)
                st.session_state.current_emotion = emotion
                
                with st.spinner("🤔 DeepSeek思考中..."):
                    response = get_deepseek_response(user_input, emotion)
                
                st.session_state.messages.append({"role": "bot", "content": response})
                
                # 语音朗读
                if st.session_state.auto_speak:
                    st.markdown(f'<script>speakText("{response.replace(chr(10), " ").replace('"', '\\"').replace("'", "\\'")}");</script>', unsafe_allow_html=True)
                
                st.rerun()
    
    with col_clear:
        if st.button("🗑️ 清空", use_container_width=True):
            st.session_state.messages = [
                {"role": "bot", "content": "你好呀！我是心灵伙伴 🌱\n\n我升级啦！现在我可以和你智能对话，还能开口说话！\n\n有什么想和我聊聊的吗？✨"}
            ]
            st.session_state.current_emotion = "neutral"
            st.rerun()
    
    with col_speak_btn:
        if st.button("🔊 朗读", use_container_width=True):
            if st.session_state.messages:
                last_bot_msg = None
                for msg in reversed(st.session_state.messages):
                    if msg["role"] == "bot":
                        last_bot_msg = msg["content"]
                        break
                if last_bot_msg:
                    st.markdown(f'<script>speakText("{last_bot_msg.replace(chr(10), " ").replace(chr(34), "\\"").replace(chr(39), "\\'")}");</script>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:20px; color:#666;">
    <p>💚 记住，你并不孤单。我一直在这里陪着你。</p>
    <p style="font-size:12px; margin-top:10px;">Powered by DeepSeek · 心灵伙伴</p>
</div>
""", unsafe_allow_html=True)
