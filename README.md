# Light Table GUI Application

The Light Table GUI application is a PyQt5-based tool designed to view and manipulate images. It allows users to adjust the brightness and contrast of an image in real time, providing an intuitive interface for image enhancement.

## Features

- **Image Display**: View any image in its original size and aspect ratio.
- **Brightness Adjustment**: Dynamically adjust the brightness of the displayed image using a slider control.
- **Contrast Adjustment**: Modify the contrast of the image with a separate slider control for finer image tuning.
- **Real-Time Updates**: See the effects of your adjustments instantly, thanks to the real-time processing of image changes.

## Environment
Ensure you have the following environment variables set.
LD_LIBRARY_PATH=~/mambaforge/envs/light-table-gui/lib/

## Installation

To run the Light Table GUI application, you need to have Python installed on your system along with the PyQt5 and Pillow libraries. You can install these dependencies using `pip`:

```bash
conda env create -f light-table-base.yml
```
