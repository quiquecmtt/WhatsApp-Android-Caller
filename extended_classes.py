class DeviceExtended(Device):
    """An extension of the Device class from PPADB"""
    def __init__(self, client, serial):
        super(),__init__(client, serial)
        screenState = self.shell("dumpsys power | grep mWakefulness=").split("=")[1]
        lockState = self.shell("dumpsys window | grep mDreamingLockscreen=").split(" ")[1].split("=")[1]
        self.screenOn = True if screenState == "Awake" else False
        self.unlocked = False if lockState == "true" else True
    
    def open_whatsapp(self):
        self.shell("am force-stop com.whatsapp")
        self.shell("am start -n com.whatsapp/com.whatsapp.Main")
    
    def open_wconversation(self, contact = "Valeria Chapperon"):
        print(f"Opening conversation with {contact} on {self.serial}")
        self.open_whatsapp()
        self.input_keyevent("KEYCODE_SEARCH")
        self.input_keyevent("KEYCODE_D") # Write any letter so that I can use de clear button
        self.input_keyevent("KEYCODE_TAB") # Move to clear button
        self.input_keyevent("KEYCODE_ENTER") # Press clear button
        self.input_text(contact)
        self.input_tap(500,250) # Enter Conversation
    
    def call(self):
        """The Device will call the contact from current WhatsApp conversation. It must be in a conversation."""
        if device.shell("dumpsys activity services | grep com.whatsapp/.voipcalling.VoiceFGService") == "":
            call_ended = True
            time.sleep(1)
        if call_ended == True:
            device.input_tap(display_size[0] - 150,150)
            if device.serial == "CB512EPK24":
                time.sleep(0.5)
                device.input_tap(display_size[0] - 100,display_size[1] / 2 + 50)
            call_ended = False
            time.sleep(1)

    def endless_call(self):
        """The Device will call the contact from current WhatsApp conversation until a Keyboard Interrupt happens. It must be in a conversation."""
        while True:
            try:
                self.call()
            except KeyboardInterrupt:
                break