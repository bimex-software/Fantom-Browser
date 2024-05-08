from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon

class MyWebBrowser(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MyWebBrowser, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("Fantom Browser")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        
        # Horizontal layout for search bar and buttons
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.horizontal_layout.setSpacing(10)  # Set spacing
        
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search or enter URL")
        self.url_bar.setStyleSheet("border-radius: 15px; padding: 5px;")  # Rounded corners
        self.url_bar.returnPressed.connect(self.navigate)
        
        self.refresh_btn = QPushButton()
        self.refresh_btn.setIcon(QIcon("free-refresh-icon-3104-thumb.png"))  # Provide the path to your refresh icon
        self.refresh_btn.setFixedSize(30, 30)  # Set fixed size for the refresh button
        self.refresh_btn.clicked.connect(self.refresh_page)
        
        self.back_btn = QPushButton("<")
        self.back_btn.setMinimumHeight(30)
        
        self.forward_btn = QPushButton(">")
        self.forward_btn.setMinimumHeight(30)

        self.add_btn = QPushButton("Add")
        self.add_btn.setMinimumHeight(30)
        self.add_btn.clicked.connect(self.add_tab)

        self.close_btn = QPushButton("Close")
        self.close_btn.setMinimumHeight(30)
        self.close_btn.clicked.connect(self.close_tab)
        
        self.horizontal_layout.addWidget(self.back_btn)
        self.horizontal_layout.addWidget(self.forward_btn)
        self.horizontal_layout.addWidget(self.url_bar)
        self.horizontal_layout.addWidget(self.refresh_btn)  # Add refresh button
        self.horizontal_layout.addWidget(self.add_btn)
        self.horizontal_layout.addWidget(self.close_btn)
        
        # Add the horizontal layout to the main layout
        self.layout.addLayout(self.horizontal_layout)
        
        # Add tab widget to hold browser tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.tabBar().setMinimumWidth(150)  # Set minimum width for all tabs
        self.tab_widget.setStyleSheet("border-radius: 15px; background-color: black;")  # Set black background for the tab widget
        self.layout.addWidget(self.tab_widget)
        
        self.create_tab()
        
        # Connect signals after browser is initialized
        self.back_btn.clicked.connect(self.current_browser.back)  
        self.forward_btn.clicked.connect(self.current_browser.forward)

        # Show the window maximized after it's displayed
        self.showMaximized()

    def navigate(self):
        text = self.url_bar.text()
        if "." in text:
            if not text.startswith('http://') and not text.startswith('https://'):
                text = 'http://' + text
            self.current_browser.setUrl(QUrl(text))
        else:
            search_url = "https://duckduckgo.com/?q=" + text
            self.current_browser.setUrl(QUrl(search_url))

    def create_tab(self):
        browser = QWebEngineView()
        browser.setUrl(QUrl("https://duckduckgo.com/?kae=d"))  # Load DuckDuckGo in dark mode by default
        self.tab_widget.addTab(browser, "DuckDuckGo")
        self.current_browser = browser
        
    def add_tab(self):
        self.create_tab()
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
        
    def close_tab(self):
        if self.tab_widget.count() > 1:
            index = self.tab_widget.currentIndex()
            widget = self.tab_widget.widget(index)
            self.tab_widget.removeTab(index)
            widget.deleteLater()
    
    def refresh_page(self):
        if self.current_browser:
            self.current_browser.reload()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            pos = event.pos()
            tab_bar = self.tab_widget.tabBar()
            tab_index = tab_bar.tabAt(pos)
            if tab_index >= 0:
                menu = QMenu()
                close_action = menu.addAction("Close Tab")
                action = menu.exec_(self.tab_widget.mapToGlobal(pos))
                if action == close_action:
                    self.close_tab()

    def event(self, event):
        if (event.type() == QEvent.KeyPress and
                event.key() == Qt.Key_Space and
                event.modifiers() & Qt.ControlModifier):
            self.add_tab()
            return True
        return super().event(event)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyWebBrowser()
    sys.exit(app.exec_())

