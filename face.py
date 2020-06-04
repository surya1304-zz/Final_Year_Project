import face_recognition

face_encoding = []
name = []

k = face_recognition.load_image_file("PRAANNAVIKA_LEFT.jpg")
l = face_recognition.face_encodings(k, num_jitters=100)
print(l)
face_encoding.append(l)
name.append("PRAANNAVIKA_LEFT")

print(len(name))
