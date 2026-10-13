"""Build the five research-card figures in assets/images/research/.

Three come from rasterised sources in figures/src/ (paper figures and a slide),
recoloured for the dark site: white -> transparent, colours inverted + hue-rotated
so black lines turn light and hues are preserved. Two are drawn here.
Run:  python3 figures/make_figures.py
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

HERE = Path(__file__).parent
SRC, OUT = HERE / "src", HERE.parent / "assets" / "images" / "research"
OUT.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, FG = "#7cc4ff", "#f5a97f", "#e8eaed"
W, H = 1600, 1000


def darkify(name, out, keep_colour=False):
    """Recolour a white-background figure for the dark site.

    White -> transparent. Default: invert + hue-rotate 180° (flips lightness,
    keeps hues). keep_colour=True: invert only the near-grey pixels (axes, text,
    black lines) and leave saturated colours (colour maps, coloured lines) as is.
    """
    im = Image.open(SRC / name).convert("RGB")
    rgb = np.asarray(im).astype(np.uint8)
    white = rgb.min(axis=2) > 235
    inv = Image.fromarray(255 - rgb).convert("HSV")
    h, s, v = [np.asarray(c).astype(np.int16) for c in inv.split()]
    h = (h + 128) % 256
    rot = Image.merge("HSV", [Image.fromarray(c.astype(np.uint8)) for c in (h, s, v)]).convert("RGBA")
    a = np.asarray(rot).copy()
    if keep_colour:
        sat = np.asarray(im.convert("HSV").split()[1]) > 60
        a[sat, :3] = rgb[sat]
    a[white, 3] = 0
    im = Image.fromarray(a)
    im.thumbnail((W, H), Image.LANCZOS)
    im.save(OUT / out, optimize=True)


def fig(wh=(W, H)):
    f, ax = plt.subplots(figsize=(wh[0] / 200, wh[1] / 200), dpi=200)
    f.patch.set_alpha(0)
    ax.set_facecolor("none")
    ax.axis("off")
    return f, ax


def ringdown():
    t = np.linspace(-0.35, 0.08, 4000)
    insp = t < 0
    f0, k = 30.0, 2.2
    phase = 2 * np.pi * f0 * (-(-t[insp]) ** (5 / 8) * 8 / 5)
    amp = (-t[insp] + 0.004) ** (-0.25)
    h = np.zeros_like(t)
    h[insp] = amp * np.cos(phase)
    peak = h[insp][-1]
    rd = ~insp
    tau, fr = 0.012, 250.0
    h[rd] = peak * np.exp(-t[rd] / tau) * np.cos(2 * np.pi * fr * t[rd])
    h /= np.abs(h).max()
    f, ax = fig()
    ax.plot(t[insp], h[insp], color=BLUE, lw=1.6, alpha=0.55)
    ax.plot(t[rd], h[rd], color=ORANGE, lw=2.2)
    env = np.exp(-t[rd] / tau)
    ax.plot(t[rd], env, color=ORANGE, lw=1, ls="--", alpha=0.7)
    ax.plot(t[rd], -env, color=ORANGE, lw=1, ls="--", alpha=0.7)
    ax.axvline(0, color=FG, lw=0.8, alpha=0.4)
    ax.text(0.004, 1.08, "ringdown", color=ORANGE, fontsize=11, va="bottom")
    ax.text(-0.12, 1.08, "inspiral  →  merger", color=BLUE, fontsize=11, va="bottom", alpha=0.9)
    ax.set_xlim(-0.3, 0.08)
    ax.set_ylim(-1.25, 1.3)
    f.savefig(OUT / "ringdown.png", transparent=True, bbox_inches="tight", pad_inches=0.05)


def source_frame():
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    f = plt.figure(figsize=(W / 200, H / 200), dpi=200)
    f.patch.set_alpha(0)
    ax = f.add_subplot(111, projection="3d", proj_type="ortho")
    ax.set_facecolor("none")
    ax.set_axis_off()
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(th), np.sin(th), 0, color=FG, lw=0.9, alpha=0.5)
    ax.plot_surface(*np.meshgrid(np.linspace(-1.3, 1.3, 2), np.linspace(-1.3, 1.3, 2)), np.zeros((2, 2)),
                    color=BLUE, alpha=0.08, linewidth=0)
    for x, y, r in ((0.75, 0, 0.16), (-0.5, 0, 0.11)):
        ax.scatter([x], [y], [0], s=r * 9000, color="#111318", edgecolors=FG, linewidths=1.2, zorder=5)
    q = dict(arrow_length_ratio=0.12, lw=2)
    ax.quiver(0, 0, 0, 0, 0, 1.3, color=BLUE, **q)
    ax.text(0.05, 0.05, 1.38, r"$\hat{L}$", color=BLUE, fontsize=14)
    N = np.array([0.95, 0.55, 0.9]) / np.linalg.norm([0.95, 0.55, 0.9]) * 1.5
    ax.quiver(0, 0, 0, *N, color=FG, **q)
    ax.text(*(N * 1.08), r"$\hat{N}$", color=FG, fontsize=14)
    K = np.array([-1.0, 0.7, 0.55]) / np.linalg.norm([-1.0, 0.7, 0.55]) * 1.2
    ax.quiver(0, 0, 0, *K, color=ORANGE, **q)
    ax.text(*(K * 1.1), r"$\vec{K}$", color=ORANGE, fontsize=14)
    # inclination arc between L and N
    s = np.linspace(0, 1, 40)
    Lh = np.array([0, 0, 1])
    arc = np.array([np.sin((1 - u) * 0.9) * Lh + np.sin(u * 0.9) * N / 1.5 for u in s]) / np.sin(0.9) * 0.55
    ax.plot(*arc.T, color=FG, lw=1, alpha=0.8)
    ax.text(0.22, 0.1, 0.62, r"$\iota$", color=FG, fontsize=13)
    arcK = np.array([np.sin((1 - u) * 1.1) * Lh + np.sin(u * 1.1) * K / 1.2 for u in s]) / np.sin(1.1) * 0.45
    ax.plot(*arcK.T, color=ORANGE, lw=1, alpha=0.8)
    ax.text(-0.42, 0.42, 0.42, r"$\theta_K$", color=ORANGE, fontsize=13)
    ax.plot([0, N[0] * 1.1], [0, N[1] * 1.1], [0, 0], color=FG, lw=0.8, ls=":", alpha=0.6)
    ax.plot([N[0], N[0]], [N[1], N[1]], [0, N[2]], color=FG, lw=0.8, ls=":", alpha=0.6)
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2); ax.set_zlim(-0.3, 1.5)
    ax.set_box_aspect((1.6, 1.6, 1.2))
    ax.view_init(elev=24, azim=-62)
    f.savefig(OUT / "source.png", transparent=True, bbox_inches="tight", pad_inches=0)


def xg():
    """Waveform band from the IITBombay2026 title slide, labels redrawn at card size."""
    im = Image.open(SRC / "xg_whisper_to_roar.png").convert("RGB").crop((0, 310, 2933, 720))
    rgb = np.asarray(im).astype(np.uint8)
    white = rgb.min(axis=2) > 235
    inv = Image.fromarray(255 - rgb).convert("HSV")
    h, s, v = [np.asarray(c).astype(np.int16) for c in inv.split()]
    rot = Image.merge("HSV", [Image.fromarray(c.astype(np.uint8)) for c in (((h + 128) % 256), s, v)]).convert("RGBA")
    a = np.asarray(rot).copy()
    a[white, 3] = 0
    f, ax = fig((W, 900))
    ax.imshow(a, extent=(0, 1, 0, 0.6), aspect="auto", interpolation="lanczos")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.text(0.04, 0.70, "2015: one whisper", color=FG, fontsize=11, ha="left")
    ax.text(0.50, 0.78, "today: a few hundred", color=FG, fontsize=11, ha="center")
    ax.text(0.98, 0.86, "next generation:\na continuous roar", color=ORANGE, fontsize=12, ha="right", va="bottom")
    f.savefig(OUT / "xg.png", transparent=True, bbox_inches="tight", pad_inches=0.05)


if __name__ == "__main__":
    xg()
    darkify("tgr_fig6_2512.04593.png", "tgr.png", keep_colour=True)
    darkify("search_fig5b_2106.00193.png", "search.png", keep_colour=True)
    ringdown()
    source_frame()
    for p in sorted(OUT.glob("*.png")):
        print(f"{p.name:12s} {p.stat().st_size // 1024:5d} KB  {Image.open(p).size}")
