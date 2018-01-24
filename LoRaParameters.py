# Time parameters are expressed in ms

class LoRaParameters:
    # Radio wakeup time from SLEEP mode

    RADIO_OSC_STARTUP = 1
    # Radio PLL lock and Mode Ready delay which can vary with the temperature
    RADIO_SLEEP_TO_RX = 2
    # Radio complete Wake-up Time with margin for temperature compensation
    RADIO_WAKEUP_TIME = (RADIO_OSC_STARTUP + RADIO_SLEEP_TO_RX)
    RECEIVE_DELAY1 = 1000
    RECEIVE_DELAY2 = 2000
    JOIN_ACCEPT_DELAY1 = 5000
    JOIN_ACCEPT_DELAY2 = 6000

    RX_WINDOW_1_DELAY = RECEIVE_DELAY1 - RADIO_WAKEUP_TIME
    RX_WINDOW_2_DELAY = JOIN_ACCEPT_DELAY2 - RADIO_WAKEUP_TIME

    RX_JOIN_WINDOW_1_DELAY = JOIN_ACCEPT_DELAY1 - RADIO_WAKEUP_TIME
    RX_JOIN_WINDOW_2_DELAY = JOIN_ACCEPT_DELAY2 - RADIO_WAKEUP_TIME

    RX_1_ACK_AIR_TIME = [170]  # TODO
    RX_2_ACK_AIR_TIME = 3  #

    RX_1_ACK_ENERGY_MJ = [6.4]  # TODO
    RX_2_ACK_ENERGY_MJ = 3  # TODO

    RX_1_NO_ACK_AIR_TIME = [170]  # TODO
    RX_2_NO_ACK_AIR_TIME = 2

    RX_1_NO_ACK_ENERGY_MJ = [6.4]  # TODO
    RX_2_NO_ACK_ENERGY_MJ = 0.0066  # TODO

    RX_2_DEFAULT_FREQ = 868525000
    RX_2_DEFAULT_SF = 9

    SPREADING_FACTORS = [12, 11, 10, 9, 8, 7]

    DEFAULT_CHANNELS = [868100000, 868300000, 868500000]
    CHANNELS = [868100000, 868300000, 868500000, 868525000]
    CHANNEL_DUTY_CYCLE = {868100000: 1, 868300000: 1, 868500000: 1, 868525000: 10}  # in procent

    JOIN_TX_TIME_MS = 160
    JOIN_TX_ENERGY_MJ = 9

    # Time and Energy consumption of RX1 after join request
    # when a DL message is received
    JOIN_RX_TIME_MS = 120
    JOIN_RX_ENERGY_MJ = 3

    # Time and Energy consumption of RX1 after join request
    # when no DL message is received
    JOIN_RX_1_WINDOW_OPEN_TIME_MS = 26
    JOIN_RX_1_WINDOW_OPEN_ENERGY_MJ = 0.8

    RADIO_PREP_ENERGY_MJ = 0.5  # fixed overhead with each transmission of 500 µJ
    RADIO_PREP_TIME_MS = 40

    ADR_MARGIN_DB = 10  # dB

    # CR: % 5..8 This is the error correction coding. Higher values mean more overhead.
    # header_implicit_mode -> header is removed
    def __init__(self, freq, sf: int, bw, cr, crc_enabled, de_enabled, header_implicit_mode, tp=14):
        self.freq = freq
        self.sf = sf
        self.bw = bw
        self.crc = crc_enabled
        self.cr = cr
        self.tp = tp

        if sf == 7:
            self.dr = 5
        elif sf == 8:
            self.dr = 4
        elif sf == 9:
            self.dr = 3
        elif sf == 10:
            self.dr = 2
        elif sf == 11:
            self.dr = 1
        elif sf == 12:
            self.dr = 0

        if bw == 125 and sf in [11, 12]:
            # low data rate optimization mandated for BW125 with SF11 and SF12
            self.de = 1
        else:
            self.de = de_enabled
        if sf == 6:
            # can only have implicit header with SF6
            self.h = 1
        else:
            self.h = header_implicit_mode

    def change_dr_to(self, dr: int):
        tmp = dr

        if tmp > 5 or tmp < 0:
            raise ValueError('Out of bound DR changing from ' + str(self.dr) + ' to ' + str(tmp))

        self.dr = tmp

        if self.dr == 5:
            self.sf = 7
        elif self.dr == 4:
            self.sf = 8
        elif self.dr == 3:
            self.sf = 9
        elif self.dr == 2:
            self.sf = 10
        elif self.dr == 1:
            self.sf = 11
        elif self.dr == 0:
            self.sf = 12

    def change_tp_to(self, tp: int):
        tmp = tp

        if tmp > 14 or tmp < 2:
            raise ValueError('Out of bound TP changing from ' + str(self.tp) + ' to ' + str(tmp))

        self.tp = tmp
