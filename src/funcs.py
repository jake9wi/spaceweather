import re

def check_cwd(cwd):
    if cwd.parts[-1] != 'spaceweather':
        raise Exception((
            'Looks like we are not in root dir. '
            'Root dir should be \"spaceweather/\"'
        ))
    return


def filter_comment_lines(text: str) -> str:
    pat = re.compile(r'^[:#]')

    good_lines = list()

    for line in text.splitlines(keepends=True):
        if pat.match(line) is None:
            good_lines.append(line)

    return ''.join(good_lines)
