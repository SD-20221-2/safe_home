from pyfirmata import Arduino, util
import time
import serial
import paho.mqtt.publish as publish
import datetime


def get_value():
    soma = 0
    # Configuração da porta serial
    serial_port = "COM5"
    serial_baud = 9600

    try:
        serial_connection = serial.Serial(serial_port, serial_baud)
        print("Conexão estabelecida com a porta", serial_port)
        serial_connection.close()
    except serial.SerialException:
        print("Não foi possível conectar à porta", serial_port)
        exit()

    # Instanciação do objeto board
    board = Arduino(serial_port)

    # Configuração dos pinos
    ldr_pin = board.get_pin('a:0:i')
    led_pin = board.get_pin('d:13:o')

    iterator = util.Iterator(board)
    iterator.start()

    i = 0
    # Loop principal
    while i < 3:

        vldr = ldr_pin.read()

        if vldr is not None:

            print("vlrd is not none")

            vldr = int(vldr * 1023)

            led_pin.write(1)  # escreve HIGH no pino LED

            soma = soma + vldr

            i += 1

            print("Valor do LDR: ", vldr)

            time.sleep(0.5)

            final = round(soma/8) - 30

            print(final)

            board.exit()
        else:
            print(vldr)
            board.exit()

    return final


def rotina(broker_address, enviorement_value):

    i = 1
    # Defina as informações de conexão com o servidor MQTT
    port = 1883

    topico = "safehome"

    # Configuração da porta serial
    serial_port = "COM5"
    serial_baud = 9600

    try:
        serial_connection = serial.Serial(serial_port, serial_baud)
        print("Conexão estabelecida com a porta", serial_port)
        serial_connection.close()
    except serial.SerialException:
        print("Não foi possível conectar à porta", serial_port)
        exit()

    # Instanciação do objeto board
    board = Arduino("COM5")

    try:

        # Configuração dos pinos
        ldr_pin = board.get_pin('a:0:i')
        led_pin = board.get_pin('d:13:o')

        iterator = util.Iterator(board)
        iterator.start()

        time.sleep(2)

        inicial_read = ldr_pin.read()

        inicial_read = int(inicial_read * 1023)

        print("leitura inicial", inicial_read)

        enviorement_value = inicial_read - 30

        print("valor do ambiente", enviorement_value)

        # Loop principal
        while True:

            vldr = ldr_pin.read()

            if vldr is not None:

                print("vlrd is not none")

                vldr = int(vldr * 1023)

                if vldr >= enviorement_value:

                    led_pin.write(0)  # escreve LOW no pino LED
                else:
                    led_pin.write(1)  # escreve HIGH no pino LED

                    # publica mensagem server mqtt
                    publish.single(topico, "Incidente ({}) ".format(i) + datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                   hostname=broker_address, port=port)
                    print("Mensagem publicada com sucesso!")
                    i += 1
                print("Valor do LDR: ", vldr)
            time.sleep(0.1)

    except KeyboardInterrupt:
        board.exit()


if __name__ == "__main__":
    valor = 0
    rotina("test.mosquitto.org", valor)
