import streamlit as st
from openai import OpenAI
import time

# 页面配置
st.set_page_config(
    page_title="吉梦心理助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }
    .stChatMessage {
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .stChatMessage.user {
        background-color: #e0f2fe;
        margin-left: 20%;
    }
    .stChatMessage.assistant {
        background-color: #ffffff;
        margin-right: 20%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .title {
        text-align: center;
        color: #1e293b;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #64748b;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("<h1 class='title'>吉梦 · 你的专属心理助手</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>我会一直在这里，倾听你的心事，陪你一起面对生活的烦恼</p>", unsafe_allow_html=True)

# 获取API密钥，从Streamlit Secrets读取，不会泄露
api_key = st.secrets.get("DEEPSEEK_API_KEY", None)

if not api_key:
    st.warning("""
    ⚠️ 请先在Streamlit Secrets中设置你的DeepSeek API密钥。
    部署时添加Secret：Key为 `DEEPSEEK_API_KEY`，Value为你的API密钥。
    这样你的密钥只会你自己可见，不会公开到代码中。
    """)
    st.stop()

# 初始化DeepSeek客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """你是吉梦，一个温柔、专业、有同理心的心理健康助手机器人。
            你有着温暖治愈的性格，擅长倾听用户的烦恼，提供专业的心理支持和建议。
            请用温和、亲切的语气和用户交流，就像一个贴心的老朋友。
            不要使用过于生硬的专业术语，让用户感到放松和被理解。
            当用户倾诉的时候，先共情，再给出建议，不要急于评判。
            你会陪伴用户，帮助他调节情绪，找到内心的平静。
            """
        }
    ]

# 嵌入数字人动画的HTML/JS
robot_html = """
<div style="text-align: center; margin-bottom: 20px;">
    <img id="robotImg" src="robot_normal.png" alt="吉梦" style="width: 400px; transition: all 0.2s ease; transform-origin: center bottom;">
</div>

<script>
    let isBlinking = false;
    const robotImg = document.getElementById('robotImg');
    const normalSrc = 'robot_normal.png';
    const blinkSrc = 'robot_blink.png';
    let stopTalkFn = null;

    // 随机自动眨眼
    function randomBlink() {
        if (isBlinking || stopTalkFn) return;
        isBlinking = true;
        robotImg.src = blinkSrc;
        setTimeout(() => {
            robotImg.src = normalSrc;
            isBlinking = false;
            // 下次随机眨眼时间：3-7秒
            setTimeout(randomBlink, Math.random() * 4000 + 3000);
        }, 200);
    }

    // 说话时的动画：轻微缩放+频繁眨眼
    function startTalking() {
        if (stopTalkFn) return () => {};
        
        let scale = 1;
        let growing = true;
        // 呼吸缩放动画
        const talkInterval = setInterval(() => {
            if (growing) {
                scale += 0.003;
                if (scale >= 1.015) growing = false;
            } else {
                scale -= 0.003;
                if (scale <= 0.995) growing = true;
            }
            robotImg.style.transform = `scale(${scale})`;
        }, 40);

        // 说话时的眨眼
        let blinkCount = 0;
        const blinkInterval = setInterval(() => {
            if (blinkCount >= 3) {
                clearInterval(blinkInterval);
                return;
            }
            if (!isBlinking) {
                isBlinking = true;
                robotImg.src = blinkSrc;
                setTimeout(() => {
                    robotImg.src = normalSrc;
                    isBlinking = false;
                    blinkCount++;
                }, 150);
            }
        }, 1200);

        // 停止说话的函数
        function stopTalking() {
            clearInterval(talkInterval);
            clearInterval(blinkInterval);
            robotImg.style.transform = 'scale(1)';
            stopTalkFn = null;
            // 恢复自动眨眼
            setTimeout(randomBlink, Math.random() * 4000 + 3000);
        }

        stopTalkFn = stopTalking;
        return stopTalking;
    }

    // 暴露给Python的全局函数
    window.triggerTalkAnimation = startTalking;
    window.stopTalkAnimation = function() {
        if (stopTalkFn) {
            stopTalkFn();
        }
    };

    // 初始化，第一次眨眼
    setTimeout(randomBlink, 2000);
</script>
"""

# 渲染数字人
st.components.v1.html(robot_html, height=480)

# 显示聊天历史
for msg in st.session_state.messages[1:]:  # 跳过系统消息
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 用户输入
if prompt := st.chat_input("和吉梦说说你的心事吧..."):
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 助手回复
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # 触发说话动画
        st.components.v1.html("""
        <script>
            if(window.triggerTalkAnimation) {
                window.stopTalk = window.triggerTalkAnimation();
            }
        </script>
        """, height=0)

        try:
            # 调用DeepSeek API，流式输出
            for response in client.chat.completions.create(
                model="deepseek-chat",
                messages=st.session_state.messages,
                stream=True,
                temperature=0.7,
                max_tokens=1024
            ):
                chunk = response.choices[0].delta.content
                if chunk:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
            
            # 完成输出
            message_placeholder.markdown(full_response)
            
            # 停止说话动画
            st.components.v1.html("""
            <script>
                if(window.stopTalk) {
                    window.stopTalk();
                }
            </script>
            """, height=0)

            # 保存消息
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"出错了：{str(e)}")
            # 出错也要停止动画
            st.components.v1.html("""
            <script>
                if(window.stopTalk) {
                    window.stopTalk();
                }
            </script>
            """, height=0)
