from generical_logging import GenericalLogging


def div(*args) -> float:
    return args[0] / args[1]


if __name__ == '__main__':
    try:
        result: float = div(2, 0)
        print(f"result: {result}")
    except ZeroDivisionError as e:
        gl = GenericalLogging(".")
        gl.logging_this_with_rotating(str(e), level="E", formater=["A"], max_bytes=1024, backup_count=10)
