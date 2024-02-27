import sys 
import RobotControl as rbt
from functools import partial
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QStatusBar,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QFormLayout,
    QLineEdit,
    QCheckBox,
    QToolButton,
)

from PyQt6.QtGui import (
    QIntValidator,
    QDoubleValidator
)

WINDOW_SIZE = 600

class GUIWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("RobotGUI")
        #self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)

        # Create an outer layout
        self.outerLayout = QVBoxLayout()
        
        # Define central widget and set the main layout
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.outerLayout)
        self.setCentralWidget(centralWidget)

        self._createButtons()
        self._createArrowButtons()
        self._createStatusBar()
        
    def _createButtons(self):
        # Create layout for fundamental functions/buttons
        baseFunctionLayout = QVBoxLayout()
        # Add base buttons to layout and connect corresponding functions
        init_button = QPushButton("Initialize Robot")
        baseFunctionLayout.addWidget(init_button)
        init_button.clicked.connect(rbt.initialize_robot)
        init_button.clicked.connect(self._statusMessage)

        pickup_button = QPushButton("Pickup Mouse")
        baseFunctionLayout.addWidget(pickup_button)
        pickup_button.clicked.connect(rbt.pickup_mouse)

        rest_button = QPushButton("Rest Position")
        baseFunctionLayout.addWidget(rest_button)
        rest_button.clicked.connect(rbt.rest_pos)

        beam_button = QPushButton("Beam Position")
        baseFunctionLayout.addWidget(beam_button)
        beam_button.clicked.connect(rbt.beam_pos)

        # Create layouts for robot/mouse movement functions 
        moveFunctionLayout = QHBoxLayout()
        moveInputLayout = QFormLayout()
        moveButtonLayout = QVBoxLayout()

         # Add forms for user input for offsetting axis and rotation
        offset_lineEdit = QLineEdit()
        offset_lineEdit.setValidator(QDoubleValidator())
        moveInputLayout.addRow("Horizontal Offset (mm): ", offset_lineEdit)

        rotation_lineEdit = QLineEdit()
        rotation_lineEdit.setValidator(QDoubleValidator())
        moveInputLayout.addRow("Joint Speed (%): ", rotation_lineEdit)

        translation_lineEdit = QLineEdit()
        translation_lineEdit.setValidator(QDoubleValidator())
        moveInputLayout.addRow("Linear Speed (%): ", translation_lineEdit)

        # Add buttons for offsetting axis and rotation and connect functions
        offset_button = QPushButton("Offset Axis")
        moveButtonLayout.addWidget(offset_button)
        offset_button.clicked.connect(partial(self.offset_wrapper, offset_lineEdit))

        rotation_button = QPushButton("Rotation")
        moveButtonLayout.addWidget(rotation_button)
        rotation_button.clicked.connect(partial(self.rotation_wrapper, rotation_lineEdit))

        translation_button = QPushButton("Translation")
        moveButtonLayout.addWidget(translation_button)
        translation_button.clicked.connect(partial(self.translation_wrapper, translation_lineEdit))
        
        # Add input and button layouts to overall move function layout
        moveFunctionLayout.addLayout(moveInputLayout)
        moveFunctionLayout.addLayout(moveButtonLayout)
        #Add sub layouts to outer layout
        self.outerLayout.addLayout(baseFunctionLayout)
        self.outerLayout.addLayout(moveFunctionLayout)

    def _createArrowButtons(self):
        self.baseArrowLayout = QHBoxLayout()
        YZArrowLayout = QVBoxLayout()
        YArrowLayout = QHBoxLayout()
        XArrowLayout = QVBoxLayout()

        #add line edit for changing jog speed
        jogSpeed_lineEdit = QLineEdit()
        jogSpeed_lineEdit.setValidator(QDoubleValidator())

        Z_pos_button = QToolButton()
        Z_pos_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        Z_pos_button.setText("Z+")
        Z_pos_button.setArrowType(QtCore.Qt.ArrowType.UpArrow)
        Z_pos_button.setAutoRepeat(True)
        Z_pos_button.clicked.connect(partial(self.jog_wrapper, "Z_pos", jogSpeed_lineEdit))

        Z_neg_button = QToolButton()
        Z_neg_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        Z_neg_button.setText("Z-")
        Z_neg_button.setArrowType(QtCore.Qt.ArrowType.DownArrow)
        Z_neg_button.setAutoRepeat(True)
        Z_neg_button.clicked.connect(partial(self.jog_wrapper, "Z_neg", jogSpeed_lineEdit))

        Y_pos_button = QToolButton()
        Y_pos_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        Y_pos_button.setText("Y+")
        Y_pos_button.setArrowType(QtCore.Qt.ArrowType.RightArrow)
        Y_pos_button.setAutoRepeat(True)
        Y_pos_button.clicked.connect(partial(self.jog_wrapper, "Y_pos", jogSpeed_lineEdit))

        Y_neg_button = QToolButton()
        Y_neg_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        Y_neg_button.setText("Y-")
        Y_neg_button.setArrowType(QtCore.Qt.ArrowType.LeftArrow)
        Y_neg_button.setAutoRepeat(True)
        Y_neg_button.clicked.connect(partial(self.jog_wrapper, "Y_neg", jogSpeed_lineEdit))

        X_pos_button = QToolButton()
        X_pos_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        X_pos_button.setText("X+")
        X_pos_button.setArrowType(QtCore.Qt.ArrowType.DownArrow)
        X_pos_button.setAutoRepeat(True)
        X_pos_button.clicked.connect(partial(self.jog_wrapper, "X_pos", jogSpeed_lineEdit))

        X_neg_button = QToolButton()
        X_neg_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        X_neg_button.setText("X-")
        X_neg_button.setArrowType(QtCore.Qt.ArrowType.UpArrow)
        X_neg_button.setAutoRepeat(True)
        X_neg_button.clicked.connect(partial(self.jog_wrapper, "X_neg", jogSpeed_lineEdit))

        YZArrowLayout.addWidget(Z_pos_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        YArrowLayout.addWidget(Y_neg_button)
        YArrowLayout.addWidget(Y_pos_button)
        YZArrowLayout.addLayout(YArrowLayout)
        YZArrowLayout.addWidget(Z_neg_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        XArrowLayout.addWidget(X_neg_button)
        XArrowLayout.addWidget(X_pos_button)

        jogSpeedLayout = QVBoxLayout()
        jogSpeedLayout.addWidget(QLabel("Jog Speed (mm/s)"))
        jogSpeedLayout.addWidget(jogSpeed_lineEdit)
        self.baseArrowLayout.addLayout(jogSpeedLayout)

        self.baseArrowLayout.addLayout(YZArrowLayout)
        self.baseArrowLayout.addLayout(XArrowLayout)

        self.outerLayout.addLayout(self.baseArrowLayout)


    def _createStatusBar(self):
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Robot not initialized")
        self.setStatusBar(self.status_bar)

    def _statusMessage(self):
        self.status_bar.showMessage("Robot initialized and homed")

    def offset_wrapper(self, line_obj):
        horizontal_offset = line_obj.text()
        rbt.offset_axis(float(horizontal_offset))

    def rotation_wrapper(self, line_obj):
        joint_speed = line_obj.text()
        rbt.rotate_mouse(float(joint_speed))

    def translation_wrapper(self, line_obj):
        linear_speed = line_obj.text()
        rbt.translate_mouse(float(linear_speed))

    def jog_wrapper(self, direction, speed):
        linear_speed = speed.text()
        rbt.jog_robot(direction, float(linear_speed))

def main():
    GUI = QApplication([])
    GUI.setStyle('Fusion')
    interfaceWindow = GUIWindow()
    interfaceWindow.show()
    sys.exit(GUI.exec())


if __name__ == "__main__":
    main()