#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Hand Detection
# GNU Radio version: 3.7.13.4
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
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Hand Detection")

        ##################################################
        # Variables
        ##################################################
        self.variable_slider_0 = variable_slider_0 = 0
        self.samp_rate = samp_rate = 8e5
        self.ctr_freq = ctr_freq = 883e6

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title='Scope Plot',
        	sample_rate=samp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Counts',
        )
        self.Add(self.wxgui_scopesink2_0.win)
        _variable_slider_0_sizer = wx.BoxSizer(wx.VERTICAL)
        self._variable_slider_0_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_variable_slider_0_sizer,
        	value=self.variable_slider_0,
        	callback=self.set_variable_slider_0,
        	label='variable_slider_0',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._variable_slider_0_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_variable_slider_0_sizer,
        	value=self.variable_slider_0,
        	callback=self.set_variable_slider_0,
        	minimum=0,
        	maximum=360,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.Add(_variable_slider_0_sizer)
        self.uhd_usrp_source_1 = uhd.usrp_source(
        	",".join(("serial=30D6B32", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_1.set_samp_rate(samp_rate)
        self.uhd_usrp_source_1.set_center_freq(ctr_freq, 0)
        self.uhd_usrp_source_1.set_gain(10, 0)
        self.uhd_usrp_source_1.set_antenna('RX2', 0)
        self.uhd_usrp_source_1.set_auto_dc_offset("", 0)
        self.uhd_usrp_source_1.set_auto_iq_balance("", 0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=22,
                taps=None,
                fractional_bw=None,
        )
        self.blocks_threshold_ff_0 = blocks.threshold_ff(-0.040, 0.040, 0)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.audio_sink_0 = audio.sink(44100, '', True)
        self.analog_sig_source_x_2 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 10000, 1, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_2, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.blocks_complex_to_mag_0, 0))

    def get_variable_slider_0(self):
        return self.variable_slider_0

    def set_variable_slider_0(self, variable_slider_0):
        self.variable_slider_0 = variable_slider_0
        self._variable_slider_0_slider.set_value(self.variable_slider_0)
        self._variable_slider_0_text_box.set_value(self.variable_slider_0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)
        self.uhd_usrp_source_1.set_samp_rate(self.samp_rate)
        self.analog_sig_source_x_2.set_sampling_freq(self.samp_rate)

    def get_ctr_freq(self):
        return self.ctr_freq

    def set_ctr_freq(self, ctr_freq):
        self.ctr_freq = ctr_freq
        self.uhd_usrp_source_1.set_center_freq(self.ctr_freq, 0)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
