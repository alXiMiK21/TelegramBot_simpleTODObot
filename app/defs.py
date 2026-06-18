import time

def timeNow(type):
    match type:
        case 't': return time.strftime("%H:%M:%S", time.localtime())
        case 'd': return time.strftime("%Y-%m-%d", time.localtime())
        case 'td': return time.strftime("%H:%M:%S %Y-%m-%d", time.localtime())