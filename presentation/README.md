# Defense presentation (pt-BR)

HTML slide deck for the master's defense. Open `index.html` in a browser; it has no build step or external dependencies.

| Key | Action |
|---|---|
| → / Space / ← | Next / previous step |
| Shift + → / ← | Next / previous slide |
| `S` | Presenter window (notes, timer, next slide) |
| `N` | Notes overlay |
| `O` | Slide index |
| `F` | Fullscreen |
| `<n>` + Enter | Go to slide *n* |

A slide and step can be linked directly: `index.html#/19/3`.

## Structure

- 36 main slides (about 32 min of planned time, set per slide in `data-time`) plus 9 backup slides (A–I) after "Obrigado!".
- Speaker notes are in each slide's `<aside class="notes">`.
- `style.css` holds the shared styles; slide-specific rules are in the `<style>` block of `index.html`.
- `deck.js` is the slide engine (fragments `.f` with `data-f`, presenter sync via `BroadcastChannel`).

## Figures

- `assets/fig_04_*`, `fig_07_*`, `fig_09_*`: Portuguese versions of the Evaluation figures (Chapter 6).
- `assets/fig_11_densidade_atraso_vo.{png,svg}`: Voice alert-age density (the dissertation's `fig:eval:vo_density`) with pt-BR labels and the deck colours. Regenerate with `scripts/plot_vo_delay_density_slides.py` from the per-packet samples that `scripts/extract_vo_delay_vec.py` extracts from the `.vec` traces:

  ```bash
  python scripts/extract_vo_delay_vec.py vo_delays.npz <veins_inet_highway_heavy/results>
  python scripts/plot_vo_delay_density_slides.py vo_delays.npz presentation/assets/fig_11_densidade_atraso_vo
  ```

  Requires `numpy`, `scipy`, and `matplotlib`.

## Numbers on the slides

Every number on the slides comes from the dissertation (Chapter 6 tables and text) or from the hotspot `.sca` scalars of the same runs. The hotspot channel-grant shares (DCF 100 %, EDCA/stable/guarded 78 %, emergency 61 %) and the share of the crash node's BE dropped by emergency (≈ 42 %) are three-seed averages of `channelAccessGranted:count` on `edcaf[1]` (or the DCF channel access for `plain`) and `beDroppedWhileBlockedCount`.
