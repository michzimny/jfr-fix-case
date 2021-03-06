import os


class ParyResultDirectory:
    W_FILENAME_BEGIN = 'w-'
    W_FILENAME_END = '.html'

    FILENAME_PATTERNS = [
        'W-PREFIX\.html',
        'H-PREFIX-lista\.html',
        'H-PREFIX-(\d+)\.html',
        'PREFIXWYN\.html',
        'PREFIXWYN\.txt',
    ]

    STATIC_CHANGES = {
        'myajaxp.js': 'myAjaxP.js',
        's.gif': 'S.gif',
        'h.gif': 'H.gif',
        'c.gif': 'C.gif',
        'd.gif': 'D.gif',
        'n.gif': 'N.gif',
    }

    def __init__(self, filenames):
        self.filenames = filenames

    def get_changes(self):
        prefixes = list(self._deduce_prefixes())
        for filename in self.filenames:
            for prefix in prefixes:
                fixed_filename = self._fix_case_for_filename(prefix, filename)
                if filename != fixed_filename:
                    yield filename, fixed_filename
            if filename in self.STATIC_CHANGES:
                yield filename, self.STATIC_CHANGES[filename]

    def _deduce_prefixes(self):
        for filename in self.filenames:
            if filename.startswith(self.W_FILENAME_BEGIN) and filename.endswith(self.W_FILENAME_END):
                yield self._extract_prefix(filename)

    def _extract_prefix(self, filename):
        without_begin = filename[len(self.W_FILENAME_BEGIN):]
        return without_begin[:(len(without_begin) - len(self.W_FILENAME_END))]

    def _fix_case_for_filename(self, prefix, filename):
        if filename == 'w-' + prefix + '.html':
            return 'W-' + prefix + '.html'
        if filename.startswith('h-' + prefix) and filename.endswith('.html'):
            return filename.replace('h-', 'H-', 1)
        if filename == prefix + 'wyn.html':
            return prefix + 'WYN.html'
        if filename == prefix + 'wyn.txt':
            return prefix + 'WYN.txt'
        return filename


def test():
    assert ParyResultDirectory([])._extract_prefix('w-19XXyy.html') == '19XXyy'
    assert list(ParyResultDirectory([]).get_changes()) == []

    wrong_filenames = [
        'w-19XXyy.html',
        'h-19XXyy-lista.html',
        'h-19XXyy-11.html',
        '19XXyywyn.html',
        '19XXyywyn.txt',
        '19XXyy049.html',
        'myajaxp.js',
        'w-innypref.html',
    ]
    proper_filenames = [
        'W-19XXyy.html',
        'H-19XXyy-lista.html',
        'H-19XXyy-11.html',
        '19XXyyWYN.html',
        '19XXyyWYN.txt',
        '19XXyy049.html',
        'myAjaxP.js',
        'W-innypref.html',
    ]

    fixed_filenames = _copy(wrong_filenames)
    changes = { src: dest for src, dest in ParyResultDirectory(wrong_filenames).get_changes() }
    for i, filename in enumerate(fixed_filenames):
        if filename in changes:
            fixed_filenames[i] = changes[filename]

    assert fixed_filenames == proper_filenames, fixed_filenames


def _copy(wrong_filenames):
    if hasattr(wrong_filenames, 'copy'):
        return wrong_filenames.copy()
    else:
        import copy
        return copy.deepcopy(wrong_filenames)


def process(rootpath):
    for dirpath, subdirnames, filenames in os.walk(rootpath):
        for src_filename, dest_filename in ParyResultDirectory(filenames).get_changes():
            print("%s: %s => %s" % (dirpath, src_filename, dest_filename))
            src_path = os.path.join(dirpath, src_filename)
            dest_path = os.path.join(dirpath, dest_filename)
            os.rename(src_path, dest_path)

if __name__ == '__main__':
    print('Testing...')
    test()
    print('Testing done. Now processing...')
    print()

    process('.')

    print()
    print('Done')
