from lettuce import step, world
import boto
import os
import re
import settings

world.settings = settings.test
world.aws_id = world.settings.aws_access_key_id
world.aws_secret = world.settings.aws_secret_access_key
world.reference_bucket_name = world.settings.publishing_buckets_prefix + \
                              world.settings.reference_eif_bucket
world.eif_bucket_name = world.settings.publishing_buckets_prefix + \
                              world.settings.eif_bucket
world.zip_drop_bucket_name = world.settings.publishing_buckets_prefix + \
                              world.settings.production_bucket


@step("the reference EIF file (?P<filename>.+) is available")
def check_file_available(step, filename):
    """
    :type step lettuce.core.Step
    """
    connection = boto.connect_s3(world.aws_id, world.aws_secret)
    try:
        reference_bucket = connection.get_bucket(world.reference_bucket_name)
    except:
        raise
    finally:
        connection.close()
    assert filename in [key.name for key in reference_bucket.list()], \
        "{0} not found in bucket {1}".format(filename, reference_bucket.name)


@step("the EIF destination location is available")
def check_destination_available(step):
    """
    :type step lettuce.core.Step
    """
    get_bucket(world.eif_bucket_name)


@step("I empty the EIF destination location before I start")
def empty_destination(step):
    """
    :type step lettuce.core.Step
    """
    try:
        eif_bucket = get_bucket(world.eif_bucket_name)
        eif_bucket.delete_keys([key.name for key in eif_bucket.list()])
    except:
        raise
    assert len([key.name for key in eif_bucket.list()]) == 0, \
        "Objects remain after trying to delete all from bucket {0}".format(eif_bucket.name)


@step("I expect to see a file in the EIF destination with the filename (?P<expected_filename>.+)")
def check_destination_filename(step, expected_filename):
    """
    :type step lettuce.core.Step
    :type expected_filename str
    """
    match = re.match("elife-([0-9]+)-v([0-9]+)\.json", expected_filename)
    (art_id, art_version) = (match.group(1), match.group(2))
    eif_bucket = get_bucket(world.eif_bucket_name)
    keys = eif_bucket.get_all_keys()
    for key in keys:
        if contains_expected_filename(art_id, art_version, expected_filename, key):
            return True
    raise AssertionError("Can't find expected file at {0}.{1}/[any uuid is "
                         "valid here]/{2} in bucket {3}"
                         .format(art_id, art_version, expected_filename, eif_bucket.name))


@step("I trigger the generation of the EIF file from the source file (?P<filename>.+)")
def drop_file_into_bucket(step, filename):
    """
    :type step lettuce.core.Step
    :type filename str
    """
    bucket = get_bucket(world.zip_drop_bucket_name)
    # TODO: can this path be derived in a better way?
    path = "elife-bot/tests/test_data/"
    full_path = os.path.abspath(os.path.join(path, filename))
    key = bucket.new_key(filename)
    key.set_contents_from_filename(full_path)


def get_bucket(name):
    connection = boto.connect_s3(world.aws_id, world.aws_secret)
    try:
        return connection.get_bucket(name)
    except:
        raise
    finally:
        connection.close()


def contains_expected_filename(elife_id, version, expected_filename, key):
    """ Format of expected key name is:
        id.version/uuid for run/filename
        (the UUID may be anything).
    """
    return re.match(elife_id + "\." + version + "/[^/]+/" + expected_filename + "$", key.name)
