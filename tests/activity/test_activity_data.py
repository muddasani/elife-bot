import json
import classes_mock
import base64

json_output_parameter_example_string = open("tests/test_data/ConvertJATS_json_output_for_add_update_date_to_json.json", "r").read()
json_output_parameter_example = json.loads(open("tests/test_data/ConvertJATS_json_output_for_add_update_date_to_json.json", "r").read())
json_output_return_example = json.loads(open("tests/test_data/ConvertJATS_add_update_date_to_json_return.json", "r").read())
json_output_return_example_string = open("tests/test_data/ConvertJATS_add_update_date_to_json_return.json", "r").read()

xml_content_for_xml_key = open("tests/test_data/ConvertJATS_content_for_test_origin.xml", "r").read()

bucket_origin_file_name = "test_origin.xml"
bucket_dest_file_name = "test_dest.json"

session_example = {
            'version': '1',
            'article_id': '00353',
            'run': '1ee54f9a-cb28-4c8e-8232-4b317cf4beda',
            'expanded_folder': '00353.1/1ee54f9a-cb28-4c8e-8232-4b317cf4beda',
            'update_date': '2012-12-13T00:00:00Z',
            'file_name': 'elife-00353-vor-v1.zip',
            'filename_last_element': 'elife-00353-vor-r1.zip',
            'eif_location': '00353.1/cf9c7e86-7355-4bb4-b48e-0bc284221251/elife-00353-v1.json'
        }
data_example_before_publish = {
            "status": "vor",
            "update_date": "2012-12-13T00:00:00Z",
            "run": "cf9c7e86-7355-4bb4-b48e-0bc284221251",
            "expanded_folder": "00353.1/cf9c7e86-7355-4bb4-b48e-0bc284221251",
            "version": "1",
            "eif_location": "",
            "article_id": "00353",
            'file_name': 'elife-00353-vor-v1.zip',
            'filename_last_element': 'elife-00353-vor-r1.zip'}

key_names = [u'00353.1/1ee54f9a-cb28-4c8e-8232-4b317cf4beda/elife-00353-fig1-v1.tif', u'00353.1/1ee54f9a-cb28-4c8e-8232-4b317cf4beda/elife-00353-v1.pdf',
             u'00353.1/1ee54f9a-cb28-4c8e-8232-4b317cf4beda/elife-00353-v1.xml']

bucket = {
    bucket_origin_file_name: xml_content_for_xml_key,
    bucket_dest_file_name: ""
}

run_example = '1ee54f9a-cb28-4c8e-8232-4b317cf4beda'


def PreparePost_session_example(update_date):
        return {
            'version': '1',
            'article_id': '00353',
            'run': '1ee54f9a-cb28-4c8e-8232-4b317cf4beda',
            'expanded_folder': '00353.1/1ee54f9a-cb28-4c8e-8232-4b317cf4beda',
            'update_date': update_date,
            'article_version_id': '00353.1',
            'status': 'vor',
            'eif_location': '00353.1/1ee54f9a-cb28-4c8e-8232-4b317cf4beda/elife-00353-v1.json',
            'article_path': 'content/1/e00353v1'
        }
PreparePostEIF_test_dir = "fake_sqs_queue_container"
PreparePostEIF_message = {'eif_location': '00353.1/1ee54f9a-cb28-4c8e-8232-4b317cf4beda/elife-00353-v1.json', 'passthrough': {'status': 'vor', 'update_date': '2012-12-13T00:00:00Z', 'run': '1ee54f9a-cb28-4c8e-8232-4b317cf4beda', 'expanded_folder': '00353.1/1ee54f9a-cb28-4c8e-8232-4b317cf4beda', 'version': '1', 'article_path': 'content/1/e00353v1', 'article_id': '00353'}, 'eif_bucket': 'dest_bucket'}
PreparePostEIF_json_output_return_example = json.loads(open("tests/test_data/PreparePostEIF_json_return.json", "r").read())
PreparePostEIF_message_no_update_date = {'eif_location': '00353.1/1ee54f9a-cb28-4c8e-8232-4b317cf4beda/elife-00353-v1.json', 'passthrough': {'status': 'vor', 'update_date': None, 'run': '1ee54f9a-cb28-4c8e-8232-4b317cf4beda', 'expanded_folder': '00353.1/1ee54f9a-cb28-4c8e-8232-4b317cf4beda', 'version': '1', 'article_path': 'content/1/e00353v1', 'article_id': '00353'}, 'eif_bucket': 'dest_bucket'}
PreparePostEIF_json_output_return_example_no_update_date = json.loads(open("tests/test_data/PreparePostEIF_json_return_no_update_date.json", "r").read())
PreparePostEIF_data = {u'event_time': u'2016-06-07T10:45:18.141126Z', u'event_name': u'ObjectCreated:Put', u'file_name': u'elife-00353-vor-v1-20121213000000.zip', u'file_etag': u'1e17ebb1fad6c467fce9cede16bb752f', u'bucket_name': u'jen-elife-production-final', u'file_size': 1097506, u"run": u"1ee54f9a-cb28-4c8e-8232-4b317cf4beda", u"update_date": u"2012-12-13T00:00:00Z"}

