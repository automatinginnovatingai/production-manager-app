from PIL import Image

img = Image.open("tools/automating_innovating_ai_photo.jpg")
img.save("photo.ico", format='ICO', sizes=[(256, 256)])