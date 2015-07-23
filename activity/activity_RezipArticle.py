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
from elifetools import parseJATS as parser
from elifetools import xmlio

from wand.image import Image

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
        self.TMP_DIR = self.get_tmp_dir() + os.sep + "tmp_dir"
        self.INPUT_DIR = self.get_tmp_dir() + os.sep + "input_dir"
        self.JUNK_DIR = self.get_tmp_dir() + os.sep + "junk_dir"
        self.ZIP_DIR = self.get_tmp_dir() + os.sep + "zip_dir" 
        self.OUTPUT_DIR = self.get_tmp_dir() + os.sep + "output_dir"
       
        # Bucket settings
        self.output_bucket = "elife-articles-renamed"
        # Temporarily upload to a folder during development
        self.output_bucket_folder = "samples03/"
        
        # EPS file bucket
        self.eps_output_bucket = "elife-eps-renamed"
        self.eps_output_bucket_folder = ""
        self.tif_resolution = 600
        
        # Temporary detail of files from the zip files to an append log
        self.zip_file_contents_log_name = "rezip_article_zip_file_contents.txt"
        
        
        self.journal = 'elife'
            
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
        
        verified = None
        for folder in self.folder_list(self.INPUT_DIR):
            if(self.logger):
                self.logger.info('processing files in folder ' + folder)
            
            self.unzip_article_files(self.file_list(folder))
    
            (fid, status, version) = self.profile_article(self.INPUT_DIR, folder)
            
            file_name_map = self.rename_files(self.journal, fid, status,
                                              version, self.article_xml_file())
            
            (verified, renamed_list, not_renamed_list) = self.verify_rename_files(file_name_map)
            if(self.logger):
                self.logger.info("verified " + folder + ": " + str(verified))
                self.logger.info(file_name_map)

            if len(not_renamed_list) > 0:
                if(self.logger):
                    self.logger.info("not renamed " + str(not_renamed_list))
        
            # Get the new zip file name
            zip_file_name = self.new_zip_filename(self.journal, fid, status, version)
            self.create_new_zip(zip_file_name)
            
            if verified and zip_file_name:
                self.upload_article_zip_to_s3()
            
            # Copy EPS files
            #self.copy_eps_files_to_s3()
            
            # Covert EPS to tif
            #self.eps_to_tif()
            #self.copy_tif_files_to_s3()
            
            # Partial clean up
            self.clean_directories()
            
        # Get a list of file names and sizes
        self.log_zip_file_contents()
        
        # Full Clean up
        self.clean_directories(full = True)
            
        
        # Return the activity result, True or False
        if verified is True:
            result = True
        else:
            result = False

        return result

    def log_zip_file_contents(self):
        """
        For now, append zip file contents to a separate file
        """
        file_log = open(self.get_tmp_dir() + os.sep
                        + ".." + os.sep
                        + self.zip_file_contents_log_name, 'ab')
        for filename in self.file_list(self.ZIP_DIR):
            
            myzip = zipfile.ZipFile(filename, 'r')
            for i in myzip.infolist():
                file_log.write("\n" + filename.split(os.sep)[-1]
                               + "\t" + str(i.filename)
                               + "\t" + str(i.file_size))

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
                os.mkdir(self.INPUT_DIR + os.sep + subfolder_name)
            except:
                pass

            filename_plus_path = (self.INPUT_DIR
                                  + os.sep + subfolder_name
                                  + os.sep + filename)
            mode = "wb"
            f = open(filename_plus_path, mode)
            s3_key.get_contents_to_file(f)
            f.close()

    def upload_article_zip_to_s3(self):
        """
        Upload the article zip files to S3
        """
        
        bucket_name = self.output_bucket
        bucket_folder_name = self.output_bucket_folder
        
        # Connect to S3 and bucket
        s3_conn = S3Connection(self.settings.aws_access_key_id, self.settings.aws_secret_access_key)
        bucket = s3_conn.lookup(bucket_name)
    
        for file in self.file_list(self.ZIP_DIR):
            s3_key_name = bucket_folder_name + file.split(os.sep)[-1]
            s3key = boto.s3.key.Key(bucket)
            s3key.key = s3_key_name
            s3key.set_contents_from_filename(file, replace=True)
            if(self.logger):
                self.logger.info("uploaded " + s3_key_name + " to s3 bucket " + bucket_name)

    def copy_files_to_s3(self, dir_name, file_extension):
        """
        Copy .eps files or .tif to an S3 bucket for later
        code mostly copied from upload_article_zip_to_s3()
        and can probably refactor much of it into the s3 provider library later
        """

        bucket_name = self.eps_output_bucket
        bucket_folder_name = self.eps_output_bucket_folder
        
        # Connect to S3 and bucket
        s3_conn = S3Connection(self.settings.aws_access_key_id, self.settings.aws_secret_access_key)
        bucket = s3_conn.lookup(bucket_name)
    
        for file in self.file_list(dir_name):
            if file.split('.')[-1] == file_extension:
                s3_key_name = bucket_folder_name + file.split(os.sep)[-1]
                s3key = boto.s3.key.Key(bucket)
                s3key.key = s3_key_name
                s3key.set_contents_from_filename(file, replace=True)
                if(self.logger):
                    self.logger.info("uploaded " + s3_key_name + " to s3 bucket " + bucket_name)

    def copy_eps_files_to_s3(self):
        """
        Copy .eps files to an S3 bucket for later
        """
        self.copy_files_to_s3(dir_name = self.OUTPUT_DIR, file_extension = 'eps')
                    
    def copy_tif_files_to_s3(self):
        """
        Copy .tif files or .tif to an S3 bucket for later
        """
        self.copy_files_to_s3(dir_name = self.TMP_DIR, file_extension = 'tif')
          
    def eps_to_tif(self):
        """
        Covert eps file to tif format
        """
        for file in self.file_list(self.OUTPUT_DIR):
            if file.split('.')[-1] == 'eps':
                file_without_path = file.split(os.sep)[-1]
                tif_filename = self.TMP_DIR + os.sep + file_without_path.replace('.eps', '.tif')
                with Image(filename=file, resolution=self.tif_resolution) as img:
                     img.format = 'tif'
                     img.save(filename=tif_filename)
        

    def list_dir(self, dir_name):
        dir_list = os.listdir(dir_name)
        dir_list = map(lambda item: dir_name + os.sep + item, dir_list)
        return dir_list
    
    def folder_list(self, dir_name):
        dir_list = self.list_dir(dir_name)
        return filter(lambda item: os.path.isdir(item), dir_list)
    
    def file_list(self, dir_name):
        dir_list = self.list_dir(dir_name)
        return filter(lambda item: os.path.isfile(item), dir_list)
    
    def folder_name_from_name(self, input_dir, file_name):
        folder_name = file_name.split(input_dir)[1]
        folder_name = folder_name.split(os.sep)[1]
        return folder_name
    
    def file_name_from_name(self, file_name):
        name = file_name.split(os.sep)[-1]
        return name
    
    def file_extension(self, file_name):
        name = self.file_name_from_name(file_name)
        if name:
            if len(name.split('.')) > 1:
                return name.split('.')[-1]
            else:
                return None
        return None
    
    def file_type(self, file_name):
        """
        File type is the file extension is not a zip, and
        if a zip, then look for the second or last or third to last element
        that is not r1, r2, etc.
        """
        if not self.file_extension(file_name):
            return None
        
        if self.file_extension(file_name) != 'zip':
            return self.file_extension(file_name)
        else:
            if not file_name.split('.')[-2].startswith('r'):
                return file_name.split('.')[-2]
            elif not file_name.split('.')[-3].startswith('r'):
                return file_name.split('.')[-3]
        return None
    
    def unzip_or_move_file(self, file_name, to_dir, do_unzip = True):
        """
        If file extension is zip, then unzip contents
        If file the extension 
        """
        if (self.file_extension(file_name) == 'zip'
            and self.is_poa_ds_file(file_name) is False
            and do_unzip is True):
            # Unzip
            if(self.logger):
                self.logger.info("going to unzip " + file_name + " to " + to_dir)
            myzip = zipfile.ZipFile(file_name, 'r')
            myzip.extractall(to_dir)
    
        elif self.file_extension(file_name):
            # Copy
            if(self.logger):
                self.logger.info("going to move and not unzip " + file_name + " to " + to_dir)
            shutil.copyfile(file_name, to_dir + os.sep + self.file_name_from_name(file_name))
    
    
    def is_poa_ds_file(self, file_name):
        if self.file_name_from_name(file_name).split('.')[0].endswith('_ds'):
            return True
        return False
    
    def approve_file(self, file_name):
        """
        Choose which files to unzip and keep, basically do not need svg or jpg packages
        """
        good_zip_file_types = ['xml','pdf','img','video','suppl','figures']
        if self.file_type(file_name) in good_zip_file_types:
            return True
        # Check for PoA DS files
        if self.is_poa_ds_file(file_name):
            return True
        
        # Default
        return False
    
    
    def unzip_article_files(self, file_list):
        
        for file_name in file_list:
            if self.approve_file(file_name):
                if(self.logger):
                    self.logger.info("unzipping or moving file " + file_name)
                self.unzip_or_move_file(file_name, self.TMP_DIR)
                folder_name = self.folder_name_from_name(self.INPUT_DIR, file_name)
            else:
                if(self.logger):
                    self.logger.info("not approved for repackaging " + file_name)
                self.unzip_or_move_file(file_name, self.JUNK_DIR, do_unzip = False)
    
    def add_filename_fid(self, filename, fid):
        return filename + '-' + str(fid).zfill(5)
        
    def add_filename_status(self, filename, status):
        return filename + '-' + status.lower()
        
    def add_filename_version(self, filename, version):
        if version is None:
            return filename
        else:
            return filename + '-' + 'v' + str(version)
            
    def add_filename_asset(self, filename, asset, ordinal = None):
        filename += '-' + asset
        if ordinal:
            filename += str(ordinal)
        return filename
    
    def new_filename(self, soup, old_filename, journal, fid, status, version = None):
        
        new_filename = None
        
        new_filename = self.new_filename_special(soup, old_filename, journal, fid, status, version)
        if not new_filename:
            new_filename = self.new_filename_generic(soup, old_filename, journal, fid, status, version)  
            
        return new_filename
    
    def new_filename_special(self, soup, old_filename, journal, fid, status, version):
        """
        Special files to be renamed in a certain way, if it matches any of these rules
        If it does not, then try new_filename_generic on the file name
        """
        new_filename = None
    
        if old_filename.endswith('.xml'):
            # Confirm it is the article XML file
            if (old_filename == 'elife' + str(fid).zfill(5) + '.xml'
                or old_filename.startswith('elife_poa_e' + str(fid).zfill(5))):
                new_filename = journal
                new_filename = self.add_filename_fid(new_filename, fid)
                new_filename = self.add_filename_version(new_filename, version)
                new_filename += '.xml'
            
        if old_filename.endswith('.pdf'):
            # Confirm it is the article PDF file or figures PDF
            if (old_filename == 'elife' + str(fid).zfill(5) + '.pdf'
                or old_filename.startswith('decap_elife_poa_e' + str(fid).zfill(5))
                or old_filename == 'elife' + str(fid).zfill(5) + '-figures.pdf'):
                new_filename = journal
                new_filename = self.add_filename_fid(new_filename, fid)
                if 'figures' in old_filename:
                    new_filename += '-figures'
                new_filename = self.add_filename_version(new_filename, version)
                new_filename += '.pdf'
                
        if old_filename.endswith('_ds.zip'):
            # PoA digital supplement file
            # TODO - may want to unwrap the zip and rename its child zip
            new_filename = journal
            new_filename = self.add_filename_fid(new_filename, fid)
            new_filename += '-supp'
            new_filename = self.add_filename_version(new_filename, version)
            new_filename += '.zip'
    
        return new_filename
    
    def parent_levels_by_type(self, item):
        """
        Given an item dict representing a matched tag,
        depending on its type, it will have different parent levels
        """
        # Here we want to set the parentage differently for videos
        #  because those items are their own parents, in a way
        if 'type' in item and item['type'] == 'media' and 'mimetype' in item:
            first_parent_level = ''
            second_parent_level = 'parent_'
            third_parent_level = 'p_parent_'
        else:
            first_parent_level = 'parent_'
            second_parent_level = 'p_parent_'
            third_parent_level = 'p_p_parent_'
        
        return first_parent_level, second_parent_level, third_parent_level
    
    def new_filename_generic(self, soup, old_filename, journal, fid, status, version):
        """
        After filtering out known exceptions for file name renaming,
        this will try and get a new file name based on the old filename
        """
        new_filename = None
        
            
        
        # File extension
        extension = self.file_extension(old_filename)
        if extension is None:
            return None
        new_extension = '.' + extension.lower()
    
        (asset, type, ordinal, parent_type, parent_ordinal,
        p_parent_type, p_parent_ordinal) = self.asset_details(fid, old_filename, soup)
    
        # For now, only allow ones that have an ordinal,
        #  to be sure we matched the full start of the file name
        if not ordinal:
            if(self.logger):
                self.logger.info('found no ordinal for ' + old_filename)
            return None
        
        if not asset:
            if(self.logger):
                self.logger.info('found no asset for ' + old_filename)
        
        new_filename = journal
        new_filename = self.add_filename_fid(new_filename, fid)
        
        # Need to lookup the item again to get the parent levels
        item = self.scan_soup_for_xlink_href(old_filename, soup)
        (first_parent_level, second_parent_level, third_parent_level) = \
            self.parent_levels_by_type(item)
        
        if p_parent_type:
            # TODO - refactor to get the asset name
            p_parent_asset = self.asset_from_soup(old_filename, soup, third_parent_level)
            if not p_parent_asset:
                if(self.logger):
                    self.logger.info('found no p_parent_asset for ' + old_filename)
            else:
                new_filename = self.add_filename_asset(new_filename, p_parent_asset, p_parent_ordinal)
        
        if parent_type:
            # TODO - refactor to get the asset name
            parent_asset = self.asset_from_soup(old_filename, soup, second_parent_level)
            if not parent_asset:
                if(self.logger):
                    self.logger.info('found no parent_asset for ' + old_filename)
            else:
                new_filename = self.add_filename_asset(new_filename, parent_asset, parent_ordinal)

        if asset:
            new_filename = self.add_filename_asset(new_filename, asset, ordinal)
            new_filename = self.add_filename_version(new_filename, version)
    
    
            new_filename += new_extension
    
        return new_filename
    
    def asset_details(self, fid, old_filename, soup):
        
        asset = None
        type = None
        ordinal = None
        parent_type = None
        parent_ordinal = None
        p_parent_type = None
        p_parent_ordinal = None
        
        item = self.scan_soup_for_xlink_href(old_filename, soup)
        if item:
            type = item.get('type')
            
        # Here we want to set the parentage differently for videos
        #  because those items are their own parents, in a way
        (first_parent_level, second_parent_level, third_parent_level) = \
            self.parent_levels_by_type(item)
        
        asset = self.asset_from_soup(old_filename, soup, first_parent_level)
        
        # Get parent details
        details = self.parent_details_from_soup(old_filename, soup, first_parent_level)
        if details:
            type = details['type']
            if 'sibling_ordinal' in details:
                ordinal = details['sibling_ordinal']
        if not ordinal:
            # No parent, use the actual element ordinal
            details = self.details_from_soup(old_filename, soup)
            if details:
                ordinal = details['ordinal']
            
        details = self.parent_details_from_soup(old_filename, soup, second_parent_level)
        if details:
            parent_type = details['type']
            parent_ordinal = details['sibling_ordinal']
            
        details = self.parent_details_from_soup(old_filename, soup, third_parent_level)
        if details:
            p_parent_type = details['type']
            p_parent_ordinal = details['sibling_ordinal']
        
        return asset, type, ordinal, parent_type, parent_ordinal, p_parent_type, p_parent_ordinal
    
    def items_to_match(self, soup):
        graphics = parser.graphics(soup)
        media = parser.media(soup)
        self_uri = parser.self_uri(soup)
        inline_graphics = parser.inline_graphics(soup)
        return graphics + media + self_uri + inline_graphics
    
    def scan_soup_for_xlink_href(self, xlink_href, soup):
        """
        Look for the usual suspects that have an xlink_href of interest
        and try to match it
        """
    
        for item in self.items_to_match(soup):
            if 'xlink_href' in item:
                # Try and match the exact filename first
                if item['xlink_href'] == xlink_href:
                    return item
                elif item['xlink_href'] == xlink_href.split('.')[0]:
                    # Try and match without the file extension
                    return item
        return None
    
    def asset_from_soup(self, old_filename, soup, level):
        asset = None
        item = self.scan_soup_for_xlink_href(old_filename, soup)
        
        if item:
            if level + 'type' in item:
                # Check for a parent_type
                if item[level + 'type'] == 'fig':
                    if level + 'asset' in item and item[level + 'asset'] == 'figsupp':
                        asset = 'figsupp'
                    else:
                        asset = 'fig'
                elif level + 'asset' in item:
                    # If asset is set, use it
                    asset = item[level + 'asset']
                elif item[level + 'type'] == 'supplementary-material':
                    asset = 'supp'
                # TODO may want a different subarticle value
                elif item[level + 'type'] == 'sub-article':
                    asset = 'subarticle'
                elif 'mimetype' in item and item['mimetype'] == 'video':
                    asset = 'media'
            elif 'mimetype' in item and item['mimetype'] == 'video':
                asset = 'media'
            elif 'inf' in old_filename:
                asset = 'inf'
                
        return asset
        
    
    def details_from_soup(self, old_filename, soup):
        details = {}
    
        matched_item = self.scan_soup_for_xlink_href(old_filename, soup)
        if not matched_item:
            return None
    
        if 'ordinal' in matched_item:
            details['ordinal'] = matched_item['ordinal']
    
        return details
    
    def parent_details_from_soup(self, old_filename, soup, level):
        if level not in ['', 'parent_', 'p_parent_', 'p_p_parent_']:
            return None
        
        details = {}
        matched_item = self.scan_soup_for_xlink_href(old_filename, soup)
        if not matched_item:
            return None
        
        if level + 'type' in matched_item:
            details['type'] = matched_item[level + 'type']
        if level + 'sibling_ordinal' in matched_item:
            if level + 'asset' in matched_item and matched_item[level + 'asset'] == 'figsupp':
                # Subtract 1 from ordinal for figure supplements for now
                #  so the first figure is ignored from the count
                details['sibling_ordinal'] = matched_item[level + 'sibling_ordinal'] - 1
            else:
                details['sibling_ordinal'] = matched_item[level + 'sibling_ordinal']
    
        if len(details) > 0:
            return details
        else:
            return None
    
    
    def rename_files(self, journal, fid, status, version, xml_file):
        
        file_name_map = {}
        
        # Ignore these files we do not want them anymore
        ignore_files = ['elife05087s001.docx', 'elife05087s002.docx']
        
        dirfiles = self.file_list(self.TMP_DIR)
        
        soup = self.article_soup(xml_file)
        
        for df in dirfiles:
            filename = df.split(os.sep)[-1]
            
            if filename in ignore_files:
                continue
            
            # Get the new file name
            file_name_map[filename] = None
            renamed_filename = self.new_filename(soup, filename, journal, fid, status, version)
            
            if renamed_filename:
                file_name_map[filename] = renamed_filename
            else:
                if(self.logger):
                    self.logger.info('there is no renamed file for ' + filename)
        
        # Covert the XML
        self.convert_xml(xml_file, file_name_map)
        
        for old_name,new_name in file_name_map.iteritems():
            if new_name is not None:
                shutil.move(self.TMP_DIR + os.sep + old_name, self.OUTPUT_DIR + os.sep + new_name)
        
        return file_name_map
    
    def verify_rename_files(self, file_name_map):
        """
        Each file name as key should have a non None value as its value
        otherwise the file did not get renamed to something new and the
        rename file process was not complete
        """
        verified = True
        renamed_list = []
        not_renamed_list = []
        for k,v in file_name_map.items():
            if v is None:
                verified = False
                not_renamed_list.append(k)
            else:
                renamed_list.append(k)
                
        return (verified, renamed_list, not_renamed_list)
    
    def convert_xml(self, xml_file, file_name_map):
        # TODO
        
        # Register namespaces
        xmlio.register_xmlns()
        
        root = xmlio.parse(xml_file)
        
        # Convert xlink href values
        total = xmlio.convert_xlink_href(root, file_name_map)
        # TODO - compare whether all file names were converted
        
        # TODO For PoA, add the published date to the XML
        
    
        # Start the file output
        reparsed_string = xmlio.output(root)
        
        f = open(xml_file, 'wb')
        f.write(reparsed_string)
        f.close()
    
    
    def new_zip_filename(self, journal, fid, status, version = None):
        filename = journal
        filename = self.add_filename_fid(filename, fid)
        filename = self.add_filename_status(filename, status)
        filename = self.add_filename_version(filename, version)
        filename += '.zip'
        return filename
    
    def create_new_zip(self, zip_file_name):
    
        new_zipfile = zipfile.ZipFile(self.ZIP_DIR + os.sep + zip_file_name, 'w', zipfile.ZIP_DEFLATED)
            
        dirfiles = self.file_list(self.OUTPUT_DIR)
        
        for df in dirfiles:
            filename = df.split(os.sep)[-1]
            new_zipfile.write(df, filename)
            
        new_zipfile.close()
    
    def clean_directories(self, full = False):
        """
        Deletes all the files from the activity directories
        in order to save on disk space immediately
        A full clean is only after all activities have finished,
        a non-full clean can be done after each article
        """
        for file in self.file_list(self.TMP_DIR):
            os.remove(file)
        for file in self.file_list(self.OUTPUT_DIR):
            os.remove(file)
        for file in self.file_list(self.JUNK_DIR):
            os.remove(file)

        if full is True:
            for file in self.file_list(self.ZIP_DIR):
                os.remove(file)
            for folder in self.folder_list(self.INPUT_DIR):
                for file in self.file_list(folder):
                    os.remove(file)

    
    def profile_article(self, input_dir, folder):
        """
        Temporary, profile the article by folder names in test data set
        In real code we still want this to return the same values
        """
        # Temporary setting of version values from directory names
        
        soup = self.article_soup(self.article_xml_file())
        
        # elife id / doi id / manuscript id
        fid = parser.doi(soup).split('.')[-1]
    
        # article status
        if parser.is_poa(soup) is True:
            status = 'poa'
        else:
            status = 'vor'
        
        # version
        version = self.version_number(input_dir, folder)
    
            
        return (fid, status, version)
    
    def version_number(self, input_dir, folder):
        
        # Version is hacky at the moment for test data only
        version = None
        if '_' in self.folder_name_from_name(input_dir, folder):
            if self.folder_name_from_name(input_dir, folder).split('_')[-1] == 'v1':
                version = 1
            elif self.folder_name_from_name(input_dir, folder).split('_')[-1] == 'v2':
                version = 2
            else:
                version = 1
        else:
            if self.folder_name_from_name(input_dir, folder) == '06250':
                version = 3
            elif self.folder_name_from_name(input_dir, folder) == '04525':
                version = 2
            else:
                version = 1
                
        return version
    
    def article_xml_file(self):
        for file_name in self.file_list(self.TMP_DIR):
            if file_name.endswith('.xml'):
                return file_name
    
    def article_soup(self, xml_filename):
        return parser.parse_document(xml_filename)






    def create_activity_directories(self):
        """
        Create the directories in the activity tmp_dir
        """
        try:
            os.mkdir(self.TMP_DIR)
            os.mkdir(self.INPUT_DIR)
            os.mkdir(self.JUNK_DIR)
            os.mkdir(self.ZIP_DIR)
            os.mkdir(self.OUTPUT_DIR)
            
        except:
            pass