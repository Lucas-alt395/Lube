import sys
import re
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLineEdit, QToolBar, QAction, QMenu, QTabWidget, QToolButton, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtCore import QUrl


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lube Browser")
        self.setGeometry(100, 100, 1000, 700)

        # Tab Widget to manage tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Add the first tab
        self.add_new_tab(QUrl("https://www.webtinq.nl/lube/lube-lo.html"), "New Tab")

        # Set the central widget
        self.setCentralWidget(self.tabs)

        # Navigation bar
        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        # Create a menu for grouped actions (buttons like Back, Forward, Reload, etc.)
        self.menu = QMenu("Options", self)

        # Add the actions to the menu
        back_action = QAction("Back", self)
        back_action.triggered.connect(lambda: self.current_browser().back())
        back_action.setShortcut("Left")  # Keybind for back
        self.menu.addAction(back_action)

        forward_action = QAction("Forward", self)
        forward_action.triggered.connect(lambda: self.current_browser().forward())
        forward_action.setShortcut("Right")  # Keybind for forward
        self.menu.addAction(forward_action)

        reload_action = QAction("Reload", self)
        reload_action.triggered.connect(lambda: self.current_browser().reload())
        reload_action.setShortcut("Ctrl+R")  # Keybind for reload
        self.menu.addAction(reload_action)

        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(self.new_tab)
        new_tab_action.setShortcut("Ctrl+T")  # Keybind for new tab
        self.menu.addAction(new_tab_action)

        # Add Developer Tools action to the menu
        dev_tools_action = QAction("Developer Tools", self)
        dev_tools_action.triggered.connect(self.open_dev_tools)
        self.menu.addAction(dev_tools_action)

        # Add Settings button to the menu
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        self.menu.addAction(settings_action)

        # Create a button for the dropdown (Options button)
        dropdown_button = QToolButton(self)
        dropdown_button.setText("Options")  # Set text for the button
        dropdown_button.setMenu(self.menu)  # Set the menu to the button
        dropdown_button.setPopupMode(QToolButton.InstantPopup)  # Make it show the menu when clicked
        self.navbar.addWidget(dropdown_button)  # Add the button to the toolbar

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)

        # Update the URL bar when the active tab changes
        self.tabs.currentChanged.connect(self.update_url_bar)

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl("https://www.google.com")

        # Create a new browser tab
        browser = QWebEngineView()

        # Set a custom user agent using page settings
        browser.page().profile().setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        )

        # Enable cookies
        self.enable_cookies(browser)

        # Set the URL
        browser.setUrl(qurl)
        browser.urlChanged.connect(self.update_url_bar)

        # Connect titleChanged to update the tab title
        browser.titleChanged.connect(lambda title: self.update_tab_title(self.tabs.indexOf(browser), title))

        # Add the new tab
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

    def enable_cookies(self, browser):
        # Enable cookies in the current browser profile
        profile = browser.page().profile()
        cookie_store = profile.cookieStore()

        # You can also use signals to listen to cookie events
        cookie_store.cookieAdded.connect(self.on_cookie_added)

    def on_cookie_added(self, cookie):
        print(f"Cookie added: {cookie.name()} = {cookie.value()}")

    def open_dev_tools(self):
        # Get the current browser and open developer tools
        current_browser = self.current_browser()
        if current_browser is not None:
            page = current_browser.page()
            page.setDevToolsPage(QWebEnginePage(page.profile()))  # Open developer tools

    def open_settings(self):
        # Placeholder for Settings functionality
        #QMessageBox.information(self, "Settings", "Settings window not implemented yet!")
        print("Opening settings...")
        subprocess.run(["python", "settings.py"])

    def update_tab_title(self, index, title):
        if index >= 0:  # Ensure the tab index is valid
            self.tabs.setTabText(index, title)

    def current_browser(self):
        # Return the current active browser (QWebEngineView)
        return self.tabs.currentWidget()

    def navigate_to_url(self):
        url = self.url_bar.text()
        if url.endswith(".lo") or url.endswith(".lw"):
            # Replace .lo/.lw with -lo/-lw and construct the redirect URL
            modified_url = url.replace(".lo", "-lo").replace(".lw", "-lw")
            redirect_url = f"https://www.webtinq.nl/lube/{modified_url}.html"
            self.current_browser().setUrl(QUrl(redirect_url))
            # Keep the original URL in the address bar
            self.url_bar.setText(url)
        else:
            # Handle normal URLs
            if not url.startswith("http"):
                url = "http://" + url
            self.current_browser().setUrl(QUrl(url))

    def update_url_bar(self, index):
        if index == -1:  # No tabs are open
            self.url_bar.clear()
            return

        # Get the current browser
        current_browser = self.current_browser()
        if current_browser is not None:
            qurl = current_browser.url()

            # Check if the URL matches the redirection pattern
            pattern = re.compile(r"https://www\.webtinq\.nl/lube/(.*)-(lo|lw)\.html")
            match = pattern.match(qurl.toString())
            if match:
                # Convert back to the .lo or .lw format
                original_url = f"{match.group(1)}.{match.group(2)}"
                self.url_bar.setText(original_url)
            else:
                # Show the normal URL
                self.url_bar.setText(qurl.toString())
        else:
            self.url_bar.clear()

    def new_tab(self):
        self.add_new_tab()

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())