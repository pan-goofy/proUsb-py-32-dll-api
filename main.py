import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget,QMessageBox
from PySide2.QtGui import QIcon
from PySide2.QtCore import QCoreApplication,Slot
import multiprocessing as mp
from web_socket import SocketThread
import configparser
import json
import asyncio
from ui_index import Ui_Form
from card import Card
class LoginGui(QWidget, Ui_Form):
    cf = configparser.ConfigParser()
    cf.read('./config.ini', encoding='utf-8')
    cf_ip = cf.get("Sections","ip")
    cf_port = cf.get("Sections","port")
    websocket =''
    socket_thread = ''
    def __init__(self):
        super(LoginGui, self).__init__()   # 调用父类的初始化方法
        # 检查是否已经有一个实例运行
        app_id = "my_app_identifier"
        # 创建共享内存
        lock = mp.Lock()
        is_running = False
        # 尝试获取锁，如果获取成功，则说明没有运行的实例
        if lock.acquire(block=False):
           is_running = False
        else:
           is_running = True
        if is_running ==True:
            QMessageBox.critical(None, "Error", "发卡器已经运行.")
            sys.exit()
        self.setupUi(self)                 #  调用Ui_MainWindow的setupUi方法布置界面
        _translate = QCoreApplication.translate
        self.ip.setText(_translate("Form", self.cf_ip))
        self.port.setText(_translate("Form", self.cf_port))
        #self.startService.clicked.connect(self.startServer)
        self.setWindowIcon(QIcon('Icon.ico'))
        self.startServer()
        #打开usb
        cardUsb = Card()
        cardUsb.openUsb()
    def startServer(self):
        self.startService.setDisabled(True)
        self.socket_thread = SocketThread(self.cf_ip,self.cf_port)
        #socket.run()
        self.socket_thread.finished.connect(self.on_thread_finished)
        self.socket_thread.start()
    @Slot(str,object)
    def on_thread_finished(self,message,websocket):
        print("socket",message)
        
        self.websocket = websocket
        msg = json.loads(message)
        self.setDevice(msg)
      
        
    
    def setDevice(self,msg):
        print(msg.get('action'))
        cards = Card()
        action = msg.get('action')
        data ={}
        if action == 'openUsb':
            res = cards.openUsb()    
        elif action == 'readDll':
            res = cards.readDll()
            data.update({'version':res.get('version')})
        elif action == 'sound':
            timeer = msg.get('timeer')
            res = cards.sound(timeer)
        elif action == 'writeCard':
            res = cards.writeCard(msg.get('dai'),msg.get('llock'),msg.get('cardNo'),msg.get('pdoors'),msg.get('bdate'),msg.get('edate'),msg.get('lockNo'))
        elif action == 'readCard':
            res = cards.readCard()
            data.update({'cardBuffer':res.get('cardBuffer')})
        elif action == 'clearCard':
            res = cards.clearCard()
        elif action == 'readCardType':
            res = cards.readCardType()
            data.update({'cardType':chr(res.get('cardType'))})
        elif action == 'readCardTime':
            res = cards.readCardTime()
            data.update({'cardDate':res.get('cardDate')})
        elif action == 'cardLock':
            res = cards.cardLock()  
            data.update({'lockNo':res.get('lockNo')})                      
        if res !="":    
            data.update({
                "status":res.get('status'),
                "type" : action
            })
            asyncio.run(self.socket_thread.sendMsg(json.dumps(data),self.websocket))             
    
        
if __name__ == '__main__':
    app = QApplication([])
    # 创建一个 QIcon 对象，用于设置应用程序的图标
    gui = LoginGui()
    gui.show()
    app.exec_()
