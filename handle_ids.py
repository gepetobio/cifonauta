#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Script looks into linked_media (folder with symbolic links) and identifies
# new files, which are copied to the site_media folder with unique names and
# converted to lightweight web formats.

import os
import pickle
import subprocess
from datetime import datetime
from shutil import copy2
from media_utils import read_iptc, rename_file, convert_to_web, watermarker, build_call, grab_still

# Directory with symbolic links files.
BASEPATH = os.path.abspath('linked_media/oficial')
# Directory with symbolic links files.
BASESITE = os.path.abspath('site_media')
# Get list of file names in site_media.
site_filenames = []
for root, dirs, files in os.walk(BASESITE):
    for filename in files:
        site_filenames.append(filename)
# Pickled file with unique names dumped from database.
db_filenames = pickle.load(open('unique_names.pkl'))
UNIQUE_NAMES = site_filenames + db_filenames
# File extensions.
PHOTO_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif',)
VIDEO_EXTENSIONS = ('avi', 'mov', 'mp4', 'ogg', 'ogv', 'dv', 'mpg', 'mpeg',
                    'flv', 'm2ts', 'wmv',)


class File:
    def __init__(self, root, filename):
        self.root = root
        self.filename = filename
        self.define_paths(self.root, self.filename)
        self.authors = self.get_authors()
        if not self.check_name():
            self.get_unique_name()
            self.rename_new()
            self.define_paths(self.root, self.filename)
            self.new = True
        else:
            self.new = False
        self.filetype = self.get_filetype()
        self.sitepath = self.prepare_sitepath()
        self.modified = self.check_timestamp()

    def define_paths(self, root, filename):
        '''Define and redefine filepaths.'''
        self.filepath = os.path.join(root.decode('utf-8'), filename.decode('utf-8'))
        self.abspath = os.path.abspath(self.filepath)
        self.srcpath = os.readlink(self.abspath)
        self.txt_abspath = self.check_txt()

    def prepare_sitepath(self):
        '''Prepare paths for site media.'''
        # Define filetype.
        middle_sitepath = os.path.join(BASESITE, self.filetype + 's')
        # Create directory.
        try:
            os.makedirs(middle_sitepath)
        except OSError:
            pass
        # Make sitepath always point to jpg file.
        jpg_filename = os.path.splitext(self.filename)[0] + '.jpg'
        # Build final path.
        sitepath = os.path.join(middle_sitepath, jpg_filename)
        return sitepath

    def check_timestamp(self):
        '''Compare timestamps between linked and site media.'''
        self.timestamp = datetime.fromtimestamp(os.path.getmtime(self.abspath))
        try:
            site_timestamp = datetime.fromtimestamp(
                os.path.getmtime(self.sitepath))
        except:
            return True
        if self.timestamp > site_timestamp:
            return True
        else:
            return False

    def copy_to_site(self):
        '''Copy linked file to site media directory.'''
        # copy2(self.abspath, self.sitepath)
        # subprocess.call(['touch', self.sitepath])
        if self.filetype == 'video':
            self.txt_sitepath = os.path.splitext(self.sitepath)[0] + '.txt'
            if self.txt_abspath:
                copy2(self.txt_abspath, self.txt_sitepath)

    def get_filetype(self):
        '''Discover if photo or video.'''
        if self.filename.lower().endswith(PHOTO_EXTENSIONS):
            return 'photo'
        elif self.filename.lower().endswith(VIDEO_EXTENSIONS):
            return 'video'
        else:
            return None

    def check_txt(self):
        '''Check if there is a .txt associated file.'''
        txt_abspath = os.path.splitext(self.abspath)[0] + '.txt'
        try:
            os.lstat(txt_abspath)
            return txt_abspath
        except:
            try:
                head = os.path.split(self.abspath)[0]
                tail = os.path.split(self.srcpath)[1]
                raw_txt = os.path.join(head, os.path.splitext(tail)[0] + '.txt')
                os.lstat(raw_txt)
                new_txt = os.path.splitext(self.abspath)[0] + '.txt'
                os.rename(raw_txt, new_txt)
                return new_txt
            except:
                return ''

    def get_authors(self):
        '''Reads IPTC and extracts authors.'''
        info_iptc = read_iptc(self.abspath)
        if info_iptc:
            return info_iptc.data['by-line']
        else:
            if self.txt_abspath:
                info_mov = pickle.load(open(self.txt_abspath))
                return info_mov['author']
            else:
                return ''

    def check_name(self):
        '''Verifies if file name is an ID.'''
        if os.path.splitext(self.filename)[0] + '.jpg' in UNIQUE_NAMES:
            return True
        else:
            return False

    def get_unique_name(self):
        '''Get a new unique name.'''
        unique_name = rename_file(self.filename, self.authors)
        self.filename = unique_name
        if self.check_name():
            self.get_unique_name()

    def rename_new(self):
        '''Rename link with unique name.'''
        self.renamed_path = os.path.join(os.path.split(self.abspath)[0],
                                         self.filename)
        os.rename(self.abspath, self.renamed_path)
        print(u'\nRenamed %s to %s' % (self.abspath, self.renamed_path))
        if self.txt_abspath:
            self.renamed_txt_abspath = os.path.join(
                os.path.split(self.txt_abspath)[0],
                os.path.splitext(self.filename)[0] + '.txt')
            os.rename(self.txt_abspath, self.renamed_txt_abspath)
            print(u'Renamed %s to %s' % (self.txt_abspath,
                                        self.renamed_txt_abspath))

    def process_for_web(self):
        '''Resize and add watermark for web.'''
        print(u'Processing %s...' % self.filename)
        if self.filetype == 'photo':
            try:
                # Convert file to web format.
                convert_to_web(self.abspath, self.sitepath)
                # Insert watermark.
                watermarker(self.sitepath)
            except IOError:
                print(u'Conversion error for %s, check ImageMagick.' %
                      self.sitepath)
            else:
                print(u'%s converted successfully!' % self.sitepath)
        elif self.filetype == 'video':
            ffmpeg_call = build_call(self.abspath)
            webm_path = os.path.splitext(self.sitepath)[0] + '.webm'
            mp4_path = os.path.splitext(self.sitepath)[0] + '.mp4'
            ogv_path = os.path.splitext(self.sitepath)[0] + '.ogv'
            # webm
            ffmpeg_call.append(webm_path)
            subprocess.call(ffmpeg_call)
            ffmpeg_call.pop()
            # mp4
            ffmpeg_call.append(mp4_path)
            subprocess.call(ffmpeg_call)
            ffmpeg_call.pop()
            # ogv
            ffmpeg_call.append(ogv_path)
            subprocess.call(ffmpeg_call)
            ffmpeg_call.pop()
            # Create still image.
            grab_still(mp4_path)
            # Finally, remove original source file to save space.
            #os.remove(self.sitepath)
        else:
            pass

# Search all links in linked_media.
for root, dirs, files in os.walk(BASEPATH):
    for filename in files:
        if not filename.endswith('.txt'):
            # Create instance and rename if necessary.
            one_file = File(root, filename)
            if one_file.new or one_file.modified:
                one_file.copy_to_site()
                one_file.process_for_web()
            else:
                continue
