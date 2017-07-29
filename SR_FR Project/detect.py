import math
import cv2
import config


# given an image with the dimensions of face and eyes, return the face in leveled position
def levelFace(image, face):
    ((x, y, w, h), eyedim) = face
    if len(eyedim) != 2:
        # only rotate the face if there are two eyes found
        return image[y:y+h, x:x+w]

    leftx = eyedim[0][0]
    lefty = eyedim[0][1]
    rightx = eyedim[1][0]
    righty = eyedim[1][1]
    if leftx > rightx:
        leftx, rightx = rightx, leftx
        lefty, righty = righty, lefty
    if lefty == righty or leftx == rightx:
        return image[y:y+h, x:x+w]

    rotDeg = math.degrees(math.atan((righty - lefty) / float(rightx - leftx)))
    if abs(rotDeg) < 20:
        rotMat = cv2.getRotationMatrix2D((leftx, lefty), rotDeg, 1)
        rotImg = cv2.warpAffine(image, rotMat, (image.shape[1], image.shape[0]))
        return rotImg[y:y+h, x:x+w]

    return image[y:y+h, x:x+w]


def detectFaces(image, faceCascade, eyeCascade=None, returnGray=True):
    cas_rejectLevel = 1.3
    cas_levelWeight = 5

    # Convert color input image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #
    # Detect faces using grayscale images and XML Files
    #
    faces = faceCascade.detectMultiScale(gray, cas_rejectLevel, cas_levelWeight)

    # If faces are found
    result = []
    for (x, y, w, h) in faces:
        eyes = []
        if eyeCascade != None:
            roi_gray = gray[y:y+h, x:x+w]
            eyes = eyeCascade.detectMultiScale(roi_gray)

        result.append(((x, y, w, h), eyes))

    if returnGray:
        return gray, result
    else:
        return image, result


if __name__ == '__main__':
    path = "/Users/Mohamad/AUT/B.Sc. Thesis/SR_FR Project/high-res.png"

    # cv2.namedWindow("camera", 1)
    # capture = cv2.VideoCapture(0)

    # To improve performance, can specify a lower resolution. e.g. 320x240
    # width = 3
    # height = 4

    # ADD CASCADES
    haarFaceCascade = cv2.CascadeClassifier(config.HAAR_FACE_CASCADE_FILE)
    haarEyeCascade = cv2.CascadeClassifier(config.HAAR_EYE_CASCADE_FILE)
    lbpFaceCascade = cv2.CascadeClassifier(config.LBP_FACE_CASCADE_FILE)


    # if width is None:
    #     width = int(path.get(cv2.CAP_PROP_FRAME_WIDTH))
    # else:
    #     path.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    #
    # if height is None:
    #     height = int(path.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # else:
    #     path.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # result = np.zeros((height, width, 3), np.uint8)

    # while True:
    # retval, img = capture.read()
    haar_img = cv2.imread(path)
    lbp_img = cv2.imread(path)

    # HAAR Cascade
    haar_image, face_dim = detectFaces(haar_img, haarFaceCascade, haarEyeCascade, False)
    for ((x, y, w, h), eye_dim) in face_dim:
        cv2.rectangle(haar_image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        for (ex, ey, ew, eh) in eye_dim:
            cv2.rectangle(haar_image, (ex+x, ey+y), (ex+x+ew, ey+y+eh), (0, 255, 0), 2)

    # LBP Cascade
    lbp_image, face_dim = detectFaces(lbp_img, lbpFaceCascade, None, False)
    for ((x, y, w, h), eye_dim) in face_dim:
        cv2.rectangle(lbp_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        for (ex, ey, ew, eh) in eye_dim:
            cv2.rectangle(lbp_image, (ex+x, ey+y), (ex+x+ew, ey+y+eh), (0, 255, 0), 2)

    # cv2.imshow("camera", image)
    cv2.imwrite("Resources/Detected/image_0001_haar_detected.jpg", haar_image)
    cv2.imwrite("Resources/Detected/image_0001_lbp_detected.jpg", lbp_image)
    # if cv2.waitKey(30) & 0xFF == ord('q'):
        # break

    # capture.release()
    # cv2.destroyAllWindows()
