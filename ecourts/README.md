# eCourts app icons

Ten distinct designs. Each has its own light and dark SVG. Click any preview to open the editable artwork.

All icons use a 1024 × 1024 canvas with a full background for launcher masking. Paths, gradients and named layers stay editable; there are no embedded images, external fonts or scripts.

## Metal, stone and leather

| Design | Light | Dark |
| --- | --- | --- |
| **Balance**<br>Bronze balance with linked suspension chains, engraved metal, enamel pans and a turned pedestal. | [<img src="main/icons/01-balance/light.svg" width="180" alt="Balance, light">](main/icons/01-balance/light.svg)<br>51.1 KiB | [<img src="main/icons/01-balance/dark.svg" width="180" alt="Balance, dark">](main/icons/01-balance/dark.svg)<br>51.0 KiB |
| **Courthouse**<br>A domed courthouse in carved sandstone, with ribbed roof, fluted columns, arched windows and layered steps. | [<img src="main/icons/02-courthouse/light.svg" width="180" alt="Courthouse, light">](main/icons/02-courthouse/light.svg)<br>24.0 KiB | [<img src="main/icons/02-courthouse/dark.svg" width="180" alt="Courthouse, dark">](main/icons/02-courthouse/dark.svg)<br>23.9 KiB |
| **Verdict**<br>Walnut gavel with curved wood grain, machined brass cuffs and a concentric sounding block. | [<img src="main/icons/03-verdict/light.svg" width="180" alt="Verdict, light">](main/icons/03-verdict/light.svg)<br>36.5 KiB | [<img src="main/icons/03-verdict/dark.svg" width="180" alt="Verdict, dark">](main/icons/03-verdict/dark.svg)<br>36.4 KiB |
| **Statute**<br>Burgundy leather law book with foil border, embossed scales, gilt page edges and a silk bookmark. | [<img src="main/icons/04-statute/light.svg" width="180" alt="Statute, light">](main/icons/04-statute/light.svg)<br>130.4 KiB | [<img src="main/icons/04-statute/dark.svg" width="180" alt="Statute, dark">](main/icons/04-statute/dark.svg)<br>130.2 KiB |
| **Counsel seal**<br>Sculpted wax seal with milled bronze rim, guilloche engraving, fountain nib and laurel branches. | [<img src="main/icons/05-counsel-seal/light.svg" width="180" alt="Counsel seal, light">](main/icons/05-counsel-seal/light.svg)<br>112.7 KiB | [<img src="main/icons/05-counsel-seal/dark.svg" width="180" alt="Counsel seal, dark">](main/icons/05-counsel-seal/dark.svg)<br>112.7 KiB |

## Glass

| Design | Light | Dark |
| --- | --- | --- |
| **Court shield**<br>Faceted optical-glass shield with refracted edges, a divided glass face and a raised silver court column. | [<img src="liquid-glass/icons/01-court-shield/light.svg" width="180" alt="Court shield, light">](liquid-glass/icons/01-court-shield/light.svg)<br>17.6 KiB | [<img src="liquid-glass/icons/01-court-shield/dark.svg" width="180" alt="Court shield, dark">](liquid-glass/icons/01-court-shield/dark.svg)<br>17.5 KiB |
| **Case docket**<br>Layered glass case folders with folded documents, recessed index plaque and polished folder lip. | [<img src="liquid-glass/icons/02-case-docket/light.svg" width="180" alt="Case docket, light">](liquid-glass/icons/02-case-docket/light.svg)<br>13.2 KiB | [<img src="liquid-glass/icons/02-case-docket/dark.svg" width="180" alt="Case docket, dark">](liquid-glass/icons/02-case-docket/dark.svg)<br>13.2 KiB |
| **Hearing day**<br>Lavender glass hearing calendar with steel binder rings, selected date and an inset precision clock. | [<img src="liquid-glass/icons/03-hearing-day/light.svg" width="180" alt="Hearing day, light">](liquid-glass/icons/03-hearing-day/light.svg)<br>19.4 KiB | [<img src="liquid-glass/icons/03-hearing-day/dark.svg" width="180" alt="Hearing day, dark">](liquid-glass/icons/03-hearing-day/dark.svg)<br>19.3 KiB |
| **Ionic column**<br>Carved jade-glass Ionic column with spiral volutes, egg-and-dart capital, eleven flutes and a stepped plinth. | [<img src="liquid-glass/icons/04-ionic-column/light.svg" width="180" alt="Ionic column, light">](liquid-glass/icons/04-ionic-column/light.svg)<br>24.6 KiB | [<img src="liquid-glass/icons/04-ionic-column/dark.svg" width="180" alt="Ionic column, dark">](liquid-glass/icons/04-ionic-column/dark.svg)<br>24.6 KiB |
| **Court search**<br>Emerald optical magnifier with a silver courthouse inside the lens, a milled rim and metal-banded handle. | [<img src="liquid-glass/icons/05-court-search/light.svg" width="180" alt="Court search, light">](liquid-glass/icons/05-court-search/light.svg)<br>58.2 KiB | [<img src="liquid-glass/icons/05-court-search/dark.svg" width="180" alt="Court search, dark">](liquid-glass/icons/05-court-search/dark.svg)<br>58.2 KiB |

## Direct SVG links

Use the paths in [manifest.json](manifest.json). For example:

- [Balance, light SVG](https://raw.githubusercontent.com/WikioApps/cdn/main/ecourts/main/icons/01-balance/light.svg)
- [Balance, dark SVG](https://raw.githubusercontent.com/WikioApps/cdn/main/ecourts/main/icons/01-balance/dark.svg)
- [Court shield, light SVG](https://raw.githubusercontent.com/WikioApps/cdn/main/ecourts/liquid-glass/icons/01-court-shield/light.svg)
- [Court shield, dark SVG](https://raw.githubusercontent.com/WikioApps/cdn/main/ecourts/liquid-glass/icons/01-court-shield/dark.svg)

For a pinned CDN URL, replace `main` in a raw URL with the desired commit SHA.

These are SVG source assets, not Android VectorDrawable XML. For a native launcher resource, export the chosen source to the required Android bitmap densities; keep the full square background so the launcher can apply its mask.

Regenerate with `python3 ecourts/source/build_icons.py` from the repository root. The generator uses only the Python standard library.
