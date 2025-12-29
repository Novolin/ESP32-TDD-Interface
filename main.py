# testing some stuff to make sure I know what I'm doing:


from machine import UART #type:ignore
from array import array
import asyncio


class USB_terminal:
    def __init__(self) -> None:
        self.in_buff = array("B") # unsigned, 8-bit only. It's just going to be ascii or utf-8.
        self.out_buff = array("B")
        self.uart = UART(1, baudrate = 115200) # will autoinit, we're good.
        self.do_uart = True         # something to fuck with to kill the terminal
        

    def parse_buffer(self) -> int:
        count = 0
        for c in self.in_buff:
            if c != "\n":
                self.out_buff.append(c)
                count += 1
            else:
                break

        self.in_buff.clear()
        return count
    
    async def poll_input(self):
        while self.do_uart:
            self.uart.readinto(self.in_buff)
            await asyncio.sleep(0)  # keep on keepin on


    async def check_output(self):
        last_check = 0
        while self.do_uart:
            charsread = 0
            if len(self.in_buff) > 0:

                charsread = self.parse_buffer()
                self.uart.write(f"Read {charsread} characters from input!\n{last_check} seconds since last message.\n")
                for c in self.out_buff:
                    self.uart.write(c)
                last_check = 0
            await asyncio.sleep(1)
            last_check += 1
            self.uart.write(last_check)
            if last_check == 60:
                self.do_uart = False
                self.uart.write("No input for 60 seconds, aborting....")

uart = USB_terminal()

async def main():
    # run the uart, see if it can recognize commands and stuff:
    asyncio.create_task(uart.poll_input())
    asyncio.create_task(uart.check_output())


asyncio.run(main())

