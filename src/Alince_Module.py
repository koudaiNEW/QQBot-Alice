
import time
import json  
import socket  
#import pandas as pd  
import requests  


SK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SK.bind(('127.0.0.1', 5720))  # 绑定IP及端口号
SK.listen(100)  

# 用来回复go-cqhttp上报，防止黄色的上报指令的输出，以及不可操控的程序错误
HttpResponseHeader = '''HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'''
# ---------------------------------------------------------------------------------------------------


# 存放获取的各种消息，以后有必要可能需要将各个消息存放的内容分开

#群内收到消息
dict_receive_group_1 = {'message_type': 'group',
                        'sender_msg': '',
                        'sender_name': '',
                        'sender_id': '',
                        'sender_msg_id': '',
                        'sender_group_id': '',
                        'sender_self_id': ''}
# 私聊收到消息
dict_receive_private = {'message_type': 'private',
                        'sender_msg': '',
                        'sender_name': '',
                        'sender_id': '',
                        'sender_msg_id': '',
                        'sender_group_id': '',
                        'sender_self_id': ''}

# ---------------------------------------------------------------------------------------------------
# 获取群的ID与名称，为了实现多群喊话做准备
group_id_list = []
group_name_list = []
# 在这里进行消息之间的同道连接，以及获得的消息的第一步处理，进行字典化
class Listener():  # 获取网页的json并获取消息
 
    def receiver(self):
        Client, Address = SK.accept()  # 被动接受TCP客户端连接,(阻塞式)等待连接的到来
        Reporting_events = Client.recv(1024).decode(encoding='utf-8')  # 主动初始化TCP服务器连接,并解码
 
        Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))  # 完整发送TCP数据,并回复go-cqhttp的上报
        # print(Reporting_events)
        Client.close()  # 关闭连接
        return Reporting_events  # 返回上报文字
 
    def Preprocessing_segment(self, Preprocess_Text):  # 处理上报文字
        # 用切片的方法把“{”找到，并获取后面的消息
        num = 0
        while True:
            num = num + 1
            # 用切片的方法把“{”找到，并获取后面的消息
            Processing_text = Preprocess_Text[num]
            if Processing_text == "{":
                Processed_text = Preprocess_Text[num:]
                # print(Processed_text)
                break
            else:
                pass
        return json.loads(Processed_text)  # 将字符串转变为字典



class Detach_Message():
    # 精细化分离消息，准备实现私聊与群聊的回复
    def group_separation(self, Set_to_be_separated):
 
        # 判断群私聊
        if Set_to_be_separated["post_type"] == "message":
            if Set_to_be_separated["message_type"] == "group":
                dict_receive_group_1['message_type'] = 'group'
                return None
 
            elif Set_to_be_separated["message_type"] == "private":
                dict_receive_private['message_type'] = 'private'
                return None
 
            else:
                pass
        else:  # 因为发送新消息时监听的消息集合与没有消息时的集合，不一样
            pass
        return None
 
    def Other_separation(self, Set_to_be_separated):  # 其他消息的获取
 
        if Set_to_be_separated["post_type"] == "message":
            sender_msg = Set_to_be_separated["message"]  # 获取消息
            sender_name = Set_to_be_separated["sender"]["nickname"]  # 获取发送者的名字
            sender_id = Set_to_be_separated["sender"]["user_id"]  # 获取发送者的QQ号
            sender_msg_id = Set_to_be_separated["message_id"]  # 获取消息的ID
            sender_self_id = Set_to_be_separated["self_id"]  # 获取自己的QQ号
            # return sender_msg,sender_name,sender_id,sender_msg_id
            if Set_to_be_separated["message_type"] == "group":
                sender_group_id = Set_to_be_separated["group_id"]  # 获取发送群的群号
 
                dict_receive_group_1['sender_msg'] = sender_msg
                dict_receive_group_1['sender_name'] = sender_name
                dict_receive_group_1['sender_id'] = str(sender_id)
                dict_receive_group_1['sender_msg_id'] = str(sender_msg_id)
                dict_receive_group_1['sender_group_id'] = str(sender_group_id)
                dict_receive_group_1['sender_self_id'] = str(sender_self_id)
            else:
                dict_receive_private['sender_msg'] = sender_msg
                dict_receive_private['sender_name'] = sender_name
                dict_receive_private['sender_id'] = str(sender_id)
                dict_receive_private['sender_msg_id'] = str(sender_msg_id)
                dict_receive_private['sender_self_id'] = str(sender_self_id)
        else:
            pass
 
        return None

class Send_operation():  # 可视化获取的消息类别等

    def Send_operation_first(self):
        # 输出获取到的消息
        if dict_receive_group_1['message_type'] == 'private':
            print('>>>:' * 3 + "获取:  \n" + "名字:  " + dict_receive_group_1['sender_name'] + '\n' + 'QQ号:  ' + dict_receive_group_1['sender_id'] + '\n' + "消息内容:  " + dict_receive_group_1['sender_msg'] + '\n' + '消息ID：' + dict_receive_group_1['sender_msg_id'])
        elif dict_receive_group_1['message_type'] == 'group':
            print('>>>:' * 3 + "获取:  \n" + "名字:  " + dict_receive_group_1['sender_name'] + '\n' + 'QQ号:  ' + dict_receive_group_1['sender_id'] + '\n' + '群号:  ' + dict_receive_group_1['sender_group_id'] + '\n' + "消息内容:  " + dict_receive_group_1['sender_msg'] + '\n' + '消息ID: ' + dict_receive_group_1['sender_msg_id'])
        else:
            pass
        return None
 
    def Send_operation_second(self, msg, *age):  # 进行回复
        # 输出逻辑回答的消息
        #url = 'http://127.0.0.1:5700'
        if msg['message_type'] == 'private':
            urls = "http://127.0.0.1:5700/send_private_msg?user_id=" + str(msg['user_id']) + '&message=' + msg['message']
            answer_post_use = requests.post(url=urls).json()  # 发送消息
            print('>>>:' * 3 + "已回答:" + "\n " + msg['message'],flush=True)
        elif msg['message_type'] == 'group':
            urls = 'http://127.0.0.1:5700/send_group_msg?group_id=' + str(msg['group_id']) + '&message=' + msg['message']
            answer_post_use = requests.post(url=urls)  # 发送消息
            print('>>>:' * 3 + "\n" + "已回答:" + msg['message'],flush=True)
        else:
            pass
 

class Clear_Dictionary():  
    def clear_(self):
        dict_receive_group_1['sender_msg'] = ''
        dict_receive_group_1['sender_name'] = ''
        dict_receive_group_1['sender_id'] = ''
        dict_receive_group_1['sender_msg_id'] = ''
        dict_receive_group_1['sender_group_id'] = ''
        dict_receive_group_1['message_type'] = ''
        dict_receive_group_1['sender_self_id'] = ''
 