"""
Render jinja data
"""
import tempfile

try:
    import _jsonnet

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


async def render(hub, data):
    """
    Render the given data through jsonnet
    """
    if not isinstance(data, (str, bytes, bytearray)):
        data = data.read()
    with tempfile.NamedTemporaryFile("w+") as fp:
        fp.write(data)
        fp.flush()
        ret = _jsonnet.evaluate_file(fp.name)

    return hub.rend.json.render(ret)
