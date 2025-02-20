import cv2
import numpy as np
from pyzxing import BarCodeReader
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.image import Image

class QRScannerScreen(MDScreen):
    def __init__(self, **kwargs):
        super(QRScannerScreen, self).__init__(**kwargs)
        self.capture = None
        self.scanner = BarCodeReader()

        # Layout
        self.layout = MDBoxLayout(orientation='vertical', spacing=10, padding=10)

        # QR Preview Container
        self.qr_preview = Image()
        self.qr_card = MDCard(size_hint=(None, None), size=(400, 400), elevation=5)
        self.qr_card.add_widget(self.qr_preview)
        self.layout.add_widget(self.qr_card)

        # Label
        self.qr_label = MDLabel(text="Scanning...", halign="center", theme_text_color="Primary")
        self.layout.add_widget(self.qr_label)

        # Back Button
        self.back_button = MDRaisedButton(text="Back to Dashboard", pos_hint={"center_x": 0.5})
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def on_enter(self):
        """ Start Camera when entering the screen """
        self.start_camera()

    def on_leave(self):
        """ Stop Camera when leaving the screen """
        self.stop_camera()

    def start_camera(self):
        """ Open Webcam """
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def stop_camera(self):
        """ Release Camera """
        if self.capture:
            self.capture.release()
        Clock.unschedule(self.update)

    def update(self, dt):
        """ Keep Updating Camera Preview & Scan QR Code Continuously """
        ret, frame = self.capture.read()
        if ret:
            # Convert frame to texture for displaying
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.qr_preview.texture = texture

            # QR Code Detection
            cv2.imwrite("temp_qr.png", frame)
            result = self.scanner.decode("temp_qr.png")

            if result:
                qr_text = result[0].get("parsed")
                self.qr_label.text = f"QR Code: {qr_text}"

    def go_back(self, instance):
        self.manager.current = "dashboard"
