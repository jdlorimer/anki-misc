
# -*- coding: utf-8 -*-
"""
Clickable_Tags add-on 0.1 alpha release- inspired by Dybamic_Tags add-on
The styles used here are from Power format pack add-on
Copyright: Abdolmahdi Saravi, 2013 <amsaravi@yahoo.com>
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
This add-on Displays the Cards Tag in style of keyboard keys that has the 
ability to click on them witch opens the anki browser and lists the cards that match clicked tag.
You can change the style of tags by editing the code.
You can also use {{Tags}} in card template to position the tags on the card. by default if you don't use the
{{Tags}} in your Cards the add-on puts the tags before any content of the card. you can change this behavior
by setting the variable TAG_IN_ALL_CARDS to False
Also you can use this add-on as a global css injector. css styles that is defined here are visible on all note types
if you Double Click on a tag within viewer the related Tags within current Deck will be showed
Good Luck
https://bitbucket.org/amsaravi/ankiaddons
"""
from aqt import DialogManager  # we need it to fix the anki behavior not to deal with minimized state of window
from aqt.reviewer import Reviewer
from anki.hooks import wrap
from aqt.utils import showInfo
from aqt import mw
import aqt
from anki.cards import Card
from anki.template import Template
import re
from aqt.qt import *
from aqt.browser import Browser
kbd_css = """
kbd {
    box-shadow: inset 0px 1px 0px 0px #ffffff;
    background: -webkit-gradient(linear, left top, left bottom, color-stop(0.05, #f9f9f9), color-stop(1, #e9e9e9) );
    background-color: #f9f9f9;
    border-radius: 4px;
    border: 1px solid #dcdcdc;
    display: inline-block;
    font-size:15px;
    height: 15px;
    line-height: 15px;
    padding:4px 4px;
    margin:5px;
    text-align: center;
    text-shadow: 1px 1px 0px #ffffff;
    cursor: pointer; cursor: hand;
}
"""
java_script = """
<script type="text/javascript">
var timer = 0;
var delay = 200;
var prevent = false;
function click_func(tags) {
    timer = setTimeout(function() {
        if (!prevent) {
            py.link(tags);
        }
        prevent = false;
    }, delay);
}

function dblclick_func(tags_deck) {
    clearTimeout(timer);
    prevent = true;
    py.link(tags_deck);
}

</script>
"""
TAG_MARK = "{{Tags}}"
FRNT_SIDE = "{{FrontSide}}"
TAG_IN_ALL_CARDS = True
# TAG_IN_ALL_CARDS=False    #uncomment and put the fields in your cards manually

def tagClicklinkHandler(reviewer, url, isPreview=False):   
    if isPreview:
        pass    #the function called from preview form 
    if url.startswith("tagclick_"):
        tag = url.split("tagclick_")[-1]
        browser = aqt.dialogs.open("Browser", reviewer.mw)
        browser.setFilter("tag:%s" % tag)
        
    elif url.startswith("_tagdblclick_"):
        dec, tag = url.split("_tagdblclick_")[1:]
        browser = aqt.dialogs.open("Browser", reviewer.mw)       
        browser.setFilter("tag:%s \"deck:%s\"" % (tag, dec))
        browser.setWindowState(browser.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    else:
        oldLinkHandler(reviewer, url)
        
def new_css(card):
    return old_css(card) + "<style>%s</style>" % kbd_css

def new_render(self, template=None, context=None, encoding=None):
    template = template or self.template
    context = context or self.context
    if context is not None:
        dec = context['Deck']
        tags = context['Tags'].split()
        tagStr = "".join(["<kbd ondblclick='dblclick_func(\"%s\")' onclick='click_func(\"tagclick_%s\")'>%s</kbd>"
                         % ("_tagdblclick_%s_tagdblclick_%s" % (dec, tag), tag, tag) for tag in tags])
        tagStr += java_script
        template, n = re.subn(TAG_MARK, tagStr, template)
        if (not n) and (template.rfind(FRNT_SIDE) == -1) and (TAG_IN_ALL_CARDS):
            template = tagStr + template    
    return old_render(self, template, context, encoding)

"function to change anki behavior of opening  minimized windows that anki doesn't deals with it"
def unminimize(dlgmngr, name, *args):
    instance=old_open(dlgmngr,name, *args)
    if instance:
        instance.setWindowState(instance.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    return instance

oldLinkHandler = Reviewer._linkHandler
Reviewer._linkHandler = tagClicklinkHandler

old_css = Card.css
Card.css = new_css

old_render = Template.render
Template.render = new_render

def unminimize(dlgmngr, name, *args):
    instance=old_open(dlgmngr,name, *args)
    if instance:
        instance.setWindowState(instance.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    return instance

old_open= DialogManager.open
DialogManager.open =  unminimize

def new_renderPreview(self, cardChanged=False):    
    if self._previewWindow:
        self._previewWeb.setLinkHandler(lambda url: tagClicklinkHandler(self,url, True))

Browser._renderPreview=wrap(Browser._renderPreview, new_renderPreview, "before")
