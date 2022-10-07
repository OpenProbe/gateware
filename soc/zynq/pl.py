from amaranth.vendor.xilinx import XilinxPlatform

__all__ = ['ZynqPL']

class ZynqPL(XilinxPlatform):
    _vivado_file_templates = None
    _vivado_command_templates = None
    _fsbl = None
    _app = None

    def __init__(self, **kwargs):
        self._fsbl = kwargs["fsbl"]
        self._app = kwargs["app"]
        self._vivado_file_templates = {
            **XilinxPlatform._vivado_file_templates,
            "{{name}}.bif": r"""
                all:
                {
                    [bootloader] {{platform._fsbl}}
                    {{name}}.bit
                    {{platform._app}}
                }
            """
        }

        self._vivado_command_templates = [
            *XilinxPlatform._vivado_command_templates,
            r"""
                bootgen
                -image {{name}}.bif
                -arch zynq
                -o BOOT.bin
                -w on
            """
        ]

        super().__init__()
