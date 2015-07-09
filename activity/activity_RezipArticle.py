import os
import boto.swf
import json
import random
import datetime
import importlib
import calendar
import time

import zipfile
import requests
import urlparse
import glob
import shutil
import re

import activity

import boto.s3
from boto.s3.connection import S3Connection

import provider.article as articlelib
import provider.s3lib as s3lib


"""
RezipArticle activity
"""

class activity_RezipArticle(activity.activity):
    
    def __init__(self, settings, logger, conn = None, token = None, activity_task = None):
        activity.activity.__init__(self, settings, logger, conn, token, activity_task)

        self.name = "RezipArticle"
        self.version = "1"
        self.default_task_heartbeat_timeout = 30
        self.default_task_schedule_to_close_timeout = 60*30
        self.default_task_schedule_to_start_timeout = 30
        self.default_task_start_to_close_timeout= 60*15
        self.description = "Download files for an article, unzip them, rename, modify, zip them and upload again."
        
        # Bucket settings
        self.article_bucket = settings.bucket
        self.poa_bucket = settings.poa_packaging_bucket
        
        # Bucket settings
        self.article_bucket = settings.bucket
        
        # Local directory settings
        self.TMP_DIR = "tmp_dir"
        self.INPUT_DIR = "input_dir"
        self.JUNK_DIR = "junk_dir"
        self.ZIP_DIR = "zip_dir" 
        self.OUTPUT_DIR = "output_dir"
       
        # Bucket settings
        self.output_bucket = "elife-articles-renamed"
        
            
    def do_activity(self, data = None):
        """
        Activity, do the work
        """
        if(self.logger):
            self.logger.info('data: %s' % json.dumps(data, sort_keys=True, indent=4))
        
        # Data passed to this activity
        elife_id = data["data"]["elife_id"]
        
        # Create output directories
        self.create_activity_directories()

        # Download the S3 objects
        self.download_files_from_s3(elife_id)
        
        # Return the activity result, True or False
        result = True

        return result

    def download_files_from_s3(self, doi_id):
        
        self.download_vor_files_from_s3(doi_id)


    def download_poa_files_from_s3(self, doi_id):
        """

        """
        pass
        
    def download_vor_files_from_s3(self, doi_id):
        """

        """
        subfolder_name = str(doi_id).zfill(5)
        prefix = subfolder_name + '/'
        
        # Connect to S3 and bucket
        s3_conn = S3Connection(self.settings.aws_access_key_id, self.settings.aws_secret_access_key)
        bucket = s3_conn.lookup(self.article_bucket)

        # get item list from S3
        s3_key_names = s3lib.get_s3_key_names_from_bucket(
            bucket = bucket,
            prefix = prefix)
        
        # Remove the prefix itself, is also a key it seems
        if prefix in s3_key_names:
            s3_key_names.remove(prefix)
   
        self.download_s3_key_names_to_subfolder(bucket, s3_key_names, subfolder_name)
        
        
        
    def download_s3_key_names_to_subfolder(self, bucket, s3_key_names, subfolder_name):
        
        for s3_key_name in s3_key_names:
            # Download objects from S3 and save to disk
            
            s3_key = bucket.get_key(s3_key_name)

            filename = s3_key_name.split("/")[-1]

            # Make the subfolder if it does not exist yet
            try:
                os.mkdir(self.get_tmp_dir() + os.sep + self.INPUT_DIR
                         + os.sep + subfolder_name)
            except:
                pass

            filename_plus_path = (self.get_tmp_dir() + os.sep +
                                  self.INPUT_DIR
                                  + os.sep + subfolder_name
                                  + os.sep + filename)
            mode = "wb"
            f = open(filename_plus_path, mode)
            s3_key.get_contents_to_file(f)
            f.close()












    def create_activity_directories(self):
        """
        Create the directories in the activity tmp_dir
        """
        try:
            os.mkdir(self.get_tmp_dir() + os.sep + self.TMP_DIR)
            os.mkdir(self.get_tmp_dir() + os.sep + self.INPUT_DIR)
            os.mkdir(self.get_tmp_dir() + os.sep + self.JUNK_DIR)
            os.mkdir(self.get_tmp_dir() + os.sep + self.ZIP_DIR)
            os.mkdir(self.get_tmp_dir() + os.sep + self.OUTPUT_DIR)
            
        except:
            pass