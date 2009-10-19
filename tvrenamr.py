import os
from optparse import OptionParser

from core.core import TvRenamr

parser = OptionParser()
parser.add_option('-a', '--auto', dest='auto_move', help='Automatically move renamed files to the appropriate directory under the directory specified. Mutually exclusive to -r')
parser.add_option('-e', '--episode', dest='episode', help='Set the episode number. Currently this will cause errors when working with more than one file')
parser.add_option('-n', '--name', dest='name', help='Set the show name for renaming')
parser.add_option('-o', '--output', dest='output_format', help='Set the output format for the episodes being renamed')
parser.add_option('-r', "--renamed", dest='renamed_dir', help='The directory to move renamed files to. Mutually exclusive to -a')
parser.add_option('--regex', dest='regex', help='The regular expression to set the format of files being renamed. Use %n to specify the show name, %s for the season number and %e for the episode number. All spaces are converted to periods before the regex is run')
parser.add_option('-s', '--season', dest='season', help='Set the season number.')
parser.add_option('-t', '--the', action='store_true', dest='the', help='Set the position of \'The\' in a show\'s name to the end of the file')
parser.add_option('-w', '--working', dest='working_dir', help='The working directory to run tvrenamr in. Required!')
(options, args) = parser.parse_args()

# options.working_dir = '/Volumes/Media/TV/Scrubs/Season\ 4/Scrubs\ \[S4E16\]\ My\ Quarantine.avi'
#options.name = ''
# options.regex = '%s.[S%sE%e'

def script_rename(working_dir, fn):
    tv = TvRenamr(working_dir, 'debug')
    try:
        credentials = tv.extract_episode_details_from_file(fn, user_regex=options.regex)
        if options.name: credentials['series']=options.name
        if options.season: credentials['season']=options.season
        if options.episode: credentials['episode']=options.episode
        title = tv.retrieve_episode_name(credentials['series'],credentials['season'],credentials['episode'])
        if options.the: credentials['series'] = tv.set_position_of_leading_the_to_end_of_show_name(title['series'])
        else: credentials['series'] = title['series']
        credentials['title'] = title['title']
        path = tv.build_path(series=credentials['series'], season=credentials['season'], episode=credentials['episode'], title=credentials['title'], extension=credentials['extension'], renamed_dir=options.renamed_dir, auto_move=options.auto_move, format=None)
        tv.rename(fn,path)
    except Exception, e: print e

if os.path.isdir(options.working_dir):
    for each_tuple in os.walk(options.working_dir):
        for fname in each_tuple[2]:
            script_rename(each_tuple[0], fname)
elif os.path.isfile(options.working_dir):
    working = os.path.split(options.working_dir)
    script_rename(working[0], working[1])