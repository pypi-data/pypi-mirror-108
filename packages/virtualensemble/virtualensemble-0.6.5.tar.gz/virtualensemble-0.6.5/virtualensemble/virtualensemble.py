#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QDialog, QLabel, QRubberBand,  QMainWindow, QHeaderView, QMessageBox, QFileDialog, QApplication
from PySide6.QtCore import Qt, QSize, QTimer, QRect, QTime
from PySide6.QtGui import QCursor, QPainter, QPen, QColor, QTextCursor, QPixmap

from scipy.ndimage import maximum_filter1d
from scipy.signal import correlate
import numpy as np
import soundfile as sf
import psutil

import traceback
import re
import sys
import subprocess as subprocess
import os as os
import json
import os.path as path
import datetime as datetime
import tempfile
import math as math
import pathlib

import multiprocessing
import time

try:
	from .utils import qt_routines as qt_routines
	from .gui.Virtualensemble_UI import Ui_MainWindow
	from .gui.Info_UI import Ui_Dialog

except:
	from utils import qt_routines as qt_routines
	from gui.Virtualensemble_UI import Ui_MainWindow
	from gui.Info_UI import Ui_Dialog

MAX_BLANK_SECONDS_AT_END = 10
COMM_Q_PERIOD = 10
PREVIEW_PERIOD = 50
FFMPEG_FILENAMES = ['ffmpeg','ffmpeg.exe']
FFPROBE_FILENAMES = ['ffprobe','ffprobe.exe']
FFMPEG_SAVE_LOCATION = os.path.join(os.path.expanduser('~'), ".VirtualEnsemble","ffmpegpath")
TEMPFILE_LOCATION = os.path.join(os.path.expanduser('~'), ".VirtualEnsemble")
FALLBACK_LOUDNORM = "volume=1.0"
MAX_FPS = 60
FDKAAC_AAC_QUALITY = "4"
FFMPEG_AAC_QUALITY = "225k"
SYNC_AUDIO = "Sync_track_for_syncing.flac"
SYNC_AUDIO_BACKING = "Sync_track_for_backing.flac"
SIGNAL_PREVIEW_DONE = "Preview_ready"
SIGNAL_MESSAGE = "Message_ready"
SIGNAL_STDOUT_DATA = "Stdout"
SIGNAL_TIMELAG_DATA = "Timelag_data"
SIGNAL_TIMELAG_TARGET = "Timelag_target"
OUT_H_Default = 1080.0
OUT_W_Default = 1920.0
PREVIEW_H = 1080.0 / 3
PREVIEW_W = 1920.0 / 3
VID_QUALITY = 22
OGGQUALITY = 7 # ogg quality for encoding
AUDIO_QUALITY = 7
FADE_START = 1
FADE_START_LEN = 1.5
FADE_END_LEN = 1.5
FADE_END = 2
BORDER_WIDTH_DEFAULT = 3
SAMPLERATE_DEFAULT = 12000  # sample rate use for running the correlation
FPS = 30  # assumed FPS for output only
MAX_FILTER_SECS = 1
MAX_LOUD_RANGE = 14.0
MIN_LOUD_RANGE = 1.0
TARGET_PEAK = -1.5
FRAMERATE = 30
FFMPEG_OUTPUT = ["-loglevel", "error"]
STDOUT_HEADER = "\n\n" + "=" * 120 + "\n{0}\n" + "=" * 120 + "\n\n"
MESSAGE_HEADER = "\n\n" + "-" * 120 + "\n{0}\n" + "-" * 120 + "\n\n"
STATS_PERIOD = 5
MAX_FILTER_MIN = 1/100000 # This is the minimal value for scaling the input audio when calculating the lags

def get_audio_details_for_render(vid_table):
		
	audio_mix_details = []
	
	for row in vid_table: 
		if row["audio_weight"] != 0.0:
			audio_mix_details.append({'file' : row['file'], 'audio_weight' : row['audio_weight'], 'timelag' : row['timelag']})
				
	return audio_mix_details

def get_vid_details_for_render(vid_table, num_vids):
		
	vids = []
	timelags = {}
	zooms = []
	x_offs = []
	y_offs = []
	
	for i in range(1, num_vids + 1):
		#find rows with this position
		vid_lists = [row for row in vid_table if row["position"] == i]
		
		if len(vid_lists) == 0:
			return False, None, None, None, None, None,
		else:
			vid_list = vid_lists[0]
			vids.append(vid_list["file"])
			zooms.append(vid_list["zoom"])				
			x_offs.append(vid_list["x_off"])				
			y_offs.append(vid_list["y_off"])		
			timelags[vid_list["file"]] = vid_list["timelag"]
	
	return True, vids, timelags, zooms, x_offs, y_offs

class Info_dialog(QDialog, Ui_Dialog):
	
	def __init__(self, file_to_show = None, block = True):
		super(Info_dialog, self).__init__() # Call the inherited classes __init__ method
		self.setupUi(self)
		self.setModal(block)
		self.show()
		self.textBrowser.setSource(file_to_show)
	
class Preview(QLabel):	

		def __init__(self, parent):
			super(Preview, self).__init__(parent)
			self.x_down = None
			self.y_down = None
			self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
			self.shift = False
			self.origin = None
			self.mouse_pos = None
			self.mouse_down = False
			self.setCursor(QCursor(Qt.CrossCursor))
		
		def set_callback(self, call_on_release):
			self.call_on_release = call_on_release			

		def mousePressEvent(self, mouse_event):
			self.mouse_down = True
			self.x_down = mouse_event.x()
			self.y_down = mouse_event.y()
			self.origin = mouse_event.pos()	
			modifiers = QApplication.keyboardModifiers()
			if modifiers == Qt.ShiftModifier:
				self.shift = True
				self.rubberband.setGeometry(QRect(self.origin, mouse_event.pos()).normalized())
				self.rubberband.show()
			else:
				self.shift = False

		def paintEvent(self, event):
			super(Preview, self).paintEvent(event)
			if self.origin is not None and self.mouse_pos is not None and self.mouse_down and not self.shift:
				painter = QPainter()
				painter.begin(self)
				newpen = QPen()
				newpen.setColor(QColor(0, 0, 255, 125))
				newpen.setWidth(2)
				painter.setPen(newpen)
				painter.drawLine(self.origin, self.mouse_pos)
				painter.end()
				


		def mouseMoveEvent(self, mouse_event):
			self.mouse_pos = mouse_event.pos()
			self.rubberband.setGeometry(QRect(self.origin, mouse_event.pos()).normalized())
			if self.mouse_down:
				self.update()

		def mouseReleaseEvent(self, mouse_event):
			self.call_on_release(self.x_down, self.y_down, mouse_event.x(), mouse_event.y(), self.shift)		
			self.x_down = None
			self.y_down = None
			self.rubberband.hide()
			self.mouse_down = False
			self.update()
	
