import os, shutil

from nose.tools import *

import urlopenmock #stub urlopen calls
from core.core import TvRenamr

class TestCore(object):
    working = 'tests/data/working'
    
    def setUp(self):
        files = 'tests/data/files'
        self.tv = TvRenamr(self.working, log_level='debug')
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(self.working, fn))
    
    def tearDown(self):
        for fn in os.listdir(self.working): os.remove(os.path.join(self.working,fn))
    
    def test_passing_in_a_series_name_renames_a_file_using_that_name(self):
        fn = 'avatar.s1e08.blah.HDTV.XViD.avi'
        credentials = self.tv.extract_episode_details_from_file(fn, user_regex='%n.s%s{1}e%e{2}.blah')
        title = self.tv.retrieve_episode_name(series='Avatar: The Last Airbender', season=credentials['season'], episode=credentials['episode'])
        credentials['series'] = title['series']
        credentials['title'] = title['title']
        path = self.tv.build_path(series=credentials['series'], season=credentials['season'], episode=credentials['episode'], title=credentials['title'], extension=credentials['extension'])
        self.tv.rename(fn, path)
        assert_true(os.path.isfile(os.path.join(self.working, 'Avatar: The Last Airbender - 108 - Winter Solstice (2): Avatar Roku.avi')))
    