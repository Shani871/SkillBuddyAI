import cv2
from deepface import DeepFace
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators import gzip
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load Google Gemini API Key
genai.configure(api_key=os.getenv("AIzaSyDmZZR-GpCrnLjRz62PcxHqClsd1eWZffE"))


class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        if not self.video.isOpened():
            raise RuntimeError("Error: Could not open webcam.")
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        if not ret:
            return None  # Skip processing if no frame

        # Convert frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=6, minSize=(30, 30))

        detected_emotion = "Neutral"

        for (x, y, w, h) in faces:
            face_roi = frame[y:y + h, x:x + w]  # Extract BGR face region

            try:
                result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
                detected_emotion = result[0].get('dominant_emotion', 'Unknown') if result else 'No face detected'
            except Exception as e:
                print("Error analyzing face:", e)
                detected_emotion = "Error"

            # Draw rectangle around the face and add emotion text
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, detected_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Convert processed frame to JPEG format
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes(), detected_emotion


def gen(camera):
    """Generate a video frame stream."""
    while True:
        frame, emotion = camera.get_frame()
        if frame:  # Only send valid frames
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@login_required(login_url='login')
@gzip.gzip_page
def video_feed(request):
    """Django view to serve the video feed."""
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace; boundary=frame")
    except RuntimeError as e:
        print("Error streaming video:", e)
        return None


def chatbot_response(request):
    """Django view to return chatbot response based on emotion."""
    detected_emotion = request.GET.get("emotion", "neutral")

    # Define emotion-based prompts
    prompts = {
        "happy": "I see that you're happy! Would you like a fun fact, a joke, or a motivational quote?",
        "sad": "You seem sad. I'm here for you. Do you want to hear something uplifting or get some advice?",
        "angry": "You seem upset. Do you want some stress-relief tips or a relaxation exercise?",
        "surprised": "Wow, you look surprised! Want to talk about something exciting?",
        "neutral": "Just chilling? How about a random fun fact or an interesting topic?"
    }

    # Select prompt based on detected emotion
    user_input = prompts.get(detected_emotion.lower(), "How can I assist you today?")

    # Get response from Google Gemini API
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(user_input)

    return JsonResponse({"emotion": detected_emotion, "response": response.text})