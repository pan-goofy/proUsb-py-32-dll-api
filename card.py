import ctypes
import os
import configparser
lib = ctypes.WinDLL('proRFL.dll')
class Card():
    cardBuffer = ''
    cf = configparser.ConfigParser()
    cf.read('./config.ini', encoding='utf-8')
    hotelId = int(cf.get("Sections","hotelId"))
    d12 = cf.get("Sections","d12")
    lockNo = ''
    buf =''
    def strat(self):
        #buf = '551501C9011F30E38181010061E76B97E80B800505EA2493FF0000000000000000000000'.encode("utf-8")
        self.openUsb()
        self.readDll()
        #self.sound(100)
        self.readCard()
        #self.readCardType()
        self.cardLock()
        #self.readCardTime()
        #self.writeCard()
        #self.clearCard()
    def openUsb(self):
        result = lib.initializeUSB(str(self.d12))
        return {'status':result}
    def readDll(self):
        # 调用函数
        buffer_size = 256
        buffer = (ctypes.c_char * buffer_size)()
        result = lib.GetDLLVersion(buffer)    
        # 检查调用结果
        version = buffer.value.decode("utf-8")
        return {'status':result,'version':version}   
    def sound(self,timeer):
        result = lib.Buzzer(self.d12,timeer)
        return {'status':result}
    def writeCard(self,dai,llock,cardNo,pdoors,bdate,edate,lockNo):
        dai = dai.encode()
        llock = llock.encode()
        cardNo = cardNo.encode()
        pdoors = pdoors.encode()
        bdate = bdate.encode()
        edate = edate.encode()
        lockNo = lockNo.encode()
        result = lib.GuestCard(self.d12,self.hotelId,cardNo,dai,llock,pdoors,bdate,edate,lockNo,self.cardBuffer)    
        return {'status':result}
                   
    def readCard(self):
        buffer_size = 255
        buffer = (ctypes.c_char * buffer_size)()
        result = lib.ReadCard(self.d12,buffer)   
        card = '' 
        if result ==0:
            self.cardBuffer = buffer
            card = buffer.value.decode("utf-8")
        #print('buffer',buffer)
        return {'status':result,'cardBuffer':card}    
    #注销卡片        
    def clearCard(self):
        result = lib.CardErase(self.d12,self.hotelId,self.getBuf())
        if result ==0:
            print('clear ok')
    def readCardType(self):
        buffer_size = 1
        CardType = (ctypes.c_ubyte * buffer_size)()
        result = lib.GetCardTypeByCardDataStr(self.getBuf(),CardType)
        cardType = ''    
        if result == 0:
            for i in CardType:
                cardType = i
        else:
            print(result,'error')    
        return {'status':result,'cardType':cardType}    
    def getBuf(self):
        buffer_size = 255
        buffer = (ctypes.c_char * buffer_size)()
        result = lib.ReadCard(self.d12,buffer) 
        print('result:wei',result)  
        if result == 0:
            buf = buffer
            return buf
        return buffer
    def cardLock(self):
        lock = (ctypes.c_ubyte * 8)()
        result = lib.GetGuestLockNoByCardDataStr(self.hotelId,self.getBuf(), lock)  
        if result == 0:
            for i in lock:
                self.lockNo += str(chr(i))        
        print('cardNo',self.lockNo)        
        return {'status':result,'lockNo':self.lockNo}    
    def readCardTime(self):
        cTime = (ctypes.c_byte *10)()
        result = lib.GetGuestETimeByCardDataStr(self.hotelId,self.getBuf(),cTime)
        cardDate = ''
        if result ==0:
            for i in cTime:
                cardDate += str(chr(i))
        print(cardDate) 
        return {'status':result,'cardDate':cardDate}              
if __name__ =="__main__":
    card = Card()
    card.strat()