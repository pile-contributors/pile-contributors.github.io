#!/usr/bin/env python
'''
Script that constructs the documentation for piles.

Usage:

.. code-block:: none

    docpiles.py path/to/piles

'''
__authors__ = 'Nicu Tofan'
__copyright__ = 'Copyright 2015, Piles Contributors'
__credits__ = []
__license__ = '3-clause BSD'
__maintainer__ = 'Nicu Tofan'
__email__ = 'nicu.tofan@gmail.com'

import argparse
from copy import deepcopy
import logging
import os
from shutil import move as move_file
import subprocess
from subprocess import check_output

from constants import *
from logsetup import setup_logging
from dynfiles import file_with_dyn_area

LOGGER = None

class DocumRun(object):
    '''
    Class that manages the creation of piles documentation.

    Parameters
    ----------
    path : the top level path that contains all the piles
    doxygen : (path and) name of the doxygen executable
    '''
    def __init__(self, path, doxygen, doxyfile, outpath, sitepath, pull):
        '''
        Constructor.
        '''
        self.pilespath = path
        self.doxygen = doxygen
        self.doxyfile = doxyfile
        self.outpath = outpath
        # if not defined (None) no post processing step takes place
        self.sitepath = sitepath
        self.pull = pull

        # data for a pile while iterating
        self.pile_vars = {
            'res_path': os.getcwd()}
        # The tree of data for all detected piles
        self.tree = {}
        # dictionary of category name and list of piles that belong here
        self.categories = {}
        # dictionary of tag name and list of piles that belong to that tag
        self.tags = {}

        super(DocumRun, self).__init__()

    def _pile_cmake_data(self, mtch, stat):
        '''
        Gets the information from a cmake file line.

        This is a utility function for setup_dict_for_pile().
        '''
        if stat == CMAKE_STAT_PROP_VERSION:
            vlist = mtch.group(1).split(';')
            self.pile_vars['pile_version'] = '%s.%s.%s' % (
                vlist[0], vlist[1], vlist[2])
            self.pile_vars['pile_version_list'] = vlist
            self.pile_vars['pile_version_major'] = vlist[0]
            self.pile_vars['pile_version_minor'] = vlist[1]
            self.pile_vars['pile_version_patch'] = vlist[2]
            self.pile_vars['pile_version_debug'] = \
                'debug' if vlist[3] == 'd' else 'release'
        elif stat == CMAKE_STAT_PROP_CONFIG:
            self.pile_vars['pile_config'] = mtch.group(1)
        elif stat == CMAKE_STAT_PROP_MODE:
            # self.pile_vars['pile_mode'] = mtch.group(1)
            pass
        elif stat == CMAKE_STAT_PROP_DEPS:
            self.pile_vars['pile_deps'] = mtch.group(1).split(';')
        elif stat == CMAKE_STAT_PROP_CATEGS:
            self.pile_vars['pile_categ'] = mtch.group(1)
        elif stat == CMAKE_STAT_PROP_TAGS:
            self.pile_vars['pile_tags'] = mtch.group(1).split(';')

    def _pile_readme_data(self, pile_full_dir):
        '''
        Gets the information from a Readme file.

        This is a utility function for setup_dict_for_pile().
        '''
        # read the readme file and extract information from it
        # The file is expected to start with a title marked using
        # a ===== underline; next non-empty line after that is the
        # brief description that should consist of a single line.

        readme_file = os.path.join(pile_full_dir, 'README.md')
        self.pile_vars['pile_brief'] = '%s is great.' % self.pile_vars['pile']
        with open(readme_file, 'r') as finp:
            stat = README_STAT_HEADER
            for fileline in finp:
                fileline = fileline[:-1]
                if stat == README_STAT_HEADER:
                    if fileline.startswith('=='):
                        stat = README_STAT_WAIT_LINE
                elif stat == README_STAT_WAIT_LINE:
                    fileline = fileline.strip()
                    if len(fileline) > 0:
                        self.pile_vars['pile_brief'] = fileline
                        break

    def setup_dict_for_pile(self, pile_dir_name, pile_full_dir, pile_output):
        '''
        Fills in pile dependent variables in self.pile_vars.

        Parameters
        ----------
        pile_dir_name : name of the directory for the pile (== unix pile name)
        pile_full_dir : full path towards the pile
        pile_output : full path towards the destination directory

        Returns
        -------
        doxypile : the full path tovards the doxygen configuration file
        '''
        self.pile_vars['pile_dir_name'] = pile_dir_name
        self.pile_vars['pile_full_dir'] = pile_full_dir
        self.pile_vars['pile_output'] = pile_output

        # read the .cmake file and extract information from it
        cmake_file = os.path.join(pile_full_dir, '%s.cmake' % pile_dir_name)
        with open(cmake_file, 'r') as finp:
            stat = CMAKE_STAT_FIND_NAME
            for fileline in finp:
                fileline = fileline[:-1]
                if stat == CMAKE_STAT_FIND_NAME:
                    mtch = REX_CAMEL_PILE_NAME.match(fileline)
                    if mtch:
                        self.pile_vars['pile'] = mtch.group(1)
                        stat = CMAKE_STAT_PROP_START
                elif stat == CMAKE_STAT_PROP_START:
                    mtch = REX_PILE_SET_COMMON.match(fileline)
                    if mtch:
                        stat = CMAKE_STAT_PROP_NAME
                else:
                    mtch = REX_PILE_PROP.match(fileline)
                    if mtch:
                        self._pile_cmake_data(mtch, stat)
                    stat = stat + 1
                if stat >= CMAKE_STAT_PROP_END:
                    break

        self._pile_readme_data(pile_full_dir)

        # a tag file is used to link documentation together
        self.pile_vars['pile_tag_file'] = os.path.join(
            pile_output, '%s.tagpile' % pile_dir_name)

        LOGGER.debug('  Variables: ')
        for kkk in sorted(self.pile_vars):
            LOGGER.debug('  - %s = %s', kkk, str(self.pile_vars[kkk]))

    def create_doxy_pile(self, out_dir):
        '''
        Reads the template Doxyfile, replaces the variables and writes to file.

        Parameters
        ----------
        outdir : directory where doxygen output will be stored

        Returns
        -------
        doxypile : the full path tovards the doxygen configuration file
        '''

        # output file
        doxypile = os.path.join(out_dir, 'Doxypile')

        # read, replace and write t destination
        with open(self.doxyfile, 'r') as finp:
            fcontent = finp.read() % self.pile_vars
            with open(doxypile, 'w') as fout:
                fout.write(fcontent)

        return doxypile

    def collect(self):
        '''
        Collects information from the directory structure.
        '''
        self.tree = {}
        LOGGER.info('Collecting data ...')

        for subdir_name in os.walk(self.pilespath).next()[DIRNAMES]:
            # get full path
            subdir = os.path.join(self.pilespath, subdir_name)

            # filter out the tools
            if subdir_name.startswith('pile-'):
                continue
            LOGGER.debug('  Entering %s', subdir)

            # Top level directory contains a directory called `src`
            # hosting the helpers; the pile is always inside, in a directory
            # with the same name as top level direcotry fr the pile.
            pile_dir = os.path.join(subdir, 'src', subdir_name)
            if not os.path.isdir(pile_dir):
                LOGGER.warning('  Pile `%s` is invalid: directory %s '\
                               'does not exist', subdir_name, pile_dir)
                continue

            # update the source code from upstream
            if self.pull:
                pull_one(pile_dir)

            # compute output directory for this pile
            out_dir = os.path.join(self.outpath, subdir_name)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

            # fill in variables
            self.setup_dict_for_pile(subdir_name, pile_dir, out_dir)

            # save to general tree
            self.tree[subdir_name] = deepcopy(self.pile_vars)

    def _adjust_dependency(self, data, dep):
        '''
        Locate a dependent pile and save a link to it (None if not found).

        This is a utility function for adjust().
        '''
        dep_low = dep.lower()
        try:
            dep_vars = self.tree[dep_low]
        except KeyError:
            dep_vars = None
            LOGGER.warn('Dependency %s for pile %s could not be located',
                        dep, data['pile'])
        data['pile_dep_data'].append(dep_vars)

    def _adjust_category(self, data, category):
        '''
        Compose the tree of categories.

        This is a utility function for adjust().
        '''
        try:
            self.categories[category].append(data)
        except KeyError:
            self.categories[category] = [data]

    def _adjust_tags(self, data, tags):
        '''
        Compose the tree of tags.

        This is a utility function for adjust().
        '''
        for tag in tags:
            try:
                self.tags[tag].append(data)
            except KeyError:
                self.tags[tag] = [data]

    def adjust(self):
        '''
        Create internal links.
        '''
        LOGGER.info('Linking ...')
        self.categories = {}
        self.tags = {}

        for subdir in self.tree:
            data = self.tree[subdir]
            # look at each dependency
            data['pile_dep_data'] = []
            for dep in data['pile_deps']:
                self._adjust_dependency(data, dep)
            self._adjust_category(data, data['pile_categ'])
            self._adjust_tags(data, data['pile_tags'])

        LOGGER.debug('Categories (%d):', len(self.categories))
        for categ in self.categories:
            LOGGER.debug('  - %s (%d)', categ, len(self.categories[categ]))

        LOGGER.debug('Tags (%d):', len(self.tags))
        for tag in self.tags:
            LOGGER.debug('  - %s (%d)', tag, len(self.tags[tag]))

    def generate(self):
        '''
        Create doxygen documentation from collected information.
        '''
        LOGGER.info('Creating documentation...')
        for subdir in self.tree:
            LOGGER.info(subdir)
            self.pile_vars = self.tree[subdir]

            # generate a Doxyfile for this pile
            doxypile = self.create_doxy_pile(self.pile_vars['pile_output'])

            # run doxygen for this directory
            try:
                doxy_out = check_output([self.doxygen, doxypile],
                                        stderr=subprocess.STDOUT,
                                        shell=False,
                                        cwd=self.pile_vars['pile_output'])
                LOGGER.debug(doxy_out)
            except subprocess.CalledProcessError as exc:
                LOGGER.warning('  Pile `%s` error: `%s` failed ' \
                               'with error code %s: %s',
                               subdir, exc.cmd,
                               exc.returncode, exc.output)
                break
            except WindowsError as exc:
                LOGGER.warning('  Pile `%s` error: command failed ' \
                               'with error code %s: %s %s',
                               subdir, exc.errno, exc.message,
                               exc.strerror)
                break

    def postproc(self):
        '''
        Post process doxygen documentation.
        '''
        if not self.sitepath:
            return

        def common_file(lst, src_path, asset):
            '''Processing for common sets of files.'''
            for fname in lst:
                full_in = os.path.join(src_path, fname)
                full_out = os.path.join(self.sitepath, 'assets', asset, fname)
                if os.path.exists(full_in):
                    if os.path.exists(full_out):
                        os.remove(full_in)
                    else:
                        move_file(full_in, full_out)

        def brute_force_images(html_file):
            '''Replace all occurences of images to proper path.'''
            with open(html_file, 'rt') as finp:
                fcont = finp.read()
            for fname in COMMON_IMAGE_FILES:
                fcont = fcont.replace(
                    'src="' + fname + '"',
                    'src="../../../assets/images/' + fname + '"')
            with open(html_file, 'wt') as fout:
                fout.write(fcont)

        def pile_link(data):
            '''Create a html link for a pile'''
            return '<a href="%s/html/index.html" ' \
                    'title="%s version %s: %s">%s</a>' % (
                        data['pile_dir_name'], data['pile'], data['pile_version'],
                        data['pile_brief'], data['pile'])

        def tag_link(tag):
            '''Create a html link for a tag'''
            return '<a href="tags.html#tag-%s">%s</a>' % (tag, tag)

        def category_link(category):
            '''Create a html link for a category'''
            return '<a href="categories.html#categ-%s">%s</a>' % (
                category, category)

        def alphabetical_html():
            '''Generate an alphabetical list of piles.'''
            result = ''
            for subdir in sorted(self.tree):
                data = self.tree[subdir]
                s_categ_tags = [category_link(data['pile_categ'])]
                tags = data['pile_tags']
                for tag in tags:
                    s_categ_tags.append(tag_link(tag))
                s_categ_tags = ', '.join(s_categ_tags)
                result += \
                    '        <dt>%s&nbsp;<sup><a href="' \
                    'https://github.com/pile-contributors/%s">' \
                    'GitHub</a></sup></dt><dd>%s (%s)</dd>\n' % (
                        pile_link(data), subdir,
                        data['pile_brief'], s_categ_tags)
            return result

        def categories_html():
            '''Generate an alphabetical list of categories.'''
            result = ''
            for categ in sorted(self.categories):
                data = self.categories[categ]
                result += \
                    '        <dt id="categ-%s">%s</dt><dd>%s</dd>\n' % (
                        categ,
                        category_link(categ),
                        ', '.join([pile_link(pdata) 
                        for pdata in sorted(data)]))

            return result

        def tags_html():
            '''Generate an alphabetical list of tags.'''
            result = ''
            for tag in sorted(self.tags):
                data = self.tags[tag]
                result += \
                    '        <dt id="tag-%s">%s</dt><dd>%s</dd>\n' % (
                        tag,
                        tag_link(tag),
                        ', '.join([pile_link(pdata) 
                        for pdata in sorted(data)]))

            return result

        LOGGER.info('Post-processing...')
        for subdir in self.tree:
            data = self.tree[subdir]
            src_path = os.path.join(data['pile_output'], 'html')
            common_file(COMMON_JS_FILES, src_path, 'js')
            common_file(COMMON_CSS_FILES, src_path, 'css')
            common_file(COMMON_IMAGE_FILES, src_path, 'images')
            for fname in os.listdir(src_path):
                if fname.endswith('.html'):
                    brute_force_images(os.path.join(src_path, fname))

        # alphabetical list of piles
        file_with_dyn_area(
            os.path.join(self.outpath, 'index.html'),
            alphabetical_html())
        file_with_dyn_area(
            os.path.join(self.outpath, 'categories.html'),
            categories_html())
        file_with_dyn_area(
            os.path.join(self.outpath, 'tags.html'),
            tags_html())


    def run(self):
        '''
        Generates the documentation.
        '''
        LOGGER.debug('Starting documentation generation in %s',
                     self.pilespath)

        # make sure that the output directory exists
        if not os.path.exists(self.outpath):
            os.makedirs(self.outpath)

        self.collect()
        self.adjust()
        self.generate()
        self.postproc()

        LOGGER.debug('Ending documentation generation in %s', self.pilespath)
        LOGGER.info('Done.')

    def pull_all(self):
        '''
        Looks up all directories for git files.
        '''
        LOGGER.debug('Updating all piles...')

        for subdir, dirs, files in os.walk(self.pilespath):
            for drname in dirs:
                if drname == '.git':
                    full_path = os.path.join(subdir, drname)
                    pull_one(subdir)
                    LOGGER.debug('  Entering %s', full_path)
            for fname in files:
                if fname == '.git':
                    full_path = os.path.join(subdir, fname)
                    LOGGER.debug('  Entering %s', full_path)
                    pull_one(subdir)

        LOGGER.debug('All piles were updated')

