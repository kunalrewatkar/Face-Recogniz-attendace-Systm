import face_recognition
import numpy as np
import cmake
from datetime import datetime
import csv
import cv2

video_capture = cv2.VideoCapture(0)
#loading Known Faces

kunal_images = face_recognition.load_image_file("faces/kunal.jpeg")
kunal_encodings = face_recognition.face_encodings(kunal_images)[0]

vansh_images = face_recognition.load_image_file("faces/vansh.jpg")
vansh_encodings = face_recognition.face_encodings(vansh_images)[0]

vedant_images = face_recognition.load_image_file("faces/vedant.jpg")
vedant_encodings = face_recognition.face_encodings(vedant_images)[0]

vivek_images = face_recognition.load_image_file("faces/Vivek.jpg")
vivek_encodings = face_recognition.face_encodings(vivek_images)[0]

known_faces_encodings = [kunal_encodings,vansh_encodings,vedant_encodings,vivek_encodings]
known_faces_names = ["kunal","vansh","vedant","vivek"]

students = known_faces_names.copy()

face_locations = []
face_encodings = []

# Get the current date and time

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.15, fy=0.15)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Recognise faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_faces_encodings, face_encoding)
        face_distance = face_recognition.face_distance(known_faces_encodings, face_encoding)
        best_match_index = np.argmin(face_distance)

        if (matches[best_match_index]):
            name = known_faces_names[best_match_index]

            # Add the text if a person is present
            if name in known_faces_names:
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10, 100)
                fontScale = 1.5
                fontColor = (255, 0, 0)
                thickness = 3
                lineType = 2
                cv2.putText(frame, name + " Present", bottomLeftCornerOfText, font, fontScale, fontColor, thickness,   lineType)

                if name in students:
                    students.remove(name)
                    current_time = now.strftime("%H:%M:%S")
                    lnwriter.writerow([name, current_time])

    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
