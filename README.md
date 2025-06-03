# 🧠 3D Brain Viewer

**3D Brain Viewer** is an interactive application built for medical image analysis and visualization. It allows users to input DICOM files and step through various image processing stages, ultimately reconstructing a 3D model of the patient's brain.

![3D Brain Visualization](https://github.com/raind-dev/3DBrainViewer/blob/main/3D%20Brain%20Viewer%20GUI.jpg)

## 🚀 Features

- 📂 Load a DICOM folder via the main UI
- 🖼️ Step-by-step visualization of image processing stages for brain tissue extraction
- 🧠 Final 3D brain rendering using OpenGL
- 🧪 Modular design for medical image analysis pipelines

## 🛠️ Built With

- [PySide6](https://pypi.org/project/PySide6/) - GUI framework for creating the main window and file browser
- [OpenCV (cv2)](https://opencv.org/) - Image processing
- [OpenGL (via PyOpenGL)](https://pypi.org/project/PyOpenGL/) - Real-time 3D rendering
- [Numba](https://numba.pydata.org/) - Accelerated computation for pixel-wise operations

---

## 🧑‍💻 How to Use

1. Clone this repository:
    git clone https://github.com/raind-dev/3DBrainViewer.git
    cd 3DBrainViewer

2. Run the application:
    python main.py

3. In the main window:
* Use the File Browser to select your DICOM folder
* Click the Confirm button
* Image processing and 3D rendering will begin automatically

## 🎯 Future Goals
We plan to integrate deep learning-based brain tissue extraction using a U-Net architecture implemented with PyTorch. This will enhance automation and accuracy by replacing traditional image processing methods with AI-driven segmentation.

## 📬 Contact
For any questions or collaboration proposals, feel free to reach out:

📧 Email: scoser6510@gmail.com

💼 LinkedIn: [Rain Ho](https://www.linkedin.com/in/rain-ho-2164a9106/)