from torch.nn import (
    Module,
    Sequential,
)

from kubiki.blocks.conv_block import ConvBlock


class ResBlock(Module):
    def __init__(
            self,
            in_channels: int,
            out_channels: int,
            kernel_size: int = 3,
            padding: int = 1,
        ):
        super().__init__()
        self.res_block = Sequential(
            ConvBlock(
                in_channels=in_channels,
                out_channels=out_channels,
                kernel_size=kernel_size,
                padding=padding,
                bias=False,
                instance_norm=True,
            ),
            ConvBlock(
                in_channels=out_channels,
                out_channels=out_channels,
                kernel_size=kernel_size,
                padding=padding,
                bias=False,
                instance_norm=True,
                act=False,
            ),
        )

    def forward(self, x):
        x = x + self.res_block(x)

        return x
