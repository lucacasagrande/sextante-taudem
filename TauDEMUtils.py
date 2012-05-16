# -*- coding: utf-8 -*-

#******************************************************************************
#
# TauDEM SEXTANTE Provider
# ---------------------------------------------------------
# A suite of Digital Elevation Model (DEM) tools for the extraction and
# analysis of hydrologic information from topography as represented by
# a DEM of vector layer.
#
# Copyright (C) 2012 Alexander Bruy (alexander.bruy@gmail.com)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
#******************************************************************************

import os
import subprocess

from sextante.core.SextanteConfig import SextanteConfig
from sextante.core.SextanteLog import SextanteLog
from sextante.core.SextanteUtils import SextanteUtils

class TauDEMUtils:

    TAUDEM_FOLDER = "TAUDEM_FOLDER"

    @staticmethod
    def taudemPath():
        folder = SextanteConfig.getSetting(TauDEMUtils.TAUDEM_FOLDER)
        if folder == None:
            folder = ""

        return folder

    @staticmethod
    def taudemDescriptionPath():
        return os.path.join(os.path.dirname(__file__), "description")

    @staticmethod
    def executeSaga(progress):
        if SextanteUtils.isWindows():
            command = ["cmd.exe", "/C ", SagaUtils.sagaBatchJobFilename()]
        else:
            os.chmod(SagaUtils.sagaBatchJobFilename(), stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
            command = [SagaUtils.sagaBatchJobFilename()]
        loglines = []
        loglines.append("SAGA execution console output")
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines=True).stdout
        for line in iter(proc.readline, ""):
            if "%" in line:
                s = "".join([x for x in line if x.isdigit()])
                progress.setPercentage(int(s))
            else:
                loglines.append(line)
        SextanteLog.addToLog(SextanteLog.LOG_INFO, loglines)

    @staticmethod
    def executeOtb(commands, progress):
        loglines = []
        loglines.append("OTB execution console output")
        os.putenv('ITK_AUTOLOAD_PATH', OTBUtils.otbLibPath())
        fused_command = ''.join(['"%s" ' % c for c in commands])
        proc = subprocess.Popen(fused_command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines=True).stdout
        for line in iter(proc.readline, ""):
            if "[*" in line:
                idx = line.find("[*")
                perc = int(line[idx-4:idx-2].strip(" "))
                if perc !=0:
                    progress.setPercentage(perc)
            else:
                loglines.append(line)
        SextanteLog.addToLog(SextanteLog.LOG_INFO, loglines)

    @staticmethod
    def executeTauDEM(command, progress):
        loglines = []
        loglines.append("TauDEM execution console output")
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout
        for line in iter(proc.readline, ""):
            if "%" in line:
                s = "".join([x for x in line if x.isdigit()])
                progress.setPercentage(int(s))
            else:
                loglines.append(line)
        SextanteLog.addToLog(SextanteLog.LOG_INFO, loglines)