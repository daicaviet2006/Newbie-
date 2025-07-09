import speech_recognition
from gtts import gTTS
from openai import OpenAI
import pygame

client = OpenAI(
    #api
)

robot_ear = speech_recognition.Recognizer()
robot_brain = ""
pygame.mixer.init()

while True:
    with speech_recognition.Microphone() as mic:
        print("Robot: Tôi đang nghe ...")
        audio = robot_ear.listen(mic)
        print("Robot: ...")

    try:
        you = robot_ear.recognize_google(audio, language="vi-VN")
    except:
        you = ""

    print("You: " + you)

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "Bạn trả lời ngắn gọn xúc tích."},
                {"role": "user", "content": you}
            ],
            temperature=0.7,
            max_tokens=100
        )
        robot_brain = completion.choices[0].message.content
    except:
        robot_brain = "Tôi đang bận, vui lòng để lại lời nhắn"

    print("Robot: " + robot_brain)
    tts = gTTS(text=robot_brain, lang="vi")
    tts.save("voice.mp3")
    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
