#!/usr/bin/env python3
"""Generate index.html from content/sermons.json.

Weekly workflow:
  1. Add a sermon object to content/sermons.json
  2. python3 build.py
  3. git add -A && git commit && git push

Never hand-edit index.html -- it is generated and will be overwritten.
Scripture text in sermons.json is authoritative and is emitted verbatim.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CSS  = open(os.path.join(ROOT, 'templates/style.css'), encoding='utf-8').read()
LOGO = open(os.path.join(ROOT, 'templates/logo.txt'), encoding='utf-8').read().strip()
DATA = json.load(open(os.path.join(ROOT, 'content/sermons.json'), encoding='utf-8'))

S       = DATA['series']
SERMONS = DATA['sermons']
YTSVG   = '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>'


def verse_rows(sermon):
    """Render one sermon's verse table. Scripture is emitted exactly as stored."""
    out, sections = [], sermon.get('sections', {})
    for v in sermon['verses']:
        heading = sections.get(str(v['n']))
        if heading:
            out.append('<div class="section-divider"><div class="sd-cell">%s</div>'
                       '<div class="sd-cell"></div></div>' % heading)
        state = 'preached' if v.get('summary') else 'context'
        ddid  = 'dd-%s-%d' % (sermon['id'], v['n'])
        com = ''
        if v.get('summary'):
            com += '<div class="c-summary">%s</div>' % v['summary']
        if v.get('deep'):
            com += ('<button class="dd-toggle" onclick="toggleDD(\'%s\')">'
                    '<span class="dd-label">Deep Dive</span>'
                    '<span class="dd-arrow">&#9662;</span></button>'
                    '<div class="dd-body" id="%s">%s</div>' % (ddid, ddid, v['deep']))
        out.append('<div class="verse-row %s"><div class="bible-col">'
                   '<sup class="vnum">%d</sup>%s</div>'
                   '<div class="commentary-col">%s</div></div>'
                   % (state, v['n'], v['text'], com))
    return ''.join(out)


def sidebar():
    """Sermon list grouped by chapter, in the order sermons appear."""
    groups, order = {}, []
    for s in SERMONS:
        groups.setdefault(s['chapter'], []).append(s)
        if s['chapter'] not in order:
            order.append(s['chapter'])
    out = []
    for ch in order:
        items = ''.join(
            '<div class="sermon-item" id="item-%s" onclick="jumpTo(\'%s\')">'
            '<div class="sermon-item-text"><div class="s-passage">%s</div>'
            '<div class="s-title">%s</div></div>'
            '<a class="yt-btn" href="%s" target="_blank" rel="noopener" '
            'onclick="event.stopPropagation()" title="Watch on YouTube">%s</a></div>'
            % (s['id'], s['id'], s['short'], s['title'], s['youtube'], YTSVG)
            for s in groups[ch])
        out.append('<div class="chapter-group"><div class="chapter-label">Chapter %d</div>%s</div>'
                   % (ch, items))
    return ''.join(out)


def sermon_sections():
    out = []
    for s in SERMONS:
        out.append(
          '<div class="sermon-divider" id="sermon-%s" data-sermon="%s">'
          '<div class="sd-yt-bar"><a class="sd-yt-link" href="%s" target="_blank" rel="noopener">%s Watch Sermon on YouTube</a></div>'
          '<div class="sd-hero-inner">'
          '<div class="sd-passage">%s</div>'
          '<div class="sd-title">%s</div>'
          '<div class="sd-meta">%s &middot; %s</div>'
          '<div class="sd-context"><strong>Pastor&rsquo;s Note:</strong> %s</div>'
          '<button class="note-toggle" onclick="toggleNote(this)">Show more</button>'
          '</div></div>'
          '<div class="commentary-area">'
          '<div class="col-headers"><div class="col-hdr">Scripture (ESV)</div>'
          '<div class="col-hdr">Pastoral Commentary</div></div>%s</div>'
          % (s['id'], s['id'], s['youtube'], YTSVG, s['passage'], s['title'],
             S['church'], S['short'], s['note'], verse_rows(s)))
    return ''.join(out)


def main():
    n_serm = len(SERMONS)
    n_chap = len({s['chapter'] for s in SERMONS})
    n_vers = sum(len(s['verses']) for s in SERMONS)
    ids    = ','.join('"%s"' % s['id'] for s in SERMONS)

    js = open(os.path.join(ROOT, 'templates/app.js'), encoding='utf-8').read()
    js = js.replace('__SERMON_IDS__', ids)

    html = open(os.path.join(ROOT, 'templates/page.html'), encoding='utf-8').read()
    html = (html
        .replace('__CSS__', CSS)
        .replace('__LOGO__', LOGO)
        .replace('__SIDEBAR__', sidebar())
        .replace('__SERMONS__', sermon_sections())
        .replace('__JS__', js)
        .replace('__TITLE__', S['title'])
        .replace('__SHORT__', S['short'])
        .replace('__BOOK__', S['book'])
        .replace('__CHURCH__', S['church'])
        .replace('__PASTOR__', S['pastor'])
        .replace('__N_SERM__', str(n_serm))
        .replace('__L_SERM__', 'Sermon' if n_serm == 1 else 'Sermons')
        .replace('__N_CHAP__', str(n_chap))
        .replace('__L_CHAP__', 'Chapter' if n_chap == 1 else 'Chapters')
        .replace('__N_VERS__', str(n_vers)))

    out = os.path.join(ROOT, 'index.html')
    open(out, 'w', encoding='utf-8').write(html)
    print('built index.html  %d sermons / %d chapters / %d verses  (%d bytes)'
          % (n_serm, n_chap, n_vers, len(html.encode('utf-8'))))


if __name__ == '__main__':
    main()