def PostEIFBridge_data(published, update_date):
        return {
                'eif_location': '00353.1/cf9c7e86-7355-4bb4-b48e-0bc284221251/elife-00353-v1.json',
                'eif_bucket':  'jen-elife-publishing-eif',
                'article_id': u'00353',
                'version': u'1',
                'run': u'cf9c7e86-7355-4bb4-b48e-0bc284221251',
                'article_path': 'content/1/e00353v1',
                'published': published,
                'expanded_folder': u'00353.1/cf9c7e86-7355-4bb4-b48e-0bc284221251',
                'status': u'vor',
                'update_date': update_date
            }
PostEIFBridge_test_dir = "fake_sqs_queue_container"
PostEIFBridge_message = {'workflow_name': 'PostPerfectPublication', 'workflow_data': {'status': u'vor', 'update_date': u'2012-12-13T00:00:00Z', 'run': u'cf9c7e86-7355-4bb4-b48e-0bc284221251', 'expanded_folder': u'00353.1/cf9c7e86-7355-4bb4-b48e-0bc284221251', 'version': u'1', 'eif_location': '00353.1/cf9c7e86-7355-4bb4-b48e-0bc284221251/elife-00353-v1.json', 'article_id': u'00353'}}
PostEIFBridge_message_no_update_date = {'workflow_name': 'PostPerfectPublication', 'workflow_data': {'status': u'vor', 'update_date': None, 'run': u'cf9c7e86-7355-4bb4-b48e-0bc284221251', 'expanded_folder': u'00353.1/cf9c7e86-7355-4bb4-b48e-0bc284221251', 'version': u'1', 'eif_location': '00353.1/cf9c7e86-7355-4bb4-b48e-0bc284221251/elife-00353-v1.json', 'article_id': u'00353'}}

def ApprovePublication_publication_data(update_date):
            return {
                "workflow_name": "PostPerfectPublication",
                "workflow_data": {
                            "status": "vor",
                            "update_date": update_date,
                            "run": "cf9c7e86-7355-4bb4-b48e-0bc284221251",
                            "expanded_folder": "00353.1/cf9c7e86-7355-4bb4-b48e-0bc284221251",
                            "version": "1",
                            "eif_location": "00353.1/cf9c7e86-7355-4bb4-b48e-0bc284221251/elife-00353-v1.json",
                            "article_id": "00353"}
                }

def ApprovePublication_data(update_date):
        return {
            "article_id": "00353",
            "version": "1",
            "run": "cf9c7e86-7355-4bb4-b48e-0bc284221251",
            "publication_data": base64.encodestring(json.dumps(ApprovePublication_publication_data(update_date)))
            }
ApprovePublication_test_dir = "fake_sqs_queue_container"
def ApprovePublication_json_output_return_example(update_date):
            return ApprovePublication_publication_data(update_date)

# ExpandArticle

ExpandArticle_data = {u'event_time': u'2016-06-07T10:45:18.141126Z', u'event_name': u'ObjectCreated:Put', u'file_name': u'elife-00353-vor-v1-20121213000000.zip', u'file_etag': u'1e17ebb1fad6c467fce9cede16bb752f', u'bucket_name': u'jen-elife-production-final', u'file_size': 1097506, u"run": u"1ee54f9a-cb28-4c8e-8232-4b317cf4beda"}
ExpandArticle_data1 = {u'event_time': u'2016-06-07T10:45:18.141126Z', u'event_name': u'ObjectCreated:Put', u'file_name': u'elife-00353-v1-20121213000000.zip', u'file_etag': u'1e17ebb1fad6c467fce9cede16bb752f', u'bucket_name': u'jen-elife-production-final', u'file_size': 1097506, u"run": u"1ee54f9a-cb28-4c8e-8232-4b317cf4beda"}
ExpandArticle_filename = 'elife-00353-vor-v1-20121213000000.zip'
ExpandArticle_path = 'elife-00353-vor-v1'
ExpandArticle_files_source_folder = 'tests/files_source'
ExpandArticle_files_dest_folder = 'tests/files_dest'
ExpandArticle_files_dest_expected = ['elife-00353-fig1-v1.tif', 'elife-00353-v1.pdf', 'elife-00353-v1.xml']
ExpandArticle_files_dest_bytes_expected = [{'name': 'elife-00353-fig1-v1.tif', 'bytes': 961324}, {'name': 'elife-00353-v1.pdf', 'bytes': 936318}, {'name': 'elife-00353-v1.xml', 'bytes': 9458}]

