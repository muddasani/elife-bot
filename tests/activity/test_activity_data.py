import json

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
        }

bucket = {
    bucket_origin_file_name: xml_content_for_xml_key,
    bucket_dest_file_name: ""
}

run_example = '1ee54f9a-cb28-4c8e-8232-4b317cf4beda'



# import activity
# import settings as s_lib
# import random
# import log
# import boto
#
# s = s_lib.get_settings("exp")
# identity = "worker_%s" % int(random.random() * 1000)
# logFile = "worker.log"
# logger = log.logger(logFile, s.setLevel, identity)
# conn = None #boto.swf.layer1.Layer1(s.aws_access_key_id, s.aws_secret_access_key)
#
# cj = activity.activity_ConvertJATS(s, logger, conn, None, None)
#
# x = cj.do_activity("{\"json\": \"hello\"}")
#
# print x



#import activity

#fake_activity = activity.activity()