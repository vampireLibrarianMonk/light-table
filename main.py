import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt
from PIL import Image, ImageEnhance

class LightTable(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle('Light Table GUI')
        self.setGeometry(100, 100, 800, 600)  # Set default window size

        # Flags and values for initial state
        self.first_show = True  # Check if image is shown for the first time
        self.brightness_value = 1  # Initial brightness value
        self.contrast_value = 1    # Initial contrast value
        self.opacity_value = 1     # Initial opacity value

        self.brightness_value_label = QLabel('100', self)  # Initial value label for brightness
        self.contrast_value_label = QLabel('100', self)  # Initial value label for contrast
        self.opacity_value_label = QLabel('100', self)  # Initial value label for opacity

        # Image Display Setup
        self.setup_image_display()

        # Brightness Adjustment Setup
        self.setup_brightness_control()

        # Contrast Adjustment Setup
        self.setup_contrast_control()

        # Opacity Adjustment Setup
        self.setup_opacity_control()

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
        self.slider.setMaximum(100)
        self.slider.setValue(50)  # Default value representing no change
        self.slider.valueChanged.connect(self.adjust_brightness)

        self.brightness_value_label = QLabel('50', self)  # Initial label text reflecting default value

    def setup_contrast_control(self):
        """Setup the contrast adjustment slider and label."""
        self.contrast_label = QLabel('Adjust Contrast:', self)
        self.contrast_label.setAlignment(Qt.AlignCenter)

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(0)
        self.contrast_slider.setMaximum(100)
        self.contrast_slider.setValue(50)  # Default value representing no change
        self.contrast_slider.valueChanged.connect(self.adjust_contrast)

        self.contrast_value_label = QLabel('50', self)  # Initial label text reflecting default value

    def setup_opacity_control(self):
        """Setup the opacity adjustment slider and label."""
        self.opacity_label = QLabel('Adjust Opacity:', self)
        self.opacity_label.setAlignment(Qt.AlignCenter)

        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(100)  # Default value, representing 100% opacity
        self.opacity_slider.valueChanged.connect(self.adjust_opacity)

    def configure_layout(self):
        # Brightness Slider Layout
        brightness_slider_layout = QHBoxLayout()
        brightness_slider_layout.addWidget(self.slider_label)
        brightness_slider_layout.addWidget(self.slider)
        brightness_slider_layout.addWidget(self.brightness_value_label)  # Add brightness value label

        # Contrast Slider Layout
        contrast_slider_layout = QHBoxLayout()
        contrast_slider_layout.addWidget(self.contrast_label)
        contrast_slider_layout.addWidget(self.contrast_slider)
        contrast_slider_layout.addWidget(self.contrast_value_label)  # Add contrast value label

        # Opacity Slider Layout
        opacity_slider_layout = QHBoxLayout()
        opacity_slider_layout.addWidget(self.opacity_label)
        opacity_slider_layout.addWidget(self.opacity_slider)
        opacity_slider_layout.addWidget(self.opacity_value_label)  # Add opacity value label

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(brightness_slider_layout)
        layout.addLayout(contrast_slider_layout)
        layout.addLayout(opacity_slider_layout)

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
        # Adjust the scale to interpret 50 as no change (1.0)
        adjusted_value = (value - 50) / 50 + 1
        self.brightness_value_label.setText(str(value))  # Update label text
        self.brightness_value = adjusted_value
        self.apply_image_adjustments()

    def adjust_contrast(self, value):
        # Adjust the scale to interpret 50 as no change (1.0)
        adjusted_value = (value - 50) / 50 + 1
        self.contrast_value_label.setText(str(value))  # Update label text
        self.contrast_value = adjusted_value
        self.apply_image_adjustments()

    def adjust_opacity(self, value):
        """Adjust the opacity of the image based on the slider's value."""
        self.opacity_value = value / 100.0
        self.apply_image_adjustments()
        self.opacity_value_label.setText(str(value))

    def apply_image_adjustments(self):
        """Apply brightness and contrast adjustments to the image."""
        brightness_enhancer = ImageEnhance.Brightness(self.original_image)
        brightened_image = brightness_enhancer.enhance(self.brightness_value)

        contrast_enhancer = ImageEnhance.Contrast(brightened_image)
        contrasted_image = contrast_enhancer.enhance(self.contrast_value)

        opacity_enhancer = ImageEnhance.Brightness(contrasted_image)
        final_image = opacity_enhancer.enhance(self.opacity_value)

        self.show_image(final_image)

    def show_image(self, pil_image):
        """Display the image in the QLabel with adjusted opacity."""
        # Convert the PIL image to a format QImage can use
        q_image = QImage(pil_image.tobytes(), pil_image.width, pil_image.height, QImage.Format_RGB32)
        q_image = q_image.rgbSwapped()  # Swap the RGB channels on the QImage object
        pixmap = QPixmap.fromImage(q_image)  # Then convert to QPixmap

        # Scale the pixmap if it's not the first time showing the image
        if not self.first_show:
            pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Create a transparent pixmap to overlay
        transparent_pixmap = QPixmap(pixmap.size())
        transparent_pixmap.fill(Qt.transparent)

        # Create a QPainter to draw the image pixmap onto the transparent pixmap
        painter = QPainter(transparent_pixmap)
        painter.setOpacity(self.opacity_value)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        # Set the transparent pixmap to the label
        self.image_label.setPixmap(transparent_pixmap)

        # Update the first_show flag
        if self.first_show:
            self.first_show = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_path = '/home/flaniganp/Pictures/Screenshots/big_chungus.png'  # Update this path to your image
    window = LightTable(image_path)
    window.show()
    sys.exit(app.exec_())
