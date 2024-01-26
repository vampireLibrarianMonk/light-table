import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageEnhance

class LightTable(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle('Light Table GUI')
        self.setGeometry(100, 100, 800, 600)  # Set default window size

        # Flags for initial state
        self.first_show = True  # Check if image is shown for the first time
        self.brightness_value = 1  # Initial brightness value
        self.contrast_value = 1  # Initial contrast value

        # Image Display Setup
        self.setup_image_display()

        # Brightness Adjustment Setup
        self.setup_brightness_control()

        # Contrast Adjustment Setup
        self.setup_contrast_control()

        # Layout Configuration
        self.configure_layout()

        # Load and display the initial image
        self.original_image = self.load_image(image_path)
        self.show_image(self.original_image)

    def setup_image_display(self):
        """Setup the image display label."""
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)  # Center the image

    def setup_brightness_control(self):
        """Setup the brightness adjustment slider and label."""
        self.slider_label = QLabel('Adjust Brightness:', self)
        self.slider_label.setAlignment(Qt.AlignCenter)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(200)
        self.slider.setValue(100)  # Default value for no brightness change
        self.slider.valueChanged.connect(self.adjust_brightness)

    def setup_contrast_control(self):
        """Setup the contrast adjustment slider and label."""
        self.contrast_label = QLabel('Adjust Contrast:', self)
        self.contrast_label.setAlignment(Qt.AlignCenter)

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(0)
        self.contrast_slider.setMaximum(200)
        self.contrast_slider.setValue(100)  # Default value for no contrast change
        self.contrast_slider.valueChanged.connect(self.adjust_contrast)

    def configure_layout(self):
        """Configure the main layout of the window."""
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.slider_label)
        slider_layout.addWidget(self.slider)

        contrast_slider_layout = QHBoxLayout()
        contrast_slider_layout.addWidget(self.contrast_label)
        contrast_slider_layout.addWidget(self.contrast_slider)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(slider_layout)
        layout.addLayout(contrast_slider_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_image(self, image_path):
        """Load an image from a path and handle errors."""
        try:
            with Image.open(image_path) as img:
                return img.convert("RGBA")  # Convert image to RGBA format
        except IOError:
            print(f"Unable to load image from path: {image_path}")
            sys.exit(1)

    def adjust_brightness(self, value):
        """Adjust the brightness of the image."""
        self.brightness_value = value / 100
        self.apply_image_adjustments()

    def adjust_contrast(self, value):
        """Adjust the contrast of the image."""
        self.contrast_value = value / 100
        self.apply_image_adjustments()

    def apply_image_adjustments(self):
        """Apply brightness and contrast adjustments to the image."""
        brightness_enhancer = ImageEnhance.Brightness(self.original_image)
        brightened_image = brightness_enhancer.enhance(self.brightness_value)

        contrast_enhancer = ImageEnhance.Contrast(brightened_image)
        final_image = contrast_enhancer.enhance(self.contrast_value)

        self.show_image(final_image)

    def show_image(self, pil_image):
        """Display the image in the QLabel."""
        q_image = QImage(pil_image.tobytes(), pil_image.width, pil_image.height, QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(q_image)

        if self.first_show:
            self.image_label.setPixmap(pixmap)
            self.first_show = False
        else:
            scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_path = '/home/flaniganp/Pictures/Screenshots/big_chungus.png'  # Update this path to your image
    window = LightTable(image_path)
    window.show()
    sys.exit(app.exec_())
