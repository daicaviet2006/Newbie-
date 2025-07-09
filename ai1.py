import streamlit as st
import google.generativeai as genai
from textblob import TextBlob
import pandas as pd

# Thay API_KEY của bạn tại đây
#api

# Hàm gọi Gemini AI
def generate_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text if response.text else "Xin lỗi, tôi không thể trả lời lúc này."
    except Exception as e:
        return f"Lỗi: {str(e)}"


# Phân tích cảm xúc
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.5:
        return "Rất tích cực", polarity
    elif 0.1 < polarity <= 0.5:
        return "Tích cực", polarity
    elif -0.1 <= polarity <= 0.1:
        return "Trung lập", polarity
    elif -0.5 < polarity < -0.1:
        return "Tiêu cực", polarity
    else:
        return "Rất tiêu cực", polarity


# Gợi ý cách đối phó
def provide_coping_strategy(sentiment):
    strategies = {
        "Rất tích cực": "Hãy tiếp tục giữ vững tinh thần tích cực này nhé! Bạn có thể chia sẻ niềm vui với người khác.",
        "Tích cực": "Bạn đang có một tinh thần tốt! Hãy duy trì nó bằng cách làm những điều bạn thích.",
        "Trung lập": "Không sao cả nếu bạn cảm thấy bình thường. Hãy thử một hoạt động thú vị để cải thiện tâm trạng!",
        "Tiêu cực": "Có vẻ bạn đang cảm thấy hơi tệ. Hãy thử thư giãn bằng cách nghe nhạc hoặc đi dạo.",
        "Rất tiêu cực": "Tôi rất tiếc khi nghe điều đó. Hãy tâm sự với bạn bè hoặc tìm sự giúp đỡ từ chuyên gia tâm lý."
    }
    return strategies.get(sentiment, "Bạn hãy cố gắng giữ vững tinh thần nhé!")


# Hiển thị cảnh báo bảo mật
def display_disclaimer():
    st.sidebar.markdown("### ⚠️ Thông báo về quyền riêng tư")
    st.sidebar.markdown(
        "Ứng dụng này chỉ lưu trữ dữ liệu tạm thời trong suốt phiên làm việc của bạn. "
        "Vui lòng không chia sẻ thông tin cá nhân hoặc nhạy cảm."
    )


# Giao diện ứng dụng Streamlit
st.title("🧠 Trợ lý Hỗ trợ Tâm lý")

# Nút bắt đầu lại hội thoại
if st.button("🔄 Bắt đầu lại cuộc trò chuyện"):
    st.session_state["messages"] = []
    st.session_state["mood_tracker"] = []

# Khởi tạo bộ nhớ hội thoại
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "mood_tracker" not in st.session_state:
    st.session_state["mood_tracker"] = []

# Nhập tin nhắn
user_message = st.text_input("Bạn:", key="user_input")

# Xử lý tin nhắn khi gửi
if user_message:
    # Xóa hội thoại cũ để bắt đầu cuộc hội thoại mới
    st.session_state["messages"] = []
    st.session_state["mood_tracker"] = []

    # Phân tích cảm xúc và gợi ý
    sentiment, polarity = analyze_sentiment(user_message)
    coping_strategy = provide_coping_strategy(sentiment)

    # Gọi Gemini AI
    response = generate_response(user_message)

    # Lưu vào bộ nhớ
    st.session_state["messages"].append(("Bạn", user_message))
    st.session_state["messages"].append(("Bot", response))
    st.session_state["mood_tracker"].append((user_message, sentiment, polarity))

# Hiển thị tin nhắn
for sender, message in st.session_state["messages"]:
    st.text(f"{sender}: {message}")

# Hiển thị biểu đồ cảm xúc
if st.session_state["mood_tracker"]:
    mood_data = pd.DataFrame(st.session_state["mood_tracker"], columns=["Tin nhắn", "Cảm xúc", "Điểm số"])
    st.line_chart(mood_data["Điểm số"])

# Hiển thị gợi ý đối phó
if user_message:
    st.write(f"📌 **Gợi ý đối phó:** {coping_strategy}")

# Hiển thị tài nguyên hỗ trợ
st.sidebar.title("📞 Tài nguyên hỗ trợ")
st.sidebar.write("Nếu bạn cần trợ giúp ngay lập tức, vui lòng liên hệ:")
st.sidebar.write("1. 📞 Tổng đài hỗ trợ tâm lý VN: 1900 6233")
st.sidebar.write("2. 📲 Nhắn tin hỗ trợ: 111")
st.sidebar.write("[🔗 Thêm tài nguyên](https://www.mentalhealth.gov/get-help/immediate-help)")

# Hiển thị tổng kết phiên trò chuyện
if st.sidebar.button("📊 Xem tổng kết"):
    st.sidebar.write("### 📌 Tổng kết phiên trò chuyện")
    for i, (message, sentiment, polarity) in enumerate(st.session_state["mood_tracker"]):
        st.sidebar.write(f"{i + 1}. {message} - Cảm xúc: {sentiment} (Điểm số: {polarity})")

display_disclaimer()
