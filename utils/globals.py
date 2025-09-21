
class init_status: # 初始化状态
    value = True

class ui_stream: # ui消息流
    max_length=100
    text_list=[]
    text_str=""
    stop=False

    @classmethod # 类方法,无需实例化即可修改类属性
    def push(cls,msg:str):
        if len(cls.text_list)>=cls.max_length:
           del cls.text_list[0]
        cls.text_list.append(msg)
        cls.text_str = '\n'.join(cls.text_list)
    