from gpiozero import MCP3201


def read_fp07da802n(cs):
    adc = MCP3201(channel=0, select_pin=cs)

