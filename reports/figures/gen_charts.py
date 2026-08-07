# generate dot-and-interval svgs for the two report pages
# tokens are css vars so the chart inherits the page palette

GREEN, GOLD = "var(--green)", "var(--gold)"
INK, INK_SOFT, INK_FAINT, HAIR, CARD = "var(--ink)", "var(--ink-soft)", "var(--ink-faint)", "var(--hair)", "var(--card)"
MONO = "JetBrains Mono, ui-monospace, Menlo, monospace"

def sc(x, xmin, xmax, x0, x1):
    # linear scale from data to pixel space
    return x0 + (x - xmin) / (xmax - xmin) * (x1 - x0)

def chart(rows, xmin, xmax, ticks, legend, fname, label_w=250):
    W, X0, X1 = 780, label_w + 14, 660
    row_h = 32
    top = 24 + 20 * len(legend) + 12
    n = len(rows)
    H = top + n * row_h + 40
    out = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" font-family="{MONO}">']
    # legend stacked vertically so no entry can clip
    for j, (colour, text) in enumerate(legend):
        ly = 16 + j * 20
        out.append(f'<circle cx="6" cy="{ly}" r="4.5" fill="{colour}"/>')
        out.append(f'<text x="17" y="{ly+4}" font-size="10.5" fill="{INK_SOFT}">{text}</text>')
    # zero line + ticks
    zx = sc(0, xmin, xmax, X0, X1)
    out.append(f'<line x1="{zx:.1f}" y1="{top-10}" x2="{zx:.1f}" y2="{top + n*row_h}" stroke="{HAIR}" stroke-dasharray="3 4" stroke-width="1"/>')
    for t in ticks:
        tx = sc(t, xmin, xmax, X0, X1)
        lab = '0' if t == 0 else f'{t:+.2f}'
        out.append(f'<text x="{tx:.1f}" y="{top + n*row_h + 22}" font-size="10" fill="{INK_FAINT}" text-anchor="middle">{lab}</text>')
    for i, r in enumerate(rows):
        y = top + i * row_h + row_h / 2
        if r.get("header"):
            out.append(f'<text x="0" y="{y+4:.1f}" font-size="11" font-weight="700" letter-spacing="1.5" fill="{INK}">{r["label"]}</text>')
            continue
        est, lo, hi, colour, ev = r["est"], r["lo"], r["hi"], r["colour"], r["ev"]
        xl, xr, xe = sc(lo, xmin, xmax, X0, X1), sc(hi, xmin, xmax, X0, X1), sc(est, xmin, xmax, X0, X1)
        out.append('<g>')
        out.append(f'<title>{r["label"]}: {est:.3f} [{lo:.3f}, {hi:.3f}], E-value bound {ev}</title>')
        out.append(f'<text x="{label_w}" y="{y+3.5:.1f}" font-size="10.5" letter-spacing="1" fill="{INK_SOFT}" text-anchor="end">{r["label"].upper()}</text>')
        out.append(f'<line x1="{xl:.1f}" y1="{y:.1f}" x2="{xr:.1f}" y2="{y:.1f}" stroke="{colour}" stroke-width="2" stroke-linecap="round"/>')
        out.append(f'<circle cx="{xe:.1f}" cy="{y:.1f}" r="4.5" fill="{colour}" stroke="{CARD}" stroke-width="2"/>')
        # fixed right-aligned value column: no collisions possible
        out.append(f'<text x="{W}" y="{y+3.5:.1f}" font-size="10" fill="{INK_FAINT}" text-anchor="end">{est:+.3f} · E {ev}</text>')
        out.append('</g>')
    out.append('</svg>')
    open(fname, 'w').write('\n'.join(out))
    print(fname, f'{n} rows, H={H}')

work = [
    dict(header=True, label="+10 HOURS PER WEEK"),
    dict(label="fatigue", est=0.079, lo=0.035, hi=0.123, colour=GREEN, ev="1.22"),
    dict(label="perceived physical health", est=-0.055, lo=-0.100, hi=-0.010, colour=GOLD, ev="1.10"),
    dict(label="perceived support", est=0.047, lo=0.002, hi=0.092, colour=GOLD, ev="1.04"),
    dict(header=True, label="−10 HOURS PER WEEK"),
    dict(label="fatigue", est=-0.042, lo=-0.069, hi=-0.015, colour=GREEN, ev="1.13"),
    dict(label="body mass index", est=-0.020, lo=-0.034, hi=-0.006, colour=GOLD, ev="1.08"),
    dict(label="perceived physical health", est=0.030, lo=0.003, hi=0.057, colour=GOLD, ev="1.06"),
]
chart(work, -0.14, 0.16, [-0.10, -0.05, 0, 0.05, 0.10],
      [(GREEN, "least vulnerable to unmeasured confounding"), (GOLD, "interval excludes zero; E-value modest")],
      "fig-work-hours.svg")

att = [
    dict(label="sexual satisfaction", est=0.086, lo=0.046, hi=0.126, colour=GREEN, ev="1.25"),
    dict(label="meaning and purpose", est=0.085, lo=0.044, hi=0.126, colour=GREEN, ev="1.25"),
    dict(label="forgiveness", est=0.075, lo=0.034, hi=0.116, colour=GREEN, ev="1.21"),
    dict(label="meaning and sense", est=0.071, lo=0.025, hi=0.117, colour=GREEN, ev="1.18"),
    dict(label="short-form health", est=0.061, lo=0.022, hi=0.100, colour=GREEN, ev="1.16"),
    dict(label="body satisfaction", est=0.058, lo=0.021, hi=0.095, colour=GREEN, ev="1.16"),
    dict(label="gratitude", est=0.046, lo=0.002, hi=0.090, colour=GOLD, ev="1.05"),
    dict(label="body mass index", est=-0.031, lo=-0.060, hi=-0.002, colour=GOLD, ev="1.05"),
]
chart(att, -0.09, 0.17, [-0.05, 0, 0.05, 0.10],
      [(GREEN, "meets the E-value reliability threshold"), (GOLD, "interval excludes zero; E-value modest")],
      "fig-attendance.svg")
