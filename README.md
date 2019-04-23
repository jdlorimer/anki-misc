Miscellaneous Anki Projects
===========================

## Clickable Tags

![Clickable Tags](https://raw.githubusercontent.com/luoliyan/anki-misc/master/screenshots/clickable-tags.png)

A stripped-down port of the [Clickable Tags](https://ankiweb.net/shared/info/1321188674) add-on to Anki 2.1.

Just add the `{{Tags}}` special field to your card template. The add-on will take care of the rest.

Single-click the tag to search for notes with that tag. Double-click to limit the search to the current deck.

## HTML Editor Tweaks

![HTML Editor Tweaks](https://raw.githubusercontent.com/luoliyan/anki-misc/master/screenshots/html-editor-tweaks.png)

A set of tweaks to the built-in HTML editor. Hopefully an improvement for those who spend a lot of time editing cards.

Very alpha. Seems to work 99% of the time, but please make a backup of your collection first.

### Tweaks

- Prettifies the HTML by running it through _Beautiful Soup_
    - Reformats pretty aggressively, which is what I wanted, but not everyone will like it
- Remaps <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd> to <kbd>F12</kbd>
- Sets a decent monospace font (assumes [Iosevka](https://github.com/be5invis/Iosevka); edit `__init__.py` to change)
- Resizes the editor to something more reasonable than **400 x 300**
- Disables the default behaviour of loading the cursor on the last line (personal preference, yes)

### Known Issues

- Adds spurious space just before `<sub>` or `<sup>`
- Incorrect handling of tags inside parentheses
