import Alince_Module
import string
import Alince_BA
import threading
import Alince_Anime
import time

Reply_threadingLock = threading.Lock()  #回复用线程锁

#线程马内甲！
def Thread_Management():
    global last_msg
    #解码
    try:
        raw_msg = Alince_Module.Listener().Preprocessing_segment(Alince_Module.Listener().receiver())  # 解码消息
        Alince_Module.Detach_Message().Other_separation(raw_msg)   # 细分解码消息
        print(time.strftime("%Y-%m-%d %H:%M:%S") + str(raw_msg),flush=True)
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
        if new_msg in last_msg and last_msg in new_msg:
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


#Anime模块线程
def Alince_Anime_Go():
    Anime_msg = {
        'message_type':'group',
        }
    Alince_Anime.Anime_Analysis.Anime_Flash_Anime_Dict(1)  #爬取信息
    while True:
        try:
            Alince_Anime.Anime_Analysis.Anime_Main(1)  #时间轮询
        except:
            print('Anime线程错误 1', flush=True)
        #推送
        try:
            for name in Alince_Anime.title:
                if Alince_Anime.Anime[name]['ready_To_Push'] == 1 and Alince_Anime.Anime[name]['push_Flag'] == 0:
                    Anime_msg['group_id'] = 521609770  #群号
                    Anime_msg['message'] = '番剧更新\n[CQ:image,file=' + Alince_Anime.Anime[name]['image'][0] +']\n\n'+ name +'\n\n版权方：\n'  #推送格式
                    for push_Addr in Alince_Anime.Anime[name]['copyright']:
                        Anime_msg['message'] = Anime_msg['message'] + push_Addr +'\n'
                    Reply_threadingLock.acquire(timeout=60) #拿锁
                    Alince_Module.Send_operation().Send_operation_second(Anime_msg)  # 发送信息
                    Reply_threadingLock.release()  #释放锁
                    Alince_Anime.Anime[name]['push_Flag'] = 1
                    time.sleep(1.5)  
        except:
            print('Anime线程错误 2', flush=True)
        time.sleep(60)  #一分钟轮询




if __name__ == '__main__':
    Anime_thread = threading.Thread(target=Alince_Anime_Go)  #Anime线程
    Anime_thread.start()
    while True:
        try:
            Thread_Management()
        except:
            print('未知错误',flush=True)
    

