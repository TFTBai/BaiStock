import logging as log

'''
日志类
'''

# 日志配置
log.basicConfig(level=log.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='baseStock.log',
                filemode='w')

#################################################################################################
# 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = log.StreamHandler()
console.setLevel(log.INFO)
formatter = log.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
log.getLogger('').addHandler(console)


#################################################################################################

def info(msg):
    log.info(msg)
