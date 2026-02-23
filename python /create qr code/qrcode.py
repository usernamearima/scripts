import qrcode # pip install qrcode

url = input('enter the url: ').strip()
file_path = 'C:\\Users\\user\\Downloads\\qrcode.png'

qr = qrcode.QRCode()
qr.add_data(url)

img = qr.make_image()
img.save(file_path)

print(f'QR Code saved to {file_path}')
