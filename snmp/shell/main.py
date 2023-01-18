import os
import sys
from timeit import default_timer as timer
from datetime import timedelta

start = timer()

lines = []

READ_KEY = "public"
WRITE_KEY = "private"
IP_ADDR = "192.168.0.222"

START_OID = ".1.3.6.1.2.1"

TYPE_DICT = {
    "INTEGER": "i",
    "Counter32": "u",
    "Gauge32": "u",
    "Timeticks": "t",
    "STRING": "s",
    "Hex-STRING": "x",
    "DECIMAL STRING": "d",
    "Counter64": "U",
    "IpAddress": "a",
    "OID": "o",
}


class Line:
    def __init__(self, oid, type, value) -> None:

        self.oid = oid
        self.type = type

        if type == "Timeticks":
            value = value[value.find("(") + 1 : value.find(")")]

        self.value = value

        lines.append(self)

    def printInfo(self):

        print(f"\nOID = {self.oid}\nType = {self.type}\nValue = {self.value}\n")


def printHelp():

    print(
        """   snmpwalk = -w (ip address) (public key) (start oid optional)
                snmpget = -g (ip address) (public key) (oid)
                snmpset
          """
    )


def readTempFile():

    with open("temp", "r") as tempFile:

        tempLines = tempFile.readlines()

        for tempLine in tempLines:
            if (
                (tempLine.find(":") == -1)
                or (tempLine.find("iso") == -1)
                or (
                    (tempLine[tempLine.find("=") + 2 : tempLine.find(":")] == "STRING")
                    and (tempLine[tempLine.find(":") + 2 : -1].count('"') < 2)
                )
            ):
                # no value passed
                pass

            else:
                Line(
                    oid=tempLine[0 : tempLine.find("=")],
                    type=tempLine[tempLine.find("=") + 2 : tempLine.find(":")],
                    value=tempLine[tempLine.find(":") + 2 : -1],
                )


def analizeTempFile():

    for line in lines:
        line.printInfo()


def writeIntoRouter():

    for line in lines:
        if line.type == "STRING":

            # print(f"snmpset -v2c -c {WRITE_KEY} {IP_ADDR} {line.oid} {TYPE_DICT[line.type]} {line.value[1 : -1]}")
            os.system(
                f"snmpset -v2c -c {WRITE_KEY} {IP_ADDR} {line.oid} {TYPE_DICT[line.type]} {line.value[1 : -1]}"
            )

        elif (
            (line.type == "Counter32" or line.type == "Gauge32") and line.value == "0"
        ) or line.type == "OID":

            pass

        else:

            # print(f"snmpset -v2c -c {WRITE_KEY} {IP_ADDR} {line.oid} {TYPE_DICT[line.type]} {line.value}")
            os.system(
                f"snmpset -v2c -c {WRITE_KEY} {IP_ADDR} {line.oid} {TYPE_DICT[line.type]} {line.value}"
            )

    if os.path.exists("./temp"):

        os.remove("./temp")

    else:

        print("Temp file does not exist")


def snmpWalk():

    os.system(f"snmpwalk -v2c -c {READ_KEY} {IP_ADDR} {START_OID} >> temp")


if __name__ == "__main__":

    for arg in sys.argv:

        if ".py" in arg:
            pass

        elif arg == "--help":
            printHelp()

            break

        elif "-" in arg:
            for char in arg:
                if char == "w":
                    snmpWalk()

                elif char == "r":
                    readTempFile()
                    writeIntoRouter()

                elif char == "a":
                    readTempFile()
                    analizeTempFile()

        else:
            print("Wrong arguments")

            break

    end = timer()
    print(timedelta(seconds=end - start))
