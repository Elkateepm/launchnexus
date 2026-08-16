# Product screenshots

Drop files here and the matching case study picks them up on the next
`python3 build.py`. No markup changes needed — until a file exists, the page
falls back to the CSS mockup.

Expected filenames:

    launchsession-register.png    LaunchSession live register

## Before you capture anything

**Never screenshot a real register.** It shows children's full names, and
nearby screens carry medical and safeguarding data. Publishing that would be a
personal-data breach involving minors, and the organisation — not LaunchNexus
— is the data controller, so it isn't ours to authorise. Blurring is not
sufficient: it is often reversible, and partial names alongside an org name
can still identify a child.

Capture from a **demo organisation seeded with invented people**. It is also
the better screenshot, because the data can be arranged to look right.

## Capture settings

- Browser window 1440px wide, on a HiDPI/retina display so the capture comes
  out at 2880px and stays sharp when scaled down.
- Hide bookmarks bar and any personal browser chrome, or capture the page
  region only.
- Light mode, default zoom.
- Save as PNG. Run it through the optimiser afterwards:

      python3 tools/optimise-shots.py

  which resizes to 1600px wide, strips metadata and re-encodes. Screenshots
  are the heaviest thing on the site, so this matters.

## Naming

Assets are cached for a year as immutable. If you replace a screenshot, give
it a new filename (`-v2`) rather than overwriting, or the old one will persist
in visitors' browsers.
