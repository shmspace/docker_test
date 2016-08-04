#coding=utf-8

# 对象代理
# 用于解决需要在包调用与业务代码之间增加一些其他操作的场景
# 比如：应用程序中使用redis包对象，我们希望在redis包对象出错时尝试一次重连
# 又比如: 我们希望在调用包的某方法时纪录日志
# 使用此代理容器可以在不修改包及业务代码的情况下，实现以上功能

# 代理基类
# 该基类实现代理转发的基本功能，子类根据业务需要继承该类，并实现绑定方法
# 注意：为了避免透传的时候命名冲突，代理容器所有属性或者方法需要以abc_agent_开头
class AgentContainer(object):
    # 初始化类对象，将代理对象添加到属性中
    def __init__(self, current_object):
        self.abc_agent_current_object = current_object
        self.abc_agent_current_func = ""
        self.abc_agent_error = ""
        self.abc_agent_debug = True

    # 代理方法，用于代理对象方法的透传
    def abc_agent_container(self, *args, **kargs):
        result = None
        self.abc_agent_before_container(*args, **kargs)
        func = getattr(self.abc_agent_current_object, self.abc_agent_current_func)
        try:
            result = func(*args, **kargs)
        except Exception,e:
            self.abc_agent_object_error(e)

        self.abc_agent_after_container(*args, **kargs)
        return result

    # 透传前的回调
    def abc_agent_before_container(self, *args, **kargs):
        self.abc_agent_log("before container")

    # 透传后的回调
    def abc_agent_after_container(self, *args, **kargs):
        self.abc_agent_log("after container")

    # 调用代理对象方法出错后触发
    def abc_agent_object_error(self, except_info):
        self.abc_agent_log("object error")
        self.abc_agent_error = except_info
        return except_info

    # 调用方法或者属性触发
    def __getattr__(self, func_name):
        self.abc_agent_log("container function is:",func_name)
        self.abc_agent_current_func = func_name
        func = getattr(self.abc_agent_current_object, func_name)
        if not callable(func):
            return func
        else:
            return self.abc_agent_container

    def __setattr__(self, attr_name, attr_value):
        pre_str = "abc_agent_"
        if attr_name.startswith(pre_str):
            object.__setattr__(self, attr_name, attr_value)
        else:
            self.abc_agent_before_container(attr_name, attr_value)
            setattr(self.abc_agent_current_object, attr_name, attr_value)
            self.abc_agent_after_container(attr_name, attr_value)

    def abc_agent_log(self, *args):
        if self.abc_agent_debug:
            print "".join(args)

# 应用举例：
# 场景：使用代理容器代理redis，当调用redis出错时，重连redis

# 需要代理的类对象
class Redis(object):

    def hget(self, *args,**kargs):
        return "show is ok"

    def hset(self, k, v):
        #模拟redis hset方法报错
        raise Exception("offline")

    def __init__(self):
        self.name = "polo"

# 基于代理基类派生出的redis高可用代理
# 当捕获到redis错误后对redis进行重连，完成后继续抛出错误
class HRedis(AgentContainer):
    def __init__(self):
        redis = Redis()
        AgentContainer.__init__(self, redis)
        #是否打印调试信息，调试信息打印方法可以重载为其他日志输出方式
        self.abc_agent_debug = True

    def abc_agent_object_error(self, except_info):
        self.abc_agent_current_object = Redis()
        raise except_info



redis = HRedis()
print redis.hget("ssssss")
print '========='
print redis.hset('a', 'b')
print "============"