ExpandArticle_data_invalid_article = {u'event_time': u'2016-06-07T10:45:18.141126Z', u'event_name': u'ObjectCreated:Put', u'file_name': u'aaa.zip', u'file_etag': u'1e17ebb1fad6c467fce9cede16bb752f', u'bucket_name': u'jen-elife-production-final', u'file_size': 1097506, u"run": u"1ee54f9a-cb28-4c8e-8232-4b317cf4beda"}

ExpandArticle_data_invalid_status = {u'event_time': u'2016-06-07T10:45:18.141126Z', u'event_name': u'ObjectCreated:Put', u'file_name': u'elife-00353-v1-20121213000000.zip', u'file_etag': u'1e17ebb1fad6c467fce9cede16bb752f', u'bucket_name': u'jen-elife-production-final', u'file_size': 1097506, u"run": u"1ee54f9a-cb28-4c8e-8232-4b317cf4beda"}

ExpandArticle_data_invalid_status1_session_example = {
            'version': '1',
            'article_id': '00353',
            'run': '1ee54f9a-cb28-4c8e-8232-4b317cf4beda',
            'expanded_folder': '00353.1/1ee54f9a-cb28-4c8e-8232-4b317cf4beda',
            'update_date': '2012-12-13T00:00:00Z',
            'file_name': 'elife-00353-vor-v1.zip',
            'filename_last_element': 'elife-00353-vor-v-1-20121213000000.zip'
        }
ExpandArticle_data_invalid_status2_session_example = {
            'version': '1',
            'article_id': '00353',
            'run': '1ee54f9a-cb28-4c8e-8232-4b317cf4beda',
            'expanded_folder': '00353.1/1ee54f9a-cb28-4c8e-8232-4b317cf4beda',
            'update_date': '2012-12-13T00:00:00Z',
            'file_name': 'elife-00353-vor-v1.zip',
            'filename_last_element': 'elife-00353-v1-20121213000000.zip'
        }

lax_article_versions_response_data = {u'1':
                                          {u'rev4_decision': None, u'date_initial_decision': u'2015-05-06',
                                           u'datetime_record_updated': u'2016-05-24T16:45:13.815502Z',
                                           u'date_initial_qc': u'2015-04-29', u'date_rev3_qc': None,
                                           u'title': u'Multiple abiotic stimuli are integrated in the regulation of rice gene expression under field conditions',
                                           u'decision': u'RVF',
                                           u'version': 1, u'date_rev4_decision': None,
                                           u'rev3_decision': None,
                                           u'datetime_record_created': u'2016-02-24T15:11:51.831000Z',
                                           u'type': u'research-article', u'status': u'poa', u'date_full_qc': u'2015-05-13',
                                           u'date_rev3_decision': None, u'date_rev1_qc': u'2015-09-17', u'date_rev1_decision': u'2015-10-13',
                                           u'datetime_submitted': None, u'ejp_type': u'RA', u'volume': 4, u'manuscript_id': 8411, u'doi': u'10.7554/eLife.08411',
                                           u'initial_decision': u'EF', u'rev1_decision': u'RVF', u'rev2_decision': u'AF',
                                           u'date_rev2_qc': u'2015-11-11', u'date_rev2_decision': u'2015-11-25', u'date_rev4_qc': None,
                                           u'date_full_decision': u'2015-06-15', u'website_path': u'content/4/e08411v1',
                                           u'datetime_published': u'2015-11-26T00:00:00Z'},
                                      u'2':
                                          {u'rev4_decision': None, u'date_initial_decision': u'2015-05-06',
                                           u'datetime_record_updated': u'2016-05-24T16:45:13.815502Z', u'date_initial_qc': u'2015-04-29',
                                           u'date_rev3_qc': None,
                                           u'title': u'Multiple abiotic stimuli are integrated in the regulation of rice gene expression under field conditions',
                                           u'decision': u'RVF', u'version': 2, u'date_rev4_decision': None, u'rev3_decision': None,
                                           u'datetime_record_created': u'2016-02-24T15:11:51.831000Z',
                                           u'type': u'research-article', u'status': u'vor', u'date_full_qc': u'2015-05-13', u'date_rev3_decision': None,
                                           u'date_rev1_qc': u'2015-09-17', u'date_rev1_decision': u'2015-10-13', u'datetime_submitted': None,
                                           u'ejp_type': u'RA', u'volume': 4, u'manuscript_id': 8411, u'doi': u'10.7554/eLife.08411',
                                           u'initial_decision': u'EF', u'rev1_decision': u'RVF', u'rev2_decision': u'AF',
                                           u'date_rev2_qc': u'2015-11-11', u'date_rev2_decision': u'2015-11-25', u'date_rev4_qc': None,
                                           u'date_full_decision': u'2015-06-15', u'website_path': u'content/4/e08411v1', u'datetime_published': u'2015-12-31T00:00:00Z'}
                                      }


