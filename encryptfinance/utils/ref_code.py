import uuid


def ref_generator():
    code = str(uuid.uuid4()).replace("-", "")[:7]
    return code
