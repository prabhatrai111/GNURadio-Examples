#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0
#
##################################################
# GNU Radio Python Flow Graph
# Title: Fm Channels
# Generated: Mon Oct 22 16:00:55 2018
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

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt4 import Qt
from broadcast_fm_rx import broadcast_fm_rx  # grc-generated hier_block
from broadcast_fm_tx import broadcast_fm_tx  # grc-generated hier_block
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import math
import sip
from gnuradio import qtgui


class fm_channels(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Fm Channels")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Fm Channels")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fm_channels")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.delta_f = delta_f = 75e3
        self.chan_rate = chan_rate = 192e3
        self.tx_ch_2 = tx_ch_2 = 3
        self.tx_ch_1 = tx_ch_1 = 1
        self.tx_ch_0 = tx_ch_0 = 0
        self.tx_amp_2 = tx_amp_2 = 1
        self.tx_amp_1 = tx_amp_1 = 1
        self.tx_amp_0 = tx_amp_0 = 1
        self.sensitivity = sensitivity = 2*math.pi*delta_f / chan_rate
        self.rx_vol = rx_vol = 0.75
        self.rx_chan = rx_chan = 0
        self.nchans = nchans = 21
        self.audio_rate = audio_rate = 32e3

        ##################################################
        # Blocks
        ##################################################
        self._tx_ch_2_tool_bar = Qt.QToolBar(self)
        self._tx_ch_2_tool_bar.addWidget(Qt.QLabel('TX Channel 2'+": "))
        self._tx_ch_2_line_edit = Qt.QLineEdit(str(self.tx_ch_2))
        self._tx_ch_2_tool_bar.addWidget(self._tx_ch_2_line_edit)
        self._tx_ch_2_line_edit.returnPressed.connect(
        	lambda: self.set_tx_ch_2(int(str(self._tx_ch_2_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._tx_ch_2_tool_bar, 0, 3, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._tx_ch_1_tool_bar = Qt.QToolBar(self)
        self._tx_ch_1_tool_bar.addWidget(Qt.QLabel('TX Channel 1'+": "))
        self._tx_ch_1_line_edit = Qt.QLineEdit(str(self.tx_ch_1))
        self._tx_ch_1_tool_bar.addWidget(self._tx_ch_1_line_edit)
        self._tx_ch_1_line_edit.returnPressed.connect(
        	lambda: self.set_tx_ch_1(int(str(self._tx_ch_1_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._tx_ch_1_tool_bar, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._tx_ch_0_tool_bar = Qt.QToolBar(self)
        self._tx_ch_0_tool_bar.addWidget(Qt.QLabel('TX Channel 0'+": "))
        self._tx_ch_0_line_edit = Qt.QLineEdit(str(self.tx_ch_0))
        self._tx_ch_0_tool_bar.addWidget(self._tx_ch_0_line_edit)
        self._tx_ch_0_line_edit.returnPressed.connect(
        	lambda: self.set_tx_ch_0(int(str(self._tx_ch_0_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._tx_ch_0_tool_bar, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._tx_amp_2_range = Range(0, 1, 0.01, 1, 200)
        self._tx_amp_2_win = RangeWidget(self._tx_amp_2_range, self.set_tx_amp_2, 'TX Amp 2', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tx_amp_2_win, 1, 3, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._tx_amp_1_range = Range(0, 1, 0.01, 1, 200)
        self._tx_amp_1_win = RangeWidget(self._tx_amp_1_range, self.set_tx_amp_1, 'TX Amp 1', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tx_amp_1_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._tx_amp_0_range = Range(0, 1, 0.01, 1, 200)
        self._tx_amp_0_win = RangeWidget(self._tx_amp_0_range, self.set_tx_amp_0, 'TX Amp 0', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tx_amp_0_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rx_vol_range = Range(0, 1, 0.01, 0.75, 200)
        self._rx_vol_win = RangeWidget(self._rx_vol_range, self.set_rx_vol, 'RX Volume', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_vol_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rx_chan_tool_bar = Qt.QToolBar(self)
        self._rx_chan_tool_bar.addWidget(Qt.QLabel('RX Channel'+": "))
        self._rx_chan_line_edit = Qt.QLineEdit(str(self.rx_chan))
        self._rx_chan_tool_bar.addWidget(self._rx_chan_line_edit)
        self._rx_chan_line_edit.returnPressed.connect(
        	lambda: self.set_rx_chan(int(str(self._rx_chan_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._rx_chan_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	nchans*chan_rate, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.01)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-70, 0)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 2, 2, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	nchans*chan_rate, #bw
        	"", #name
        	2 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.01)
        self.qtgui_freq_sink_x_0.set_y_axis(-70, 0)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not False:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "magenta", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 0.5, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.pfb_synthesizer_ccf_0 = filter.pfb_synthesizer_ccf(
        	  nchans, (firdes.low_pass_2(nchans, nchans*chan_rate, 100e3, 20e3, 50)), False)
        self.pfb_synthesizer_ccf_0.set_channel_map(([tx_ch_0, tx_ch_1, tx_ch_2]))
        self.pfb_synthesizer_ccf_0.declare_sample_delay(0)

        self.pfb_decimator_ccf_0 = pfb.decimator_ccf(
        	  nchans,
        	  (firdes.low_pass_2(rx_vol, nchans*chan_rate, chan_rate/2, chan_rate/4, 50)),
        	  rx_chan,
        	  100,
                  True,
                  True)
        self.pfb_decimator_ccf_0.declare_sample_delay(0)

        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, (firdes.complex_band_pass_2(1, nchans*chan_rate, (rx_chan * chan_rate)-chan_rate/2, (rx_chan * chan_rate)+chan_rate/2, chan_rate/10, 80)), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.broadcast_fm_tx_0_0_0 = broadcast_fm_tx(
            audio_rate=audio_rate,
            chan_rate=chan_rate,
            sensitivity=sensitivity,
        )
        self.broadcast_fm_tx_0_0 = broadcast_fm_tx(
            audio_rate=audio_rate,
            chan_rate=chan_rate,
            sensitivity=sensitivity,
        )
        self.broadcast_fm_tx_0 = broadcast_fm_tx(
            audio_rate=audio_rate,
            chan_rate=chan_rate,
            sensitivity=sensitivity,
        )
        self.broadcast_fm_rx_0 = broadcast_fm_rx(
            audio_rate=audio_rate,
            bw=10e3,
            chan_rate=chan_rate,
            sensitivity=sensitivity,
        )
        self.blocks_wavfile_source_0_1 = blocks.wavfile_source('/home/prabhat/Downloads/Untitled folder/PIERS project/fm tx rx/Martin Garrix - Animals.wav', True)
        self.blocks_wavfile_source_0_0 = blocks.wavfile_source('/home/prabhat/Downloads/Untitled folder/PIERS project/fm tx rx/Charlie Puth (Feat. Selena Gomez) - We Don_t Talk Anymore.wav', True)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/prabhat/Downloads/Untitled folder/PIERS project/fm tx rx/Charlie Puth - Attention Official Video (1).wav', True)
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_vcc((tx_amp_2, ))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((tx_amp_1, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((tx_amp_0, ))
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.audio_sink_0 = audio.sink(int(audio_rate), 'pulse', True)
        self.analog_fastnoise_source_x_0 = analog.fastnoise_source_c(analog.GR_GAUSSIAN, 0.1, 0, 8192)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fastnoise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.fft_filter_xxx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.pfb_decimator_ccf_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.pfb_synthesizer_ccf_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.pfb_synthesizer_ccf_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.pfb_synthesizer_ccf_0, 2))
        self.connect((self.blocks_wavfile_source_0, 0), (self.broadcast_fm_tx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 1), (self.broadcast_fm_tx_0, 1))
        self.connect((self.blocks_wavfile_source_0_0, 0), (self.broadcast_fm_tx_0_0, 0))
        self.connect((self.blocks_wavfile_source_0_0, 1), (self.broadcast_fm_tx_0_0, 1))
        self.connect((self.blocks_wavfile_source_0_1, 0), (self.broadcast_fm_tx_0_0_0, 0))
        self.connect((self.blocks_wavfile_source_0_1, 1), (self.broadcast_fm_tx_0_0_0, 1))
        self.connect((self.broadcast_fm_rx_0, 1), (self.audio_sink_0, 1))
        self.connect((self.broadcast_fm_rx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.broadcast_fm_tx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.broadcast_fm_tx_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.broadcast_fm_tx_0_0_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.fft_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.pfb_decimator_ccf_0, 0), (self.broadcast_fm_rx_0, 0))
        self.connect((self.pfb_synthesizer_ccf_0, 0), (self.blocks_add_xx_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fm_channels")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def setStyleSheetFromFile(self, filename):
        try:
            if not os.path.exists(filename):
                filename = os.path.join(
                    gr.prefix(), "share", "gnuradio", "themes", filename)
            with open(filename) as ss:
                self.setStyleSheet(ss.read())
        except Exception as e:
            print >> sys.stderr, e

    def get_delta_f(self):
        return self.delta_f

    def set_delta_f(self, delta_f):
        self.delta_f = delta_f
        self.set_sensitivity(2*math.pi*self.delta_f / self.chan_rate)

    def get_chan_rate(self):
        return self.chan_rate

    def set_chan_rate(self, chan_rate):
        self.chan_rate = chan_rate
        self.set_sensitivity(2*math.pi*self.delta_f / self.chan_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.nchans*self.chan_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.nchans*self.chan_rate)
        self.pfb_synthesizer_ccf_0.set_taps((firdes.low_pass_2(self.nchans, self.nchans*self.chan_rate, 100e3, 20e3, 50)))
        self.pfb_decimator_ccf_0.set_taps((firdes.low_pass_2(self.rx_vol, self.nchans*self.chan_rate, self.chan_rate/2, self.chan_rate/4, 50)))
        self.fft_filter_xxx_0.set_taps((firdes.complex_band_pass_2(1, self.nchans*self.chan_rate, (self.rx_chan * self.chan_rate)-self.chan_rate/2, (self.rx_chan * self.chan_rate)+self.chan_rate/2, self.chan_rate/10, 80)))
        self.broadcast_fm_tx_0_0_0.set_chan_rate(self.chan_rate)
        self.broadcast_fm_tx_0_0.set_chan_rate(self.chan_rate)
        self.broadcast_fm_tx_0.set_chan_rate(self.chan_rate)
        self.broadcast_fm_rx_0.set_chan_rate(self.chan_rate)

    def get_tx_ch_2(self):
        return self.tx_ch_2

    def set_tx_ch_2(self, tx_ch_2):
        self.tx_ch_2 = tx_ch_2
        Qt.QMetaObject.invokeMethod(self._tx_ch_2_line_edit, "setText", Qt.Q_ARG("QString", str(self.tx_ch_2)))
        self.pfb_synthesizer_ccf_0.set_channel_map(([self.tx_ch_0, self.tx_ch_1, self.tx_ch_2]))

    def get_tx_ch_1(self):
        return self.tx_ch_1

    def set_tx_ch_1(self, tx_ch_1):
        self.tx_ch_1 = tx_ch_1
        Qt.QMetaObject.invokeMethod(self._tx_ch_1_line_edit, "setText", Qt.Q_ARG("QString", str(self.tx_ch_1)))
        self.pfb_synthesizer_ccf_0.set_channel_map(([self.tx_ch_0, self.tx_ch_1, self.tx_ch_2]))

    def get_tx_ch_0(self):
        return self.tx_ch_0

    def set_tx_ch_0(self, tx_ch_0):
        self.tx_ch_0 = tx_ch_0
        Qt.QMetaObject.invokeMethod(self._tx_ch_0_line_edit, "setText", Qt.Q_ARG("QString", str(self.tx_ch_0)))
        self.pfb_synthesizer_ccf_0.set_channel_map(([self.tx_ch_0, self.tx_ch_1, self.tx_ch_2]))

    def get_tx_amp_2(self):
        return self.tx_amp_2

    def set_tx_amp_2(self, tx_amp_2):
        self.tx_amp_2 = tx_amp_2
        self.blocks_multiply_const_vxx_0_1.set_k((self.tx_amp_2, ))

    def get_tx_amp_1(self):
        return self.tx_amp_1

    def set_tx_amp_1(self, tx_amp_1):
        self.tx_amp_1 = tx_amp_1
        self.blocks_multiply_const_vxx_0_0.set_k((self.tx_amp_1, ))

    def get_tx_amp_0(self):
        return self.tx_amp_0

    def set_tx_amp_0(self, tx_amp_0):
        self.tx_amp_0 = tx_amp_0
        self.blocks_multiply_const_vxx_0.set_k((self.tx_amp_0, ))

    def get_sensitivity(self):
        return self.sensitivity

    def set_sensitivity(self, sensitivity):
        self.sensitivity = sensitivity
        self.broadcast_fm_tx_0_0_0.set_sensitivity(self.sensitivity)
        self.broadcast_fm_tx_0_0.set_sensitivity(self.sensitivity)
        self.broadcast_fm_tx_0.set_sensitivity(self.sensitivity)
        self.broadcast_fm_rx_0.set_sensitivity(self.sensitivity)

    def get_rx_vol(self):
        return self.rx_vol

    def set_rx_vol(self, rx_vol):
        self.rx_vol = rx_vol
        self.pfb_decimator_ccf_0.set_taps((firdes.low_pass_2(self.rx_vol, self.nchans*self.chan_rate, self.chan_rate/2, self.chan_rate/4, 50)))

    def get_rx_chan(self):
        return self.rx_chan

    def set_rx_chan(self, rx_chan):
        self.rx_chan = rx_chan
        Qt.QMetaObject.invokeMethod(self._rx_chan_line_edit, "setText", Qt.Q_ARG("QString", str(self.rx_chan)))
        self.pfb_decimator_ccf_0.set_channel(int(self.rx_chan))
        self.fft_filter_xxx_0.set_taps((firdes.complex_band_pass_2(1, self.nchans*self.chan_rate, (self.rx_chan * self.chan_rate)-self.chan_rate/2, (self.rx_chan * self.chan_rate)+self.chan_rate/2, self.chan_rate/10, 80)))

    def get_nchans(self):
        return self.nchans

    def set_nchans(self, nchans):
        self.nchans = nchans
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.nchans*self.chan_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.nchans*self.chan_rate)
        self.pfb_synthesizer_ccf_0.set_taps((firdes.low_pass_2(self.nchans, self.nchans*self.chan_rate, 100e3, 20e3, 50)))
        self.pfb_decimator_ccf_0.set_taps((firdes.low_pass_2(self.rx_vol, self.nchans*self.chan_rate, self.chan_rate/2, self.chan_rate/4, 50)))
        self.fft_filter_xxx_0.set_taps((firdes.complex_band_pass_2(1, self.nchans*self.chan_rate, (self.rx_chan * self.chan_rate)-self.chan_rate/2, (self.rx_chan * self.chan_rate)+self.chan_rate/2, self.chan_rate/10, 80)))

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.broadcast_fm_tx_0_0_0.set_audio_rate(self.audio_rate)
        self.broadcast_fm_tx_0_0.set_audio_rate(self.audio_rate)
        self.broadcast_fm_tx_0.set_audio_rate(self.audio_rate)
        self.broadcast_fm_rx_0.set_audio_rate(self.audio_rate)


def main(top_block_cls=fm_channels, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.setStyleSheetFromFile('/opt/gr/share/gnuradio/themes/projector.qss')
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
