#!/usr/bin/python3
# author: 0xtom7
# github: tom7voldemort

import argparse
import base64
import zlib
import os
import sys
import hashlib
import random
from sys import stdout
from time import sleep

reset = "\033[0m"
red = "\033[31m"
darkgreen = "\033[38;5;22m"
orange = "\033[38;5;208m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
bold = "\033[1m"
dim = "\033[2m"
italic = "\033[3m"
underline = "\033[4m"
blink = "\033[5m"

banner = f"""
{darkgreen}                        {red}___{darkgreen}         ___ __       __  
{darkgreen}  ____________  ______ {red}|__ \\{darkgreen} ____ _/ (_) /______/ /_ 
{darkgreen} / ___/ ___/ / / / __ \\{red}__/ /{darkgreen}/ __ `/ / / __/ ___/ __ \\
{darkgreen}/ /__/ /  / /_/ / /_/ /{red} __/{darkgreen}/ /_/ / / / /_/ /__/ / / /
{darkgreen}\\___/_/   \\__, / .___/{red}____/{darkgreen}\\__, /_/_/\\__/\\___/_/ /_/ 
{darkgreen}         /____/_/         /____/                     
{bold}{red}  + {dim}{white}{italic}cryp2glitch{reset}
{bold}{red}  + {dim}{white}{italic}author: tom7{reset}
{bold}{red}  + {dim}{white}{italic}github: https://github.com/tom7voldemort{reset}
{bold}{red}  + {dim}{white}{italic}version: 1.0{reset}
{reset}
"""

class strobject:
    def clear():
        os.system("cls" if os.name == "nt" else "clear")
        
    def typewrite(msg, delay=0.01):
        for ch in msg:
            stdout.write(ch)
            stdout.flush()
            sleep(delay)
        print()

    def info(msg):
        strobject.typewrite(f"{bold}{dim}{white}[{darkgreen}info +{white}] {msg}{reset}")

    def warnings(msg):
        strobject.typewrite(f"{bold}{dim}{white}[{orange}warn !{white}] {msg}{reset}")

    def errors(msg):
        strobject.typewrite(f"{bold}{dim}{white}[{red}error x{white}] {msg}{reset}")


LOADER = (
    "import base64 as b64,zlib as zl,hashlib as hs,random as rn,sys as sy\n"
    "{FAKE}\n"
    "def derivekey(sd):\n"
    "    k=hs.sha3_512(sd).digest()\n"
    "    for i in range(1337):k=hs.sha3_512(k+sd).digest()\n"
    "    return k\n"
    "def xorstream(d,k):\n"
    "    o=bytearray(len(d));kl=len(k)\n"
    "    for i,b in enumerate(d):o[i]=b^k[i%kl]^((i*0x5A^0xA5)&0xFF)\n"
    "    return bytes(o)\n"
    "def unshuffle(d,k):\n"
    "    sd=int.from_bytes(hs.md5(k).digest(),'big');rng=rn.Random(sd)\n"
    "    ix=list(range(len(d)));rng.shuffle(ix);o=bytearray(len(d))\n"
    "    for nw,ol in enumerate(ix):o[ol]=d[nw]\n"
    "    return bytes(o)\n"
    "def deobfstr(s):\n"
    "    us=''.join(chr(ord(c)-3)if c.isalpha()else c for c in s)\n"
    "    return b64.b85decode(us.encode()).decode()\n"
    "def run():\n"
    "    salt={SALT};chk={CHECK};obk={OBFKEY};chunks={CHUNKS}\n"
    "    pw=input(deobfstr(obk)+': ').encode()\n"
    "    key=derivekey(b64.b64decode(salt)+pw)\n"
    "    raw=b''.join(b64.b64decode(c)for c in chunks)\n"
    "    raw=unshuffle(raw,key)\n"
    "    raw=xorstream(raw,key)\n"
    "    try:\n"
    "        raw=zl.decompress(raw)\n"
    "    except Exception:\n"
    "        print('\\033[31m[!] Wrong password or corrupted file.\\033[0m');sy.exit(1)\n"
    "    if hs.sha3_256(raw).digest()!=b64.b64decode(chk):\n"
    "        print('\\033[31m[!] Integrity check failed.\\033[0m');sy.exit(1)\n"
    "    exec(compile(raw,'<protected>','exec'),{'__name__':'__main__'})\n"
    "run()\n"
)


