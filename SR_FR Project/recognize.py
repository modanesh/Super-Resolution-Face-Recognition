import cv2
import train
import detect
import config


# TODO 1: threshold
# TODO 2: eigenfaces vs. fisherfaces vs. LBPH


def recognizeFace(image, faceCascade, eyeCascade, faceSize, threshold, recognizer):
    found_faces = []

    gray, faces = detect.detectFaces(image, faceCascade, eyeCascade, returnGray=1)

    # If faces are found, try to recognize them
    for ((x, y, w, h), eyedim) in faces:
        # confidence formula: distance = 1.0f - sqrt( distSq / (float)(nTrainFaces * nEigens) ) / 255.0f
        label, confidence = recognizer.predict(cv2.resize(detect.levelFace(gray, ((x, y, w, h), eyedim)), faceSize))
        print "label"
        print label


        # note that for some distributions of python-opencv, the predict function
        # returns the label only.
        #label = recognizer.predict(cv2.resize(detect.levelFace(gray, ((x, y, w, h), eyedim)), faceSize))
        #confidence = -1
        # if confidence < threshold:
        found_faces.append((label, confidence, (x, y, w, h)))


    return found_faces


def prepareImage(filename, FEDetector, cascadeDetector):
    haarFaceCascade = cv2.CascadeClassifier(config.HAAR_FACE_CASCADE_FILE)
    lbpFaceCascade = cv2.CascadeClassifier(config.LBP_FACE_CASCADE_FILE)
    haarEyeCascade = cv2.CascadeClassifier(config.HAAR_EYE_CASCADE_FILE)
    faceSize = config.DEFAULT_FACE_SIZE
    threshold = 500

    recognizer = train.trainRecognizer('Train Set', FEDetector, cascadeDetector, faceSize, showFaces=True)
    print "recognizer"
    print cascadeDetector
    print FEDetector

    # cv2.namedWindow("camera", 1)
    # capture = cv2.VideoCapture(0)
    # path = "/Users/Mohamad/AUT/B.Sc. Thesis/SR_FR Project/Resources/Test Set/image_0022.jpg"
    path = filename

    # while True:
    # retval, img = capture.read()
    haar_img = cv2.imread(path)
    lbp_img = cv2.imread(path)

    if cascadeDetector == "1":
        # HAAR CASCADE
        for (label, confidence, (x, y, w, h)) in recognizeFace(haar_img, haarFaceCascade, haarEyeCascade, faceSize, threshold, recognizer):
            cv2.rectangle(haar_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(haar_img, "{} = {}".format(recognizer.getLabelInfo(label), int(confidence)), (x, y),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.imwrite("Resources/Recognized/haar_recognized.jpg", haar_img)
        recognizedPath = "/Users/Mohamad/AUT/B.Sc. Thesis/SR_FR Project/Resources/Recognized/haar_recognized.jpg"
        return recognizedPath
    elif cascadeDetector == "2":
        # LBP CASCADE
        for (label, confidence, (x, y, w, h)) in recognizeFace(lbp_img, lbpFaceCascade, None, faceSize, threshold, recognizer):
            cv2.rectangle(lbp_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(lbp_img, "{} = {}".format(recognizer.getLabelInfo(label), int(confidence)), (x, y),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.imwrite("Resources/Recognized/lbp_recognized.jpg", lbp_img)
        recognizedPath = "/Users/Mohamad/AUT/B.Sc. Thesis/SR_FR Project/Resources/Recognized/lbp_recognized.jpg"
        return recognizedPath


if __name__ == '__main__':
    prepareImage("/Users/Mohamad/AUT/B.Sc. Thesis/SR_FR Project/high-res.png", "1", "1")