#ResizeImages

ResizeImages_data = {u'event_time': u'2016-06-14T12:32:38.084176Z', u'event_name': u'ObjectCreated:Put', u'file_name': u'elife-00353-vor-v1-20121213000000.zip', u'file_etag': u'1e17ebb1fad6c467fce9cede16bb752f', u'bucket_name': u'jen-elife-production-final', u'file_size': 1097506, u"run": u"1ee54f9a-cb28-4c8e-8232-4b317cf4beda"}

#ApplyVersionNumber

ApplyVersionNumber_data_with_renaming = {u'event_time': u'2016-07-25T15:42:26.853733Z', u'event_name': u'ObjectCreated:Put', u'file_name': u'elife-15224-vor-r2.zip', u'file_etag': u'e7f639f63171c097d4761e2d2efe8dc4', u'bucket_name': u'jen-elife-production-final', u'file_size': 27992113, u"run": u"1ee54f9a-cb28-4c8e-8232-4b317cf4beda", u"run": u"1ee54f9a-cb28-4c8e-8232-4b317cf4beda"}
ApplyVersionNumber_data_no_renaming = {u'event_time': u'2016-07-25T16:33:59.329727Z', u'event_name': u'ObjectCreated:Put', u'file_name': u'elife-00353-vor-v1-20121213000000.zip', u'file_etag': u'1e17ebb1fad6c467fce9cede16bb752f', u'bucket_name': u'jen-elife-production-final', u'file_size': 1097506, u"run": u"1ee54f9a-cb28-4c8e-8232-4b317cf4beda", u"run": u"1ee54f9a-cb28-4c8e-8232-4b317cf4beda"}


#RewriteEIF

RewriteEIF_data = {
            "status": "vor",
            "update_date": "2012-12-13T00:00:00Z",
            "run": "cf9c7e86-7355-4bb4-b48e-0bc284221251",
            "expanded_folder": "00353.1/cf9c7e86-7355-4bb4-b48e-0bc284221251",
            "version": "1",
            "eif_location": "00353.1/cf9c7e86-7355-4bb4-b48e-0bc284221251/elife-00353-v1.json",
            "article_id": "00353"}
RewriteEIF_json_input_string = json.dumps({})
RewriteEIF_json_output = {"update": "2012-12-13T00:00:00Z"}

#SetPublicationStatus

SetPublicationStatus_data_activity = {u'event_time': u'2016-07-28T16:14:27.809576Z', u'event_name': u'ObjectCreated:Put', u'file_name': u'elife-15224-vor-r2.zip', u'file_etag': u'e7f639f63171c097d4761e2d2efe8dc4', u'bucket_name': u'jen-elife-production-final', u'file_size': 27992113}

# ConvertJATS

ConvertJATS_data = { "run": "1ee54f9a-cb28-4c8e-8232-4b317cf4beda"}

# data at start of IngestArticlaZipWorkflow

raw_data_activity = {u'run': u'1ee54f9a-cb28-4c8e-8232-4b317cf4beda', u'event_time': u'2016-07-28T16:14:27.809576Z', u'event_name': u'ObjectCreated:Put', u'file_name': u'elife-00353-vor-r1.zip', u'file_etag': u'e7f639f63171c097d4761e2d2efe8dc4', u'bucket_name': u'jen-elife-production-final', u'file_size': 1097506}