def DeriveKey(Seed):
    Key = hashlib.sha3_512(Seed).digest()
    for i in range(1337):
        Key = hashlib.sha3_512(Key + Seed).digest()
    return Key

def XorStream(Data, Key):
    Out  = bytearray(len(Data))
    KLen = len(Key)
    for i, b in enumerate(Data):
        Out[i] = b ^ Key[i % KLen] ^ ((i * 0x5A ^ 0xA5) & 0xFF)
    return bytes(Out)

def Shuffle(Data, Key):
    Seed = int.from_bytes(hashlib.md5(Key).digest(), 'big')
    Rng  = random.Random(Seed)
    Idx  = list(range(len(Data)))
    Rng.shuffle(Idx)
    Out  = bytearray(len(Data))
    for New, Old in enumerate(Idx):
        Out[New] = Data[Old]
    return bytes(Out)

def Unshuffle(Data, Key):
    Seed = int.from_bytes(hashlib.md5(Key).digest(), 'big')
    Rng  = random.Random(Seed)
    Idx  = list(range(len(Data)))
    Rng.shuffle(Idx)
    Out  = bytearray(len(Data))
    for New, Old in enumerate(Idx):
        Out[Old] = Data[New]
    return bytes(Out)


def SplitChunks(Data, Key):
    Seed  = int.from_bytes(Key[:4], 'big')
    Rng   = random.Random(Seed)
    Parts = []
    Pos   = 0
    while Pos < len(Data):
        Size = Rng.randint(16, 64)
        Parts.append(Data[Pos:Pos + Size])
        Pos += Size
    return Parts

def ObfuscateString(s):
    Encoded  = base64.b85encode(s.encode()).decode()
    Shuffled = ''.join(chr(ord(c) + 3) if c.isalpha() else c for c in Encoded)
    return Shuffled

def BuildFakeVars():
    Lines = []
    for i in range(random.randint(6, 12)):
        Name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(6, 14)))
        Val  = random.randint(0, 0xFFFFFFFF)
        Lines.append(f"{Name}={Val}")
    return ';'.join(Lines)

def Encrypt(InputPath, OutputPath):
    if not os.path.exists(InputPath):
        strobject.info(f" File not found: {InputPath}")
        sys.exit(1)
        
    with open(InputPath, 'rb') as f:
        Raw = f.read()

    try:
        compile(Raw, InputPath, 'exec')
    except SyntaxError as e:
        strobject.info(f" Syntax error in source: {e}")
        sys.exit(1)

    Checksum = hashlib.sha3_256(Raw).digest()
    Salt     = os.urandom(32)
    Password = input(" Set encryption password: ").encode()
    Confirm  = input(" Confirm password: ").encode()

    if Password != Confirm:
        strobject.info(" Passwords do not match.")
        sys.exit(1)

    Key = DeriveKey(Salt + Password)
    Compressed = zlib.compress(Raw, level=9)
    Xored = XorStream(Compressed, Key)
    Shuffled = Shuffle(Xored, Key)
    Chunks = SplitChunks(Shuffled, Key)
    ChunkLiterals = repr([base64.b64encode(c).decode() for c in Chunks])
    SaltLit = repr(base64.b64encode(Salt).decode())
    CheckLit = repr(base64.b64encode(Checksum).decode())
    ObfKey = repr(ObfuscateString(" Password"))

    Output = (LOADER
        .replace("{FAKE}",   BuildFakeVars())
        .replace("{SALT}",   SaltLit)
        .replace("{CHECK}",  CheckLit)
        .replace("{OBFKEY}", ObfKey)
        .replace("{CHUNKS}", ChunkLiterals)
    )

    with open(OutputPath, 'w') as f:
        f.write(Output)

    strobject.info(f"\n Encrypted  : {InputPath}")
    strobject.info(f" Output     : {OutputPath}")
    strobject.info(f" Original   : {len(Raw)} bytes")
    strobject.info(f" Protected  : {len(Output.encode())} bytes")
    strobject.info(" Layers     : zlib → XOR stream cipher → byte shuffle → chunk split")
    strobject.info(" Key derive : SHA3-512 x1337 rounds + random 32-byte salt")
    strobject.info(" Integrity  : SHA3-256 verified at runtime")
    strobject.info(" Obfuscation: fake vars + obfuscated prompt string + chunked payload")
    strobject.info(f" Salt       : {Salt.hex()[:32]}...")