class Ui(QMainWindow, Ui_MainWindow):
	
	def __init__(self, extra_functionality = False):
		super(Ui, self).__init__() # Call the inherited classes __init__ method
		self.ui = self
		self.setupUi(self)
		
		self.preview = Preview(self.tab_2)
		self.preview.set_callback(self.preview_mouse_release)
		self.preview.setObjectName(u"preview")
		self.preview.setMinimumSize(QSize(640, 360))
		self.preview.setMaximumSize(QSize(640, 360))
		self.preview.setAlignment(Qt.AlignCenter)
		self.preview_placeholder.addWidget(self.preview)
		
		if not os.path.exists(TEMPFILE_LOCATION):
			  os.makedirs(TEMPFILE_LOCATION)
		self.tempdir = tempfile.TemporaryDirectory(dir = TEMPFILE_LOCATION)

		self.sync_audio = os.path.join(os.path.dirname(os.path.realpath(__file__)), "media",SYNC_AUDIO)		
		self.backing_sync_audio = os.path.join(os.path.dirname(os.path.realpath(__file__)), "media",SYNC_AUDIO_BACKING)
			
		#connect browse buttons
		self.ui.render_audio_button.clicked.connect(lambda: self.open_file("Select audio file to render", self.ui.render_audio))
		self.ui.render_output_button.clicked.connect(lambda: self.save_file_dialog("Select output file name", self.ui.render_output, force_extension = ".mp4", file_filter = "mp4 files (*.mp4)"))
		self.ui.copy_video_button.clicked.connect(lambda: self.open_file("Select input video", self.ui.copy_video))
		self.ui.copy_audio_button.clicked.connect(lambda: self.open_file("Select input audio", self.ui.copy_audio))
		self.ui.copy_output_button.clicked.connect(lambda: self.save_file_dialog("Select output file name", self.ui.copy_output, force_extension = ".mp4", file_filter = "mp4 files (*.mp4)"))
		self.ui.backing_audio_button.clicked.connect(lambda: self.open_file("Select audio file", self.ui.backing_audio))
		self.ui.backing_output_button.clicked.connect(lambda: self.save_file_dialog("Select output file", self.ui.backing_output, force_extension = ".mp3", file_filter = "mp3 files (*.mp3)"))

		#connect slide
		self.ui.preview_slider.valueChanged.connect(self.slider_moved)

		#connect table to model
		self.vid_table = qt_routines.Table_model(\
		["file", "timelag", "position", "audio_weight", "zoom", "x_off", "y_off"], \
		types = {"file" : str, "timelag" : float, "position" : int, "audio_weight" : float, "zoom" : float, "x_off" : float, "y_off" : float}, \
		editable = ["timelag", "position", "audio_weight", "zoom", "x_off", "y_off"], \
		defaults = {"zoom" : 1.1, "audio_weight" : 1.0}, \
		delegate_data = {"timelag" : (-100000000.0, 100000000.0, 3), "position" : (None, None), "audio_weight" : (0.0, 100.0, 2), "zoom" : (0.1, 10.0, 2), "x_off" : (-1.0, 1.0, 2), "y_off" : (-1.0, 1.0, 2)}, \
		header_text = ["File", "Cut/(add) secs", "Position", "Volume (0 = mute)", "Zoom", "X offset", "Y offset"])
		self.ui.video_table.setModel(self.vid_table)
		self.vid_table.set_delegates(self.ui.video_table)
		
		#set column stretch in table
		self.ui.video_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		
		#connect buttons
		self.ui.add_files_button.clicked.connect(self.add_files_to_sync)
		self.ui.remove_all_button.clicked.connect(self.remove_all_vids)
		self.ui.remove_files_button.clicked.connect(self.remove_files)
		self.ui.render_button.clicked.connect(self.render_mosaic)
		self.ui.abort_button.clicked.connect(self.abort)
		self.ui.copy_render_button.clicked.connect(self.render_copy)
		self.ui.create_backing_button.clicked.connect(self.create_backing_track)
		self.ui.sync_audio_output_button.clicked.connect(self.output_sync_audio)
		self.ui.encode_audio_only_button.clicked.connect(lambda: self.render_mosaic(audio_only = True))
		self.ui.replace_audio_only_button.clicked.connect(lambda: self.render_mosaic(replace_audio = True))
		self.ui.start_grab.clicked.connect(lambda: self.grab_time(target = self.ui.start))
		self.ui.end_grab.clicked.connect(lambda: self.grab_time(target = self.ui.end))
		
		#connect menus
		self.ui.action_New.triggered.connect(lambda: self.load_values(load_from_new = True))
		self.ui.action_Open.triggered.connect(self.load_values)
		self.ui.action_Save.triggered.connect(self.save_values)
		self.ui.action_SaveAs.triggered.connect(self.saveas_values)
		self.ui.action_Exit.triggered.connect(self.close)
		self.ui.action_About.triggered.connect(self.show_legals)
		self.ui.action_Usage_guide.triggered.connect(self.show_guide)
		self.ui.action_Choose_FFmpeg_location.triggered.connect(lambda: self.find_ffmpeg(force_change = True))
				
		#set up periodic checking of comms q
		self.timer = QTimer()
		self.timer.timeout.connect(self.handle_comms)
		self.timer.start(COMM_Q_PERIOD)
		
		#auto set number of frames
		self.ui.number_of_videos.valueChanged.connect(self.frames_changed)
		self.ui.row_layout.stateChanged.connect(self.frames_changed)
								
		#set items for saving and loading
		self.save_items = {"text" : [self.ui.render_output, self.ui.render_audio, self.ui.render_output, self.ui.title, self.ui.subtitle, \
		self.ui.copy_video, self.ui.copy_audio, self.ui.copy_output, self.ui.backing_audio, self.ui.backing_output], \
		"currentText" : [], \
		"value" : [self.ui.sync_target, self.ui.border, self.ui.preview_slider, \
		self.ui.number_of_videos, self.ui.num_rows], \
		"time" : [self.ui.copy_start, self.ui.copy_end, self.ui.start, self.ui.end], \
		"checkState" : [self.ui.copy_non_normalised, self.ui.copy_aac, self.ui.row_layout, self.ui.vorbis], \
		}
		
		self.ui.show() # Show the GUI
		self.worker = None
		self.preview_worker = None
		self.save_file = None
		self.last_run_preview_args = None
		self.comm_q = multiprocessing.Queue()
		self.new_values = self.save_values(no_file = True) #takes a copy of values for when a new file is selected from the menu
		self.last_save_values = self.new_values
		
		self.FFMPEG_PATH = "ffmpeg"
		self.FFPROBE_PATH = "ffprobe"
						
		self.find_ffmpeg()
		self.find_ffprobe()
		
		self.FFPATHS = {"ffmpeg" : self.FFMPEG_PATH, "ffprobe" : self.FFPROBE_PATH}
	
		#set up periodic running of preview
		self.preview_timer = QTimer()
		self.preview_timer.timeout.connect(self.render_preview)
		self.preview_timer.start(PREVIEW_PERIOD) # every 200ms	
		
		self.slider_moved()

	def closeEvent(self, event):
		if self.save_check():
			event.accept()
		else:
			event.ignore()

	def find_preview_frame(self, x, y, layout):
		
		found_frame = False
		for i in range(1, layout["num_frames"] +1):
			if x >= layout['xs'][i-1] and x < layout['xs'][i-1] + layout['widths'][i-1] and \
			y >= layout['ys'][i-1] and y < layout['ys'][i-1] + layout['heights'][i-1]:
				found_frame = i
				break
		
		return found_frame

	def grab_time(self, target):
		self.slider_moved()
		qtime = QTime.fromString(self.ui.current_time.text(), "hh:mm:ss.z")
		target.setTime(qtime)
		

	def slider_moved(self, event=None):
		vid_start = sum(x * float(t) for x, t in zip([3600, 60, 1], self.start.time().toString("hh:mm:ss.zzz").split(":")))
		vid_duration = sum(x * float(t) for x, t in zip([3600, 60, 1], self.end.time().toString("hh:mm:ss.zzz").split(":"))) - vid_start
		
		if vid_duration >= 0:
			ctime = vid_start + vid_duration * self.ui.preview_slider.value() / self.ui.preview_slider.maximum()
			self.ui.current_time.setText(time.strftime('%H:%M:%S', time.gmtime(int(ctime)))+\
			".{0:02d}".format(int(round(100*(ctime-int(ctime)),0))))
		else:
			self.ui.current_time.setText("-")

	def preview_mouse_release(self, x_from, y_from, x_to, y_to, shift):
		layout = generate_layout(self.ui.number_of_videos.value(), PREVIEW_W, PREVIEW_H, row_layout = self.ui.row_layout.isChecked(), num_rows = self.ui.num_rows.value())
		from_frame = self.find_preview_frame(x_from,y_from,layout)
		to_frame = self.find_preview_frame(x_to,y_to,layout)
				
		if not from_frame:
			return
			
		frame = from_frame

		if self.ui.border.value() != 0:
			border_width = max(1,int(round(self.ui.border.value() * PREVIEW_H / OUT_H_Default,0)))
		else:
			border_width = 0

		w = layout['widths'][from_frame-1] - 2 * border_width; h = layout['heights'][from_frame-1] - 2 * border_width; 
		x_frame = layout['xs'][from_frame-1] + border_width; y_frame = layout['ys'][from_frame-1] + border_width
		
		vid_table = self.vid_table.get_data()
		
		vid_row_num = None
		for i in range(len(vid_table)):
			if vid_table[i]["position"] == frame:
				vid_row_num = i
				break

		if vid_row_num is None:
			return

		vid_row_num_to = None
		for i in range(len(vid_table)):
			if vid_table[i]["position"] == to_frame:
				vid_row_num_to = i
				break
						
		self.ui.video_table.clearSelection()
		self.ui.video_table.selectRow(vid_row_num)
		NewIndex = self.video_table.model().index(vid_row_num, 0)
		self.ui.video_table.setCurrentIndex(NewIndex)
		
		zoom = max(1, vid_table[vid_row_num]["zoom"])
		x_off = vid_table[vid_row_num]["x_off"]
		y_off = vid_table[vid_row_num]["y_off"]
	
		if not to_frame and not shift:

			vid_table[vid_row_num]["x_off"] = 0.0
			vid_table[vid_row_num]["y_off"] = 0.0
			vid_table[vid_row_num]["zoom"] = 1.0			
		
		elif not shift and from_frame != to_frame:
			if vid_row_num is not None:
				vid_table[vid_row_num]["position"] = to_frame if to_frame is not None else 0
			if vid_row_num_to is not None:
				vid_table[vid_row_num_to]["position"] = from_frame if from_frame is not None else 0
		
		elif from_frame and shift:
			zoom_to_x = min(10,zoom / max(abs(x_to - x_from), 1) * w)
			zoom_to_y = min(10,zoom / max(abs(y_to - y_from), 1) * h)
			zoom_to = round(min(10,max(1,min(zoom_to_x, zoom_to_y))),2)
			
			if zoom_to == 1:
				return
			
			x_rel_target = ((x_off + 1) * (zoom - 1) / 2 + ((x_from + x_to)/2 - x_frame) / w) / zoom
			x_off_to =  round(max(-1,min(1,(x_rel_target * zoom_to - 0.5) * 2 / (zoom_to - 1) - 1)),2)

			y_rel_target = ((y_off + 1) * (zoom - 1) / 2 + ((y_from + y_to)/2 - y_frame) / h) / zoom
			y_off_to =  round(max(-1,min(1,(y_rel_target * zoom_to - 0.5) * 2 / (zoom_to - 1) - 1)),2)
	
			vid_table[vid_row_num]["x_off"] = x_off_to
			vid_table[vid_row_num]["y_off"] = y_off_to
			vid_table[vid_row_num]["zoom"] = zoom_to
			
		else:
	
			if zoom == 1:
				return
			
			x_off_delta = ((x_to)-(x_from)) / w * 2 / (zoom - 1)
			y_off_delta = ((y_to)-(y_from)) / h * 2 / (zoom - 1)			

			vid_table[vid_row_num]["x_off"] = round(min(1,max(-1, x_off - x_off_delta)),2)
			vid_table[vid_row_num]["y_off"] = round(min(1,max(-1, y_off - y_off_delta)),2)
			
		self.vid_table.set_from_json(json.dumps(vid_table))

	def find_ffprobe(self):
		
		ffprobe_path = os.path.dirname(self.FFMPEG_PATH)
		ffprobe_file = os.path.basename(self.FFMPEG_PATH).replace("ffmpeg", "ffprobe")
		ffprobe_full_path = os.path.join(ffprobe_path,ffprobe_file)
		
		if is_installed(ffprobe_full_path, self.comm_q):
			self.FFPROBE_PATH = ffprobe_full_path
			return
		else:
			if is_installed(self.FFPROBE_PATH):
				return
		
		QMessageBox.information(self.ui, "Note:", "Could not find ffprobe, which is usually in the same place as ffmpeg.\nInstall ffprobe in same folder as ffmpeg. Exiting.")
		
		self.ui.close()
		
	def find_ffmpeg(self, force_change = False):
				
		if not force_change:
			if path.exists(FFMPEG_SAVE_LOCATION):
				try:
					with open(FFMPEG_SAVE_LOCATION, "r") as data_file:
						ffpath = json.load(data_file)['ffmpeg']
						if os.path.basename(ffpath) in FFMPEG_FILENAMES and is_installed(ffpath, self.comm_q):
							self.FFMPEG_PATH = ffpath
							return
				except:
					self.comm_q.put((SIGNAL_STDOUT_DATA, STDOUT_HEADER.format("Could not load FFmpeg save location from {0}, error message: {1}".format(FFMPEG_SAVE_LOCATION, sys.exc_info()[0]))))	
			if is_installed(self.FFMPEG_PATH, self.comm_q):
				return
			
			message = "Can't find FFmpeg"
			
		else:
			
			message = "Choose the location of FFmpeg"
		
		try:
			if path.exists(FFMPEG_SAVE_LOCATION):
				os.remove(FFMPEG_SAVE_LOCATION)
		except:
			self.comm_q.put((SIGNAL_STDOUT_DATA, STDOUT_HEADER.format("Error deleting stored FFmpeg location {0}, error message: {1}".format(FFMPEG_SAVE_LOCATION, sys.exc_info()[0]))))	
		
						
		while (QMessageBox().question(self.ui, message, "Do you want to select the location of FFmpeg?\nIt will be called ffmpeg or ffmpeg.exe and in the \"bin\" folder of where you installed FFmpeg.\nNote the program will exit if you choose No unless VirtualEnsemble can already find FFmpeg.", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes):
			ffpath, _ = QFileDialog.getOpenFileName(self, "Choose ffmpeg location", "","All Files (*)")
			if os.path.basename(ffpath) in FFMPEG_FILENAMES:
				if is_installed(ffpath, self.comm_q):
					pathlib.Path(os.path.dirname(FFMPEG_SAVE_LOCATION)).mkdir(exist_ok=True)
					with open(FFMPEG_SAVE_LOCATION, "w") as data_file:
						json.dump({'ffmpeg':ffpath}, data_file)
					self.FFMPEG_PATH = ffpath
					return
				
		if path.exists(FFMPEG_SAVE_LOCATION):
			try:
				with open(FFMPEG_SAVE_LOCATION, "r") as data_file:
					ffpath = json.load(data_file)['ffmpeg']
					if os.path.basename(ffpath) in FFMPEG_FILENAMES and is_installed(ffpath, self.comm_q):
						self.FFMPEG_PATH = ffpath
						return
			except:
				self.comm_q.put((SIGNAL_STDOUT_DATA, STDOUT_HEADER.format("Could not load FFmpeg save location from {0}, error message: {1}".format(FFMPEG_SAVE_LOCATION, sys.exc_info()[0]))))	
			if is_installed(self.FFMPEG_PATH, self.comm_q):
				return
					
		self.ui.close()
		
			
	def output_sync_audio(self):
		
		if self.worker is not None:
			if self.worker.is_alive():
				QMessageBox.information(self.ui, "Note:", "Process already running, please abort first")
				return
		
		self.worker = multiprocessing.Process(target=output_sync_audio, args=[self.vid_table.get_data(), self.comm_q, self.tempdir, self.FFPATHS], daemon=True)
		self.worker.start()
		

	def remove_all_vids(self):
		self.vid_table.clear()
		self.ui.sync_target.setValue(0)
		
	def remove_files(self):
		self.vid_table.del_rows(list(set(index.row() for index in self.ui.video_table.selectedIndexes())))
	
	def show_legals(self):
		self.legals = Info_dialog(file_to_show = os.path.join(os.path.dirname(os.path.realpath(__file__)), "LICENSE.html"))
	
	def show_guide(self):
		self.guide = Info_dialog(file_to_show = os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md"), block = False)

	def abort(self):
		if self.worker != None:
			if self.worker.is_alive():
				abort_task(self.worker.pid)
				QMessageBox.information(self.ui, "Note:", "Process aborted")
				self.comm_q.put((SIGNAL_STDOUT_DATA, STDOUT_HEADER.format("Aborted")))
				

	def frames_changed(self, value):
		if self.ui.row_layout.isChecked():
			self.ui.num_rows.setValue(math.floor(self.ui.number_of_videos.value() ** 0.5))
		else:
			self.ui.num_rows.setValue(math.floor(self.ui.number_of_videos.value() ** 0.5))

	def create_backing_track(self):
		
		if self.worker is not None:
			if self.worker.is_alive():
				QMessageBox.information(self.ui, "Note:", "Process already running, please abort first")
				return
		
		if os.path.isfile(self.ui.backing_output.text()): 
			if (QMessageBox().question(self.ui, "Note:", "Output file exists, proceed?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
				return

		args = (self.backing_sync_audio, self.ui.backing_audio.text(), self.ui.backing_output.text(), self.comm_q, self.tempdir, self.FFPATHS)
		
		#start a preview in a thread
		self.worker = multiprocessing.Process(target=create_backing_track, args=args, daemon=True)
		self.worker.start()
		
		self.ui.main_tab.setCurrentIndex(2)
	
	def render_preview(self):
	
		self.slider_moved()
		vid_start = sum(x * float(t) for x, t in zip([3600, 60, 1], self.start.time().toString("hh:mm:ss.zzz").split(":")))
		vid_duration = sum(x * float(t) for x, t in zip([3600, 60, 1], self.end.time().toString("hh:mm:ss.zzz").split(":"))) - vid_start

		vid_table = self.vid_table.get_data()

		args = (None, self.ui.render_audio.text(), vid_start + vid_duration * self.ui.preview_slider.value() / self.ui.preview_slider.maximum(), 1,\
		self.ui.render_output.text(), self.ui.title.text(), self.ui.subtitle.text(), self.ui.number_of_videos.value(), self.ui.row_layout.isChecked(), self.ui.num_rows.value(), \
		True, self.ui.border.value(), \
		vid_table, self.tempdir, self.comm_q, "vorbis", False, False, self.FFPATHS)

		#start a preview in a thread
		if self.last_run_preview_args != args:
			if (self.preview_worker is None) or (not self.preview_worker.is_alive()):
				self.preview_worker = multiprocessing.Process(target=render, args=args, daemon=True)
				self.preview_worker.start()
				self.last_run_preview_args = args
			else:
				try:
					abort_task(self.preview_worker.pid)
					self.preview_worker = multiprocessing.Process(target=render, args=args, daemon=True)
					self.preview_worker.start()
					self.last_run_preview_args = args
				except:
					pass

		self.preview_timer.start(PREVIEW_PERIOD)
		
		
	def render_copy(self):

		if self.worker is not None:
			if self.worker.is_alive():
				QMessageBox.information(self.ui, "Note:", "Process already running, please abort first")
				return
		
		if os.path.isfile(self.ui.copy_output.text()): 
			if (QMessageBox().question(self.ui, "Note:", "Output file exists, proceed?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.No):
				return

		args = (self.ui.copy_video.text(), self.ui.copy_audio.text(), self.ui.copy_output.text(),\
		self.ui.copy_start.time().toString("hh:mm:ss.zzz"), self.ui.copy_end.time().toString("hh:mm:ss.zzz"), \
		self.ui.copy_aac.isChecked(), self.ui.copy_non_normalised.isChecked(), \
		SAMPLERATE_DEFAULT, self.tempdir, self.comm_q, self.FFPATHS)
		
		#start a preview in a thread
		self.worker = multiprocessing.Process(target=copy_video_sync, args=args, daemon=True)
		self.worker.start()
		
		self.ui.main_tab.setCurrentIndex(2)

	def check_overwrite(self, file_path):
		if os.path.isfile(file_path): 
			if (QMessageBox().question(self.ui, "Note:", "{} already exists, proceed and overwrite?".format(file_path), QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes):
				return True
			else:
				return False
		else:
			return True
		
	def render_mosaic(self, audio_only = False, replace_audio = False):
	
		if self.worker is not None:
			if self.worker.is_alive():
				QMessageBox.information(self.ui, "Note:", "Process already running, please abort first")
				return
		
		if (not audio_only) and (not replace_audio) and (not self.check_overwrite(self.ui.render_output.text())): 
			return
			
		if audio_only and (not self.check_overwrite(self.ui.render_output.text()+".flac")):
			return

		if replace_audio and (not self.check_overwrite(os.path.splitext(self.ui.render_output.text())[0] + ".new_audio.mp4")):
			return
			
		vid_table = self.vid_table.get_data()

		acodec = "vorbis" if self.ui.vorbis.isChecked() else "aac"

		vid_start = sum(x * float(t) for x, t in zip([3600, 60, 1], self.start.time().toString("hh:mm:ss.zzz").split(":")))
		vid_duration = sum(x * float(t) for x, t in zip([3600, 60, 1], self.end.time().toString("hh:mm:ss.zzz").split(":"))) - vid_start

		args = (None, self.ui.render_audio.text(), vid_start, vid_duration,\
		self.ui.render_output.text(), self.ui.title.text(), self.ui.subtitle.text(), self.ui.number_of_videos.value(), self.ui.row_layout.isChecked(), self.ui.num_rows.value(), \
		False, self.ui.border.value(), \
		vid_table, self.tempdir, self.comm_q, \
		acodec, audio_only, replace_audio, self.FFPATHS)

		#start a preview in a thread
		self.worker = multiprocessing.Process(target=render, args=args, daemon=True)
		self.worker.start()

		self.ui.main_tab.setCurrentIndex(2)
		return

				
	def handle_comms(self):
		
		messages = []
		while not self.comm_q.empty():
			message = self.comm_q.get_nowait()
			messages.append(message)
		
		for message in messages:
			
			thread_event, thread_values = message		
			
			if thread_event == SIGNAL_PREVIEW_DONE:
				try:
					self.load_preview_image(thread_values)
				except:
					self.last_run_preview_args = None
					
			if thread_event == SIGNAL_MESSAGE:
				QMessageBox.information(self.ui, "Note:", thread_values)
				self.ui.stdout.moveCursor(QTextCursor.End)
				self.ui.stdout.insertPlainText(MESSAGE_HEADER.format(thread_values))
				
			if thread_event == SIGNAL_STDOUT_DATA:
				self.ui.stdout.moveCursor(QTextCursor.End)
				self.ui.stdout.insertPlainText(thread_values)
				
			if thread_event == SIGNAL_TIMELAG_DATA:
				timelags_new = thread_values
				for vid_file in timelags_new.keys():
					self.vid_table.add_row({"file" : vid_file, "timelag" : timelags_new[vid_file], "position" : self.next_position()})
					self.vid_table.refresh_all()
													
			if thread_event == SIGNAL_TIMELAG_TARGET:
				self.ui.sync_target.setValue(thread_values)
		
		#reset timer...
		self.timer.start(COMM_Q_PERIOD)
		
	def next_position(self):
		#work out the next unfilled video position
		i = 1
		vid_table = self.vid_table.get_data()
		while True:
			vid_lists = [row for row in vid_table if row["position"] == i]
			if len(vid_lists) == 0:
				return i
			i += 1
		
	def add_files_to_sync(self):
		#calculate sync and add files to the table
		
		if self.worker is not None:
			if self.worker.is_alive():
				QMessageBox.information(self.ui, "Note:", "Process already running, please abort first")
				return
		
		file_name = QFileDialog()
		file_name.setFileMode(QFileDialog.ExistingFiles)
		audio_files, _ = file_name.getOpenFileNames(self.ui, "Select video files", "", "All Files (*)")
		if len(audio_files) > 0:
			if self.vid_table.rowCount() == 0: # assume no sync target
				calc_args = (self.sync_audio, audio_files, SAMPLERATE_DEFAULT, self.comm_q, self.tempdir, None, self.FFPATHS)
				self.worker = multiprocessing.Process(target=calc_lags, args=calc_args, daemon=True)
				self.worker.start()		
			else: # use existing sync target
				calc_args = (self.sync_audio, audio_files, SAMPLERATE_DEFAULT, self.comm_q, self.tempdir, self.ui.sync_target.value(), self.FFPATHS)
				self.worker = multiprocessing.Process(target=calc_lags, args=calc_args, daemon=True)
				self.worker.start()	
	
			self.ui.main_tab.setCurrentIndex(2)
		
	def save_values(self, no_file = False, no_save_as = False):
		
		if no_save_as and (self.save_file is None or self.save_file == ""):
			return False
		
		if (not no_file) and (self.save_file is None or self.save_file == ""):
			self.saveas_values()
			return False
		
		values = dict()

		for widget in self.save_items["text"]:
			values[widget.objectName()] = widget.text()
		for widget in self.save_items["time"]:
			values[widget.objectName()] = widget.time().toString("hh:mm:ss.zzz")
		for widget in self.save_items["value"]:
			values[widget.objectName()] = widget.value()			
		for widget in self.save_items["currentText"]:			
			values[widget.objectName()] = widget.currentText()
		for widget in self.save_items["checkState"]:
			values[widget.objectName()] = widget.isChecked()
		values["vid_table"] = self.vid_table.get_json()

		if no_file:
			return values
		else:
			try:
				data_file = open(self.save_file, 'w')
				json.dump(values, data_file)
				self.last_save_values = values
				return values
			except:
				return False
		
	def saveas_values(self):	
		
		path = self.save_file_dialog("Select file to save", force_extension = ".vep", file_filter = "VirtualEnsemble Project (*.vep)")
		self.save_file = path
		return self.save_values(no_save_as = True)
				
	def save_check(self):
		
		#check values have changed since last save
		current_values = self.save_values(no_file = True)
		
		if current_values == self.last_save_values:
			return True
		else:
			selection = QMessageBox().question(self.ui, "Note:", "Save changes before proceeding", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
			if selection == QMessageBox.Yes:
				if self.save_values():
					return True
				else:
					return False
			if selection == QMessageBox.No:
				return True
			if selection == QMessageBox.Cancel:
				return False
				
				
	def load_values(self, load_from_new = False):

		if self.save_check():
			
			values = {}

			if not load_from_new:

				load_file, _ = QFileDialog.getOpenFileName(self.ui,"Open file", "","VirtualEnsemble Project (*.vep)")
				self.save_file = load_file

				if os.path.isfile(load_file):
					with open(load_file) as data_file:
			
						values = json.load(data_file)
			
			else:
				
				values = self.new_values
				self.save_file = None

			self.last_save_values = values
			
			#disconnect changing value since otherwise overwrites loaded value
			'''try:
				self.ui.number_of_videos.valueChanged.disconnect()
				self.ui.row_layout.stateChanged.disconnect()
			except:
				pass'''
		
			for widget in self.save_items["checkState"]:
				try:
					widget.setChecked(values[widget.objectName()])
				except:
					pass
			for widget in self.save_items["text"]:
				try:
					widget.setText(values[widget.objectName()])
				except:
					pass
			for widget in self.save_items["time"]:
				try:
					widget.setTime(QTime.fromString(values[widget.objectName()]))
				except:
					pass
			for widget in self.save_items["value"]:
				try:
					widget.setValue(values[widget.objectName()])
				except:
					pass
			for widget in self.save_items["currentText"]:		
				try:	
					widget.setCurrentText(values[widget.objectName()])
				except:
					pass
                
			self.vid_table.set_from_json(values["vid_table"])
			self.slider_moved()
			
	def open_file(self, message, target_widget):
		path, _ = QFileDialog.getOpenFileName(self.ui,message, "","All Files (*)")
		target_widget.setText(path)

	def load_preview_image(self, filename):
		pixmap = QPixmap(filename)
		self.ui.preview.setPixmap(pixmap)

	def save_file_dialog(self, message, target_widget = None, force_extension = False, file_filter = "All Files (*)"):
		#force_extension should be ".abc" i.e. include the dot
		
		retry = True
		
		while retry:
			file_path, _ = QFileDialog.getSaveFileName(self.ui, message, "",file_filter, options = (QFileDialog.Options() | QFileDialog.DontConfirmOverwrite))
			if force_extension and file_path != "":
				file_path = os.path.splitext(file_path)[0] + force_extension
			
			if path.exists(file_path):
				selection = QMessageBox().question(self.ui, "Note:", "File {0} exists, proceed?".format(file_path), QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
				if selection == QMessageBox.Yes:
					retry = False
				if selection == QMessageBox.No:
					retry = True
				if selection == QMessageBox.Cancel:
					return ""
			else:
				retry = False

		if target_widget is not None:
			target_widget.setText(file_path)
		return file_path

def copy_video_sync(video_file, audio_file, output_file, video_start, video_end, aac, no_normalise, samplerate, tempdir, comm_q, FFPATHS = None):

	try:

		FFMPEG_PATH = FFPATHS['ffmpeg']
		comm_q.put((SIGNAL_STDOUT_DATA, STDOUT_HEADER.format("Copying video and adding synchronised audio")))
			
		start_time = time.time()
		
		comm_q_to_run = comm_q
			
		if not path.exists(video_file):
			comm_q.put((SIGNAL_MESSAGE, "Video file does not exist\n"))
			return
					
		if not path.exists(audio_file):
			comm_q.put((SIGNAL_MESSAGE, "Audio file does not exist\n"))
			return
		
		if (output_file == ""):
			comm_q.put((SIGNAL_MESSAGE, "Please choose an output file"))
			return
		
		#parse start and end times to seconds
		video_start = sum(x * float(t) for x, t in zip([3600, 60, 1], video_start.split(":")))
		video_end = sum(x * float(t) for x, t in zip([3600, 60, 1], video_end.split(":")))
		
		#get original video file length
		try:
			video_original_length = get_length(video_file, FFPATHS = FFPATHS)
			audio_original_length = get_length(audio_file, FFPATHS = FFPATHS)
		except:
			comm_q.put((SIGNAL_MESSAGE, "Something went wrong processing the input files, check these are valid media files and try again"))
		
		#determine length of video
		if video_end == 0:
			video_length = video_original_length - video_start
		else:
			video_length = max(video_end, video_original_length) - video_start
			
		#calculate length of clipped audio
		#clipped_audio_length = video_length + audio_original_length - video_original_length
		clipped_audio_length = audio_original_length # don't clip audio

		#change length of input file, save as temporary file
		comm_q.put((SIGNAL_STDOUT_DATA, "\nClipping video\n"))
		
		#ideo_file_clipped_temp = os.path.join(tempdir.name, os.path.basename(video_file) + ".temp.timelag.mkv")
		video_file_clipped = os.path.join(tempdir.name, os.path.basename(video_file) + ".timelag.mkv")
			
		run_external([FFMPEG_PATH, 
		 "-ss", "{0:.3f}".format(video_start), "-t", "{0:.3f}".format(video_length), "-i", video_file,  \
		"-c:v", "copy", "-c:a", "pcm_s16le", "-ac", "1", "-ar", str(samplerate), "-y", video_file_clipped], \
		comm_q_to_run, tempdir, FFPATHS = FFPATHS)
		
		#save audio file as temporary file, downsampling
		
		comm_q.put((SIGNAL_STDOUT_DATA, "\nClipping audio\n"))
		audio_file_clipped = os.path.join(tempdir.name, os.path.basename(audio_file) + ".clipped.timelag.wav")
		
		#audio_start = video_start
		audio_start = 0 # don't clip audio
		
		run_external([FFMPEG_PATH, "-ss", "{0:.3f}".format(audio_start), "-t", "{0:.3f}".format(clipped_audio_length), \
		"-i", audio_file, \
		"-c:a", "pcm_s16le", "-ac", "1", "-ar", str(samplerate), "-y", audio_file_clipped], \
		comm_q_to_run, tempdir, FFPATHS = FFPATHS)

		#load, resample the audio
		comm_q.put((SIGNAL_STDOUT_DATA, "\nLoading "+ video_file))
		video_length, video_array = wave_to_array(video_file_clipped, samplerate, tempdir, convert = "Copy", comm_q = comm_q_to_run, FFPATHS = FFPATHS)
		comm_q.put((SIGNAL_STDOUT_DATA, "\nLoading "+ audio_file))
		audio_length, audio_array = wave_to_array(audio_file_clipped, samplerate, tempdir, convert = "None", comm_q = comm_q_to_run, FFPATHS = FFPATHS)

		calc_start = 0
		calc_end = len(video_array) - calc_start
		video_array = video_array[calc_start : calc_end] 

		#calculate the time lag by maximising the correlation
		comm_q.put((SIGNAL_STDOUT_DATA, "\nCalculating time lag\n"))

		cresult = np.absolute(correlate(audio_array, video_array, mode = 'full'))
		timelag = (np.argmax(cresult) - calc_start - len(video_array))/ samplerate
		
		comm_q.put((SIGNAL_STDOUT_DATA, "Estimated time lag is {0:.3f} seconds (including any extra audio retained)\n".format(timelag)))

		audio_encoded = os.path.join(tempdir.name, os.path.basename(audio_file) + "_audioencoded.mkv")

		if aac:
			acodec = "aac"
		else:
			acodec = "vorbis"

		if no_normalise:
			comm_q.put((SIGNAL_STDOUT_DATA, "\nEncoding audio\n"))
			encode_audio(audio_file, timelag + audio_start, video_length, audio_encoded, tempdir, comm_q_to_run, acodec = acodec, FFPATHS = FFPATHS)
		else:
			comm_q.put((SIGNAL_STDOUT_DATA, "\nCalculating audio normalisation values\n"))
			try:
				norm_filter = generate_loudnorm_filter(audio_file, timelag + audio_start, video_length)
			except:
				comm_q.put((SIGNAL_STDOUT_DATA, "Warning: something went wrong with normalisation"))
				norm_filter = FALLBACK_LOUDNORM	
				return
			comm_q.put((SIGNAL_STDOUT_DATA, "\nEncoding audio\n"))
			filter_complex = "," + norm_filter + ",aresample=48000,aformat=channel_layouts=stereo"
			encode_audio(audio_file, timelag + audio_start, video_length, audio_encoded, tempdir, comm_q_to_run, acodec = acodec, filter_complex_extend = filter_complex, FFPATHS = FFPATHS)		
					
		comm_q.put((SIGNAL_STDOUT_DATA, "\nReplacing audio in video\n"))

		run_external([FFMPEG_PATH, "-ss", "{0:.3f}".format(video_start), "-t", "{0:.3f}".format(video_length), "-i", video_file, \
		"-i", audio_encoded, \
		"-map", "0:v", "-map", "1:a", "-c:v", "copy", \
		"-c:a", "copy", "-shortest", "-y", output_file], \
		comm_q_to_run, tempdir, FFPATHS = FFPATHS)	

		#remove temporary files
		os.remove(audio_file_clipped)
		os.remove(video_file_clipped)	
		os.remove(audio_encoded)
		
		#show how long the process took
		
		end_time = time.time()

		#replace audio track in the video

		comm_q.put((SIGNAL_STDOUT_DATA, "\nSuccess in {0:.0f} seconds\n".format(end_time - start_time)))
		
		if (is_installed("fdkaac")) or (acodec != "aac"):
			comm_q.put((SIGNAL_MESSAGE, "Render finished"))
		else:
			comm_q.put((SIGNAL_MESSAGE, "Render finished, install fdkaac for better quality aac audio"))	

	except:
		comm_q.put((SIGNAL_MESSAGE, "Something went wrong...\n" + get_exception_message()))

def create_backing_track(sync_file, audio_file, output_file, comm_q, tempdir, FFPATHS = None):
	
	try:
		
		FFMPEG_PATH = FFPATHS['ffmpeg']
		
		comm_q.put((SIGNAL_STDOUT_DATA, STDOUT_HEADER.format("Creating backing track")))
		
		if not path.exists(sync_file):
			comm_q.put((SIGNAL_MESSAGE, "Sync file does not exist\n"))
			return

		if not path.exists(audio_file):
			comm_q.put((SIGNAL_MESSAGE, "Audio file does not exist\n"))
			return
		
		run_external([FFMPEG_PATH, "-i", sync_file, "-i", audio_file, "-filter_complex", \
		'[0:a][1:a] concat=n=2:v=0:a=1 [a]', "-map", "[a]", "-acodec", "libmp3lame", "-q:a", "1", "-y", output_file], comm_q, tempdir, FFPATHS = FFPATHS)	

		comm_q.put((SIGNAL_MESSAGE, "Backing track created"))

	except:
		comm_q.put((SIGNAL_MESSAGE, "Something went wrong...\n" + get_exception_message()))

def roundeven(num):
	#round to clostest even number
	#for some reason ffmpeg seems to need even dimensions even for sub-images
	return 2 * round(num / 2.0 , 0)

def generate_layout(num_frames, output_width, output_height, add_to_end = True, row_layout = True, num_rows = False):
	
	#special case
		
	if num_frames == 1 or num_frames == 0:
		layout = {'num_frames':1, 'widths':[output_width], 'heights':[output_height], 'xs': [0], 'ys' : [0], 'filter_layout':"[a0] colorbalance [out]"}
		return layout

	#work out the number of rows
	
	if not num_rows:
		num_rows = math.floor(num_frames ** 0.5)
		
	#work out the number of columns in each row
	
	num_cols = [1] * num_rows
		
	if add_to_end:
		current_row = num_rows - 1
		while sum(num_cols) < num_frames:
			num_cols[current_row] += 1
			current_row = (current_row - 1) % (num_rows)
	else:
		current_row = 0
		while sum(num_cols) < num_frames:
			num_cols[current_row] += 1
			current_row = (current_row + 1) % (num_rows)
		
	#generate the filter layout
	
	filter_vid_list = "".join(["[a{0}]".format(i) for i in range(num_frames)])
	
	filter_start = "{0}xstack=shortest=1:inputs={1}:layout=".format(filter_vid_list, num_frames)
	filter_end = "{0}{1} [out]"

	#flip if using column layout
	if not row_layout:
		output_height, output_width = output_width, output_height
		

	coords = []; widths = []; heights = []; xs = []; ys = []
	row = 0; col = 0
	for frame in range(num_frames):
		
		y = int(roundeven(row * output_height / num_rows))
		x = int(roundeven(col * output_width / num_cols[row]))

		if row == num_rows -1:
			y_to = int(output_height)
		else:
			y_to = int(roundeven((row + 1) * output_height / num_rows))
		
		if col == num_cols[row] -1:
			col = 0
			row += 1
			x_to = int(output_width)
		else:
			x_to = int(roundeven((col + 1) * output_width / num_cols[row]))
			col +=1
			
		if row_layout:
			coords.append("{0}_{1}".format(x,y))
			xs.append(x)
			ys.append(y)
			widths.append(x_to - x)
			heights.append(y_to - y)
		else:
			coords.append("{0}_{1}".format(y,x))
			xs.append(y)
			ys.append(x)
			widths.append(y_to - y)
			heights.append(x_to - x)
	
	all_coords = "|".join(coords)
	
	filter_final = filter_start + all_coords + filter_end
	
	layout = {'num_frames' : num_frames, 'widths' : widths, 'heights' : heights, 'xs' : xs, 'ys' : ys, 'filter_layout' : filter_final}
	
	return layout

def generate_loudnorm_filter(audio_file, audio_start, audio_length, FFPATHS = None):

	FFMPEG_PATH = FFPATHS['ffmpeg']

	if audio_start < 0:
		audio_length += audio_start
		audio_start = 0
	
	if audio_length <= 0:
		return FALLBACK_LOUDNORM
	
	result = subprocess.Popen([FFMPEG_PATH, "-ss", "{0:.3f}".format(audio_start), "-t", "{0:.3f}".format(audio_length), \
	"-i", audio_file, "-vn", "-af", "loudnorm=print_format=json", "-f", "null", "-"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	
	output_list = result.communicate()[0].decode("utf-8").splitlines()[-12:]
	output_string = "\n".join(output_list)
	output_original = json.loads(output_string)
	output = dict(output_original)
	#output['output_tp'] = TARGET_PEAK
	#output['output_lra'] = max(min(float(output_original['input_lra']),MAX_LOUD_RANGE),MIN_LOUD_RANGE)
	#output['output_i'] = float(output_original['output_i']) + float(output['output_tp']) - float(output_original['output_tp'])
	norm_filter = "loudnorm=measured_I={0}:measured_LRA={1}:measured_TP={2}:measured_thresh={3}:offset={4}:linear=true:print_format=summary".format(\
	output['input_i'],  output['input_lra'], output['input_tp'], output['input_thresh'], output['target_offset'])
	return norm_filter

def is_installed(program_name, comm_q = None):
	#nb. assumes it's safe to call "--help"

	try:
		subprocess.run([program_name, "--help"], stdout = open(os.devnull, 'w'), stderr = open(os.devnull, 'w'))
		return True
	except:
		if comm_q is not None:
			comm_q.put((SIGNAL_STDOUT_DATA, STDOUT_HEADER.format("Could not find {0}, error message: {1}".format(program_name, sys.exc_info()[0]))))				
		return False

def encode_audio(audio_file, audio_start, audio_duration, audio_file_encoded, tempdir, comm_q, acodec = "vorbis", filter_complex_extend = None, FFPATHS = None):

	FFMPEG_PATH = FFPATHS['ffmpeg']

	filter_complex = r"[0:a]adelay=delays={0}|{0}|{0}|{0}|{0}".format(-min(0, audio_start)*1000)
	if filter_complex_extend is not None:
		filter_complex += filter_complex_extend
	ffmpegargs = [FFMPEG_PATH, "-ss", "{0:.3f}s".format(max(0, audio_start)), "-i", audio_file, "-filter_complex", filter_complex, "-vn", "-t", str(audio_duration)]
		
	if acodec == "vorbis":
		ffmpegargs.extend(["-c:a", "libvorbis", "-aq", str(AUDIO_QUALITY),  "-y", audio_file_encoded])
		run_external(ffmpegargs, comm_q, tempdir, FFPATHS = FFPATHS)
	elif acodec == "flac":
		ffmpegargs.extend(["-c:a", "flac", "-y", audio_file_encoded])
		run_external(ffmpegargs, comm_q, tempdir, FFPATHS = FFPATHS)
	else: # use aac
		if is_installed("fdkaac"):
			wav_temp_file = os.path.join(tempdir.name, os.path.basename(audio_file) + ".tempaac.wav")
			ffmpegargs.extend(["-c:a", "pcm_s16le", "-y", wav_temp_file])
			run_external(ffmpegargs, comm_q, tempdir, FFPATHS = FFPATHS)
			run_external(["fdkaac", "-m", FDKAAC_AAC_QUALITY, "-w", "18000", \
			"-o", audio_file_encoded, wav_temp_file], comm_q, tempdir, FFPATHS = FFPATHS)
			os.remove(wav_temp_file)
		else:
			ffmpegargs.extend(["-c:a", "aac", "-b:a", FFMPEG_AAC_QUALITY, "-y", audio_file_encoded])
			run_external(ffmpegargs, comm_q, tempdir, FFPATHS = FFPATHS) 


def output_sync_audio(file_table, comm_q, tempdir, FFPATHS = None):

	try:

		FFMPEG_PATH = FFPATHS['ffmpeg']

		comm_q.put((SIGNAL_STDOUT_DATA, STDOUT_HEADER.format("Outputting synchroised audio")))

		for row in file_table:
			if not path.exists(row["file"]):
				comm_q.put((SIGNAL_MESSAGE, "File {0} does not exist\n".format(row["file"])))
				return

		for row in file_table:
			start_crop = max(row["timelag"],0)
			start_pad = max(-row["timelag"],0)

			output_file = row["file"] + ".timelag.flac"

			comm_q.put((SIGNAL_STDOUT_DATA, "\nProcessing {0} and saving as {1}\n".format(row["file"], output_file)))

			run_external([FFMPEG_PATH, "-ss", "{0:.3f}".format(start_crop), "-i", row["file"], \
			"-af", "adelay=delays={0}|{0}|{0}|{0}|{0}".format(start_pad*1000), "-vn", "-c:a", "flac", "-y", output_file], \
			comm_q, tempdir, FFPATHS = FFPATHS)

		comm_q.put((SIGNAL_MESSAGE, "\nSynchronised audio files output complete\n"))

	except:
		comm_q.put((SIGNAL_MESSAGE, "Something went wrong...\n" + get_exception_message()))

def calc_lags(sync_audio, audio_files, samplerate, comm_q, tempdir, sync_target = None, FFPATHS = None):
	
	try:

		comm_q.put((SIGNAL_STDOUT_DATA, STDOUT_HEADER.format("Calculating lags")))
		
		sync_point = dict()
		length = dict()
		
		if not path.exists(sync_audio):
			comm_q.put((SIGNAL_MESSAGE, "Sync file does not exist\n"))
			return
		
		comm_q.put((SIGNAL_STDOUT_DATA, "\nLoading " + sync_audio + "\n"))
		sync_length, sync_array = wave_to_array(sync_audio, samplerate, tempdir, comm_q = comm_q, FFPATHS = FFPATHS)
		
		#first calculate all of the time lags
		for audio_file in audio_files:

			if not path.exists(audio_file):
				comm_q.put((SIGNAL_MESSAGE, "Audio file {0} does not exist\n".format(audio_file)))
				return

			#load, resample the sound files
			comm_q.put((SIGNAL_STDOUT_DATA, "\nLoading "+ audio_file + "\n"))
			audio_length, audio_array = wave_to_array(audio_file, samplerate, tempdir, comm_q = comm_q, FFPATHS = FFPATHS)

			#calculate the time lag by maximising the correlation
			comm_q.put((SIGNAL_STDOUT_DATA, "\nCalculating time lag\n"))
			
			#cresult = np.absolute(correlate(audio_array, sync_array, mode = 'full'))
			#cresult = cresult / max(1,max(cresult))

			max_amps = maximum_filter1d(abs(audio_array), int(MAX_FILTER_SECS * samplerate))
			max_amps = np.clip(max_amps, MAX_FILTER_MIN, None)
			audio_array_compressed = np.nan_to_num(audio_array / max_amps)
			cresult_max = np.absolute(correlate(audio_array_compressed, sync_array, mode = 'full'))
			cresult_max = cresult_max / max(1,np.nanmax(cresult_max))

			x_from = 0
			x_to = len(cresult_max)

			timelag = (np.argmax(cresult_max[x_from:x_to]) + x_from - len(sync_array)) / samplerate
			
			comm_q.put((SIGNAL_STDOUT_DATA,"Estimated time to sync point {0:.3f} seconds\n".format(timelag)))
			
			sync_point[audio_file] = timelag
			length[audio_file] = audio_length

		#calculate the amount by which to crop each audio file at the start
		#this is the minimum crop such that all files start in the same place
		#the file will also be cropped at the end at the point of the match with the sync track
		#then output flacs for each file with the required cropping and write detailed output needed
		
		if sync_target:
			pass
		else:
			sync_target = max(sync_point.values())

		comm_q.put((SIGNAL_STDOUT_DATA,"\n\n"))

		save_details = dict()

		for audio_file in audio_files:
			
			start_crop = max(sync_point[audio_file] - sync_target,0)
			start_pad = max(sync_target - sync_point[audio_file],0)

			if start_crop > 0:
				frames = (start_crop - int(start_crop)) * FPS
				start_crop_formatted = str(datetime.timedelta(seconds=int(start_crop))) + "." + "{0:.0f}".format(frames)
			else:
				start_crop = start_pad
				frames = (start_crop - int(start_crop)) * FPS
				start_crop_formatted = "-" + str(datetime.timedelta(seconds=int(start_crop))) + "." + "{0:.0f}".format(frames) 
				start_crop = -start_pad
				
			out_string = "\
	************************************************************\n\
	Input file: {0}\n\
	Cropped from the start (seconds): {1:.3f}\n\
	Cropped from the start (hh:mm:ss.frames assuming 30fps) {2}\n\
	************************************************************\n\
	".format(audio_file, start_crop, start_crop_formatted)
			
			save_details[audio_file] = round(start_crop, 3)
				
			comm_q.put((SIGNAL_STDOUT_DATA, out_string))
		
		#show how long the process took

		comm_q.put((SIGNAL_TIMELAG_TARGET, sync_target))
		comm_q.put((SIGNAL_TIMELAG_DATA, save_details))
		comm_q.put((SIGNAL_MESSAGE, "Added files\n"))

	except:
		comm_q.put((SIGNAL_MESSAGE, "Something went wrong...\n" + get_exception_message()))

def wave_to_array(input_file, samplerate, tempdir, convert = "Full", comm_q = None, FFPATHS = None):
	"""read in a wave file and convert to a fft, first converting to a standard wave file (mono with required freq)
	note that if not converting we assume INPUTSAMPLERATE"""
	
	FFMPEG_PATH = FFPATHS['ffmpeg']
	
	#convert file to standard wave file format
	if convert == "None":
		temp_file = input_file
	else:
		temp_file = os.path.join(tempdir.name, os.path.basename(input_file) + ".timelag.wav")

	if convert == "Full":
		run_external([FFMPEG_PATH, "-ss", "0", "-i", input_file, "-ac", "1", "-ar", str(samplerate), "-y", temp_file], comm_q, tempdir, FFPATHS = FFPATHS)
		
	if convert == "Copy":
		run_external([FFMPEG_PATH, "-ss", "0", "-i", input_file, "-c:a", "copy", "-y", temp_file], comm_q, tempdir, FFPATHS = FFPATHS)
		
	#read 
	
	fft, sr = sf.read(temp_file)
	
	if convert != "None":
		os.remove(temp_file)
						
	length = len(fft) / samplerate
		
	return length, fft
	
def get_length(input_media, FFPATHS = None):
	FFPROBE_PATH = FFPATHS['ffprobe']
	result = subprocess.Popen([FFPROBE_PATH, "-i", input_media, "-show_entries", "format=duration", "-v", "quiet", "-of", 'json'], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	output = json.loads(result.communicate()[0].decode("utf-8"))
	return float(output['format']['duration'])

if sys.platform.startswith("win"):
	def abort_task(pid):
		#os.system('taskkill /F /PID {:d} /T >NUL 2>NUL'.format(pid))
		os.system('taskkill /PID {:d} /T >NUL 2>NUL'.format(pid))
else:
	def abort_task(pid):
		parent_task = psutil.Process(pid)
		for child in parent_task.children(recursive=True):
			child.terminate()
		parent_task.terminate()

def get_exception_message():
	
	ex_type, ex_value, ex_traceback = sys.exc_info()
	
	message = "{0}, {1}\n{2}".format(ex_type.__name__, ex_value, "\n".join(traceback.format_tb(ex_traceback)))
	return message

def run_external(target, comm_q, tempdir, FFPATHS = None):

	FFMPEG_PATH = FFPATHS['ffmpeg']

	if target[0] == FFMPEG_PATH and comm_q is not None:
		ffmpeg_progress = True
		progress_file = os.path.join(tempdir.name, "progress.txt")
		target.extend(FFMPEG_OUTPUT)
		target.extend(["-progress", progress_file])
	else:
		ffmpeg_progress = False

	process = subprocess.Popen(target, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	
	start = time.time()
	stats_start = time.time()
	message = ""

	count = 0
	if ffmpeg_progress:
		while process.poll() is None:
			time.sleep(0.2)
			if (time.time() - stats_start > STATS_PERIOD):
				if count == 0:
					comm_q.put((SIGNAL_STDOUT_DATA, "Processed (hh:mm:ss):"))
				elif count % 12 == 0:
					comm_q.put((SIGNAL_STDOUT_DATA, "\nProcessed (hh:mm:ss):"))					

				count += 1
				stats_start = time.time()

				try:
					with open(progress_file, "r") as text_file:
						progress = text_file.read()
					times = re.search(r'(?s:.*)out_time=([0-9][0-9]:[0-9][0-9]:[0-9][0-9])', progress)
					comm_q.put((SIGNAL_STDOUT_DATA, "[{0}]".format(times.group(1))))
				except:
					comm_q.put((SIGNAL_STDOUT_DATA, "[N/A]"))

			
		comm_q.put((SIGNAL_STDOUT_DATA, "\n"))
	
	while True:
		
		line = process.stdout.read(1)
		if not message and not line and process.poll() is not None:
			break
		if line:
			message += line.decode("utf-8").replace('\r','\n')
		
		if time.time() - start > 1:
			if time.time() - start > STATS_PERIOD:
				message = message.replace('\r','\n')
			if comm_q is not None:
				comm_q.put((SIGNAL_STDOUT_DATA, message))
			message = ""
			start = time.time()

	process.communicate()[0]
	exit_code = process.returncode
	
	if exit_code != 0:
		raise Exception("External program {0} had an error, return code {1}".format(target[0] , str(exit_code)))

	
def render(picture, audio_file, vid_start, vid_duration, output_file, title,\
subtitle, num_frames, row_layout, num_rows, sample_frame, border_width, \
vid_table, tempdir, comm_q, acodec = "vorbis", audio_only = False, replace_audio = False, FFPATHS = None):
	#audio_only - just output audio in file with the video name + .flac
	#replace_audio - replace audio into file with the video name + .new_audio.mp4

	try:

		FFMPEG_PATH = FFPATHS['ffmpeg']

		if not sample_frame:
			comm_q.put((SIGNAL_STDOUT_DATA, STDOUT_HEADER.format("Rendering mosaic")))

			audio_mix_details = get_audio_details_for_render(vid_table)
		
			if (audio_file == "") and (len(audio_mix_details) == 0):
				comm_q.put((SIGNAL_MESSAGE, "No audio file selected for render and no files selected for mixing, aborting"))
				return
			
			if replace_audio and not path.exists(output_file):
				comm_q.put((SIGNAL_MESSAGE, "Can't replace audio as output file does not exist"))
				return

		sample_frame_last = False
		
		vids = []
		timelags = []
		zooms = []
		x_offsets = []
		y_offsets = []
		vid_lengths = []
		
		for i in range(1, num_frames + 1):
			#find rows with this position
			vid_lists = [row for row in vid_table if row["position"] == i]
			
			if len(vid_lists) == 0:
				vids.append(None)
				zooms.append(1.0)
				x_offsets.append(0.0)
				y_offsets.append(0.0)
				timelags.append(0.0)
				vid_lengths.append(-MAX_BLANK_SECONDS_AT_END)
			else:
				vid_list = vid_lists[0]
				vids.append(vid_list["file"])
				zooms.append(vid_list["zoom"])				
				x_offsets.append(vid_list["x_off"])				
				y_offsets.append(vid_list["y_off"])		
				timelags.append(vid_list["timelag"] + vid_start)
				vid_lengths.append(min(vid_duration, get_length(vids[i-1],FFPATHS = FFPATHS)-timelags[i-1]))
								
		vid_duration = min(vid_duration, max(vid_lengths) + MAX_BLANK_SECONDS_AT_END)
		if vid_duration <= 9.9 and not sample_frame:
			comm_q.put((SIGNAL_MESSAGE, "All selected videos/audio must be at least 10 seconds long, check start/duration time"))
			return

		if vid_duration <= 0.05 and sample_frame:
			if set(vids) != set([None]):
				sample_frame_last = True
			vid_start_new = vid_start + vid_duration - 0.05
			for i in range(1, num_frames + 1):
				if vids[i-1] is not None:
					timelags[i-1] += vid_start_new - vid_start
			vid_start = vid_start_new
			vid_duration = 0.1
			

		if sample_frame:
			OUT_H = PREVIEW_H
			OUT_W = PREVIEW_W
			if border_width != 0:
				border_width = max(1,int(round(border_width * PREVIEW_H / OUT_H_Default,0)))
		else:
			OUT_H = OUT_H_Default
			OUT_W = OUT_W_Default

		if audio_file != "" and (not audio_only):
			if (not path.exists(audio_file)) and (not sample_frame):
				comm_q.put((SIGNAL_MESSAGE, "Audio file {0} does not exist".format(audio_file)))
				return
		else:
			if (not sample_frame) and (len(audio_mix_details) == 0):
				if len(audio_mix_details) == 0:
					comm_q.put((SIGNAL_MESSAGE, "No files selected for mixing"))
					return
		if (not audio_only) and (not replace_audio):
			for vid_file in vids:
				if (vid_file is not None) and (not path.exists(vid_file)) and (not sample_frame) :
					comm_q.put((SIGNAL_MESSAGE, "Warning: video file {0} does not exist".format(vid_file)))
					return
		
		if (output_file == "") and (not sample_frame):
			comm_q.put((SIGNAL_MESSAGE, "Please choose an output file"))
			return

		layout = generate_layout(num_frames, OUT_W, OUT_H, row_layout = row_layout, num_rows = num_rows)

		ff_args = [FFMPEG_PATH]

		fontfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "media","DejaVuSerif.ttf")
		fontsize_for_numbers = int(200 / max(OUT_W / min(layout["widths"]), OUT_H / min(layout["heights"])))
		
		for i in range(1,num_frames + 1):
			if vids[i-1] == 'Picture':
				ff_args.extend(["-loop", "1", "-i", picture])
			elif vids[i-1] is None or not path.exists(vids[i-1]):
				ff_args.extend(["-t", str(vid_duration), "-f", "lavfi", "-i", "color=c=gray:s={0}x{1}:r={5},drawtext=text={2}:fontfile='{3}':x=w/2-text_w/2:y=h/2-text_h/2:fontsize={4}"\
				.format(int(round(layout["widths"][i-1]-border_width*2,0)), int(round(layout["heights"][i-1]-border_width*2,0)),i,fontfile.replace("\\", "\\\\"), fontsize_for_numbers, FRAMERATE)])
			elif vid_lengths[i-1] < 0.01:
				ff_args.extend(["-t", str(vid_duration), "-f", "lavfi", "-i", "color=c=black:s={0}x{1}:r={2}"\
				.format(int(round(layout["widths"][i-1]-border_width*2,0)), int(round(layout["heights"][i-1]-border_width*2,0)),FRAMERATE)])
			else:
				ff_args.extend(["-ss", "{0:.3f}".format(max(0,timelags[i-1])), "-i", vids[i-1]])	

		#generate audio
		if not sample_frame: 
		
			audio_file_encoded = os.path.join(tempdir.name, "audio_file_encoded.mkv")
			
			if audio_file != "" and (not audio_only):
				comm_q.put((SIGNAL_STDOUT_DATA, "\nEncoding audio file supplied:"))
				encode_audio(audio_file, vid_start, vid_duration, audio_file_encoded, tempdir, comm_q, acodec, filter_complex_extend=r",apad=whole_dur={0:.3f}".format(vid_duration), FFPATHS = FFPATHS)
			else:
				comm_q.put((SIGNAL_STDOUT_DATA, "\nMixing input files:\n"))	

				#generate list of inputs
				audio_ffmpeg_args = [FFMPEG_PATH]
				for details in audio_mix_details:
					audio_ffmpeg_args.extend(["-ss", "{0:.3f}".format(max(0, details['timelag'] + vid_start)), \
					"-i", details['file']])

				#Calculate audio normalisation parameters
				norm_filters = []
				
				for details in audio_mix_details:
					comm_q.put((SIGNAL_STDOUT_DATA, "\nNormalising {0}\n".format(details['file'])))	
					try:
						to_append = generate_loudnorm_filter(details['file'], details['timelag'] + vid_start, vid_duration, FFPATHS = FFPATHS)
						norm_filters.append(to_append)
					except:
						comm_q.put((SIGNAL_STDOUT_DATA, "Warning: something went wrong with normalisation"))
						norm_filters.append(FALLBACK_LOUDNORM)

				#Mix the audio together	
				comm_q.put((SIGNAL_STDOUT_DATA, "\nMixing all input files:\n"))
				acount = 0
				audio_filter = ""
				amix_list = ""
				num_to_mix = len(audio_mix_details)
				for details in audio_mix_details:
					audio_filter += "[{0}:a]adelay=delays={2}|{2}|{2}|{2}|{2}, apad=whole_dur={3:.3f},{1}[async{0}];".format(acount, norm_filters[acount], -min(0, details['timelag'] + vid_start) * 1000, vid_duration)
					amix_list += "[async{0}]".format(acount)
					acount += 1			
				weights = ["{0:.3f}".format(row['audio_weight']) for row in audio_mix_details]
				amix_filter = audio_filter + amix_list + " amix=inputs={0}:duration=longest:weights={1}:dropout_transition=1000000 [aout]".format(num_to_mix, " ".join(weights))

				audio_mix_file_pre_norm = os.path.join(tempdir.name, "audio_mix_pre_norm.flac")
				
				audio_ffmpeg_args.extend(["-filter_complex", amix_filter, "-map", "[aout]", "-acodec", "flac", "-vn", \
				"-t", str(vid_duration), "-y", audio_mix_file_pre_norm])

				run_external(audio_ffmpeg_args, comm_q, tempdir, FFPATHS = FFPATHS)
				
				#Normalise the mix				
				comm_q.put((SIGNAL_STDOUT_DATA, "Normalising the mixed audio:\n"))
				try:
					norm_filter = generate_loudnorm_filter(audio_mix_file_pre_norm, 0, vid_duration, FFPATHS = FFPATHS)
				except:
					comm_q.put((SIGNAL_STDOUT_DATA, "Warning: something went wrong with normalisation"))
					norm_filter = FALLBACK_LOUDNORM
		
				audio_mix_file = os.path.join(tempdir.name, "audio_mix.flac")
				run_external([FFMPEG_PATH, "-i", audio_mix_file_pre_norm, "-af", norm_filter+",aresample=48000,aformat=channel_layouts=stereo", "-acodec", "flac", "-vn", "-y", audio_mix_file], comm_q, tempdir, FFPATHS = FFPATHS)						

				os.remove(audio_mix_file_pre_norm)
		
				if audio_only:
					audio_file_encoded = output_file + ".flac"
					acodec = "flac"
					encode_start = -vid_start
					vid_duration -= encode_start
				else:
					encode_start = 0
		
				comm_q.put((SIGNAL_STDOUT_DATA, "\nEncoding the mixed audio:\n"))						
				encode_audio(audio_mix_file, encode_start, vid_duration, audio_file_encoded, tempdir, comm_q, acodec, FFPATHS = FFPATHS)

				if audio_only:
					comm_q.put((SIGNAL_MESSAGE, "Saved new audio mix to {0}".format(audio_file_encoded)))
					return
				
				os.remove(audio_mix_file)
				
			#encode audio
			
			ff_args.extend(["-i", audio_file_encoded]) 
			
			audio_length = get_length(audio_file_encoded, FFPATHS = FFPATHS)
			vid_duration = min(vid_duration, audio_length)
			
			if vid_duration <= 10 and not sample_frame:
				comm_q.put((SIGNAL_MESSAGE, "All selected videos/audio must be at least 10 seconds long, check start/duration time"))
				os.remove(audio_file_encoded)
				return
			
		#generate video filter
		filter_base = r"[{0}:v] tpad=start_duration={1}:stop_duration={11:.3f},scale={2}:force_original_aspect_ratio=decrease,pad={4}:(ow-iw)/2:(oh-ih)/2,crop={3},pad=w={9}*2+iw:h={9}*2+ih:x={9}:y={9}"
		if sample_frame:
			filter_base += r",drawtext=text={10}"+r":fontfile='{0}':x='min(w/15, h/15)':y='min(w/15, h/15)':fontsize={1}:fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=5".format(fontfile.replace("\\", "\\\\").replace(":", "\\:"), fontsize_for_numbers/2) + "[a{0}];"
		else:
			filter_base += r",fade=in:st={5}:d={6},fade=out:st={7}:d={8} [a{0}];"
		filter_text = ""
		
		for i in range(1,num_frames + 1):
				zooms[i-1] = max(1,zooms[i-1]) 
				x_size = layout['widths'][i-1] - border_width * 2
				x_zoomed_size = int(zooms[i-1] * x_size)
				y_size = layout['heights'][i-1] - border_width * 2
				y_zoomed_size = int(zooms[i-1] * y_size)
				x_off = min(1,max(-1,x_offsets[i-1]))
				y_off = min(1,max(-1,y_offsets[i-1]))
				x = int((x_zoomed_size - x_size) * (x_off + 1) / 2)
				y = int((y_zoomed_size - y_size) * (y_off + 1) / 2)
				scale_text = "{0}:{1}".format(x_zoomed_size, y_zoomed_size)
				zoom_border = zooms[i-1] * border_width
				crop_text = "{0}:{1}:{2}:{3}".format(str(x_size),str(y_size),str(min(max(zoom_border,x), x_zoomed_size - x_size - zoom_border)),str(min(max(zoom_border,y), y_zoomed_size - y_size - zoom_border)))
				#crop_text = "{0}:{1}:{2}:{3}".format(str(x_size),str(y_size),str(x),str(y))
				pad_text = "{0}:{1}".format(str(x_zoomed_size+1),str(y_zoomed_size+1))
				filter_text += filter_base.format(i-1, "{0:.3f}".format(max(0,-timelags[i-1])), scale_text, crop_text, pad_text,FADE_START,FADE_START_LEN,vid_duration - FADE_END_LEN - FADE_END,FADE_END_LEN, border_width, "" if vids[i-1] is None else i, max(0,vid_duration - vid_lengths[i-1]))
		
		if title:
			title_file = os.path.join(tempdir.name, "title.txt")
			with open(title_file, "w") as text_file:
				text_file.write(title)
			title_filter = r",drawtext=enable='between(t,2,12)':fontfile='{1}':textfile='{0}':fontcolor=white:fontsize=h/15:box=1:boxcolor=black@0.5:boxborderw=5:x=w/70:y=h*17/20:alpha='if(lt(t,2),0,if(lt(t,3),(t-2)/1,if(lt(t,11),1,if(lt(t,12),(1-(t-11))/1,0))))'"\
			.format(title_file.replace("\\", "\\\\").replace(":", "\\:"), fontfile.replace("\\", "\\\\").replace(":", "\\:"))
		else:
			title_filter = ''
		if subtitle:
			subtitle_file = os.path.join(tempdir.name, "subtitle.txt")
			with open(subtitle_file, "w") as text_file:
				text_file.write(subtitle)
			subtitle_filter = r",drawtext=enable='between(t,2,12)':fontfile='{1}':textfile='{0}':fontcolor=white:fontsize=h/23:box=1:boxcolor=black@0.5:boxborderw=5:x=w/70:y=h*18.5/20:alpha='if(lt(t,2),0,if(lt(t,3),(t-2)/1,if(lt(t,11),1,if(lt(t,12),(1-(t-11))/1,0))))'"\
			.format(subtitle_file.replace("\\", "\\\\").replace(":", "\\:"), fontfile.replace("\\", "\\\\").replace(":", "\\:"))
		else:
			subtitle_filter = ''

		if sample_frame_last:
			title_filter = r",drawtext=text='{0}':fontfile='{1}':fontcolor=white:fontsize=h/25:box=1:boxcolor=black@0.5:boxborderw=5:x=w/2-text_w/2:y=h/2-text_h/2".format("Videos have all ended, at most {0} blank seconds will be rendered at the end".format(MAX_BLANK_SECONDS_AT_END), fontfile.replace("\\", "\\\\").replace(":", "\\:"))
			subtitle_filter = ''
		
		filter_text += layout['filter_layout'].format(title_filter,subtitle_filter)

		if not sample_frame:

			if not replace_audio:

				comm_q.put((SIGNAL_STDOUT_DATA, "\nRendering the final video:\n"))
			
				ff_args.extend(['-filter_complex', filter_text, "-map", "[out]", "-r", str(FRAMERATE), "-map", "{0}:a".format(num_frames)])
				
				ff_args.extend(["-c:v", "libx264", "-crf", str(VID_QUALITY), "-c:a", "copy", "-shortest"])
				if vid_duration is not None:
					ff_args.extend(["-t", str(vid_duration), "-y"])
				ff_args.append(output_file)
			
				ff_final = ff_args
				
				run_external(ff_final, comm_q, tempdir, FFPATHS = FFPATHS)
				
			else:
				copy_file = os.path.splitext(output_file)[0] + ".new_audio.mp4"
				comm_q.put((SIGNAL_STDOUT_DATA, "\nReplacing audio and saving as {0}:\n".format(copy_file)))
				run_external([FFMPEG_PATH, "-i", output_file, "-i", audio_file_encoded, "-codec", "copy", "-map", "0:v", "-map", "1:a", "-y", copy_file], comm_q, tempdir, FFPATHS = FFPATHS)
				
			os.remove(audio_file_encoded)
		
			if (is_installed("fdkaac")) or (acodec != "aac"):
				comm_q.put((SIGNAL_MESSAGE, "Render finished"))
			else:
				comm_q.put((SIGNAL_MESSAGE, "Render finished, install fdkaac for better quality aac audio"))			
				
		else:
			
			samplejpeg = os.path.join(tempdir.name, "sample.png")
		
			ff_args.extend(['-filter_complex', filter_text, "-map", "[out]", "-vframes", "1", "-y", samplejpeg])

			ff_final = ff_args
				
			run_external(ff_final, None, tempdir, FFPATHS = FFPATHS)

			comm_q.put((SIGNAL_PREVIEW_DONE, samplejpeg))

	except:
		if not sample_frame:
			comm_q.put((SIGNAL_MESSAGE, "Something went wrong...\n" + get_exception_message()))

def main():

	app = QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
	Ui() # Create an instance of our class
	
	app.exec_() # Start the application
	
	del app

if __name__ == "__main__":
	
	main()

