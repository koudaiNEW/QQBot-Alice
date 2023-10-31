import Alince_Module
import string
import Alince_BA
import threading

BA_threadingLock = threading.Lock()  #BA模块回复用线程锁



#线程马内甲！
def Thread_Management():
    try:
        msg = Alince_Module.Listener().Preprocessing_segment(Alince_Module.Listener().receiver())  # 解码消息
        print(msg,flush=True)

        BA_thread_1 = threading.Thread(target=Alice_go, args=(msg))
        BA_thread_1.start()
    except:
        print('Error port 1, 线程错误',flush=True)



#独立分隔，自动创建销毁，防止内存溢出等问题
def Alice_go(msg):
    try:
        Alince_Module.Detach_Message().Other_separation(msg)   # 细分解码消息
        msg_get = msg['message']  # 保存原收到信息

        Alince_BA.Blue_Archives().BA_analysis(msg)  #解析BA消息
    except:
        print('Error port 2, BA消息解析错误',flush=True)

    try:
        if msg_get == msg['message'] or msg['message'] == None:  # 未解析到有用信息
            return None

        BA_threadingLock.acquire(timeout=60) #拿锁
        Alince_Module.Send_operation().Send_operation_second(msg)  # 发送信息
        BA_threadingLock.release  #释放锁
    except:
        print('Error port 3, BA消息拿锁回复错误',flush=True)



if __name__ == '__main__':
    while True:
        try:
            Thread_Management()
        except:
            print('未知错误',flush=True)
    

