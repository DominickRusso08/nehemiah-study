# A Study Through the Book of Nehemiah

Verse-by-verse pastoral commentary pairing ESV scripture with sermons preached at
Life Church Las Vegas by Pastor Andrew Reed.

Live: https://dominickrusso08.github.io/nehemiah-study

## How this repo works

`index.html` is **generated**. Do not hand-edit it — it is overwritten on every build.

```
content/sermons.json   series info + one entry per sermon   <- the only file edited weekly
templates/page.html    page shell with __PLACEHOLDERS__
templates/style.css    stylesheet
templates/app.js       sidebar nav, deep-dive toggles, scroll spy
templates/logo.txt     Life Church logo as a data URI
build.py               renders index.html from the above
index.html             generated output — GitHub Pages serves this
```

## Weekly update

1. Add the new sermon to `content/sermons.json` (schema below).
2. `python3 build.py`
3. `git add -A && git commit -m "Add sermon N: <title>" && git push`

Pages redeploys in under a minute.

## Sermon schema

```json
{
  "id": "s2",
  "chapter": 2,
  "passage": "Nehemiah 2:1&ndash;10",
  "short": "Neh 2:1&ndash;10",
  "title": "Sermon Title",
  "youtube": "https://youtu.be/...",
  "note": "Pastor's Note — what the sermon was about overall.",
  "sections": { "1": "ESV section heading shown above verse 1" },
  "verses": [
    {
      "n": 1,
      "text": "ESV text of the verse, verbatim.",
      "summary": "Short commentary shown inline.",
      "deep": "Longer breakdown of how the pastor preached it."
    }
  ]
}
```

Notes:
- `sections` is optional; keys are verse numbers where an ESV heading appears.
- A verse with no `summary` renders greyed out via `.verse-row.context`
  (useful for context verses that were read but not preached).
- `verses[].text` is authoritative scripture and is emitted verbatim.
  It is never rewritten, paraphrased, or reformatted by the build.
- Use HTML entities (`&ndash;`, `&rsquo;`) rather than raw characters for
  consistency with the existing content.

## Scripture

Scripture quotations are from the ESV® Bible, copyright © 2001 by Crossway,
a publishing ministry of Good News Publishers. Used by permission.
All rights reserved.
