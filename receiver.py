#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0
#
##################################################
# GNU Radio Python Flow Graph
# Title: Receiver
# Generated: Sun Nov 18 23:26:13 2018
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

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx


class receiver(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Receiver")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1000000

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(1000000, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.low_pass_filter_0 = filter.interp_fir_filter_ccf(1, firdes.low_pass(
        	32, samp_rate, 0.45*samp_rate, 10000, firdes.WIN_HAMMING, 6.76))
        self.digital_packet_headerparser_b_0 = digital.packet_headerparser_b(digital.packet_header_default(40,"packet_len"))
        self.digital_header_payload_demux_0 = digital.header_payload_demux(
        	  40,
        	  1,
        	  0,
        	  "packet_len",
        	  '',
        	  True,
        	  gr.sizeof_gr_complex,
        	  "rx_time",
                  samp_rate,
                  (""),
                  0,
            )
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
        	samples_per_symbol=2,
        	gain_mu=0.175,
        	mu=0.5,
        	omega_relative_limit=0.005,
        	freq_error=0.0,
        	verbose=False,
        	log=False,
        )
        self.digital_crc32_bb_0_0 = digital.crc32_bb(True, "packet_len", True)
        self.digital_constellation_decoder_cb_0_0 = digital.constellation_decoder_cb(digital.constellation_bpsk().base())
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(digital.constellation_bpsk().base())
        self.blocks_tuntap_pdu_1 = blocks.tuntap_pdu('tun1', 10000, False)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, 'packet_len')
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_char*1, 'test', ""); self.blocks_tag_debug_0.set_display(False)
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(1, 8, "packet_len", True, gr.GR_LSB_FIRST)
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1)
        self.blks2_packet_decoder_0 = grc_blks2.packet_demod_c(grc_blks2.packet_decoder(
        		access_code='',
        		threshold=-1,
        		callback=lambda ok, payload: self.blks2_packet_decoder_0.recv_pkt(ok, payload),
        	),
        )
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 1)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.blocks_tuntap_pdu_1, 'pdus'))
        self.msg_connect((self.digital_packet_headerparser_b_0, 'header_data'), (self.digital_header_payload_demux_0, 'header_data'))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_char_0, 0))
        self.connect((self.blks2_packet_decoder_0, 0), (self.digital_header_payload_demux_0, 0))
        self.connect((self.blocks_float_to_char_0, 0), (self.digital_header_payload_demux_0, 1))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.digital_crc32_bb_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_packet_headerparser_b_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.digital_crc32_bb_0_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.digital_crc32_bb_0_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.digital_gmsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))
        self.connect((self.digital_header_payload_demux_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.digital_constellation_decoder_cb_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.digital_gmsk_demod_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.low_pass_filter_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(32, self.samp_rate, 0.45*self.samp_rate, 10000, firdes.WIN_HAMMING, 6.76))


def main(top_block_cls=receiver, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
