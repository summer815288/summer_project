class A:
    def ping(self):
        print('ping:', self)


class B(A):
    def pong(self):
        print('pong:', self)


class C(A):
    def pong(self):
        print('PONG:', self)


class D(B, C):
    def ping(self):
        super().ping()

        print('post-ping:', self)

    def pingpong(self):
        self.ping()

        super().ping()
        self.pong()
        super().pong()
        C.pong(self)


d = D()
d.pong()  # 直接调用 d.pong() 运行的是 B 类中的版本
C.pong(d)  # ➋超类中的方法都可以直接调用，此时要把实例作为显式参数传入。
d.ping()
d.pingpong()