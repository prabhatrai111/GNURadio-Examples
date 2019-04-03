#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0
#
##################################################
# GNU Radio Python Flow Graph
# Title: OFDM Tx
# Description: Example of an OFDM Transmitter
#
# Generated: Sun Nov 18 23:28:58 2018
# GNU Radio version: 3.7.12.0
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import uhd
from gnuradio.digital.utils import tagged_streams
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import numpy
import random
import time


class tx_ofdm(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "OFDM Tx")

        ##################################################
        # Variables
        ##################################################
        self.occupied_carriers = occupied_carriers = (range(-61,-42)+range(-41, -14) + range(-13, -7) +range(-6, 0) + range(1, 7) + range(7, 14) + range(15, 42)+range(43,62),)
        self.length_tag_key = length_tag_key = "packet_len"
        self.sync_word1 = sync_word1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, (-0.6456 - 0.7637j), 0, (0.8604  - 0.5096j), 0, (0.4806 - 0.8769j), 0, (-0.7417 + 0.6708j), 0, (-0.8925 - 0.4510j), 0, (-0.8244 + 0.5659j), 0, (0.6952 - 0.7188j), 0, (0.9911 - 0.1333j), 0, ( -0.1663 - 0.9861j), 0, (0.7848 + 0.6197j), 0, (0.6952 + 0.7188j), 0, (0.2318 - 0.9728j), 0, ( 0.8604 + 0.5096j), 0, (0.9911 + 0.1333j), 0, ( -0.8244 - 0.5659j), 0, (0.3594 - 0.9332j), 0, ( -0.5381 - 0.8429j), 0, (0.5932 + 0.8051j), 0, ( -0.1663 + 0.9861j), 0, (0.9645 + 0.2642j), 0, ( -0.9447 + 0.3280j), 0, (-0.997 + 0.0668j), 0, (0.4806 + 0.8769j), 0, ( - 0.997 + 0.0668j), 0, ( -0.9447 + 0.3280j), 0, (0.9645 + 0.2642j), 0, ( -0.1663 + 0.9861j), 0, (0.5932 + 0.8051j), 0,  ( -0.5381 - 0.8429j), 0, (0.3594 - 0.9332j), 0, ( -0.8244 - 0.5659j), 0, (0.9911 + 0.1333j), 0, (0.8604 + 0.5096j), 0, (0.2318 - 0.9728j), 0, (0.6952 + 0.7188j), 0, (0.7848 + 0.6197j), 0, ( -0.1663 - 0.9861j), 0, (0.9911 - 0.1333j), 0,  (0.6952 - 0.7188j), 0, ( -0.8244 + 0.5659j), 0, ( -0.8925 - 0.4510j), 0, ( -0.7417 + 0.6708j), 0, (0.4806 - 0.8769j), 0, (0.8604 - 0.5096j), 0, ( -0.6456 - 0.7637j), 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]
        self.samp_rate = samp_rate = 1.92e6
        self.rolloff = rolloff = 0
        self.pilot_symbols = pilot_symbols = (((-1+1j),(1-1j),(-1+1j),(-1-1j),),)
        self.pilot_carriers = pilot_carriers = ((-42, -14, 14, 42,),)
        self.payload_mod = payload_mod = digital.constellation_qpsk()
        self.packet_len = packet_len = 144
        self.header_mod = header_mod = digital.constellation_bpsk()
        self.header_formatter = header_formatter = digital.packet_header_ofdm(occupied_carriers, 1, length_tag_key)
        self.fft_len = fft_len = 128

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(1.2e9, 0)
        self.uhd_usrp_sink_0.set_gain(50, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(samp_rate, 0)
        self.fft_vxx_0 = fft.fft_vcc(fft_len, False, (()), True, 1)
        self.digital_packet_headergenerator_bb_0 = digital.packet_headergenerator_bb(header_formatter.formatter(), "packet_len")
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(fft_len, fft_len+fft_len/4, rolloff, length_tag_key)
        self.digital_ofdm_carrier_allocator_cvc_0 = digital.ofdm_carrier_allocator_cvc(fft_len, occupied_carriers, pilot_carriers, pilot_symbols, (sync_word1, ), length_tag_key)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, length_tag_key, True)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc((payload_mod.points()), 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((header_mod.points()), 1)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, length_tag_key, 0)
        self.blocks_tag_debug_0_0 = blocks.tag_debug(gr.sizeof_char*1, 'SEND', ""); self.blocks_tag_debug_0_0.set_display(True)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len, length_tag_key)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, payload_mod.bits_per_symbol(), length_tag_key, False, gr.GR_LSB_FIRST)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.05, ))
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 255, 1000)), True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_tag_debug_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_ofdm_carrier_allocator_cvc_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_packet_headergenerator_bb_0, 0))
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_packet_headergenerator_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers
        self.set_header_formatter(digital.packet_header_ofdm(self.occupied_carriers, 1, self.length_tag_key))

    def get_length_tag_key(self):
        return self.length_tag_key

    def set_length_tag_key(self, length_tag_key):
        self.length_tag_key = length_tag_key
        self.set_header_formatter(digital.packet_header_ofdm(self.occupied_carriers, 1, self.length_tag_key))

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_bandwidth(self.samp_rate, 0)

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers

    def get_payload_mod(self):
        return self.payload_mod

    def set_payload_mod(self, payload_mod):
        self.payload_mod = payload_mod

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.packet_len)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.packet_len)

    def get_header_mod(self):
        return self.header_mod

    def set_header_mod(self, header_mod):
        self.header_mod = header_mod

    def get_header_formatter(self):
        return self.header_formatter

    def set_header_formatter(self, header_formatter):
        self.header_formatter = header_formatter

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len


def main(top_block_cls=tx_ofdm, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
