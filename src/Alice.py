import Alince_Module
import string
import Alince_BA
import threading

Reply_threadingLock = threading.Lock()  #回复用线程锁



#线程马内甲！
def Thread_Management():
    global last_msg
    #解码
    try:
        raw_msg = Alince_Module.Listener().Preprocessing_segment(Alince_Module.Listener().receiver())  # 解码消息
        Alince_Module.Detach_Message().Other_separation(raw_msg)   # 细分解码消息
        print(raw_msg,flush=True)
        new_msg = raw_msg['message']  # 保存原收到信息
    except:
        print('Error port 4, 解码错误',flush=True)

    #BA线程
    try:
        if '/BA攻略' in raw_msg['message']:
            try:
                BA_thread = threading.Thread(target=Alice_BA_Go, kwargs=raw_msg)  #传入字典，下同
                BA_thread.start()
            except:
                print('Error port 1, BA线程错误',flush=True)
    except:
        print('Error port 7',flush=True)

    #复读
    try:
        if (new_msg in last_msg) and (last_msg in new_msg):
            try:
                last_msg = 'last_msg' 
                new_msg = 'new_msg'
                REP_thread = threading.Thread(target=Alice_Repeater_Go, kwargs=raw_msg)
                REP_thread.start()
            except:
                print('Error port 5, 复读线程错误',flush=True)
    except:
        print('Error port 8',flush=True)
    last_msg = new_msg

#复读机
def Alice_Repeater_Go(**msg):
    try:
        repeater_msg = msg
        Reply_threadingLock.acquire(timeout=60) #拿锁
        Alince_Module.Send_operation().Send_operation_second(repeater_msg)  # 发送信息，消息原路返回
        Reply_threadingLock.release()  #释放锁
    except:
        print('Error port 6, 复读机消息拿锁回复错误',flush=True)


#独立分隔，自动创建销毁，防止内存溢出等问题
def Alice_BA_Go(**msg):
    #BA模块
    try:
        BA_msg = msg  #安全
        if Alince_BA.Blue_Archives().BA_analysis(BA_msg) :  #解析BA消息
            try:
                Reply_threadingLock.acquire(timeout=60) #拿锁
                Alince_Module.Send_operation().Send_operation_second(BA_msg)  # 发送信息，消息原路返回
                Reply_threadingLock.release()  #释放锁
            except:
                print('Error port 3, BA消息拿锁回复错误',flush=True)
        else :
            print('BA信息无效',flush=True)
    except:
        print('Error port 2, BA消息解析错误',flush=True)




if __name__ == '__main__':
    while True:
        try:
            Thread_Management()
        except:
            print('未知错误',flush=True)
    

