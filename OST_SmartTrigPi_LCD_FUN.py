import time
import socket
import SCPIParser as parse
import lgpio
import board
import digitalio
from adafruit_rgb_display.st7789 import ST7789
from PIL import Image, ImageDraw

def main():
    HOST = '0.0.0.0'
    PORT = 50007
    baud = 24000000
    width = 240
    height = 240
    IDNRESPONSE = 'OST CUSTOM TECHNOLOGY,SMARTTRIG,000001,0.1'

    
    trigChannel1 = 4
    trigChannel2 = 17
    heartBeatChannel = 18
    levelSelect = 26 #LOW = 5Vout HIGH = 3V3OUT
    transmitSelect = 25 #LOW = HiZ HIGH = Tranmission

    button1 = 21
    button2 = 20
    button3 = 13
    button4 = 16

    spiMiso = 21
    spiMosi = 19
    spiClk = 23
    #spics0 = 24
    spics1 = 26
    
    #ldcDC = 15
    lcdBL = 12
    lcdTE = 27
    #lcdRST = 14

    spics0 = digitalio.DigitalInOut(board.D24)
    ldcDC = digitalio.DigitalInOut(board.D15)
    lcdRST  = digitalio.DigitalInOut(board.D14)

    inpChannelList = [button1, button2, button3, button4]
    outChannelList = [trigChannel1, trigChannel2, heartBeatChannel, levelSelect, transmitSelect, lcdBL, lcdTE] #TBD

    chip = gpioSetup(inL = inpChannelList, outL = outChannelList)
    spi = board.SPI() # spiSetup(0, 0, baud = baud)

    disp = ST7789(spi, height=240, y_offset=80, rotation=180, cs=spics0, dc= ldcDC, rst=lcdRST,  baudrate=baud)
    image = Image.new("RGB", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image)

    image = imgResize("/mnt/usb/bees.jpg", width=width, height=height)
    disp.image(image)

    lgpio.gpio_write(chip, lcdBL, 1)

    frequency = 1.5
    duty = 70
    lgpio.tx_pwm(chip, heartBeatChannel, frequency, duty, 0, 0)

    s = networkSetup(HOST,PORT)
    s.listen()
    print('Server Listening on', PORT)

   
    try:
        while True:
            conn, addr = s.accept()
            with conn:
                print("Connection recieved")
                data = conn.recv(512)
                cmd = data.decode().strip()                
                parser = parse.SCPIParser({
                    "*TRG": lambda *args: trigger(chip = chip, channel = trigChannel1, conn = conn, heartBeatChannel = heartBeatChannel),
                    "*IDN?" : lambda *args: identify(conn = conn, IDNRESPONSE = IDNRESPONSE)
                })
                parser.execute(cmd)
            
    except KeyboardInterrupt:
        closeConnection(s)
        closeGPIO(chip, inpChannelList[0], outChannelList[0], disp)
        print('Interrupted: Closed Successfully')
    return

def gpioSetup(inL, outL):
    chip = lgpio.gpiochip_open(0)
    lgpio.group_claim_input(chip, inL)
    lgpio.group_claim_output(chip, outL)

    return chip

def networkSetup(host: str, port: int):
    s = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    return s    

def spiSetup(device, channel, baud, spi_flags = 0):
    spi = lgpio.spi_open(device, channel, baud, spi_flags)
    return spi

def closeGPIO(chip, leaderIn, leaderOut, disp):
    lgpio.group_free(chip, leaderIn)
    lgpio.group_free(chip, leaderOut)
    lgpio.gpiochip_close(chip)
    image = Image.new("RGB", (240, 240))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 240, 240), outline=0, fill=(0, 0, 0))
    disp.image(image)


def imgResize(name, width, height):
    image = Image.open(name)
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))
    return image

def closeConnection(s):
    s.close()

def identify(conn, IDNRESPONSE):
    conn.sendall(IDNRESPONSE.encode())


def trigger(chip, channel, conn, heartBeatChannel): 
    lgpio.gpio_write(chip, channel, 1)
    lgpio.tx_pwm(chip, heartBeatChannel, 12, 30,0,0)
    time.sleep(.25)
    conn.sendall(b'Triggering')
    lgpio.tx_pwm(chip, heartBeatChannel, 1.5, 70,0,0)
    lgpio.gpio_write(chip, channel, 0)

if __name__ == "__main__":
    main()