glencoe_metadata = \
    {"media2": {
        "source_href": "http://static-movie-usa.glencoesoftware.com/source/10.7554/114/1245b554bd5cbda4fa4beeba806e659f0624128e/elife-12620-media2.mov", "doi": "10.7554/eLife.12620.008",
        "flv_href": "http://static-movie-usa.glencoesoftware.com/flv/10.7554/114/1245b554bd5cbda4fa4beeba806e659f0624128e/elife-12620-media2.flv",
        "uuid": "674a799d-20f8-40c2-99b2-b9bd18fe6b7b",
        "title": "",
        "video_id": "media2",
        "solo_href": "http://movie-usa.glencoesoftware.com/video/10.7554/eLife.12620/media2",
        "height": 512,
        "ogv_href": "http://static-movie-usa.glencoesoftware.com/ogv/10.7554/114/1245b554bd5cbda4fa4beeba806e659f0624128e/elife-12620-media2.ogv",
        "width": 512,
        "href": "elife-12620-media2.mov",
        "webm_href": "http://static-movie-usa.glencoesoftware.com/webm/10.7554/114/1245b554bd5cbda4fa4beeba806e659f0624128e/elife-12620-media2.webm",
        "jpg_href": "http://static-movie-usa.glencoesoftware.com/jpg/10.7554/114/1245b554bd5cbda4fa4beeba806e659f0624128e/elife-12620-media2.jpg",
        "duration": 43.159999999999997,
        "mp4_href": "http://static-movie-usa.glencoesoftware.com/mp4/10.7554/114/1245b554bd5cbda4fa4beeba806e659f0624128e/elife-12620-media2.mp4",
        "legend": "<div class=\"caption\"><h3 class=\"title\">Effects of a highly-focused laser spot on directional motility in <i>Synechocystis.<\/i><\/h3><p>Cells are imaged by fluorescence from the photosynthetic pigments, and are moving towards an oblique LED light at the bottom of the frame: note the focused light spot at the rear edge of each cell. The superimposed red spot indicates the position of the laser, and time in min is shown at the top left.&#160;LED, light emitting diode.<\/p><p><b>DOI:<\/b> <a href=\"10.7554/eLife.12620.008\">http://dx.doi.org/10.7554/eLife.12620.008<\/a><\/p><\/div>", "size": 2578518},
     "media1": {
         "source_href": "http://static-movie-usa.glencoesoftware.com/source/10.7554/114/1245b554bd5cbda4fa4beeba806e659f0624128e/elife-12620-media1.mp4",
         "doi": "10.7554/eLife.12620.004",
         "flv_href": "http://static-movie-usa.glencoesoftware.com/flv/10.7554/114/1245b554bd5cbda4fa4beeba806e659f0624128e/elife-12620-media1.flv",
         "uuid": "e1f617d7-a3d7-45ec-8fcc-6b66f8f26505",
         "title": "",
         "video_id": "media1",
         "solo_href": "http://movie-usa.glencoesoftware.com/video/10.7554/eLife.12620/media1",
         "height": 720,
         "ogv_href": "http://static-movie-usa.glencoesoftware.com/ogv/10.7554/114/1245b554bd5cbda4fa4beeba806e659f0624128e/elife-12620-media1.ogv",
         "width": 1280, "href": "elife-12620-media1.mp4",
         "webm_href": "http://static-movie-usa.glencoesoftware.com/webm/10.7554/114/1245b554bd5cbda4fa4beeba806e659f0624128e/elife-12620-media1.webm",
         "jpg_href": "http://static-movie-usa.glencoesoftware.com/jpg/10.7554/114/1245b554bd5cbda4fa4beeba806e659f0624128e/elife-12620-media1.jpg",
         "duration": 89.400000000000006, "mp4_href": "http://static-movie-usa.glencoesoftware.com/mp4/10.7554/114/1245b554bd5cbda4fa4beeba806e659f0624128e/elife-12620-media1.mp4",
         "legend": "<div class=\"caption\"><h3 class=\"title\">Motility of <i>Synechocystis<\/i> cells under different illumination regimes.<\/h3><p>The video gives a schematic overview of the experimental set-up, followed by movement of cells in a projected light gradient, and with oblique illumination from two orthogonal directions, and then from both directions simultaneously. In each case, the raw video data is followed by the same movie clip with the tracks of cells superimposed. Time in minutes is indicated.<\/p><p><b>DOI:<\/b> <a href=\"10.7554/eLife.12620.004\">http://dx.doi.org/10.7554/eLife.12620.004<\/a><\/p><\/div>",
         "size": 21300934}}