'''
Routines for generating dynamic files.
'''

def file_with_dyn_area(
        file_path, content,
        first_guard='<!-- guard line: beginning -->',
        second_guard='<!-- guard line: end -->'):
    '''
    The function reads a file, locates the guards, replaces the content.
    '''
    full_content = ''
    guard_count = 0
    with open(file_path, 'rt') as finp:
        for fline in finp:
            finp_trim = fline[:-1].strip()
            if guard_count == 0:
                full_content += fline
                if finp_trim == first_guard:
                    guard_count = 1
                    full_content += content
            elif guard_count == 1:
                if finp_trim == second_guard:
                    full_content += fline
                    guard_count = 2
            else:
                full_content += fline
    if guard_count != 2:
        raise IOError('file %s is not a proper template' % file_path)

    with open(file_path, 'wt') as fout:
        fout.write(full_content)
