import hashlib
from urllib.parse import quote


def encry_sign(parm):
    str_parm = ''
    for p in sorted(parm):
        if isinstance(parm[p], str):
            str_parm = str_parm + str(p) + "=" + str(quote(parm[p])) + "&"
            continue
        str_parm = str_parm + str(p) + "=" + str(parm[p]) + "&"
    if str_parm:
        str_parm = str_parm[:-1]
    hl = hashlib.md5()
    hl.update(str_parm.encode(encoding='utf-8'))
    return hl.hexdigest().upper()


mobile_id = '999991'
key = '0MUy9P2xuZRLxpoAIFoil3WZAQgvwaip'

sign = encry_sign({'cust_id': mobile_id, 'key': key})
print(sign)
