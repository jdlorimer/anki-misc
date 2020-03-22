# Copyright © 2019-2020 Joseph Lorimer <joseph@lorimer.me>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import re
import warnings

from aqt import gui_hooks, QDialog, QFont
from aqt.utils import openHelp
import aqt

from bs4 import BeautifulSoup

open_space_open = re.compile('(<[^/>]+>) (<[^/>]+>)')
close_space_close = re.compile('(</[^>]+>) (</)')
open_space_text = re.compile('(<[^/>]+>) ([^<>]+)')
open_text_close = re.compile('(<[^/>]+>) ([^<>]+) (</)')
tag_space_punc = re.compile('(>) ([.,:;])')


# _onHtmlEdit should be kept in sync with upstream, except:
#   - Set a decent monospace font for the QTextEdit box
#   - Set dialog size to something more reasonable than 400x300
#   - Don't force the cursor to the end of the box
#   - Prettify field contents before passing to `setPlainText`
#   - Postprocess edited field contents before saving


def _onHtmlEdit(self, field):
    d = QDialog(self.widget)
    form = aqt.forms.edithtml.Ui_Dialog()
    form.setupUi(d)
    form.buttonBox.helpRequested.connect(lambda: openHelp('editor'))
    font = QFont('Iosevka')
    font.setStyleHint(QFont.Monospace)
    form.textEdit.setFont(font)
    form.textEdit.setPlainText(prettify(self.note.fields[field]))
    d.resize(700, 600)
    d.show()
    d.exec_()
    html = form.textEdit.toPlainText()
    if html.find('>') > -1:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            html = str(
                BeautifulSoup(
                    postprocess(form.textEdit.toPlainText()), 'html.parser'
                )
            )
    self.note.fields[field] = html
    self.note.flush()
    self.loadNote(focusTo=field)


def prettify(s):
    return reindent(
        BeautifulSoup(s, 'html.parser').prettify(formatter='html5')
    )


def reindent(s, factor=4):
    """Increase indentation of pretty printed HTML.

    Beautiful Soup indents by a single space at each indentation level,
    probably because it also places each tag on its own line, resulting
    in heavily nested markup. In many situations this will pose
    readability issues, but in Anki the editor only deals with HTML
    fragments, not entire documents. 4 spaces is more reasonable.
    """
    t = []
    for line in s.split('\n'):
        r = re.match('( +)([^ ].*)', line)
        if r:
            n = len(r.group(1)) * factor
            t.append('{}{}'.format(' ' * n, r.group(2)))
        else:
            t.append(line)
    return '\n'.join(t)


def postprocess(s):
    """Collapse pretty printed HTML, keeping somewhat sensible white space.

    Beautiful Soup replaces any spacing around tags with newlines and
    indentation. A naive function that attempts to reverse this by
    collapsing the newlines and indentation into a single white space
    will leave spurious spaces around tags. On the other hand, some of
    this white space is essential both semantically and for readability.
    We attempt to reach a sane compromise via these transformations:

    - <span> text </span> => <span>text</span>
    - <span> text         => <span>text
    - <span> <span>       => <span><span>
    - </span> </span>     => </span></span>
    - <span> ,            => <span>,
    - </span> ,           => </span>,
    """
    s = re.sub('\n', ' ', s)
    s = re.sub('[ ]+', ' ', s)
    new = s
    while True:
        new = open_text_close.sub('\\1\\2\\3', new)
        new = open_space_text.sub('\\1\\2', new)
        new = open_space_open.sub('\\1\\2', new)
        new = close_space_close.sub('\\1\\2', new)
        new = tag_space_punc.sub('\\1\\2', new)
        if new == s:
            break
        s = new
    return s


def remap(cuts, editor):
    cuts.remove(('Ctrl+Shift+X', editor.onHtmlEdit))
    cuts.append(('F12', editor.onHtmlEdit))


gui_hooks.editor_did_init_shortcuts.append(remap)
aqt.editor.Editor._onHtmlEdit = _onHtmlEdit
