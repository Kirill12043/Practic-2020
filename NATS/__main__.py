import signal
import asyncio
import argparse
from nats.aio.client import Client as NATS


parser = argparse.ArgumentParser()
parser.add_argument('-lt', action='store', required=True, dest="my_name")
parser.add_argument('-mn', action='store', required=True, dest="list_to")
parser.add_argument('-ad', action='store', required=True, dest="nats_addr")
pr = parser.parse_args()
nt = NATS()


async def start(loop):
    await nt.connect(pr.nats_addr, loop=loop)
    sid = await nt.subscribe(pr.list_to, cb=get_msg)
    while True:
        a = await loop.run_in_executor(None, input)
        if a == "":
            continue
        elif a == "/exit":
            break
        await nt.publish(pr.my_name, a.encode('UTF-8'))
    await nt.close()


async def get_msg(msg):
    print(msg.subject, " : ", msg.data.decode())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(loop))
