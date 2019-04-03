#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: GPL-3.0
#
##################################################
# GNU Radio Python Flow Graph
# Title: Jamming Avoidance Hopping
# Generated: Sun Nov 18 23:29:27 2018
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

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import hackfest
import pmt
import random
import sip
import sys
from gnuradio import qtgui


class jamming_avoidance_hopping(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Jamming Avoidance Hopping")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Jamming Avoidance Hopping")
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

        self.settings = Qt.QSettings("GNU Radio", "jamming_avoidance_hopping")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.interp = interp = 10

        self.tx_taps = tx_taps = firdes.low_pass(1.0, samp_rate*interp, 20e3, 10e3, firdes.WIN_BLACKMAN, 6.76)


        self.j_taps = j_taps = firdes.low_pass(1.0, samp_rate*interp, 30e3, 10e3, firdes.WIN_BLACKMAN, 6.76)

        self.j_power = j_power = 0

        ##################################################
        # Blocks
        ##################################################
        self._j_power_range = Range(0, 10, 0.1, 0, 200)
        self._j_power_win = RangeWidget(self._j_power_range, self.set_j_power, 'Jammer Power', "counter_slider", float)
        self.top_grid_layout.addWidget(self._j_power_win)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate*interp, #bw
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

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate*interp, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.01)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not False:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.hackfest_fhss_seq_gen_0 = hackfest.fhss_seq_gen(1, 10e3, 80)
        self.fft_filter_xxx_0_0 = filter.fft_filter_ccc(1, (j_taps), 1)
        self.fft_filter_xxx_0_0.declare_sample_delay(0)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, (tx_taps), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("trig"), 100)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_c(samp_rate*interp, analog.GR_COS_WAVE, 30e3*random.randint(-4, 3), 1, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate*interp, analog.GR_COS_WAVE, 0, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 150, 1, 0)
        self.analog_noise_source_x_0_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 0.01, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, j_power, 0)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=samp_rate,
        	quad_rate=interp*samp_rate,
        	tau=75e-6,
        	max_dev=5e3,
        	fh=-1.0,
                )



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.hackfest_fhss_seq_gen_0, 'trig'))
        self.msg_connect((self.hackfest_fhss_seq_gen_0, 'seq'), (self.analog_sig_source_x_0_0, 'freq'))
        self.connect((self.analog_nbfm_tx_0, 0), (self.fft_filter_xxx_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.fft_filter_xxx_0_0, 0))
        self.connect((self.analog_noise_source_x_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_throttle_0, 0), (self.analog_nbfm_tx_0, 0))
        self.connect((self.fft_filter_xxx_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.fft_filter_xxx_0_0, 0), (self.blocks_multiply_xx_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "jamming_avoidance_hopping")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate*self.interp)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate*self.interp)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.samp_rate*self.interp)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate*self.interp)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_interp(self):
        return self.interp

    def set_interp(self, interp):
        self.interp = interp
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate*self.interp)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate*self.interp)
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.samp_rate*self.interp)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate*self.interp)

    def get_tx_taps(self):
        return self.tx_taps

    def set_tx_taps(self, tx_taps):
        self.tx_taps = tx_taps
        self.fft_filter_xxx_0.set_taps((self.tx_taps))

    def get_j_taps(self):
        return self.j_taps

    def set_j_taps(self, j_taps):
        self.j_taps = j_taps
        self.fft_filter_xxx_0_0.set_taps((self.j_taps))

    def get_j_power(self):
        return self.j_power

    def set_j_power(self, j_power):
        self.j_power = j_power
        self.analog_noise_source_x_0.set_amplitude(self.j_power)


def main(top_block_cls=jamming_avoidance_hopping, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
