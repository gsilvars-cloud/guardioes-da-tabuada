import io
P='site/index.html'
class G:
    def __init__(s): s.t=open(P,encoding='utf-8').read()
    def rep(s,old,new,count=1):
        n=s.t.count(old); assert n==count, f'esperava {count}, achei {n}: {old[:90]!r}'
        s.t=s.t.replace(old,new)
    def save(s): open(P,'w',encoding='utf-8').write(s.t); print('salvo',len(s.t)//1024,'KB')
