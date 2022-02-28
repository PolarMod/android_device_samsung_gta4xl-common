#!/bin/env python3
#
# Copyright (C) 2020 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import common
import re

def FullOTA_InstallEnd(info):
  OTA_InstallEnd(info)
  return

def IncrementalOTA_InstallEnd(info):
  OTA_InstallEnd(info, True)
  return

def AddImage(info, basename, dest, incremental=False, path="IMAGES/"):
  name = basename
  print("Reading image from", path+name)
  if incremental:
      data = info.source_zip.read(path + basename)
  else:
      data = info.input_zip.read(path + basename)
  common.ZipWriteStr(info.output_zip, name, data)
  info.script.AppendExtra('package_extract_file("%s", "%s");' % (name, dest))

def PrintInfo(info, dest):
  info.script.Print("Patching {} image unconditionally...".format(dest.split('/')[-1]))

def OTA_InstallEnd(info, incremental=False):
  PrintInfo(info, "/dev/block/by-name/dtbo")
  AddImage(info, "dtbo.img", "/dev/block/by-name/dtbo", incremental)
  PrintInfo(info, "/dev/block/by-name/vbmeta")
  AddImage(info, "vbmeta.img", "/dev/block/by-name/vbmeta", incremental)
  PrintInfo(info, "/dev/block/by-name/recovery")
  AddImage(info, "recovery-two-step.img", "/dev/block/by-name/recovery", incremental, path="OTA/")
  return
