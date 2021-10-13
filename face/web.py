import face_recognition
from flask import Flask, jsonify, request, redirect
import numpy as np

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

bruno_image = face_recognition.load_image_file("bruno.png")
bruno_face_encoding = face_recognition.face_encodings(bruno_image)[0]

renan_image = face_recognition.load_image_file("renan.png")
renan_face_encoding = face_recognition.face_encodings(renan_image)[0]

obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>API Reconhecimento Facial</title>
    <h1>Envie sua foto!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''


def detect_faces_in_image(file_stream):
    # Pre-calculated face encoding of Obama generated with face_recognition.face_encodings(img)
    
    known_face_encoding = [
        renan_face_encoding,
        bruno_face_encoding,
        obama_face_encoding
    ]
    known_face_names = [
        "Renan",
        "Bruno Bach",
        "Obama"
    ]
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)
    print(unknown_face_encodings)
    face_found = False
    is_bruno = False


    matches = face_recognition.compare_faces(known_face_encoding, unknown_face_encodings[0])
    name = "Unknown"
    face_distances = face_recognition.face_distance(known_face_encoding, unknown_face_encodings[0])
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_face_names[best_match_index]
    
    print(name)
    if len(unknown_face_encodings) > 0:
        face_found = True
        
        # See if the first face in the uploaded image matches the known face of Obama
    match_results = face_recognition.compare_faces([bruno_face_encoding], unknown_face_encodings[0])
    if match_results[0]:
        is_bruno = True

    # Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_bruno": is_bruno,
        "name": name
  
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)