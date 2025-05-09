from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget
from PyQt5.QtWidgets import QDesktopWidget, QFileDialog,QProgressBar
from PyQt5.QtGui import QPixmap
from PIL import Image
import os

gradient_style = (
    "QPushButton {"
    "   background-color: #ff0061;"  # Default color
    "   border: none;"
    "   padding: 10px;"
    "   border-radius: 5px;"
    "   color: white;"  # Text color
    "   font-weight: bold;"  # Bold text
    "}"
    "QPushButton:hover {"
    "   background-color: #cc004d;"  # Darker color on hover
    "}"
)


app = QApplication([])

main_window = QWidget()
main_window.setWindowTitle('LEUKO-Leukemia Detection AI')

# Set white background color using CSS styling
main_window.setStyleSheet("background-color: white;")

# Get the screen size
screen = QDesktopWidget().screenGeometry()
screen_width, screen_height = screen.width(), screen.height()
main_window.resize(screen_width, screen_height)


#Widgets and Objects
title = QLabel("LEUKO")
subtitle = QLabel("Leukemia Detection AI")
logo_label = QLabel()


title.setStyleSheet("color: #ff0061; font-weight: bold; font-size: 56px;") 
subtitle.setStyleSheet("color: black; font-size: 34px;")

# Load logo image
logo_path = "logo.jpg"  
if os.path.exists(logo_path):
    logo = QPixmap(logo_path)
    w,h=logo_label.width(),logo_label.height()
    logo=logo.scaled(100,100)
    logo_label.setPixmap(logo)
else:
    logo_label = QLabel("Logo Not Found")


btn_folder = QPushButton("Folder")
file_list = QListWidget()
submit_btn = QPushButton("Submit")
clear_btn = QPushButton("Clear")

true=QLabel('True')
true_label=QLabel("True Label")
true_label.setStyleSheet("border: 2px solid black; padding: 15px 110px; border-radius: 10px;")
predicted=QLabel('Predicted')
predicted_label=QLabel("Predicted Label")
predicted_label.setStyleSheet("border: 2px solid black; padding: 15px 100px; border-radius: 10px;")
accuracy = QLabel('Accuracy')
accuracy_label = QProgressBar()  # Use QProgressBar for the accuracy bar graph
accuracy_label.setRange(0, 100)  # Set the range of the progress bar
accuracy_label.setValue(75)
accuracy_label.setStyleSheet(
    """
    QProgressBar {
        width: 280px; /* Set the width */
        color: white; /* Text color */
        text-align:center
    }
    QProgressBar::chunk {
        background-color: #ff0061; /* Progress bar color */
        border-radius: 5px; /* Rounded corners (same as container) */
    }
    """
)



picture_box = QLabel()
placeholder_image_path = 'placeholder.png'
if os.path.exists(placeholder_image_path):
    placeholder_image = QPixmap(placeholder_image_path)
    picture_box.setPixmap(placeholder_image)
else:
    picture_box.setText("Image will appear here")
picture_box.setStyleSheet("border-radius=5")

                       
#Dropdown box
model_selector = QComboBox()
model_selector.addItem("Vision Transform")
model_selector.addItem("ResNet")
model_selector.addItem("VGG-19")


#NavBar
navbar_layout = QHBoxLayout()
# navbar_layout.addStretch()  
logo_layout = QVBoxLayout()  # Nested layout for the logo
title_layout = QVBoxLayout()  # Nested layout for the title and subtitle
title_layout.addWidget(title, alignment=Qt.AlignCenter)
title_layout.addWidget(subtitle, alignment=Qt.AlignCenter)
logo_layout.addWidget(logo_label, alignment=Qt.AlignRight)
navbar_layout.addLayout(title_layout, 90)  # Title layout takes 80% of navbar space
navbar_layout.addLayout(logo_layout, 10)  # Logo layout takes 20% of navbar space
# navbar_layout.addStretch() 


master_layout=QHBoxLayout()
side_panel=QVBoxLayout()
main_panel=QVBoxLayout()

#Creating a side panel
side_panel.addWidget(btn_folder)
side_panel.addWidget(file_list)


#Creating main panel

body_layout=QHBoxLayout()
col1=QVBoxLayout()
col1.addWidget(picture_box,alignment=Qt.AlignCenter)
col1.addWidget(model_selector)
col1.addWidget(submit_btn)
col1.addWidget(clear_btn)


col2=QVBoxLayout()
row1=QHBoxLayout()
row2=QVBoxLayout()
row3=QHBoxLayout()
col2.addLayout(row1,35)
col2.addLayout(row2,30)
col2.addLayout(row3,35)
row2.addWidget(true,alignment=Qt.AlignLeft)
row2.addWidget(true_label,alignment=Qt.AlignLeft)
row2.addWidget(predicted,alignment=Qt.AlignLeft)
row2.addWidget(predicted_label,alignment=Qt.AlignLeft)
row2.addWidget(accuracy,alignment=Qt.AlignLeft)
row2.addWidget(accuracy_label,alignment=Qt.AlignLeft)

body_layout.addLayout(col1,50)
body_layout.addLayout(col2,50)


main_panel.addLayout(navbar_layout,5)
main_panel.addLayout(body_layout,95)



master_layout.addLayout(side_panel,20)
master_layout.addLayout(main_panel,80)

main_window.setLayout(master_layout)

#Adding Stylesheets
clear_btn.setStyleSheet(gradient_style)
submit_btn.setStyleSheet(gradient_style)
btn_folder.setStyleSheet(gradient_style)
model_selector.setStyleSheet("""
    QComboBox {
        padding: 10px;
        background-color: #ff0061;
        font-weight: bold;
        border-radius: 5px;
        color: white;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;
    }
    QComboBox::down-arrow {
        image: url(down.png);
    }
    QComboBox::down-arrow:on {
        image: url(:/icons/up_arrow.png);
    }
    QComboBox QAbstractItemView {
        background-color: #ff0061;
        color: white;
        selection-background-color: #00ff61;
        
    }
""")

picture_box.setMinimumSize(400, 400)

#Accessing the folders
working_directory = ""

def filter(files, extensions):
    results = []
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                results.append(file)
    return results

#choose current working directory
def getWorkDirectory():
    global working_directory
    working_directory = QFileDialog.getExistingDirectory()
    extensions = ['.jpg', '.jpeg', '.png', '.svg']
    filenames = filter(os.listdir(working_directory), extensions)
    file_list.clear()
    for filename in filenames:
        file_list.addItem(filename)

class Editor:
    def __init__(self):
        self.image = None
        self.original = None
        self.filename = None
    
    def load_image(self, filename):
        self.filename = filename
        fullname = os.path.join(working_directory, self.filename)
        self.image = Image.open(fullname)
        self.original = self.image.copy()

    def show_image(self, path):
        picture_box.hide()
        image = QPixmap(path)
        w, h = picture_box.width(), picture_box.height()
        image = image.scaled(w, h, Qt.KeepAspectRatio)
        picture_box.setPixmap(image)
        picture_box.show()

def displayImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        main.load_image(filename)
        main.show_image(os.path.join(working_directory, main.filename))

def clearImage():
    picture_box.clear()  # Clear the contents of the picture box

clear_btn.clicked.connect(clearImage)


main = Editor()

btn_folder.clicked.connect(getWorkDirectory)
file_list.currentRowChanged.connect(displayImage)

#show/run
main_window.show()
app.exec_()
