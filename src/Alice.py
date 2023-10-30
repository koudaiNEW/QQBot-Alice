import Alince_Module
import string
import Alince_BA


if __name__ == '__main__':
    while True:
        try:
            msg = Alince_Module.Listener().Preprocessing_segment(Alince_Module.Listener().receiver())  # 解码消息
            print(msg)
            Alince_Module.Detach_Message().Other_separation(msg)   # 细分解码消息
            msg_get = msg['message']  # 保存原收到信息
            Alince_BA.Blue_Archives().BA_analysis(msg)  #解析BA消息
            if msg_get == msg['message'] or msg['message'] == None:  # 未解析到有用信息
                continue
            Alince_Module.Send_operation().Send_operation_second(msg)  # 发送信息
        except:
            print('未知错误',flush=True)
    

