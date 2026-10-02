# eCourts interface assets

197 original symbols, each supplied as static and animated SVG in light, dark and mono variants. The existing eCourts app icon, logo, launch animation and loading animation are outside this package and remain unchanged.

Download [the preview](index.html) and open it in a browser, or serve it from an HTML-capable host. The preview embeds every SVG and the complete mapping, so the one file works offline. It includes a searchable catalog, four surface comparisons, 16–48 px sizing, reduced-motion behavior and the source inventory. GitHub's file viewer and some CDNs serve HTML as source instead of rendering it; downloading and opening this file works without a server.

## Scope and coverage

The source snapshots are immutable:

| App branch | Audited commit |
| --- | --- |
| `main` | `6a1f600624981355b519fd83a1908637d25afc7c` |
| `liquid-glass-ui` | `b89473c58878765ac7a139826d6589af104cb07c` |

All 144 main-source Kotlin, Java and XML files across the two trees were reviewed. [inventory.csv](inventory.csv) maps individual icon uses, drawable resources, state graphics, data-driven identifiers and all 140 profile-picker choices in each branch. [inventory.json](inventory.json) also records wrapper/data-flow locations, file blob IDs and exclusions. Renderer definitions that are not currently used are labelled `declared-symbol`; text-only features and statuses are labelled separately, so they are not misrepresented as existing icon controls.

The geometry is newly authored in [tools/artwork.py](tools/artwork.py). Existing application paths and its Lucide-derived profile drawings were not imported. The approved CDN branding supplies the warm coral/peach treatment, controlled curves and settled component motion. Interface silhouettes are drawn on their own 24-unit grid, not reduced versions of the app logo.

No changes were made to either app branch, application logic, workflows, APK configuration or saved-data formats.

## Files and CDN addresses

| Purpose | Relative path |
| --- | --- |
| Light static | `static/light/{id}.svg` |
| Dark static | `static/dark/{id}.svg` |
| Tintable static | `static/mono/{id}.svg` |
| Animated | `animated/{light,dark,mono}/{id}.svg` |
| Android static | `android/res/drawable/ecui_{id_with_underscores}.xml` |
| Android mono | `android/res/drawable/ecui_{id_with_underscores}_mono.xml` |
| Android animated | `android/res/drawable/ecui_{id_with_underscores}_animated.xml` |

`catalog.json` is the complete machine-readable catalog, including motion descriptions, durations, aliases and paths. Alias entries are mappings, not duplicated files. For example, the stored profile name `landmark` resolves to `courthouse.svg`; there is no `landmark.svg`. Normalize underscores to hyphens before looking up an old `MIcon` name.

The public CDN URL pattern is:

```text
https://cdn.jsdelivr.net/gh/WikioApps/cdn@{revision}/ecourts/interface/static/dark/courthouse.svg
```

Replace `{revision}` with the published asset commit for production. `@main` is a mutable convenience URL and can remain cached after an update. [url-status.json](url-status.json) distinguishes checked URLs from proposed patterns and gives the verified revision when available. A local file or successful GitHub commit alone is not proof that a CDN URL is serving it. The app source links in the inventory may require access to the app repository.

## Size and theme treatment

- The viewBox is `0 0 24 24`, with a 1.65-unit primary stroke. The active interface uses roughly 15–24 dp symbols; empty states use larger versions of the same geometry. Use 20–24 dp where possible and keep small, densely detailed profile symbols at 24 dp or above. The gallery includes 16 px to expose the tradeoff.
- Backgrounds are transparent. Light assets use dark wine outlines and deeper coral accents; dark assets use warm light outlines and peach accents. The outline carries recognition; the translucent fill is only a finishing layer.
- Glass assets use the appropriate light or dark variant. Choose by the final frosted surface under the icon, not by an arbitrary wallpaper colour. Give icons a stable, sufficiently opaque local surface when the content behind the glass is highly variable. Avoid adding glow or drop shadows to small icons.
- Do not put the full app icon in action buttons. The separate `courthouse`, `court-order`, `fir-search`, `clipboard` and `briefcase` concepts have different jobs.
- Disabled, selected and destructive colours remain state-driven in the app; apply its tokens to mono geometry rather than multiplying files for every colour. Keep control hit areas at least as large as the current app's controls. Icon dimensions do not define touch-target dimensions.

## SVG rendering

The SVGs contain paths, a small internal gradient and, in animated files, CSS keyframes. They have no scripts, raster images, fonts, filters or external resources. Static SVGs have complete standalone colour attributes, so a renderer that ignores CSS still has a usable drawing.

```html
<button aria-label="Download court order">
  <img src="/ecourts/interface/static/light/download.svg"
       width="24" height="24" alt="">
</button>
```

Inline SVG supports these optional CSS properties:

```css
.court-icon {
  --ec-icon-ink: #482f36;
  --ec-icon-accent: #e9543e;
  --ec-icon-accent-end: #c93639;
  --ec-icon-soft: #e9543e;
  --ec-icon-surface: #fff4ed;
}
```

Inline mono assets inherit `currentColor`. An external SVG loaded through `<img>` does **not** inherit the parent document's colour variables or `currentColor`. Use the explicit light/dark files, or use a static mono file as a CSS mask:

```css
.court-symbol {
  width: 24px;
  height: 24px;
  background: currentColor;
  mask: url('/ecourts/interface/static/mono/courthouse.svg') center / contain no-repeat;
  -webkit-mask: url('/ecourts/interface/static/mono/courthouse.svg') center / contain no-repeat;
}
```

