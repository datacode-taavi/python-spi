"""
Python wrapper for SPI communication
"""

import ctypes

from ioctl_numbers import _IOR, _IOW
from struct import pack
from fcntl import ioctl

SPI_IOC_MAGIC   = ord("k")

SPI_CPHA	= 0x01
SPI_CPOL	= 0x02

SPI_MODE_0	= (0|0)
SPI_MODE_1	= (0|SPI_CPHA)
SPI_MODE_2	= (SPI_CPOL|0)
SPI_MODE_3	= (SPI_CPOL|SPI_CPHA)

SPI_CS_HIGH	= 0x04
SPI_LSB_FIRST	= 0x08
SPI_3WIRE	= 0x10
SPI_LOOP	= 0x20
SPI_NO_CS	= 0x40
SPI_READY	= 0x80

# Read / Write of SPI mode (SPI_MODE_0..SPI_MODE_3)
SPI_IOC_RD_MODE          = _IOR(SPI_IOC_MAGIC, 1, "=B")
SPI_IOC_WR_MODE          = _IOW(SPI_IOC_MAGIC, 1, "=B")

# Read / Write SPI bit justification
SPI_IOC_RD_LSB_FIRST     = _IOR(SPI_IOC_MAGIC, 2, "=B")
SPI_IOC_WR_LSB_FIRST     = _IOW(SPI_IOC_MAGIC, 2, "=B")

# Read / Write SPI device word length (1..N)
SPI_IOC_RD_BITS_PER_WORD = _IOR(SPI_IOC_MAGIC, 3, "=B")
SPI_IOC_WR_BITS_PER_WORD = _IOW(SPI_IOC_MAGIC, 3, "=B")

# Read / Write SPI device default max speed hz
SPI_IOC_RD_MAX_SPEED_HZ  = _IOR(SPI_IOC_MAGIC, 4, "=I")
SPI_IOC_WR_MAX_SPEED_HZ  = _IOW(SPI_IOC_MAGIC, 4, "=I")

def SPI_IOC_MESSAGE(size):
    return _IOW(SPI_IOC_MAGIC, 0, "=" + ("QQIIHBBI" * size))

class SPI(object):
    delay         = 0
    speed         = 500000
    mode          = 0
    cs_change     = 0
    bits_per_word = 8
    
    def __init__(self, device):
	self.handle = open(device, "w+")
    
    def set_speed(self, speed):
	p = pack("=I", speed)

	ioctl(self.handle, SPI_IOC_RD_MAX_SPEED_HZ, p)
	ioctl(self.handle, SPI_IOC_WR_MAX_SPEED_HZ, p)
	
	self.speed = speed

    def set_bits_per_word(self, bpw):
	p = pack("=B", bpw)

	ioctl(self.handle, SPI_IOC_RD_BITS_PER_WORD, p)
	ioctl(self.handle, SPI_IOC_WR_BITS_PER_WORD, p)

	self.bits_per_word = bpw

    def set_mode(self, mode):
	p = pack("=B", mode)

	ioctl(self.handle, SPI_IOC_RD_MODE, p)
	ioctl(self.handle, SPI_IOC_WR_MODE, p)

	self.mode = mode
    
    def transfer(self, content):
	txbuf = ctypes.create_string_buffer(str(content))
	rxbuf = ctypes.create_string_buffer(len(content))

	""" The struct for ioctl is:
	struct spi_ioc_transfer {
		__u64		tx_buf;
		__u64		rx_buf;

		__u32		len;
		__u32		speed_hz;

		__u16		delay_usecs;
		__u8		bits_per_word;
		__u8		cs_change;
		__u32		pad;
	}; """

	p = pack("=QQIIHBBI", ctypes.addressof(txbuf),
			ctypes.addressof(rxbuf), len(content),
			self.speed, self.delay, self.bits_per_word,
			self.cs_change, 0)
	
	ioctl(self.handle, SPI_IOC_MESSAGE(1), p)

	return ctypes.string_at(rxbuf, len(content))
