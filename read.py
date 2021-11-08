import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pytesseract

img=Image.open('out.png')
img=img.crop(box=(220,40,330,80))
np_img = np.array(img)

plt.imshow(np_img)
plt.show()

print(np_img.shape)
np_img[np_img.min(axis=2)<100]=0
np_img[np_img.min(axis=2)>=100]=255
np_img=255-np_img
img=Image.fromarray(np_img)

plt.imshow(np_img)
plt.show()

#img.
text=pytesseract.image_to_string(img)
print(text)
img.close()
