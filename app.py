import streamlit as st
from openai import OpenAI

st.title("ChatGPT 연동 챗봇")

# OpenAI API key 
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"


# 챗봇 채팅 내역 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("채팅을 입력하세요."):
    # 사용자 메시지를 채팅 기록에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 사용자 메시지를 채팅 메시지 컨테이너에 표시
    with st.chat_message("user"):
        st.markdown(prompt)

    # 어시스턴트 응답을 채팅 메시지 컨테이너에 표시
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})