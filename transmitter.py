#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0
#
##################################################
# GNU Radio Python Flow Graph
# Title: Transmitter
# Generated: Sun Nov 18 23:26:25 2018
# GNU Radio version: 3.7.12.0
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx


class transmitter(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Transmitter")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1000000

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("addr==192.168.10.2", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        	"packet_len",
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(1000000, 0)
        self.uhd_usrp_sink_0.set_gain(0, 0)
        self.digital_packet_headergenerator_bb_0 = digital.packet_headergenerator_bb(digital.packet_header_default(40,"packet_len"), "packet_len")
        self.digital_gmsk_mod_0 = digital.gmsk_mod(
        	samples_per_symbol=2,
        	bt=0.35,
        	verbose=False,
        	log=False,
        )
        self.digital_crc32_bb_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_chunks_to_symbols_xx_1_0 = digital.chunks_to_symbols_bc((digital.constellation_bpsk().points()), 1)
        self.digital_chunks_to_symbols_xx_1 = digital.chunks_to_symbols_bc((digital.constellation_bpsk().points()), 1)
        self.blocks_tuntap_pdu_0 = blocks.tuntap_pdu('tun0', 10000, False)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, "packet_len", 0)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, 1, "packet_len", False, gr.GR_LSB_FIRST)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blks2_packet_encoder_0 = grc_blks2.packet_mod_c(grc_blks2.packet_encoder(
        		samples_per_symbol=2,
        		bits_per_symbol=1,
        		preamble='',
        		access_code='',
        		pad_for_usrp=False,
        	),
        	payload_length=0,
        )



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tuntap_pdu_0, 'pdus'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.blks2_packet_encoder_0, 0), (self.digital_gmsk_mod_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_1_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_packet_headergenerator_bb_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blks2_packet_encoder_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.digital_packet_headergenerator_bb_0, 0), (self.digital_chunks_to_symbols_xx_1, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)


def main(top_block_cls=transmitter, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
