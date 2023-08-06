import PyQt5
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

def browser(name, url):
    class MainWindow(QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            self.browser = QWebEngineView()
            self.browser.setUrl(QUrl(url))
            self.setCentralWidget(self.browser)
            self.showMaximized()

            # navbar
            navbar = QToolBar()
            self.addToolBar(navbar)

            back_btn = QAction('Back', self)
            back_btn.triggered.connect(self.browser.back)
            navbar.addAction(back_btn)

            forward_btn = QAction('Forward', self)
            forward_btn.triggered.connect(self.browser.forward)
            navbar.addAction(forward_btn)

            reload_btn = QAction('Reload', self)
            reload_btn.triggered.connect(self.browser.reload)
            navbar.addAction(reload_btn)

            home_btn = QAction('Home', self)
            home_btn.triggered.connect(self.navigate_home)
            navbar.addAction(home_btn)

            self.url_bar = QLineEdit()
            self.url_bar.returnPressed.connect(self.navigate_to_url)
            navbar.addWidget(self.url_bar)

            self.browser.urlChanged.connect(self.update_url)

        def navigate_home(self):
            self.browser.setUrl(QUrl(url))

        def navigate_to_url(self):
            url = self.url_bar.text()
            self.browser.setUrl(QUrl(url))

        def update_url(self, q):
            self.url_bar.setText(q.toString())


    app = QApplication(sys.argv)
    QApplication.setApplicationName(name)
    window = MainWindow()
    app.exec_()

def notepad(name):
    compiler = Tk()
    compiler.title(name)
    file_path = ''


    def set_file_path(path):
        global file_path
        file_path = path


    def open_file():
        path = askopenfilename(filetypes=[('Python Files', '*.py'),('HTML Files', '*.html'),('Text File', '*.txt'),('Javascript File', '*.js'),('CSS File', '*.css')])
        with open(path, 'r') as file:
            code = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0', code)
            set_file_path(path)


    def save_as():
        if file_path == '':
            path = asksaveasfilename(filetypes=[('Python Files', '*.py'),('HTML Files', '*.html'),('Text File', '*.txt'),('Javascript File', '*.js'),('CSS File', '*.css')])
        else:
            path = file_path
        with open(path, 'w') as file:
            code = editor.get('1.0', END)
            file.write(code)
            set_file_path(path)


    def run():
        if file_path == '':
            save_prompt = Toplevel()
            text = Label(save_prompt, text='Please save your code')
            text.pack()
            return
        command = f'python {file_path}'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        code_output.insert('1.0', output)
        code_output.insert('1.0',  error)


    menu_bar = Menu(compiler)

    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label='Open', command=open_file)
    file_menu.add_command(label='Save', command=save_as)
    file_menu.add_command(label='Save As', command=save_as)
    file_menu.add_command(label='Exit', command=exit)
    menu_bar.add_cascade(label='File', menu=file_menu)

    run_bar = Menu(menu_bar, tearoff=0)
    run_bar.add_command(label='Run', command=run)
    menu_bar.add_cascade(label='Run', menu=run_bar)

    compiler.config(menu=menu_bar)

    editor = Text()
    editor.pack()

    code_output = Text(height=10)
    code_output.pack()

    compiler.mainloop()

