# # 1.
# import qrcode

# img = qrcode.make('This is my QR code!')
# print(type(img))  # qrcode.image.pil.PilImage
# img.save("qrcode_1.png")


# # 2.
# import pyqrcode
# import png
# from pyqrcode  import QRCode
# QRstring = "This is my QR code!"
# url = pyqrcode.create(QRstring)
# url.png('qrcodeYT.png', scale=8)
