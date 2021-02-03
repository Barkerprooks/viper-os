#!/usr/bin/env python3
import subprocess, errno
import os, sys, time
import tarfile, zlib
import threading
import serial

VERSION = "0.0.5"
SYSROOT = "system"

upy_installed = True

def timeout(proc):
    global upy_installed
    if proc.poll() is None:
        try:
            proc.kill()
            upy_installed = False
        except OSError as e:
            if e.errno != errno.ESRCH:
                raise

def compress(path):
    zipname = path + ".zz"
    with open(path, "rb") as i:
        uncompressed = i.read()
        with open(zipname, "wb+") as o:
            o.write(zlib.compress(uncompressed))
    return zipname

def r_tarzip(directory):

    tarname = directory + ".tar"

    with tarfile.open(tarname, 'w') as tar:
        for fd in os.listdir(directory):
            path = directory + '/' + fd
            if os.path.isdir(path):
                zipped = r_tarzip(path)
                tar.add(zipped)
            elif os.path.isfile(path):
                delete = compress(path)
                tar.add(delete)
                os.remove(delete)

    zipped = compress(tarname)
    os.remove(tarname)

    for entry in os.fwalk(directory):
        for f in entry[2]:
            if f.endswith(".zz"):
                os.remove(entry[0] + '/' + f)

    return zipped

def main(argv):

    proc = subprocess.Popen(["ampy", "-p", "/dev/ttyUSB0", "run", "bin/version"])
    thread = threading.Timer(3, timeout, [proc])

    thread.start()
    
    if not upy_installed:
        print("MicroPython not installed")
        os.system("esptool.py -p /dev/ttyUSB0 erase_flash")
        os.system("esptool.py -p /dev/ttyUSB0 -b 460800 write_flash -z 0x1000 bin/upy_v1.13.bin")

    thread.join()
    thread.cancel()

    print("compressing root level directories...")
    zipname = r_tarzip(SYSROOT)

    print("wiping file system (backups not enabled)")
    delay = 5
    while delay:
        msg = "press ctrl+c to cancel... will continue in %s" % delay
        print(msg, end='')
        print("\033[%dD" % len(msg), end='')
        if delay == 1:
            print()
        sys.stdout.flush()
        time.sleep(1)
        delay -= 1

    os.system("ampy -p /dev/ttyUSB0 run bin/nuke-fs")

    print("uploading...")
    with subprocess.Popen(["ampy", "-p", "/dev/ttyUSB0", "put", zipname], stdout=subprocess.PIPE) as proc:
        if proc.stdout.read():
            print("failed to upload")
        else:
            print("upload complete")

    os.remove(zipname)

    print("unpacking file system...")
    os.system("ampy -p /dev/ttyUSB0 run bin/extract-fs") 
    os.system("ampy -p /dev/ttyUSB0 run bin/version")
    os.system("ampy -p /dev/ttyUSB0 run system/bin/dsk")


if __name__ == "__main__":
    print("ViperOS -- Install Tool")
    print(f"viper v{VERSION}")
    if os.getuid():
        print("must run as root for access to serial port (device), sorry! ;(")
        print("use: sudo %s" % sys.argv[0])
        exit(0)
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("\nctrl+c pressed")
        exit(0)

