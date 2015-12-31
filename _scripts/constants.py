import re

CMAKE_STAT_FIND_NAME = 1
CMAKE_STAT_PROP_START = 2
CMAKE_STAT_PROP_NAME = 3
CMAKE_STAT_PROP_VERSION = 4
CMAKE_STAT_PROP_CONFIG = 5
CMAKE_STAT_PROP_MODE = 6
CMAKE_STAT_PROP_DEPS = 7
CMAKE_STAT_PROP_CATEGS = 8
CMAKE_STAT_PROP_TAGS = 9
CMAKE_STAT_PROP_END = 10

README_STAT_HEADER = 1
README_STAT_WAIT_LINE = 2

# os.walk constant
DIRNAMES = 1

# patterns for .cmake file parsing
REX_CAMEL_PILE_NAME = re.compile('^\s*set\s*\(\s*[A-Z0-9]+_INIT_NAME' \
                                 '\s+"(.+)"\s*\)\s*$')
REX_PILE_SET_COMMON = re.compile('^\s*pileSetCommon\s*\(\s*$')
REX_PILE_PROP = re.compile('^\s*"(.+)"\s*\)*\s*$')

COMMON_JS_FILES = [
    'dynsections.js',
    'jquery.js',
    'navtree.js',
    'resize.js'
]

COMMON_CSS_FILES = [
    'doxygen.css',
    'navtree.css',
    
    'styleSheetFile.css',
    
    'tabs.css'
]

COMMON_IMAGE_FILES = [
    'arrowdown.png',
    'arrowright.png',
    'bc_s.png',
    'bdwn.png',
    'class_app_opts.png',
    'closed.png',
    'doc.png',
    'doxygen.png',
    'folderclosed.png',
    'folderopen.png',
    'open.png',
    'splitbar.png',
    'sync_off.png',
    'sync_on.png',
    'nav_a.png',
    'nav_b.png',
    'nav_c.png',
    'nav_d.png',
    'nav_e.png',
    'nav_f.png',
    'nav_g.png',
    'nav_h.png',
    'nav_i.png',
    'nav_j.png',
    'nav_k.png',
    'nav_l.png',
    'nav_m.png',
    'nav_n.png',
    'nav_o.png',
    'nav_p.png',
    'nav_q.png',
    'nav_r.png',
    'nav_s.png',
    'nav_t.png',
    'nav_u.png',
    'nav_v.png',
    'nav_w.png',
    'nav_x.png',
    'tab_a.png',
    'tab_b.png',
    'tab_c.png',
    'tab_d.png',
    'tab_e.png',
    'tab_f.png',
    'tab_g.png',
    'tab_h.png',
    'tab_i.png',
    'tab_j.png',
    'tab_k.png',
    'tab_l.png',
    'tab_m.png',
    'tab_n.png',
    'tab_o.png',
    'tab_p.png',
    'tab_q.png',
    'tab_r.png',
    'tab_s.png',
    'tab_t.png',
    'tab_u.png',
    'tab_v.png',
    'tab_w.png',
    'tab_x.png'
]
