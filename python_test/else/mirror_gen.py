import contextlib


@contextlib.contextmanager  # 应用 contextmanager 装饰器
def looking_glass():
    import sys
    original_write = sys.stdout.write  # ➋贮存原来的 sys.stdout.write 方法

    def reverse_write(text):  # ➌定义自定义的 reverse_write 函数；在闭包中可以访问 original_write
        original_write(text[::-1])
        sys.stdout.write = reverse_write  # ➍把 sys.stdout.write 替换成 reverse_write
        yield 'JABBERWOCKY'  # ➎➎ 产出一个值，这个值会绑定到 with 语句中 as 子句的目标变量上。执行 with 块中的代码时，这个函数会在这一点暂停
        sys.stdout.write = original_write  # ➏控制权一旦跳出 with 块，继续执行 yield 语句之后的代码；这里是恢复成原来的 sys.stdout.write 方法
