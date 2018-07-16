from PyQt5 import QtWidgets
import _thread, Backend_Process
from ui import Ui_MainWindow
import sys
import temp.text


class mainclass(Ui_MainWindow):
    # initializing main UI from PyQT
    def __init__(self,MainWindow):
        Ui_MainWindow.__init__(self)
        self.setupUi(MainWindow)
        #self.source_MAC_box.setVisible(False)
        _thread.start_new_thread(self.populateinterfaces, ())
        # self.interface_box.activated[str].connect(self.act)
        self.arp_send.clicked.connect(lambda :self.arp_send1("send"))
        self.arp_code.clicked.connect(lambda :self.arp_send1("code"))
        self.send_button.clicked.connect(lambda : self.clipboard_send("send"))
        self.exit.clicked.connect(self.exitfn)
        self.clipboard_button.clicked.connect(lambda :self.clipboard_send('clip'))
        self.protocolbox.activated[str].connect(self.deactivator)

    def arp_send1(self,text):
        s_ip = self.dest_IP_box.currentText()
        ifc = self.interface_box.currentText()
        request_or_response=self.arp_response_radio.isChecked()
        if text == "send":
            report = Backend_Process.arp_send(ifc,s_ip,request_or_response)
            report=str(report)
            self.statusBar.showMessage(report,5000)
        elif text == "code":
            report = temp.text.arp_code(ifc, s_ip,request_or_response)
            report = str(report)
            self.Clipboard.setText(report)

    def exitfn(self):
        sys.exit(0)

    def populateinterfaces(self):
        iface = Backend_Process.getinterfaces()
        ips = Backend_Process.IP_addr
        macs = Backend_Process.MAC
        for element in iface:
            self.interface_box.addItem(element)
        for mac_address in macs:
            self.source_MAC_box.addItem(mac_address)

    def clipboard_send(self,text):
        ethsrc = self.source_MAC_box.currentText()
        ethdst = self.dest_MAC_box.currentText()
        ipsrc = self.source_IP_box.currentText()
        ipdes = self.dest_IP_box.currentText()
        ifc = self.interface_box.currentText()
        portsrc = self.sourceport.text()
        portdst = self.lineEdit_2.text()
        protocol = self.protocolbox.currentText()
        payload = None
        flag = None

        for i in range (1):
            if self.payload_no.isChecked() == True:
                break
            elif self.payloadPcap.isChecked() ==True:
                temp_var_for_holding_int = int(self.xintotimes.text())
                payload = 'X' * temp_var_for_holding_int
                print(payload)
                break
            elif self.payload_string.isChecked() == True:
                payload = self.stringbox.text()
                print (payload)
                break
        #if self.source_IP_box.currentText() == (None or '') and self.dest_IP_box.currentText() == (None or ''):
        if self.tabWidget.currentIndex() == 0:
            if text == "clip":
                self.Clipboard.setText(temp.text.Ether_header(sr=ethsrc, ds=ethdst, ifc=ifc))
            elif text == "send":
                a = Backend_Process.eth(ethsrc, ethdst, ifc)
                self.statusBar.showMessage(str(a),5000)
        #elif self.sourceport.text() == (None or '') and self.lineEdit_2.text() ==(None or ''):
        elif self.tabWidget.currentIndex() == 1:
            if text == "clip":
                self.Clipboard.setText(temp.text.ip_header(ethsrc,ethdst,ipsrc,ipdes,ifc))
            elif text == "send":
                a = Backend_Process.ip_header(ethsrc, ethdst, ipsrc, ipdes, ifc)
                self.statusBar.showMessage(str(a), 5000)
        elif self.tabWidget.currentIndex() == 2:
            if text == "clip":
                self.Clipboard.setText(temp.text.transport_layer(protocol, portsrc, portdst, flag, payload, ipsrc, ipdes, ifc))
            if text == "send":
                a = Backend_Process.transport_layer(protocol, portsrc, portdst, flag, payload, ipsrc, ipdes, ifc)
                self.statusBar.showMessage(a, 5000)
            pass
    def deactivator(self,text):
        self.sourceport.setVisible(True)
        self.lineEdit_2.setVisible(True)
        self.groupBox_fo_flags.setHidden(False)

        if text == "ICMP":
            self.sourceport.setVisible(False)
            self.lineEdit_2.setVisible(False)
            self.groupBox_fo_flags.setHidden(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    prog=mainclass(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
