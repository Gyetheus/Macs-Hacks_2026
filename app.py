from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QScrollArea,
    QWidget,
)
from CalculationEngine import MathEngine
import re

GREEN_BUTTON_STYLE = """
    QPushButton {
        background-color: #2ecc71;
        color: white;
        border-radius: 6px;
        padding: 10px;
        font-size: 14px;
        font-weight: bold;
        border: none;
    }
    QPushButton:hover {
        background-color: #27ae60;
    }
    QPushButton:pressed {
        background-color: #1e8449;
    }
"""

NORMAL_BUTTON_STYLE = """
    QPushButton {
        background-color: #2ecc71;
        color: white;
        border-radius: 6px;
        padding: 10px;
        font-size: 14px;
        font-weight: bold;
        border: none;
    }
    QPushButton:hover {
        background-color: #27ae60;
    }
    QPushButton:pressed {
        background-color: #1e8449;
    }
"""

# Define our mainWindow class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cooler Calculator")

        self.engine = MathEngine()

        # 1. Create the overarching Horizontal Layout to hold Left (Scroll) and Right (Main)
        appLayout = QHBoxLayout()

        # ==========================================
        # LEFT SIDE: Variables Scroll Area
        # ==========================================
        variable_scroll = QScrollArea()
        variable_scroll.setWidgetResizable(True)
        # Optional: Keep the sidebar from taking up too much space
        # variable_scroll.setMaximumWidth(250) 

        # Create the container widget and its layout
        variable_container = QWidget()
        self.variableLayout = QFormLayout() # QFormLayout is perfect for key-value pairs

        # Populate the variables (Note the .items() added here)
        for key, value in self.engine.variables.items():
            key_label = QLabel(f"<b>{key}:</b>")
            value_label = QLabel(str(value))
            value_label.setWordWrap(True) 
            
            self.variableLayout.addRow(key_label, value_label)

        # Attach the layout to the container, and the container to the scroll area
        variable_container.setLayout(self.variableLayout)
        variable_scroll.setWidget(variable_container)

        # ==========================================
        # RIGHT SIDE: Main Application Layout
        # ==========================================
        mainLayout = QVBoxLayout()
        gridLayout = QGridLayout()

        # Expression line
        self.expressionLine = QLineEdit("")
        font = self.expressionLine.font()
        font.setPointSize(15)
        self.expressionLine.setFont(font)
        self.expressionLine.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.expressionLine.setStyleSheet("min-height: 40px")
        mainLayout.addWidget(self.expressionLine)

        # Result line
        self.resultLabel = QLabel()
        font = self.resultLabel.font()
        font.setPointSize(30)
        self.resultLabel.setFont(font)
        self.resultLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        mainLayout.addWidget(self.resultLabel)

        # Add the grid (or your calculator widgets) to the main layout
        mainLayout.addLayout(gridLayout)

        # ==========================================
        # COMBINE: Add Left and Right to the App Layout
        # ==========================================
        appLayout.addWidget(variable_scroll)  # Added first, so it sits on the left
        appLayout.addLayout(mainLayout)       # Added second, so it sits on the right

        # Finally, set the appLayout as the main layout for your window/widget
        central_widget = QWidget()
        central_widget.setLayout(appLayout)

        # Set this widget as the center of your QMainWindow
        self.setCentralWidget(central_widget)

        btn = QPushButton()
        font = btn.font()
        font.setPointSize(14)
        font.setBold(True)

        # Calculator buttons
        # Top row
        btn = QPushButton("%")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,0,0)

        btn = QPushButton("CE")
        btn.setFont(font)
        btn.clicked.connect(self.clear_entry_clicked)
        gridLayout.addWidget(btn,0,1)

        btn = QPushButton("C")
        btn.setFont(font)
        btn.clicked.connect(self.clear_clicked)
        gridLayout.addWidget(btn,0,2)

        btn = QPushButton("⌫")
        btn.setFont(font)
        btn.clicked.connect(self.backspace_clicked)
        gridLayout.addWidget(btn,0,3)
        # Fifth bottom row
        btn = QPushButton("1/x")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,1,0)

        btn = QPushButton("x²")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,1,1)

        btn = QPushButton("√x")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,1,2)

        btn = QPushButton("÷")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,1,3)

        # Fourth bottom row
        btn = QPushButton("7")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,2,0)

        btn = QPushButton("8")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,2,1)

        btn = QPushButton("9")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,2,2)

        btn = QPushButton("×")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,2,3)

        # Third bottom row
        btn = QPushButton("4")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,3,0)

        btn = QPushButton("5")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,3,1)

        btn = QPushButton("6")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,3,2)

        btn = QPushButton("-")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,3,3)

        # Second bottom row
        btn = QPushButton("1")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,4,0)

        btn = QPushButton("2")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,4,1)

        btn = QPushButton("3")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,4,2)

        btn = QPushButton("+")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,4,3)

        # Bottom Row
        btn = QPushButton("+/-")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,5,0)

        btn = QPushButton("0")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,5,1)

        btn = QPushButton(".")
        btn.setFont(font)
        btn.clicked.connect(self.button_clicked)
        gridLayout.addWidget(btn,5,2)

        btn = QPushButton("=")
        # Apply the green color using custom CSS styles
        btn.setStyleSheet(GREEN_BUTTON_STYLE)
        btn.clicked.connect(self.evaluateExpression)
        gridLayout.addWidget(btn,5,3)

    # Call to add operator or number to expression
    def button_clicked(self):
        string = self.expressionLine.text()
        string2 = self.sender().text()
        string2 = string2.replace("+/-", "-")
        string2 = string2.replace("√x", "√")
        string2 = string2.replace("x²", "²")
        string2 = string2.replace("1/x", "1/")
        self.expressionLine.setText(string + string2)

    def backspace_clicked(self):
        text = self.expressionLine.text()
        text = text[:-1]
        self.expressionLine.setText(text)

    def clear_clicked(self):
        self.expressionLine.setText("")
        self.resultLabel.setText("")

    def clear_entry_clicked(self):
        text = self.expressionLine.text()
        # strip leading ints
        updated_text = re.sub(r'[\d.]+$', '', text)
        
        self.expressionLine.setText(updated_text)



    # Call to evaluate the expression
    def evaluateExpression(self):
        line = self.expressionLine.text().strip()
        if(line == ""): return
        line = line.replace("×", "*")
        line = line.replace("÷", "/")
        line = line.replace("²", "**2")
        line = line.replace("%", "/100")
        line = self.replace_sqrt_symbol(line)
        result = self.engine.process_input(line)
        if (result == None):
            self.resultLabel.setText("Error")
        else:
            self.resultLabel.setText(str(result))
        self.update_variable_display()

    # AI code
    def replace_sqrt_symbol(self, expression):
        # Pattern explanation:
        # √         : Matches the literal square root symbol
        # \s*       : Matches any optional spaces after the symbol
        # (         : Starts the capture group (this will be our 'x')
        # \d+       : Matches one or more digits
        # (?:\.\d+)?: Optionally matches a decimal point followed by more digits
        # )         : Ends the capture group
        pattern = r'√\s*(\d+(?:\.\d+)?)'
        
        # re.sub replaces the matched pattern. 
        # r'sqrt(\1)' inserts the captured number (group 1) into the parentheses.
        formatted_expression = re.sub(pattern, r'sqrt(\1)', expression)
        
        return formatted_expression

    def update_variable_display(self):
        # 1. Clear out all existing labels in the layout
        while self.variableLayout.count():
            item = self.variableLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
                
        # 2. Re-populate the layout with the updated dictionary
        for key, value in self.engine.variables.items():
            key_label = QLabel(f"<b>{key}:</b>")
            value_label = QLabel(str(value))
            value_label.setWordWrap(True) 
            
            self.variableLayout.addRow(key_label, value_label)
    # ------


# No command line args
app = QApplication([])

# Make main window
window = MainWindow()
window.show()

# Start event loop
app.exec()