def pull_one(path):
    '''
    Updates a single directory from upstream.
    '''
    try:
        git_out = check_output(['git', 'pull'],
                               stderr=subprocess.STDOUT,
                               shell=False,
                               cwd=path)
        LOGGER.debug(git_out)
    except subprocess.CalledProcessError as exc:
        LOGGER.warning('  `%s` failed with error code %s: %s',
                       exc.cmd, exc.returncode, exc.output)
    except WindowsError as exc:
        LOGGER.warning('  git pull failed with error code %s: %s %s',
                       exc.errno, exc.message,
                       exc.strerror)

def make_argument_parser():
    '''
    Creates an ArgumentParser to read the options for this script from
    sys.argv
    '''
    parser = argparse.ArgumentParser(
        description='Create piles documentation.',
        epilog='\n'.join(__doc__.strip().split('\n')[1:]).strip(),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('--debug', '-D',
                        action='store_true',
                        help='Display any DEBUG-level log messages, '
                             'suppressed by default.')
    parser.add_argument('--doxygen',
                        action='store', default='doxygen',
                        help='The path and name of the doxygen executable.')
    parser.add_argument('--pull',
                        action='store_true',
                        help='Update all repositories from upstream.')
    parser.add_argument('--doxyfile',
                        action='store', default='Doxyfile',
                        help='The path and name of the doxyfile template.')
    parser.add_argument('--outpath',
                        action='store', default='../docpiles',
                        help='Directory where the output will be generated.')
    parser.add_argument('--sitepath',
                        action='store', default='..',
                        help='Root directory for the site.')
    parser.add_argument('--logfile',
                        action='store',
                        help='Save the output to file.')
    parser.add_argument('pilespath', action='store',
                        choices=None,
                        help='The path towards the directory that ' \
                        'holds all piles')
    return parser

if __name__ == '__main__':
    PARSER = make_argument_parser()
    ARGS = PARSER.parse_args()
    LOGGER = logging.getLogger('DocumentPiles')
    setup_logging(ARGS, LOGGER)

    DocumRun(
        os.path.abspath(ARGS.pilespath),
        ARGS.doxygen, os.path.abspath(ARGS.doxyfile),
        os.path.abspath(ARGS.outpath),
        os.path.abspath(ARGS.sitepath),
        ARGS.pull).run()
