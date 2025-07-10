import time
import socket
import SCPIParser as parse
import lgpio
import board
import digitalio
import errno
from adafruit_rgb_display.st7789 import ST7789
from PIL import Image, ImageDraw, ImageFont

def main():
    HOST = '0.0.0.0'
    PORT = 50007
    baud = 24000000
    triggerLength = [0.25]
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

    disp = ST7789(spi, height=240, y_offset=80, rotation=270, cs=spics0, dc=ldcDC, rst=lcdRST,  baudrate=baud)
    image = Image.new("RGB", (width, height))
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 60)

    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill="#000000")
    disp.image(image)

    image = imgResize("/home/raspberry/Desktop/trig.jpg", width=width, height=height)
    draw = ImageDraw.Draw(image)    
    draw.text((0, 0), "READY", font=font, fill="#FF0000")
    disp.image(image)

    lgpio.gpio_write(chip, lcdBL, 1)
    lgpio.gpio_write(chip, transmitSelect, 1)
    lgpio.gpio_write(chip, levelSelect, 0)


    frequency = 1.5
    duty = 70
    lgpio.tx_pwm(chip, heartBeatChannel, frequency, duty, 0, 0)

    s = networkSetup(HOST,PORT)
    s.listen()
    print('Server Listening on', PORT)

   
    try:
        while True:
            try:
                localAlert = lgpio.gpio_read(chip, button1)
                if localAlert:
                    time.sleep(.25)
                    image = imgResize("/home/raspberry/Desktop/trig.jpg", width=width, height=height)
                    draw = ImageDraw.Draw(image)
                    draw.text((0, 0), "LOCAL", font=font, fill="#FF0000")
                    disp.image(image)
                    setMode("local", chip=chip, button1=button1, button2=button2, trigChannel=trigChannel1, heartBeatChannel=heartBeatChannel, disp=disp)
                else:
                    conn, addr = s.accept()
                    setMode("remote", conn=conn, addr=addr, triggerLength=triggerLength, chip=chip, trigChannel=trigChannel1, 
                        levelSelect=levelSelect, heartBeatChannel=heartBeatChannel, draw=draw, disp=disp, IDNRESPONSE=IDNRESPONSE)
            except socket.error as e:
                if e.errno != errno.EWOULDBLOCK:
                    print(f"Socket Error: {e}")
                else:
                    pass

    except KeyboardInterrupt:
        closeConnection(s)
        closeGPIO(chip=chip, leaderIn=inpChannelList[0], leaderOut=outChannelList[0], lcdBL=lcdBL, disp=disp)
        print('Interrupted: Closed Successfully')
    return

def gpioSetup(inL, outL):
    chip = lgpio.gpiochip_open(0)
    lgpio.group_claim_output(chip, outL)
    lgpio.group_claim_input(chip, inL)    
    return chip

def networkSetup(host: str, port: int):
    s = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.setblocking(False)
    return s    

def spiSetup(device, channel, baud, spi_flags = 0):
    spi = lgpio.spi_open(device, channel, baud, spi_flags)
    return spi

def closeGPIO(chip, leaderIn, leaderOut, lcdBL, disp):
    lgpio.gpio_write(chip, 18, 0)
    lgpio.group_free(chip, leaderIn)
    lgpio.group_free(chip, leaderOut)
    lgpio.gpio_write(chip, lcdBL, 0)
    lgpio.gpiochip_close(chip)
    image = Image.new("RGB", (240, 240))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 240, 240), outline=0, fill="#000000")

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

def setMode(type ,conn = None, addr = None, triggerLength = None, chip = None, button1 = None, button2 = None, trigChannel = None, 
            levelSelect = None, heartBeatChannel = None, draw = None, disp = None, IDNRESPONSE = None):
    if type == "local":
        localCtrl(chip=chip, button1=button1, button2 = button2, heartBeatChannel=heartBeatChannel, trigChannel = trigChannel, disp=disp)
    elif type == "remote":
        remoteCtrl(conn=conn, addr=addr, triggerLength=triggerLength, chip=chip, trigChannel=trigChannel, draw=draw,
                   levelSelect=levelSelect, heartBeatChannel=heartBeatChannel, disp=disp, IDNRESPONSE=IDNRESPONSE)

