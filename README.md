python-spi
==========

Pure Python wrapper for SPI communication

Currently only tested between a bridge between a Raspberry Pi and Arduino Mega 2560.

Basic usage
-----------
    from spi import SPI
    
    connection = SPI("/dev/spidev0.0")
    connection.set_speed(100000)
    connection.set_mode(0)
    received = connection.transfer("HELLO WORLD")
    
    print received # same length as sent string
  
Author
------
Taavi Sannik

taavi at kood.ee