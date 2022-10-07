from os.path import join, dirname
from amaranth import *
from amaranth.lib.cdc import ResetSynchronizer
from amaranth.build import *
from amaranth_boards.resources import *
from soc import ZynqPS, ZynqPL

__all__ = ["EBAZ4205Platform"]

def local_elf(name):
    if not isinstance(name, str):
        raise TypeError("ELF name must be a valid string, not {}".format(type(name)))
    return join(dirname(__file__), name)

class EBAZ4205Platform(ZynqPL):
    device = "xc7z010"
    package = "clg400"
    speed = "1"

    default_rst = "S2"

    """
    Add EBAZ4205 PL resources via following documentations:
        1.
    """
    resources   = [
        Resource("PL_CLK", 0, Pins("N18", dir="i"), Clock(50e6), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("PHY_CLK", 0, Pins("U18", dir="i"), Clock(25e6), Attrs(IOSTANDARD="LVCMOS33")),

        # Onboard Side Buttons
        Resource("S2", 0, PinsN("A17", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("S3", 0, PinsN("A14", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),

        # Onboard LEDs
        #*LEDResources(pins="W14 W13", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        # Onboard PS UART1
        UARTResource(0, rx="B19", tx="B20", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        # HelloFPGA ext board - EMIO (PS UART1)
        Resource("uart_tx", 0, Pins("H16", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("uart_rx", 0, Pins("H17", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),

        # HelloFPGA ext board - buttons
        Resource("BTNC", 0, Pins("U20", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("BTND", 0, Pins("U19", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("BTNL", 0, Pins("P19", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("BTNR", 0, Pins("V20", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),
        Resource("BTNU", 0, Pins("T19", dir="i"), Attrs(IOSTANDARD="LVCMOS33")),

        # HelloFPGA ext board - Buzzer
        Resource("buzzer", 0, Pins("D18", dir="o"), Attrs(IOSTANDARD="LVCMOS33")),

        # HelloFPGA ext board - LEDs
        *LEDResources(pins="H18 K17 E19", attrs=Attrs(IOSTANDARD="LVCMOS33")),

        # HelloFPGA ext board - LCD
        SPIResource(0, # LCD, ST7789V, 240 * 240
            cs_n="T20",         # LCD-CS
            clk="R19",          # LCD-SCL
            copi="P20",         # LCD-SDA
            cipo="dummy-cpio0",
            reset="N17",        # LCD-RES
            attrs=Attrs(IOSTANDARD="LVCMOS33"),
        ),
        Resource("lcd", 0, #
            Subsignal("dc",     Pins("T20", dir="o")),  # LCD-DC
        ),

        # HelloFPGA ext board - HDMI
        Resource("hdmi", 0,
            Subsignal("clk", Pins("F19", dir="o")),         # HDMI-CLK
            Subsignal("dat", Pins("D19 C29 B19", dir="o")), # HDMI-DAT[2:0]
            Attrs(IOSTANDARD="LVCMOS33"),
        )
    ]

    connectors = [
        Connector("default",
                "-    - "   # 1,  2
                "M17 P18"   # 3,  4
                "N20 M19"   # 5,  6
                "M18 M20"   # 7,  8
                "L16 L17"   # 9,  10 (DiffPair)
                "L19 L20"   # 11, 12 (DiffPair)
                "J19 K19"   # 13, 14 (DiffPair)
                "H20 J20"   # 15, 16 (DirrPair)
                "G20 G19"   # 17, 18 (DiffPair)
                "J18 K18"   # 19, 20
        , io="io")
    ]

    def __init__(self, fsbl=local_elf("fsbl.elf"), app=local_elf("app.elf")):
        super().__init__(fsbl=fsbl, app=app)

    def toolchain_prepare(self, products, name, **kwargs):
        overrides = {
            "": "",
        }
        return super().toolchain_prepare(products, name, **overrides, **kwargs)

    def toolchain_program(self, products, name, **kwargs):
        return super().toolchain_program(products, name, **kwargs)

class EBAZ4205(Elaboratable):
    def elaborate(self, platform):
        m = Module()
        m.domains += ClockDomain("sync")
        m.submodules.ps = ps = ZynqPS()

        clk = ps.get_clock_signal(0, 25e6)
        m.d.comb += ClockSignal("sync").eq(clk)

        rst = ps.get_reset_signal(0)
        m.submodules.reset_sync = ResetSynchronizer(rst, domain="sync")

        # bind DIP buttons to onboard leds
        m.d.comb += [
            platform.request("led", 0).o.eq(platform.request("BTNU", 0)),
            platform.request("led", 1).o.eq(platform.request("BTNC", 0)),
            platform.request("led", 2).o.eq(platform.request("BTND", 0)),
        ]


        return m

if __name__ == '__main__':

    EBAZ4205Platform().build(elaboratable=EBAZ4205())