The mono export keeps secondary surface details at reduced opacity; it does not introduce a second hue. When injecting multiple copies inline, namespace IDs and keyframe selectors per instance if you need different palettes or independent animation control. A separate external SVG document per `<img>` already isolates its IDs.

## Motion behavior

Action and profile animations run once for 800 ms, then return to the static geometry. A part moves around an appropriate hinge or along a constrained track; the whole icon does not spin. Some symbols reveal their functional stroke, such as a check, route or document text. Only `loading` and `progress` use a 1,200 ms loop. Start these only during active work, and stop them on completion or when the view leaves the screen.

SVG animation is enabled inside `@media (prefers-reduced-motion: no-preference)`. Reduced-motion users see the final static state immediately. A renderer without animation support also sees the complete static state. Keep the explicit `static/` files available for predictable native and server-side rendering.

For the app's own motion-off setting in a web surface, select the static file even if the operating system allows motion. For browser replay, replace the image instance or remount a namespaced inline SVG. The gallery's Replay button starts a fresh image document. It does not persistently animate every button on a live app screen.

## Android integration

Both audited branches are native Android interfaces. `MIcon` and `ProfileGlyph` currently draw paths in a Compose Canvas; the PDF viewer uses drawable resources. These supplied assets are for a future integration. An SVG loader such as a static image decoder must not be assumed to run the CSS animation.

Copy the scoped `android/res/` resources into the new app. Names use the `ecui_` prefix to avoid collisions with the existing branding resources. The files use platform VectorDrawable and AnimatedVectorDrawable geometry, with `values/` and `values-night/` colours. Their format is intended for the app's existing API 24 minimum.

For Compose, use a static mono vector with the app's current content colour when appropriate:

```kotlin
Icon(
    painter = painterResource(R.drawable.ecui_download_mono),
    contentDescription = "Download court order",
    tint = LocalContentColor.current,
    modifier = Modifier.size(24.dp)
)
```

Use `Image` with `painterResource` for a coloured static drawable, or use `Icon` with `tint = Color.Unspecified` to preserve its palette. Day/night resource selection follows the Android `Configuration`. If the app's custom appearance preference only changes Compose colours, also provide an appropriately themed resource context, or use the mono drawable with an explicit app tint. Do not assume a Compose theme switch changes Android resource qualifiers automatically.

For a View-based action, select motion or static resources explicitly:

```kotlin
// motionAllowed must combine the app preference and system animator setting.
imageView.setImageResource(
    if (motionAllowed) R.drawable.ecui_download_animated
    else R.drawable.ecui_download
)
if (motionAllowed) {
    (imageView.drawable as? android.graphics.drawable.Animatable)?.start()
}
```

Use the Compose animated-vector integration appropriate to the app's dependency version, or host an ImageView through `AndroidView`. A static `painterResource` does not play an AnimatedVectorDrawable. Stop active drawables when their owning screen is disposed. When disabling motion during playback, stop the drawable and replace it with its static resource; stopping alone can leave an intermediate frame. Use `ecui_notification_fetch_mono` for a monochrome notification symbol; Android controls its notification tint.

The SVG and Android exports share geometry, timing, pivots and component intentions. Their renderers differ: SVG dash reveal operates on SVG subpaths, while Android trim operates on path length. Minor antialiasing and stroke-reveal differences are possible. Resource compilation has been checked, but no APK build, emulator or physical-device playback is claimed. Check static and animated rendering in the future app on its supported Android versions before release.

## Mapping and state semantics

Use the occurrence-specific mapping in `inventory.csv`, not only the aliases. The old generic `file` symbol becomes `court-order` for order rows and `fir-document` for FIR documents. Search method `cause` maps to `clipboard`; empty states have their own simplified concepts. Shared chevrons, actions and profile meanings reuse geometry instead of adding duplicate drawings.

Retain stored profile IDs. Resolve them through `catalog.json` aliases at rendering time. The current app uses `briefcase` when the preference is missing and the first profile choice (`scale`, now `scales`) when an unrecognized stored value is present. Existing solid, split, diagonal, striped and gradient profile treatments remain caller-controlled paint styles on the new geometry; they are not separate icon meanings.

Checkbox, radio and switch files illustrate both meaningful states. They are visual layers, not complete input components. Keep the native control's state, accessibility role, label, focus, hit target and interaction logic. Similarly, the progress assets are indeterminate symbols; they do not replace a determinate progress bar's numeric value. Status companions do not replace the existing case status text, legal meaning or colour rules.

The profile symbols do not all belong in navigation. Use them in the profile picker as the audited app does. Keep repeated navigation icons static at rest, animate the acted-on control only, and do not play all list-row animations during scrolling.

## Rebuilding and checks

```sh
python3 tools/audit.py /path/to/read-only-branch-snapshots
python3 tools/build.py
aapt2 compile --dir android/res -o /tmp/ecui-resources.zip
```

The audit expects the two branch directories and their recursive tree responses, as described in `tools/audit.py`. Rebuilding artwork does not require app source if the committed inventory remains unchanged. `validation.json` records the checks performed for this version. The approved branding files are checked separately against the repository baseline.

Rendering references: [Android vector drawables](https://developer.android.com/develop/ui/views/graphics/vector-drawable-resources), [SVG as an image](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image), and [reduced-motion media queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion).
