from anki import version as anki_version

old_anki = tuple(int(i) for i in anki_version.split(".")) < (2, 1, 20)

if old_anki:
  from . import clickable
else:
  from . import ported_clickable
