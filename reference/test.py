import cloud

def square(x):
    return x*x

jid = cloud.call(square, 3)
print cloud.result(jid)