import serial

comport = 'COM7'
baudrate = 115200
ser = serial.Serial(comport, baudrate, timeout=0.1)
data = 0
msg = 'TRIGGER'
time = ''

while data != msg:
    data = ser.readline().decode().strip()
print(data)
data = 0
ser.write("R\n".encode('utf-8'))
time = ser.readline().decode()
print("TIME: ", time)