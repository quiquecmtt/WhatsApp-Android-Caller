from ppadb.client import Client
from ppadb.device import Device
import time
from multiprocessing import Process
import multiprocessing as mp
import os, cv2, sys
import numpy as np

def tap_call_icon(device):
    method = cv2.TM_SQDIFF_NORMED
    icon_gray = cv2.cvtColor(cv2.imread(os.path.dirname(__file__) + "/videocall_icon.png"), cv2.COLOR_BGR2GRAY)
    top_pad, down_pad, left_pad, right_pad = 75, 200, 0, -1
    while True: # Will run until icon is tapped
        screenshot = device.screencap()
        with open(os.path.dirname(__file__) + "/screen.png", "wb") as fp:
            fp.write(screenshot)
        img_gray = cv2.cvtColor(cv2.imread(os.path.dirname(__file__) + "/screen.png")[top_pad:down_pad,left_pad:right_pad], cv2.COLOR_BGR2GRAY)
                
        result = cv2.matchTemplate(icon_gray, img_gray, method)
        # We want the minimum squared difference
        mn,_,mnLoc,_ = cv2.minMaxLoc(result)
        if mn < 0.2:
            # Draw the rectangle:
            # Extract the coordinates of our best match
            MPx,MPy = mnLoc
            # Step 2: Get the size of the template. This is the same size as the match.
            trows,tcols = icon_gray.shape[:2]

            # Step 3: Draw the rectangle on large_image
            # cv2.rectangle(img_gray, (MPx,MPy),(MPx+tcols,MPy+trows),(255,255,255),2)
            device.input_tap(left_pad + MPx + tcols,top_pad + MPy + trows/2)

        # cv2.imshow('output', img_gray)
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        #     running = False
        #     break


def call_whatsapp(device, contact_name):
    print(device.serial)

    screenOn = False
    unlocked = False

    while screenOn == False or unlocked == False:
        screenState = device.shell("dumpsys power | grep mWakefulness=").split("=")[1]
        print(screenState)
        lockState = device.shell("dumpsys window | grep mDreamingLockscreen=").split(" ")[-2].split("=")[1]
        screenOn = True if screenState == "Awake\n" else False
        unlocked = False if lockState == "true" else True
        print(f"Unlock device {device.serial}!!")
        print(f"Screen on: {screenOn}")
        print(f"Device unlocked: {unlocked}")
        time.sleep(3)

    display_size = [int(coordinate) for coordinate in device.shell("wm size").split(": ")[1].split("x")]
    print(display_size)
    device.shell("am force-stop com.whatsapp")
    device.shell("am start -n com.whatsapp/com.whatsapp.Main")
    device.input_keyevent("KEYCODE_SEARCH")
    device.input_keyevent("KEYCODE_D") # Write any letter so that I can use de clear button
    device.input_keyevent("KEYCODE_TAB") # Move to clear button
    device.input_keyevent("KEYCODE_ENTER") # Press clear button

    device.input_text(contact_name)
    # device.input_text("Consolato Generale Italia Buenos Aires")
    # device.input_text("Martin Cametti")
    device.input_tap(500,250)
    call_ended = True
    while True:
        try:
            if device.shell("dumpsys activity services | grep com.whatsapp/.voipcalling.VoiceFGService") == "":
                call_ended = True
                time.sleep(1)
            if call_ended == True:
                tap_call_icon(device)
                # if device.serial == "CB512EPK24":
                #     time.sleep(0.5)
                #     device.input_tap(display_size[0] - 100, display_size[1] / 2 + 50)
                call_ended = False
                time.sleep(1)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    client = Client(host="127.0.0.1", port=5037)
    devices = client.devices() # Get list of currently connected devices
    processes = []
    method = cv2.TM_SQDIFF_NORMED
    icon_gray = cv2.cvtColor(cv2.imread("src/videocall_icon.png"), cv2.COLOR_BGR2GRAY)
    contact_name = sys.argv[1]
    for device in devices:
        processes.append(Process(target = call_whatsapp, args = [device, contact_name]))
        print(f"Registering process {processes[-1].name} for device {device.serial}")

    for process in processes:
        process.start()

    for process in processes:
        process.join()