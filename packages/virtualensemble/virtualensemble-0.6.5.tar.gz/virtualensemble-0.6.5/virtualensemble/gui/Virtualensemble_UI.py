# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Virtualensemble.ui'
##
## Created by: Qt User Interface Compiler version 6.0.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1090, 926)
        self.action_Open = QAction(MainWindow)
        self.action_Open.setObjectName(u"action_Open")
        self.action_Save = QAction(MainWindow)
        self.action_Save.setObjectName(u"action_Save")
        self.action_SaveAs = QAction(MainWindow)
        self.action_SaveAs.setObjectName(u"action_SaveAs")
        self.action_New = QAction(MainWindow)
        self.action_New.setObjectName(u"action_New")
        self.action_Exit = QAction(MainWindow)
        self.action_Exit.setObjectName(u"action_Exit")
        self.action_About = QAction(MainWindow)
        self.action_About.setObjectName(u"action_About")
        self.action_Usage_guide = QAction(MainWindow)
        self.action_Usage_guide.setObjectName(u"action_Usage_guide")
        self.action_Choose_FFmpeg_location = QAction(MainWindow)
        self.action_Choose_FFmpeg_location.setObjectName(u"action_Choose_FFmpeg_location")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.main_tab = QTabWidget(self.centralwidget)
        self.main_tab.setObjectName(u"main_tab")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_5 = QGridLayout(self.tab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_8 = QLabel(self.tab)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.copy_video = QLineEdit(self.tab)
        self.copy_video.setObjectName(u"copy_video")
        self.copy_video.setReadOnly(True)

        self.horizontalLayout_9.addWidget(self.copy_video)

        self.copy_video_button = QPushButton(self.tab)
        self.copy_video_button.setObjectName(u"copy_video_button")

        self.horizontalLayout_9.addWidget(self.copy_video_button)


        self.formLayout_3.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_9)

        self.label_11 = QLabel(self.tab)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_11)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.copy_audio = QLineEdit(self.tab)
        self.copy_audio.setObjectName(u"copy_audio")
        self.copy_audio.setReadOnly(True)

        self.horizontalLayout_10.addWidget(self.copy_audio)

        self.copy_audio_button = QPushButton(self.tab)
        self.copy_audio_button.setObjectName(u"copy_audio_button")

        self.horizontalLayout_10.addWidget(self.copy_audio_button)


        self.formLayout_3.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_10)

        self.label_15 = QLabel(self.tab)
        self.label_15.setObjectName(u"label_15")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_15)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.copy_output = QLineEdit(self.tab)
        self.copy_output.setObjectName(u"copy_output")
        self.copy_output.setReadOnly(True)

        self.horizontalLayout_11.addWidget(self.copy_output)

        self.copy_output_button = QPushButton(self.tab)
        self.copy_output_button.setObjectName(u"copy_output_button")

        self.horizontalLayout_11.addWidget(self.copy_output_button)


        self.formLayout_3.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_11)

        self.label_18 = QLabel(self.tab)
        self.label_18.setObjectName(u"label_18")

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.label_18)

        self.copy_start = QTimeEdit(self.tab)
        self.copy_start.setObjectName(u"copy_start")

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.copy_start)

        self.label_19 = QLabel(self.tab)
        self.label_19.setObjectName(u"label_19")

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.label_19)

        self.copy_end = QTimeEdit(self.tab)
        self.copy_end.setObjectName(u"copy_end")
        self.copy_end.setDateTime(QDateTime(QDate(2000, 1, 1), QTime(2, 0, 0)))

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.copy_end)

        self.copy_aac = QCheckBox(self.tab)
        self.copy_aac.setObjectName(u"copy_aac")

        self.formLayout_3.setWidget(5, QFormLayout.FieldRole, self.copy_aac)

        self.copy_non_normalised = QCheckBox(self.tab)
        self.copy_non_normalised.setObjectName(u"copy_non_normalised")
        self.copy_non_normalised.setChecked(True)

        self.formLayout_3.setWidget(6, QFormLayout.FieldRole, self.copy_non_normalised)


        self.gridLayout_5.addLayout(self.formLayout_3, 0, 0, 1, 1)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")

        self.gridLayout_5.addLayout(self.verticalLayout_8, 2, 0, 1, 1)

        self.copy_render_button = QPushButton(self.tab)
        self.copy_render_button.setObjectName(u"copy_render_button")

        self.gridLayout_5.addWidget(self.copy_render_button, 1, 0, 1, 1)

        self.main_tab.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_6 = QVBoxLayout(self.tab_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabWidget = QTabWidget(self.tab_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_9 = QVBoxLayout(self.tab_4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_21 = QLabel(self.tab_4)
        self.label_21.setObjectName(u"label_21")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_21)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.backing_audio = QLineEdit(self.tab_4)
        self.backing_audio.setObjectName(u"backing_audio")
        self.backing_audio.setReadOnly(True)

        self.horizontalLayout_13.addWidget(self.backing_audio)

        self.backing_audio_button = QPushButton(self.tab_4)
        self.backing_audio_button.setObjectName(u"backing_audio_button")

        self.horizontalLayout_13.addWidget(self.backing_audio_button)


        self.formLayout_4.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_13)

        self.label_22 = QLabel(self.tab_4)
        self.label_22.setObjectName(u"label_22")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_22)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.backing_output = QLineEdit(self.tab_4)
        self.backing_output.setObjectName(u"backing_output")
        self.backing_output.setReadOnly(True)

        self.horizontalLayout_14.addWidget(self.backing_output)

        self.backing_output_button = QPushButton(self.tab_4)
        self.backing_output_button.setObjectName(u"backing_output_button")

        self.horizontalLayout_14.addWidget(self.backing_output_button)


        self.formLayout_4.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_14)


        self.verticalLayout_7.addLayout(self.formLayout_4)

        self.create_backing_button = QPushButton(self.tab_4)
        self.create_backing_button.setObjectName(u"create_backing_button")

        self.verticalLayout_7.addWidget(self.create_backing_button)


        self.verticalLayout_9.addLayout(self.verticalLayout_7)

        self.tabWidget.addTab(self.tab_4, "")
        self.tabWidgetPage1 = QWidget()
        self.tabWidgetPage1.setObjectName(u"tabWidgetPage1")
        self.gridLayout_2 = QGridLayout(self.tabWidgetPage1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_12 = QLabel(self.tabWidgetPage1)
        self.label_12.setObjectName(u"label_12")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_12)

        self.sync_target = QDoubleSpinBox(self.tabWidgetPage1)
        self.sync_target.setObjectName(u"sync_target")
        self.sync_target.setEnabled(False)
        self.sync_target.setDecimals(3)
        self.sync_target.setMaximum(10000000000000000139372116959414099130712064.000000000000000)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.sync_target)


        self.verticalLayout_4.addLayout(self.formLayout_2)


        self.gridLayout_2.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.add_files_button = QPushButton(self.tabWidgetPage1)
        self.add_files_button.setObjectName(u"add_files_button")

        self.gridLayout_3.addWidget(self.add_files_button, 0, 0, 1, 1)

        self.remove_all_button = QPushButton(self.tabWidgetPage1)
        self.remove_all_button.setObjectName(u"remove_all_button")

        self.gridLayout_3.addWidget(self.remove_all_button, 1, 1, 1, 1)

        self.remove_files_button = QPushButton(self.tabWidgetPage1)
        self.remove_files_button.setObjectName(u"remove_files_button")

        self.gridLayout_3.addWidget(self.remove_files_button, 1, 0, 1, 1)

        self.sync_audio_output_button = QPushButton(self.tabWidgetPage1)
        self.sync_audio_output_button.setObjectName(u"sync_audio_output_button")

        self.gridLayout_3.addWidget(self.sync_audio_output_button, 0, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.tabWidgetPage2 = QWidget()
        self.tabWidgetPage2.setObjectName(u"tabWidgetPage2")
        self.verticalLayout_2 = QVBoxLayout(self.tabWidgetPage2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")

        self.formLayout.setLayout(0, QFormLayout.LabelRole, self.horizontalLayout_6)

        self.label = QLabel(self.tabWidgetPage2)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.number_of_videos = QSpinBox(self.tabWidgetPage2)
        self.number_of_videos.setObjectName(u"number_of_videos")
        self.number_of_videos.setMinimum(1)
        self.number_of_videos.setMaximum(144)
        self.number_of_videos.setValue(4)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.number_of_videos)

        self.row_layout = QCheckBox(self.tabWidgetPage2)
        self.row_layout.setObjectName(u"row_layout")
        self.row_layout.setChecked(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.row_layout)

        self.label_23 = QLabel(self.tabWidgetPage2)
        self.label_23.setObjectName(u"label_23")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_23)

        self.num_rows = QSpinBox(self.tabWidgetPage2)
        self.num_rows.setObjectName(u"num_rows")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.num_rows)

        self.label_9 = QLabel(self.tabWidgetPage2)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_9)

        self.border = QSpinBox(self.tabWidgetPage2)
        self.border.setObjectName(u"border")
        self.border.setMaximum(20)
        self.border.setValue(3)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.border)

        self.label_6 = QLabel(self.tabWidgetPage2)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.render_audio = QLineEdit(self.tabWidgetPage2)
        self.render_audio.setObjectName(u"render_audio")
        self.render_audio.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.render_audio)

        self.render_audio_button = QPushButton(self.tabWidgetPage2)
        self.render_audio_button.setObjectName(u"render_audio_button")

        self.horizontalLayout_3.addWidget(self.render_audio_button)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.vorbis = QCheckBox(self.tabWidgetPage2)
        self.vorbis.setObjectName(u"vorbis")
        self.vorbis.setChecked(True)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.vorbis)

        self.label_7 = QLabel(self.tabWidgetPage2)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_7)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.render_output = QLineEdit(self.tabWidgetPage2)
        self.render_output.setObjectName(u"render_output")
        self.render_output.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.render_output)

        self.render_output_button = QPushButton(self.tabWidgetPage2)
        self.render_output_button.setObjectName(u"render_output_button")

        self.horizontalLayout_4.addWidget(self.render_output_button)


        self.formLayout.setLayout(7, QFormLayout.FieldRole, self.horizontalLayout_4)

        self.label_2 = QLabel(self.tabWidgetPage2)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(self.tabWidgetPage2)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(11, QFormLayout.LabelRole, self.label_3)

        self.label_4 = QLabel(self.tabWidgetPage2)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(14, QFormLayout.LabelRole, self.label_4)

        self.title = QLineEdit(self.tabWidgetPage2)
        self.title.setObjectName(u"title")

        self.formLayout.setWidget(14, QFormLayout.FieldRole, self.title)

        self.label_5 = QLabel(self.tabWidgetPage2)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(15, QFormLayout.LabelRole, self.label_5)

        self.subtitle = QLineEdit(self.tabWidgetPage2)
        self.subtitle.setObjectName(u"subtitle")

        self.formLayout.setWidget(15, QFormLayout.FieldRole, self.subtitle)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")

        self.formLayout.setLayout(19, QFormLayout.FieldRole, self.horizontalLayout_5)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.start = QTimeEdit(self.tabWidgetPage2)
        self.start.setObjectName(u"start")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start.sizePolicy().hasHeightForWidth())
        self.start.setSizePolicy(sizePolicy)

        self.horizontalLayout_18.addWidget(self.start)

        self.start_grab = QPushButton(self.tabWidgetPage2)
        self.start_grab.setObjectName(u"start_grab")

        self.horizontalLayout_18.addWidget(self.start_grab)


        self.formLayout.setLayout(9, QFormLayout.FieldRole, self.horizontalLayout_18)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.end = QTimeEdit(self.tabWidgetPage2)
        self.end.setObjectName(u"end")
        sizePolicy.setHeightForWidth(self.end.sizePolicy().hasHeightForWidth())
        self.end.setSizePolicy(sizePolicy)
        self.end.setDateTime(QDateTime(QDate(2000, 1, 1), QTime(1, 0, 0)))
        self.end.setMinimumTime(QTime(0, 0, 10))
        self.end.setTime(QTime(1, 0, 0))

        self.horizontalLayout_19.addWidget(self.end)

        self.end_grab = QPushButton(self.tabWidgetPage2)
        self.end_grab.setObjectName(u"end_grab")

        self.horizontalLayout_19.addWidget(self.end_grab)


        self.formLayout.setLayout(11, QFormLayout.FieldRole, self.horizontalLayout_19)


        self.verticalLayout_3.addLayout(self.formLayout)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.render_button = QPushButton(self.tabWidgetPage2)
        self.render_button.setObjectName(u"render_button")

        self.horizontalLayout_7.addWidget(self.render_button)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.replace_audio_only_button = QPushButton(self.tabWidgetPage2)
        self.replace_audio_only_button.setObjectName(u"replace_audio_only_button")

        self.horizontalLayout_17.addWidget(self.replace_audio_only_button)

        self.encode_audio_only_button = QPushButton(self.tabWidgetPage2)
        self.encode_audio_only_button.setObjectName(u"encode_audio_only_button")

        self.horizontalLayout_17.addWidget(self.encode_audio_only_button)


        self.verticalLayout_3.addLayout(self.horizontalLayout_17)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.tabWidget.addTab(self.tabWidgetPage2, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.preview_placeholder = QHBoxLayout()
        self.preview_placeholder.setSpacing(0)
        self.preview_placeholder.setObjectName(u"preview_placeholder")

        self.verticalLayout_5.addLayout(self.preview_placeholder)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.preview_slider = QSlider(self.tab_2)
        self.preview_slider.setObjectName(u"preview_slider")
        self.preview_slider.setMaximum(7200)
        self.preview_slider.setSingleStep(1)
        self.preview_slider.setValue(3600)
        self.preview_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_16.addWidget(self.preview_slider)

        self.current_time = QLabel(self.tab_2)
        self.current_time.setObjectName(u"current_time")

        self.horizontalLayout_16.addWidget(self.current_time)


        self.verticalLayout_5.addLayout(self.horizontalLayout_16)

        self.label_14 = QLabel(self.tab_2)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_14)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.video_table = QTableView(self.tab_2)
        self.video_table.setObjectName(u"video_table")
        self.video_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.video_table.horizontalHeader().setMinimumSectionSize(70)
        self.video_table.verticalHeader().setCascadingSectionResizes(False)

        self.verticalLayout_6.addWidget(self.video_table)

        self.main_tab.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_4 = QGridLayout(self.tab_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stdout = QPlainTextEdit(self.tab_3)
        self.stdout.setObjectName(u"stdout")
        self.stdout.setReadOnly(True)

        self.verticalLayout.addWidget(self.stdout)

        self.abort_button = QPushButton(self.tab_3)
        self.abort_button.setObjectName(u"abort_button")

        self.verticalLayout.addWidget(self.abort_button)


        self.gridLayout_4.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.main_tab.addTab(self.tab_3, "")

        self.gridLayout.addWidget(self.main_tab, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1090, 27))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menu_Help = QMenu(self.menubar)
        self.menu_Help.setObjectName(u"menu_Help")
        self.menu_Options = QMenu(self.menubar)
        self.menu_Options.setObjectName(u"menu_Options")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.main_tab, self.copy_video)
        QWidget.setTabOrder(self.copy_video, self.copy_video_button)
        QWidget.setTabOrder(self.copy_video_button, self.copy_audio)
        QWidget.setTabOrder(self.copy_audio, self.copy_audio_button)
        QWidget.setTabOrder(self.copy_audio_button, self.copy_output)
        QWidget.setTabOrder(self.copy_output, self.copy_output_button)
        QWidget.setTabOrder(self.copy_output_button, self.copy_start)
        QWidget.setTabOrder(self.copy_start, self.copy_end)
        QWidget.setTabOrder(self.copy_end, self.copy_aac)
        QWidget.setTabOrder(self.copy_aac, self.copy_non_normalised)
        QWidget.setTabOrder(self.copy_non_normalised, self.copy_render_button)
        QWidget.setTabOrder(self.copy_render_button, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.backing_audio)
        QWidget.setTabOrder(self.backing_audio, self.backing_audio_button)
        QWidget.setTabOrder(self.backing_audio_button, self.backing_output)
        QWidget.setTabOrder(self.backing_output, self.backing_output_button)
        QWidget.setTabOrder(self.backing_output_button, self.create_backing_button)
        QWidget.setTabOrder(self.create_backing_button, self.sync_target)
        QWidget.setTabOrder(self.sync_target, self.add_files_button)
        QWidget.setTabOrder(self.add_files_button, self.sync_audio_output_button)
        QWidget.setTabOrder(self.sync_audio_output_button, self.remove_files_button)
        QWidget.setTabOrder(self.remove_files_button, self.remove_all_button)
        QWidget.setTabOrder(self.remove_all_button, self.number_of_videos)
        QWidget.setTabOrder(self.number_of_videos, self.row_layout)
        QWidget.setTabOrder(self.row_layout, self.num_rows)
        QWidget.setTabOrder(self.num_rows, self.border)
        QWidget.setTabOrder(self.border, self.render_audio)
        QWidget.setTabOrder(self.render_audio, self.render_audio_button)
        QWidget.setTabOrder(self.render_audio_button, self.vorbis)
        QWidget.setTabOrder(self.vorbis, self.render_output)
        QWidget.setTabOrder(self.render_output, self.render_output_button)
        QWidget.setTabOrder(self.render_output_button, self.start)
        QWidget.setTabOrder(self.start, self.start_grab)
        QWidget.setTabOrder(self.start_grab, self.end)
        QWidget.setTabOrder(self.end, self.end_grab)
        QWidget.setTabOrder(self.end_grab, self.title)
        QWidget.setTabOrder(self.title, self.subtitle)
        QWidget.setTabOrder(self.subtitle, self.render_button)
        QWidget.setTabOrder(self.render_button, self.replace_audio_only_button)
        QWidget.setTabOrder(self.replace_audio_only_button, self.encode_audio_only_button)
        QWidget.setTabOrder(self.encode_audio_only_button, self.preview_slider)
        QWidget.setTabOrder(self.preview_slider, self.video_table)
        QWidget.setTabOrder(self.video_table, self.abort_button)
        QWidget.setTabOrder(self.abort_button, self.stdout)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Options.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.menuFile.addAction(self.action_New)
        self.menuFile.addAction(self.action_Open)
        self.menuFile.addAction(self.action_Save)
        self.menuFile.addAction(self.action_SaveAs)
        self.menuFile.addAction(self.action_Exit)
        self.menu_Help.addAction(self.action_Usage_guide)
        self.menu_Help.addAction(self.action_About)
        self.menu_Options.addAction(self.action_Choose_FFmpeg_location)

        self.retranslateUi(MainWindow)

        self.main_tab.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"VirtualEnsemble", None))
        self.action_Open.setText(QCoreApplication.translate("MainWindow", u"&Open", None))
