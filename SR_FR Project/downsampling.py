import cv2
import os


# path = "/Users/Mohamad/AUT/B.Sc. Thesis/SR_FR Project/Resources/Downsampled/"
path = "/Users/Mohamad/AUT/B.Sc. Thesis/SR_FR Project/"
for filename in os.listdir(path):
    if filename.endswith("Lenna.png"):
        fullPath = os.path.join(path, filename)
        inImg = cv2.imread(fullPath)

        inImgH, inImgW = inImg.shape[:2]

        # Downsampling and Gaussian Blur 1
        downInImg = cv2.pyrDown(inImg, dstsize = (int(inImgW / 2), int(inImgH / 2)))
        # blurredInImg = cv2.GaussianBlur(downInImg, (5, 5), 1, 1)

        blurredInImgH, blurredInImgW = downInImg.shape[:2]

        # Downsampling and Gaussian Blur 2
        downX2InImage = cv2.pyrDown(downInImg, dstsize = (int(blurredInImgW / 2), int(blurredInImgH / 2)))
        # blurredDownX2InImage = cv2.GaussianBlur(downX2InImage, (5, 5), 1, 1)

        newFilename = "downsampled_" + filename

        cv2.imwrite(os.path.join(path, newFilename), downX2InImage)
        continue