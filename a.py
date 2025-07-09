import streamlit as st
import google.generativeai as genai
from textblob import TextBlob
import pandas as pd

# Thay thế bằng API key của Google Gemini
#api

# Hàm gọi API Gemini để tạo phản hồi
def generate_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi khi gọi API Gemini: {str(e)}"

# Hàm phân tích cảm xúc
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.5:
        return "Very Positive", polarity
    elif 0.1 < polarity <= 0.5:
        return "Positive", polarity
    elif -0.1 <= polarity <= 0.1:
        return "Neutral", polarity
    elif -0.5 < polarity < -0.1:
        return "Negative", polarity
    else:
        return "Very Negative", polarity

# Hàm đưa ra chiến lược đối phó
def provide_coping_strategy(sentiment):
    strategies = {
        "Very Positive": "Hãy tiếp tục giữ vững tinh thần tích cực!",
        "Positive": "Hãy làm những điều khiến bạn vui vẻ và hạnh phúc.",
        "Neutral": "Bạn có thể thử một số hoạt động thư giãn như nghe nhạc hoặc đi dạo.",
        "Negative": "Hãy dành thời gian nghỉ ngơi và chăm sóc bản thân.",
        "Very Negative": "Hãy tìm kiếm sự giúp đỡ từ bạn bè hoặc chuyên gia tâm lý nếu cần."
    }
    return strategies.get(sentiment, "Luôn giữ vững tinh thần, bạn không cô đơn!")

# Hiển thị ứng dụng Streamlit
st.title("Mental Health Support Chatbot")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'mood_tracker' not in st.session_state:
    st.session_state['mood_tracker'] = []

with st.form(key='chat_form'):
    user_message = st.text_input("Bạn: ")
    submit_button = st.form_submit_button(label='Gửi')

if submit_button and user_message:
    st.session_state['messages'].append(("Bạn", user_message))

    sentiment, polarity = analyze_sentiment(user_message)
    coping_strategy = provide_coping_strategy(sentiment)

    response = generate_response(user_message)

    st.session_state['messages'].append(("Bot", response))
    st.session_state['mood_tracker'].append((user_message, sentiment, polarity))

for sender, message in st.session_state['messages']:
    st.text(f"{sender}: {message}")

# Hiển thị biểu đồ theo dõi tâm trạng
if st.session_state['mood_tracker']:
    mood_data = pd.DataFrame(st.session_state['mood_tracker'], columns=["Message", "Sentiment", "Polarity"])
    st.line_chart(mood_data['Polarity'])

# Hiển thị chiến lược đối phó
if user_message:
    st.write(f"Chiến lược đối phó gợi ý: {coping_strategy}")

st.sidebar.title("Nguồn trợ giúp")
st.sidebar.write("Nếu bạn cần hỗ trợ khẩn cấp, vui lòng liên hệ:")
st.sidebar.write("1. Tổng đài hỗ trợ tâm lý Việt Nam: 1900 6233")
st.sidebar.write("2. Đường dây nóng hỗ trợ sức khỏe tâm thần: 024 7307 8999")
st.sidebar.write("[Thêm thông tin tại đây](https://www.mentalhealth.gov/get-help/immediate-help)")

# Hiển thị tóm tắt phiên làm việc
if st.sidebar.button("Xem tổng kết phiên"):
    st.sidebar.write("### Tổng kết phiên")
    for i, (message, sentiment, polarity) in enumerate(st.session_state['mood_tracker']):
        st.sidebar.write(f"{i + 1}. {message} - Cảm xúc: {sentiment} (Độ phân cực: {polarity})")