def Decrypt(InputPath, OutputPath):
    if not os.path.exists(InputPath):
        strobject.info(f" File not found: {InputPath}")
        sys.exit(1)

    with open(InputPath, 'r') as f:
        Source = f.read()

    FoundSalt   = None
    FoundCheck  = None
    FoundChunks = None

    for Line in Source.splitlines():
        L = Line.strip()
        if 'salt=' in L and 'chk=' in L and 'chunks=' in L:
            try:
                NS = {}
                exec("import base64 as b64\n" + L, NS)
                FoundSalt   = base64.b64decode(NS['salt'])
                FoundCheck  = base64.b64decode(NS['chk'])
                FoundChunks = [base64.b64decode(c) for c in NS['chunks']]
                break
            except Exception:
                continue

    if FoundSalt is None:
        strobject.info(" Could not parse encrypted file. Was it made with this tool?")
        sys.exit(1)

    Password = input(" Enter decryption password: ").encode()
    Key = DeriveKey(FoundSalt + Password)
    Raw = b''.join(FoundChunks)
    Raw = Unshuffle(Raw, Key)
    Raw = XorStream(Raw, Key)

    try:
        Raw = zlib.decompress(Raw)
    except zlib.error:
        strobject.info(" Decryption failed — wrong password or corrupted file.")
        sys.exit(1)

    if hashlib.sha3_256(Raw).digest() != FoundCheck:
        strobject.info(" Integrity check failed — wrong password or corrupted file.")
        sys.exit(1)

    with open(OutputPath, 'wb') as f:
        f.write(Raw)

    strobject.info(f"\n Decrypted  : {InputPath}")
    strobject.info(f" Output     : {OutputPath}")
    strobject.info(f" Recovered  : {len(Raw)} bytes")
    strobject.info(" Integrity  : OK")


def Main():
    Parser = argparse.ArgumentParser(
        prog="encrypt.py",
        description="Advanced Python obfuscation — multi-layer encryption + integrity check",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python3 encrypt.py -f script.py    -o protected.py -e\n"
            "  python3 encrypt.py -f protected.py -o recovered.py -d"
        )
    )
    Parser.add_argument("-f", "--file",    required=True, metavar="<file.py>",   help="Input file")
    Parser.add_argument("-o", "--output",  required=True, metavar="<output.py>", help="Output file")
    Parser.add_argument("-e", "--encrypt", action="store_true", help="Encrypt and obfuscate")
    Parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt and recover")
    Args = Parser.parse_args()

    if not Args.encrypt and not Args.decrypt:
        Parser.error("Specify -e to encrypt or -d to decrypt.")
    if Args.encrypt and Args.decrypt:
        Parser.error("Use either -e or -d, not both.")

    if Args.encrypt:
        Encrypt(Args.file, Args.output)
    else:
        Decrypt(Args.file, Args.output)


if __name__ == "__main__":
    strobject.clear()
    print(banner)
    Main()