def localCtrl(chip, button1, button2, trigChannel, heartBeatChannel, disp):
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 60)
    while True:
        localToggle = lgpio.gpio_read(chip, button1)
        localTrig = lgpio.gpio_read(chip, button2)
        if localToggle:
            image = imgResize("/home/raspberry/Desktop/bees.jpg", width=240, height=240)
            draw = ImageDraw.Draw(image)
            draw.text((0, 0), "READY", font=font, fill="#FF0000")
            disp.image(image)
            time.sleep(.5)
            return
        if localTrig:
            trigger(0.25, chip=chip, channel=trigChannel, heartBeatChannel=heartBeatChannel, disp=disp)
            time.sleep(1)
            image = imgResize("/home/raspberry/Desktop/bees.jpg", width=240, height=240)
            draw = ImageDraw.Draw(image)    
            draw.text((0, 0), "READY", font=font, fill="#FF0000")
            disp.image(image)
            return

def remoteCtrl(triggerLength, chip, trigChannel, levelSelect, conn, addr, heartBeatChannel, disp, draw, IDNRESPONSE):
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 60)

    with conn:
        print("Connection recieved")
        data = conn.recv(512)
        cmd = data.decode().strip()                
        parser = parse.SCPIParser({
            "*TRG": lambda *args: trigger(triggerLength = triggerLength[0], chip = chip, channel = args[0], conn = conn, heartBeatChannel = heartBeatChannel, disp = disp),
            "*IDN?" : lambda *args: identify(conn = conn, IDNRESPONSE = IDNRESPONSE),
            "PULS:WIDT": lambda *args: setPulse(triggerLength=triggerLength, newWidth=args[0], conn=conn),
            "VOLT": lambda *args: setVolt(chip=chip, levelSelect=levelSelect, voltMessage=args[0], conn=conn)
        })
        parser.execute(cmd)
    image = imgResize("/home/raspberry/Desktop/bees.jpg", width=240, height=240)
    draw = ImageDraw.Draw(image)    
    draw.text((0, 0), "READY", font=font, fill="#FF0000")
    disp.image(image)
    return


def closeConnection(s):
    s.close()

def identify(conn, IDNRESPONSE):
    conn.sendall(IDNRESPONSE.encode())


def trigger(triggerLength, chip, channel, heartBeatChannel, disp, conn = None): 
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 60)

    image = Image.new("RGB", (240, 240))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 240, 240), outline=0, fill="#000000")
    
    padding = -2
    x = 0
    y = padding
    draw.text((x, y), "Trigger", font=font, fill="#FFFFFF")
    bbox = font.getbbox("Trigger Length")
    height = bbox[3] - bbox[1]
    x = 0
    y += height
    draw.text((x, y), "Length:", font=font, fill="#FFFFFF")
    x = 0
    y += height
    draw.text((x, y), str(triggerLength), font=font, fill="#FFFFFF")

    disp.image(image)
    
    lgpio.gpio_write(chip, channel, 1)
    lgpio.tx_pwm(chip, heartBeatChannel, 12, 20,0,0)
    
    time.sleep(triggerLength)

    if conn:
        conn.sendall(b'Triggering')
    lgpio.tx_pwm(chip, heartBeatChannel, 1.5, 70,0,0)
    lgpio.gpio_write(chip, channel, 0)

    return triggerLength

def setPulse(triggerLength, newWidth, conn = None):
    triggerLength[0] = newWidth
    if conn:
        conn.sendall(f'Pulse Set at {newWidth}'.encode())

def setVolt(chip, levelSelect, voltMessage, conn = None):
    if conn and voltMessage == 3.3:
        lgpio.gpio_write(chip, levelSelect, 1)
        conn.sendall(f'Volt Set at {voltMessage}'.encode())

    elif conn and voltMessage == 5:
        lgpio.gpio_write(chip, levelSelect, 0)
        conn.sendall(f'Volt Set at {voltMessage}'.encode())
    elif conn:
        conn.sendall(f'Invalid Voltage -> Logic set to 5V'.encode())

if __name__ == "__main__":
    main()