#if QT_CONFIG(shortcut)
        self.action_Open.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_Save.setText(QCoreApplication.translate("MainWindow", u"&Save", None))
#if QT_CONFIG(shortcut)
        self.action_Save.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_SaveAs.setText(QCoreApplication.translate("MainWindow", u"S&ave As", None))
#if QT_CONFIG(shortcut)
        self.action_SaveAs.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+A", None))
#endif // QT_CONFIG(shortcut)
        self.action_New.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.action_Exit.setText(QCoreApplication.translate("MainWindow", u"E&xit", None))
        self.action_About.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.action_Usage_guide.setText(QCoreApplication.translate("MainWindow", u"Usage guide", None))
        self.action_Choose_FFmpeg_location.setText(QCoreApplication.translate("MainWindow", u"Choose FFmpeg location", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Video:", None))
        self.copy_video_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Audio:", None))
        self.copy_audio_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Output:", None))
        self.copy_output_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Video start (hh:mm:ss.):", None))
        self.copy_start.setDisplayFormat(QCoreApplication.translate("MainWindow", u"hh:mm:ss.zzz", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Video end (hh:mm:ss.):", None))
        self.copy_end.setDisplayFormat(QCoreApplication.translate("MainWindow", u"HH:mm:ss.zzz", None))
        self.copy_aac.setText(QCoreApplication.translate("MainWindow", u"Use aac audio", None))
        self.copy_non_normalised.setText(QCoreApplication.translate("MainWindow", u"Don't normalise audio", None))
        self.copy_render_button.setText(QCoreApplication.translate("MainWindow", u"Render", None))
        self.main_tab.setTabText(self.main_tab.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Copy video / sync audio", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Audio file:", None))
        self.backing_audio_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Output file:", None))
        self.backing_output_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.create_backing_button.setText(QCoreApplication.translate("MainWindow", u"Create backing track", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Create backing track", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Sync target (secs):", None))
        self.add_files_button.setText(QCoreApplication.translate("MainWindow", u"Add files and calculate lags...", None))
        self.remove_all_button.setText(QCoreApplication.translate("MainWindow", u"Remove all and target", None))
        self.remove_files_button.setText(QCoreApplication.translate("MainWindow", u"Remove selected files", None))
        self.sync_audio_output_button.setText(QCoreApplication.translate("MainWindow", u"Output synchronised audio", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), QCoreApplication.translate("MainWindow", u"Add files", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Number of videos:", None))
        self.row_layout.setText(QCoreApplication.translate("MainWindow", u"Row layout", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"No. rows/cols:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Border width:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Audio file (optional):", None))
        self.render_audio_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.vorbis.setText(QCoreApplication.translate("MainWindow", u"High quality audio \n"
"(not Windows/Mac compatible unless using vlc player or similar)", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Output file:", None))
        self.render_output_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Start (hh:mm:ss):", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"End (hh:mm:ss.):", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Title:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Subtitle:", None))
        self.start.setDisplayFormat(QCoreApplication.translate("MainWindow", u"HH:mm:ss.zzz", None))
        self.start_grab.setText(QCoreApplication.translate("MainWindow", u"Grab", None))
        self.end.setDisplayFormat(QCoreApplication.translate("MainWindow", u"HH:mm:ss.zzz", None))
        self.end_grab.setText(QCoreApplication.translate("MainWindow", u"Grab", None))
        self.render_button.setText(QCoreApplication.translate("MainWindow", u"Render", None))
        self.replace_audio_only_button.setText(QCoreApplication.translate("MainWindow", u"Replace audio in video", None))
        self.encode_audio_only_button.setText(QCoreApplication.translate("MainWindow", u"Encode audio only", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage2), QCoreApplication.translate("MainWindow", u"Render", None))
        self.current_time.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Shift, click and drag = zoom\n"
"Click and drag within a frame = move\n"
"Click and drag out of the preview = reset\n"
"Click and drag to another frame = swap position\n"
"N.B. the preview takes time to update but you can make other changes in the meantime", None))
        self.main_tab.setTabText(self.main_tab.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Mosaic maker", None))
        self.abort_button.setText(QCoreApplication.translate("MainWindow", u"Abort", None))
        self.main_tab.setTabText(self.main_tab.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Output", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menu_Help.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
        self.menu_Options.setTitle(QCoreApplication.translate("MainWindow", u"&Options", None))
    # retranslateUi

