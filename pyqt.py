import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QApplication,QGroupBox, QToolTip, QMessageBox, QDesktopWidget, QMainWindow, QAction, qApp, QMenu, QFileDialog, QLabel, QVBoxLayout,QMessageBox,QGraphicsScene,QGraphicsView,QGraphicsPixmapItem, QLineEdit,QHBoxLayout,QProgressBar 
from PyQt5.QtGui import QIcon, QFont, QPixmap, QImage, QBrush
from PyQt5.QtCore import Qt, QRect
import cv2
print(cv2.__version__)
import Image
import time


class Gui(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        #self.createGraphicview()
        # Custom Setting
        hbox = QHBoxLayout()
        #hbox.addStretch(1)
        
        self.scence = QGraphicsScene()
        self.graphicview = QGraphicsView(self.scence, self)
        hbox.addWidget(self.graphicview)
        hbox.addWidget(self.groupbox)
        
        vbox_1 = QVBoxLayout()
        vbox_1.addLayout(hbox)
        # Progress Bar
        self.progress = QProgressBar(self)
        vbox_1.addWidget(self.progress)
        
        self.setLayout(vbox_1)
            
        self.setGeometry(500, 500, 600, 300)
        # self.center()
        self.setWindowTitle('Face Detection GUI')
        self.setWindowIcon(QIcon('Icon.png'))
        
        self.show()
    
    def error(self):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Please Select the file')
            msg.setWindowTitle("Error")
            msg.exec_()
            
    #def createGraphicview(self):
        
        
        #graphicview.setGeometry(19,46,400,400)
    
    def initUI(self):
        self.groupbox = QGroupBox("Steps")
        vbox = QVBoxLayout(self)
        
        # First Button for Image
        self.btn_1 = QPushButton('Image', self)
        self.btn_1.setToolTip('To Select <b>Image</b> File')
        self.btn_1.clicked.connect(self.image_file)
        self.btn_1.resize(self.btn_1.sizeHint())
        self.btn_1.setStyleSheet("QPushButton"
                             "{"
                             "background-color : Green;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}")
        vbox.addWidget(self.btn_1)
        
               
        # Second Button for Cfg
        self.btn_2 = QPushButton('CFG', self)
        self.btn_2.setToolTip('To Select <b>CFG</b> File')
        self.btn_2.setEnabled(False)
        self.btn_2.clicked.connect(self.cfg_file)
        self.btn_2.resize(self.btn_2.sizeHint())
        vbox.addWidget(self.btn_2)
        
        
        # Thrid Button for Weight
        self.btn_3 = QPushButton('Weight', self)
        self.btn_3.setToolTip('To Select <b>Weight</b> File')
        self.btn_3.setEnabled(False)
        self.btn_3.clicked.connect(self.weight_file)
        self.btn_3.resize(self.btn_3.sizeHint())
        vbox.addWidget(self.btn_3)
        #vbox.addStretch()  
        #vbox.setSpacing(0)
        
        # Fourth Button for Gpu
        self.btn_4 = QPushButton('GPU', self)
        self.btn_4.setToolTip('To Check <b>GPU</b> in PC')
        self.btn_4.setEnabled(False)
        self.btn_4.clicked.connect(self.gpu)
        self.btn_4.resize(self.btn_4.sizeHint())
        vbox.addWidget(self.btn_4)
        self.line_1 = QLineEdit(self)
        self.line_1.setText('GPU Status')
        vbox.addWidget(self.line_1)
              
      
        # Fifth Button for Result
        self.btn_5 = QPushButton('Result', self)
        self.btn_5.setToolTip('To get the <b>Result</b>')
        self.btn_5.setEnabled(False)
        self.btn_5.clicked.connect(self.result)
        self.btn_5.resize(self.btn_5.sizeHint())
        vbox.addWidget(self.btn_5)
        self.line_2 = QLineEdit(self)
        self.line_2.setText('No of Faces')
        vbox.addWidget(self.line_2)
        self.line_3 = QLineEdit(self)
        self.line_3.setText('Inference Time')
        vbox.addWidget(self.line_3)
        
        # Six button Button for Blur
        self.btn_6 = QPushButton('Blur', self)
        self.btn_6.setToolTip('To <b> Blur </b> the faces')
        self.btn_6.setEnabled(False)
        self.btn_6.clicked.connect(self.Blur)
        self.btn_6.resize(self.btn_6.sizeHint())
        vbox.addWidget(self.btn_6)
        
        
        # Seven button for Save
        self.btn_7 = QPushButton('Save', self)
        self.btn_7.setToolTip('To <b> Save the Result </b>')
        self.btn_7.setEnabled(False)
        self.btn_7.clicked.connect(self.Save)
        self.btn_7.resize(self.btn_7.sizeHint())
        vbox.addWidget(self.btn_7)
        
        
        # Eight button for Clear
        self.btn_8 = QPushButton('Clear', self)
        self.btn_8.setToolTip('To <b>Clear</b>')
        self.btn_8.setEnabled(True)
        self.btn_8.setStyleSheet("QPushButton"
                                 "{"
                                 "background-color : White;"
                                 "}"
                                 "QPushButton::pressed"
                                 "{"
                                 "background-color : red;"
                                 "}")
        self.btn_8.clicked.connect(self.clear)
        self.btn_8.resize(self.btn_8.sizeHint())
        vbox.addWidget(self.btn_8)
        
         # Nine button for the Quit
        self.btn_9 = QPushButton('Quit', self)
        self.btn_9.setToolTip('To <b>Quit</b> the programm')
        self.btn_9.setEnabled(True)
        self.btn_9.setStyleSheet("QPushButton"
                                 "{"
                                 "background-color : White;"
                                 "}"
                                 "QPushButton::pressed"
                                 "{"
                                 "background-color : red;"
                                 "}")
        self.btn_9.clicked.connect(QApplication.instance().quit)
        self.btn_9.resize(self.btn_9.sizeHint())
        vbox.addWidget(self.btn_9)
                        
         
        self.groupbox.setLayout(vbox)        

 
        

    def image_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Select Image', 'Home', '*.jpg *.png *.jpeg')
        if not all(file_name) != True:
            
            self.btn_1.setStyleSheet("QPushButton"
                             "{"
                             "background-color : white;"
                             "}")
            self.btn_2.setEnabled(True)
            self.btn_2.setStyleSheet("QPushButton"
                             "{"
                             "background-color : Green;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}"
                             )
            self.image_path = file_name[0]
            self.img = Image.Image(self.image_path)
            image = QImage(self.img.data, self.img.shape[1],self.img.shape[0], QImage.Format_RGB888).rgbSwapped()
            item = QGraphicsPixmapItem(QPixmap.fromImage(image))
            self.scence.addItem(item)
        else:
            
            self.error()
            
            
    def cfg_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Select CFG', 'Home')
        if not all(file_name) != True:
            self.btn_2.setStyleSheet("QPushButton"
                             "{"
                             "background-color : white;"
                             "}")
            self.btn_3.setEnabled(True)
            self.btn_3.setStyleSheet("QPushButton"
                             "{"
                             "background-color : Green;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}"
                             )
            self.cfg_path = file_name[0]
        else:
            self.error()
        
        
    def weight_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Select Weights', 'Home')
        if not all(file_name) != True:
            self.btn_3.setStyleSheet("QPushButton"
                             "{"
                             "background-color : white;"
                             "}")
            self.btn_4.setEnabled(True)
            self.btn_4.setStyleSheet("QPushButton"
                             "{"
                             "background-color : Green;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : red;"
                             "}"
                             )
            self.weight_path = file_name[0]
        else:
            self.error()
            
            
    def gpu(self):
        self.response, text = Image.gpu()
        self.line_1.setText(str(text))
        self.btn_4.setStyleSheet("QPushButton"
                                     "{"
                                     "background-color : white;"
                                     "}")
        self.btn_5.setEnabled(True)
        self.btn_5.setStyleSheet("QPushButton"
                                     "{"
                                    "background-color : Green;"
                                     "}"
                                     "QPushButton::pressed"
                                    "{"
                                     "background-color : red;"
                                     "}"
                                    )
        
    def result(self):
        self.detection, self.time = Image.net(
            self.image_path, self.cfg_path, self.weight_path, self.response)
        self.progress.setMaximum(len(self.detection))
        no_faces = 0
        for detect in range(len(self.detection)):
            time.sleep(0.5)
            no_faces += 1
            box = self.detection[detect][2:]
            cv2.rectangle(self.img, box, color=(0, 255, 0), thickness=1)
            self.progress.setValue(detect+1)
        image = QImage(
            self.img.data, self.img.shape[1], self.img.shape[0], QImage.Format_RGB888).rgbSwapped()
        item = QGraphicsPixmapItem(QPixmap.fromImage(image))
        self.scence.addItem(item)
        self.line_2.setText(str(no_faces))
        self.line_3.setText(str(self.time))
        self.btn_5.setStyleSheet("QPushButton"
                             "{"
                             "background-color : white;"
                             "}")
        self.btn_6.setEnabled(True)
        self.btn_6.setStyleSheet("QPushButton"
                                 "{"
                                 "background-color : white;"
                                 "}"
                                 "QPushButton::pressed"
                                 "{"
                                 "background-color : red;"
                                 "}")
        self.btn_7.setEnabled(True)
        self.btn_7.setStyleSheet("QPushButton"
                                 "{"
                                 "background-color : white;"
                                 "}"
                                 "QPushButton::pressed"
                                 "{"
                                 "background-color : red;"
                                 "}")
        
    
    def Blur(self):
        self.blur_img = Image.blur(self.image_path, self.detection)
        image = QImage(
            self.blur_img.data, self.blur_img.shape[1], self.blur_img.shape[0], QImage.Format_RGB888).rgbSwapped()
        item = QGraphicsPixmapItem(QPixmap.fromImage(image))
        self.scence.addItem(item)
        if self.blur_img.size != 0:
            self.final_img = self.blur_img
    
    def Save(self):
        Image.save(self.final_img, self.time, self.detection)
    
    def clear(self):
        self.scence.clear()
        self.cfg_path = None
        self.weight_path = None
        self.line_1.clear()
        self.line_2.clear()
        self.line_3.clear()
        self.progress.setValue(0)
        #self.setStyleSheet("")


def main_():
    app = QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main_()
