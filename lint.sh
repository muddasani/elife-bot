#!/bin/bash
set -e
source venv/bin/activate

# intentionally only the script files in the root folder
pylint -E *.py provider/storage_provider.py provider/lax_provider.py activity/activity_Update*.py activity/activity_Pubmed*.py tests/activity/test_activity_update_repository.py
