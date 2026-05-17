# Beverly Xu — Portfolio

A personal portfolio hosted on GitHub Pages.

## Structure

```
beverly-portfolio/
├── index.html              # Main page (hero)
├── pages/
│   ├── about.html          # About me
│   ├── projects.html       # Projects (desktop icon grid)
│   ├── research.html       # Research (expandable cards)
│   └── 404.html            # 404 error page
├── css/
│   └── style.css           # All styles + design system
├── js/
│   └── main.js             # Cursor, animations, modals, etc.
└── assets/
    └── resume.pdf          # Your resume (add this!)
```

## Setup

1. **Add your photo**  
   Replace the `PLACEHOLDER` divs in `index.html` and `pages/about.html` with:
   ```html
   <img src="assets/your-photo.jpg" alt="Beverly Xu" />
   ```
   Put your photos in the `assets/` folder.

2. **Add your resume PDF**  
   Drop your resume at `assets/resume.pdf`. The nav "resume ↗" link points there.

3. **Fill in PLACEHOLDER text**  
   - `pages/about.html` — bio blocks 01, 02, 04, and fun facts
   - `pages/research.html` — RoboLand lab details (problem statement, professor name, etc.)
   - The mosaic photo placeholders in `pages/about.html`

4. **Enable GitHub Pages**  
   - Push this folder to a GitHub repo
   - Go to Settings → Pages → Source: Deploy from branch → `main` → `/ (root)`
   - Your site will be live at `https://<username>.github.io/<repo-name>/`

5. **Custom 404**  
   GitHub Pages automatically serves `404.html` — no extra config needed as long as it's at the root. If it's in `/pages/`, add this to your repo root:
   ```
   # in root 404.html
   ```
   Or move `pages/404.html` to the root level.

## Color Palette

| Name     | Hex       | Usage                     |
|----------|-----------|---------------------------|
| Lavender | `#C8C8E9` | About page BG, accents    |
| Sage     | `#D8E8C3` | Research page BG, tags    |
| Cream    | `#E8E8CC` | Projects page BG, tags    |

## Customization

- **Fonts**: Syne (UI) + DM Serif Display (headings) + IBM Plex Mono (code/labels)  
  All loaded from Google Fonts — no install needed.

- **Dark mode**: Toggle button in navbar. Persists to `localStorage`.

- **Adding projects**: In `pages/projects.html`, duplicate a `.project-icon` div and update the `data-project` JSON attribute with your project details.

- **Adding research**: In `pages/research.html`, duplicate a `.research-item` block.

## Design Notes

- Custom pixel cursor (CSS + JS blend-mode trick)
- Orbiting leaf on the projects page follows scroll position
- WiFi disconnect toast triggers on `window offline` event (+ 8s demo on homepage)
- All project cards open in a modal overlay
- Research cards use a CSS accordion (no JS library needed)
- Scroll-reveal animations via IntersectionObserver
- Retro desktop OS window chrome on projects page
