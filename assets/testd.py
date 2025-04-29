import sys
import inspect
import traceback
import bdb
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QLineEdit, QPushButton,
    QTreeWidget, QTreeWidgetItem, QTextBrowser,
    QLabel, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QMutex, QWaitCondition
from PyQt5.QtGui import QTextCursor, QColor, QTextFormat

class Debugger(bdb.Bdb):
    def __init__(self, thread):
        super().__init__()
        self.thread = thread

    def user_line(self, frame):
        if frame.f_code.co_filename == '<exec>':
            lineno = frame.f_lineno - 1
            self.thread.line_executed.emit(lineno)
            # pause until step requested
            self.thread.wait_for_step()
        # continue tracing

class ExecutorThread(QThread):
    line_executed = pyqtSignal(int)
    output_written = pyqtSignal(str)

    def __init__(self, code_text, namespace):
        super().__init__()
        self.code_text = code_text
        self.namespace = namespace
        self._mutex = QMutex()
        self._step_cond = QWaitCondition()
        self._step_requested = False

    def run(self):
        debugger = Debugger(self)
        orig_out, orig_err = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = self, self
        try:
            # compile and run under debugger
            compiled = compile(self.code_text, '<exec>', 'exec')
            debugger.run(compiled, self.namespace, self.namespace)
        except Exception:
            err = traceback.format_exc()
            self.output_written.emit(err)
        finally:
            sys.stdout, sys.stderr = orig_out, orig_err

    def write(self, msg):
        self.output_written.emit(msg)

    def request_step(self):
        self._mutex.lock()
        self._step_requested = True
        self._step_cond.wakeAll()
        self._mutex.unlock()

    def wait_for_step(self):
        self._mutex.lock()
        while not self._step_requested:
            self._step_cond.wait(self._mutex)
        self._step_requested = False
        self._mutex.unlock()

class CodeExecutor(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.namespace = {}
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Stepping Python Executor")
        self.resize(1200, 700)

        # Code editor
        self.code_input = QPlainTextEdit()
        self.code_input.setPlaceholderText("Enter your Python code here...")

        # Buttons
        self.next_btn = QPushButton("Step")
        self.reset_btn = QPushButton("Run & Reset")
        self.next_btn.clicked.connect(self.step)
        self.reset_btn.clicked.connect(self.reset)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addWidget(self.next_btn)

        # Console
        self.console_output = QTextBrowser()
        self.console_input = QLineEdit()
        self.console_input.setPlaceholderText(">>>")
        self.console_input.returnPressed.connect(self.exec_console)
        console_layout = QVBoxLayout()
        console_layout.addWidget(QLabel("Console Output"))
        console_layout.addWidget(self.console_output, 3)
        console_layout.addWidget(QLabel("Console Input"))
        console_layout.addWidget(self.console_input)

        # Left panel
        left = QVBoxLayout()
        left.addWidget(self.code_input, 5)
        left.addLayout(btn_layout)
        left.addLayout(console_layout, 4)
        left_widget = QWidget()
        left_widget.setLayout(left)

        # Variables
        self.var_tree = QTreeWidget()
        self.var_tree.setHeaderLabels(["Variable","Value"])
        self.var_tree.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.var_tree.itemSelectionChanged.connect(self.show_vals)
        self.value_display = QTextBrowser()
        right = QVBoxLayout()
        right.addWidget(QLabel("Variables"))
        right.addWidget(self.var_tree,3)
        right.addWidget(QLabel("Values"))
        right.addWidget(self.value_display,2)
        right_widget = QWidget()
        right_widget.setLayout(right)

        # Splitter
        split = QSplitter(Qt.Horizontal)
        split.addWidget(left_widget)
        split.addWidget(right_widget)
        split.setStretchFactor(0,2)
        split.setStretchFactor(1,1)

        main = QHBoxLayout()
        main.addWidget(split)
        self.setLayout(main)

    def reset(self):
        # stop existing thread
        if self.thread and self.thread.isRunning():
            self.thread.terminate()
            self.thread.wait()
        self.namespace.clear()
        self.var_tree.clear()
        self.value_display.clear()
        self.console_output.clear()
        self.console_input.clear()
        code_text = self.code_input.toPlainText()
        self.thread = ExecutorThread(code_text, self.namespace)
        self.thread.line_executed.connect(self.on_line)
        self.thread.output_written.connect(self.console_output.append)
        self.thread.start()
        self.next_btn.setEnabled(True)

    def step(self):
        if self.thread:
            self.thread.request_step()
            self.update_vars()

    def on_line(self, lineno):
        # highlight executed line
        extras = []
        block = self.code_input.document().findBlockByNumber(lineno)
        sel = QPlainTextEdit.ExtraSelection()
        sel.format.setBackground(QColor("yellow").lighter(160))
        sel.format.setProperty(QTextFormat.FullWidthSelection, True)
        sel.cursor = QTextCursor(block)
        extras.append(sel)
        self.code_input.setExtraSelections(extras)

    def exec_console(self):
        cmd = self.console_input.text()
        if not cmd:
            return
        try:
            out = eval(cmd, self.namespace)
            self.console_output.append(repr(out))
        except Exception:
            try:
                exec(cmd, self.namespace)
            except Exception:
                self.console_output.append(traceback.format_exc())
        self.console_input.clear()
        self.update_vars()

    def update_vars(self):
        self.var_tree.clear()
        for n, v in sorted(self.namespace.items()):
            if n.startswith("__"):
                continue
            parent = QTreeWidgetItem(self.var_tree, [n, repr(v)])
            if inspect.isclass(v):
                for a, val in v.__dict__.items():
                    if a.startswith("__"):
                        continue
                    QTreeWidgetItem(parent, [f"{n}.{a}", repr(val)])
            if hasattr(v, '__dict__'):
                for a, val in v.__dict__.items():
                    if a.startswith("__"):
                        continue
                    QTreeWidgetItem(parent, [f"{n}.{a}", repr(val)])
        self.var_tree.expandAll()

    def show_vals(self):
        items = self.var_tree.selectedItems()
        if not items:
            self.value_display.clear()
            return
        lines = [f"{i.text(0)} = {i.text(1)}" for i in items]
        self.value_display.setText("\n".join(lines))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CodeExecutor()
    w.show()
    sys.exit(app.exec_())
