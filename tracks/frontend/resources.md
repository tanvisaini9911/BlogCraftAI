# Frontend Resources & Tooling

## Toolchain

- **Node.js 20 + pnpm** – package management for frontend tooling.
- **Vite** – lightning-fast asset bundler with HMR.
- **Sass** – design token management and Bootstrap customization.
- **HTMX** – declarative server-driven interactions.
- **Alpine.js** – lightweight interactivity for modals/toasts where HTMX isn't ideal.
- **Playwright** – end-to-end testing framework.
- **Jest + Testing Library** – component/unit testing.
- **axe-core CLI & pa11y** – accessibility auditing tools.
- **Lighthouse CI** – automated performance and accessibility scoring.

## Reference Links

| Topic | Link |
| --- | --- |
| Bootstrap theming | <https://getbootstrap.com/docs/5.3/customize/sass/> |
| HTMX patterns | <https://htmx.org/examples/> |
| Accessible form design | <https://www.w3.org/WAI/tutorials/forms/> |
| Progressive enhancement | <https://developer.mozilla.org/en-US/docs/Glossary/Progressive_enhancement> |
| Service worker basics | <https://developers.google.com/web/fundamentals/primers/service-workers> |
| Lighthouse CI | <https://github.com/GoogleChrome/lighthouse-ci> |

## Performance Budget Template

```json
{
  "metrics": {
    "first-contentful-paint": 1800,
    "largest-contentful-paint": 2200,
    "total-blocking-time": 150,
    "cumulative-layout-shift": 0.08,
    "speed-index": 2100
  }
}
```

## Accessibility Checklist (excerpt)

- [ ] All interactive elements have accessible names and roles.
- [ ] Form fields include `aria-describedby` for error/help text.
- [ ] Color contrast ratios meet WCAG AA (use tooling to verify).
- [ ] Keyboard trap tests executed for modals, dropdowns, off-canvas menus.
- [ ] Focus management on dynamic updates handled via HTMX `hx-trigger` callbacks.
- [ ] Provide skip-to-content link and accessible breadcrumb navigation.

## UI Kit Assets

- Figma community file: **BlogCraftAI UI Library** (components, tokens, icons).
- Icon set: Feather Icons + custom editorial glyphs.
- Illustration pack: Storyset (royalty-free) aligned with brand colors.

## QA Checkpoints

1. **Design QA** – Compare implementation vs. Figma specs using tooling like PixelSnap.
2. **Accessibility QA** – Run axe + manual keyboard testing for each screen.
3. **Performance QA** – Execute Lighthouse and WebPageTest; record metrics in dashboard.
4. **Content QA** – Validate copy, placeholder text, localization tokens.

## Collaboration Spaces

- Slack channel `#frontend-guild` for async updates and design critiques.
- Weekly design/dev sync with recorded demos.
- Shared Notion workspace for component documentation and release notes.

