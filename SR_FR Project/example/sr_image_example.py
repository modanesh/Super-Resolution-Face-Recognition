from PIL import Image
from sr_factory.sr_image_factory import SRImageFactory

def LRImage_example(path):
    print "6.1"
    image = Image.open(path)
    print "6.2"
    sr_image = SRImageFactory.create_sr_image(image)
    print "6.3"
    reconstructed_sr_image = sr_image.reconstruct(4, 'iccv09')
    print "6.4"
    reconstructed_sr_image.save("/Users/Mohamad/AUT/B.Sc. Thesis/SR_FR Project/high-res.png", "png")
    print "6.5"


if __name__ == '__main__':
    LRImage_example("/Users/Mohamad/AUT/B.Sc. Thesis/SR_FR Project/Lenna.png")
