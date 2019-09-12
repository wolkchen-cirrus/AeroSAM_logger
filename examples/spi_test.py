import spidev

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 5000
spi.mode = 0b00

spi.xfer([0x00])
