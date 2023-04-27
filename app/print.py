from pathlib import Path

with open(Path("./web/742afed192a0391065163340276dd243/file.txt")) as file:
    content = file.read()
    content_repr = repr(content)
    print(content_repr)
