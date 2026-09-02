# BBQ Analytics - Frontend Style Guide

## Design System Overview

This style guide ensures consistent, professional, and accessible user interfaces across the BBQ Analytics platform.

---

## Color System

### Brand Colors

| Color | Hex | RGB | Usage | Variants |
|-------|-----|-----|-------|----------|
| **Primary** | `#D84C1A` | `216, 76, 26` | Buttons, links, accents | Light: `#E8703B`, Dark: `#B63A0F` |
| **Secondary** | `#2C3E50` | `44, 62, 80` | Sidebar, secondary text | - |
| **Success** | `#27AE60` | `39, 174, 96` | Growth, positive metrics | Light: `#52C77A` |
| **Warning** | `#F39C12` | `243, 156, 18` | Alerts, caution | Light: `#F8B739` |
| **Error** | `#E74C3C` | `231, 76, 60` | Errors, critical alerts | Light: `#EC7063` |
| **Info** | `#3498DB` | `52, 152, 219` | Information, neutral | Light: `#5DADE2` |

### Neutral Palette (Light Theme)

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| **Background Primary** | `#F8F6F2` | `248, 246, 242` | Page background |
| **Background Secondary** | `#FFFFFF` | `255, 255, 255` | Cards, modals |
| **Text Primary** | `#1A1A1A` | `26, 26, 26` | Body text, headings |
| **Text Secondary** | `#5C5C5C` | `92, 92, 92` | Labels, metadata |
| **Text Tertiary** | `#8B8B8B` | `139, 139, 139` | Disabled, hints |
| **Border** | `#E8E6E2` | `232, 230, 226` | Borders, dividers |
| **Divider** | `#E0DDD8` | `224, 221, 216` | Subtle separators |

### Neutral Palette (Dark Theme)

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| **Background Primary** | `#0F1419` | `15, 20, 25` | Page background |
| **Background Secondary** | `#1A1F2E` | `26, 31, 46` | Cards, modals |
| **Text Primary** | `#F5F5F5` | `245, 245, 245` | Body text, headings |
| **Text Secondary** | `#B8B8B8` | `184, 184, 184` | Labels, metadata |
| **Text Tertiary** | `#7A7A7A` | `122, 122, 122` | Disabled, hints |
| **Border** | `#2A2F3E` | `42, 47, 62` | Borders, dividers |
| **Divider** | `#242B3B` | `36, 43, 59` | Subtle separators |

### Color Usage Rules

1. **Primary Color (#D84C1A)**
   - Primary buttons
   - Active navigation
   - Links
   - Focus states
   - Key highlights

2. **Secondary Color (#2C3E50)**
   - Sidebar background
   - Secondary text
   - Borders (subtle)
   - Shadows

3. **Semantic Colors**
   - Success: Revenue growth, positive changes
   - Warning: Alerts, cautions, deviations
   - Error: Errors, critical issues
   - Info: General information, notifications

4. **Never Mix Themes**
   - Use CSS variables, never hardcoded colors
   - Colors adjust automatically for dark mode
   - Always define colors in `:root` and `@media` blocks

---

## Typography

### Font Stack

```css
/* Display - Headlines */
font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
font-weight: 700; /* Bold for headings */

/* Body - Default */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
font-weight: 400-600; /* Regular or semibold */

/* Mono - Data */
font-family: 'IBM Plex Mono', 'Monaco', monospace;
font-weight: 400-600; /* Regular or semibold */
```

### Type Scale

```
xs:   0.75rem  (12px)  - Captions, badges
sm:   0.875rem (14px)  - Labels, small text
base: 1rem     (16px)  - Body text
lg:   1.125rem (18px)  - Subheadings
xl:   1.25rem  (20px)  - Section headers
2xl:  1.5rem   (24px)  - Page titles
3xl:  1.875rem (30px)  - Major headings
4xl:  2.25rem  (36px)  - Hero text
```

### Font Weights

```
400 - Regular  (Body text, default UI)
500 - Medium   (Labels, emphasis)
600 - Semibold (Strong emphasis, labels)
700 - Bold     (Headings, highlights)
```

### Line Heights

```
tight:   1.25  (Headings, compact)
normal:  1.5   (Body text, default)
relaxed: 1.75  (Long-form, accessibility)
```

### Typography Examples

#### Heading (H1)
```css
font-family: 'Poppins', sans-serif;
font-size: 2.25rem;
font-weight: 700;
line-height: 1.25;
letter-spacing: -0.02em;
```

#### Subheading (H3)
```css
font-family: 'Poppins', sans-serif;
font-size: 1.5rem;
font-weight: 700;
line-height: 1.25;
```

#### Body Text
```css
font-family: 'Inter', sans-serif;
font-size: 1rem;
font-weight: 400;
line-height: 1.5;
```

#### Data/Metrics
```css
font-family: 'IBM Plex Mono', monospace;
font-size: 1.75rem;
font-weight: 700;
letter-spacing: -0.02em;
```

---

## Spacing Scale

```
xs:   0.25rem  (4px)   - Tiny gaps
sm:   0.5rem   (8px)   - Small gaps
md:   1rem     (16px)  - Standard spacing
lg:   1.5rem   (24px)  - Large spacing
xl:   2rem     (32px)  - Extra large
2xl:  3rem     (48px)  - Section spacing
3xl:  4rem     (64px)  - Major sections
4xl:  6rem     (96px)  - Hero sections
```

### Spacing Rules

- **Never use arbitrary spacing** - Always use scale values
- **Consistent padding** - Use same scale inside components
- **Consistent margins** - Use same scale between components
- **Horizontal symmetry** - Match left/right padding
- **Vertical rhythm** - Stack elements on scale

### Spacing Examples

```css
/* Button padding */
padding: var(--spacing-md) var(--spacing-lg);  /* Vertical, Horizontal */

/* Card padding */
padding: var(--spacing-lg);

/* Section gap */
gap: var(--spacing-xl);

/* Margin between sections */
margin-top: var(--spacing-3xl);
```

---

## Border Radius

```
sm:   4px    - Subtle rounding
md:   6px    - Standard (buttons, inputs)
lg:   8px    - Cards, modals
xl:   12px   - Large containers
2xl:  16px   - Extra large components
full: 9999px - Circular (avatars)
```

### Usage

```css
/* Button radius */
border-radius: var(--radius-md);

/* Card radius */
border-radius: var(--radius-lg);

/* Avatar radius */
border-radius: var(--radius-full);
```

---

## Shadows

```
xs:   0 1px 1px 0 rgba(0, 0, 0, 0.03)      - Minimal
sm:   0 1px 2px 0 rgba(0, 0, 0, 0.05)      - Subtle
md:   0 4px 6px -1px rgba(0, 0, 0, 0.1)    - Standard
lg:   0 10px 15px -3px rgba(0, 0, 0, 0.1)  - Elevated
xl:   0 20px 25px -5px rgba(0, 0, 0, 0.1)  - Modal/Dropdown
2xl:  0 25px 50px -12px rgba(0, 0, 0, 0.25) - Overlay
```

### Shadow Rules

- **Base state** - Use `--shadow-sm` or none
- **Hover state** - Elevate to `--shadow-md`
- **Active state** - Back to `--shadow-sm`
- **Modals/Dropdowns** - Use `--shadow-xl` or `--shadow-2xl`

---

## Transitions

```
fast:  150ms cubic-bezier(0.4, 0, 0.2, 1)  - Micro-interactions
base:  250ms cubic-bezier(0.4, 0, 0.2, 1)  - Standard
slow:  350ms cubic-bezier(0.4, 0, 0.2, 1)  - Page transitions
```

### Usage

```css
/* Hover effects */
transition: all var(--transition-base);

/* State changes */
transition: background-color var(--transition-fast);

/* Page navigation */
transition: opacity var(--transition-slow);
```

### Easing Function

The easing `cubic-bezier(0.4, 0, 0.2, 1)` creates smooth, professional animations. This is the Material Design standard (Ease In Out Cubic).

---

## Components

### Button Styles

#### Primary Button
```css
background-color: var(--color-primary);
color: white;
padding: 0.875rem 1.5rem;
border-radius: var(--radius-md);
font-weight: 600;
box-shadow: 0 2px 8px rgba(216, 76, 26, 0.3);
```

**Hover:**
```css
background-color: var(--color-primary-light);
box-shadow: 0 4px 12px rgba(216, 76, 26, 0.4);
transform: translateY(-2px);
```

#### Secondary Button
```css
background-color: transparent;
color: var(--color-primary);
border: 2px solid var(--color-primary);
padding: 0.75rem 1.5rem;
```

**Hover:**
```css
background-color: rgba(216, 76, 26, 0.05);
border-color: var(--color-primary-light);
```

### Input Fields

```css
padding: 0.75rem 1rem;
border: 1px solid var(--color-border);
border-radius: var(--radius-md);
font-family: var(--font-body);
font-size: 1rem;
color: var(--color-text-primary);
background-color: var(--color-bg-secondary);
transition: all var(--transition-base);
```

**Focus:**
```css
border-color: var(--color-primary);
box-shadow: 0 0 0 3px rgba(216, 76, 26, 0.1);
outline: none;
```

### Cards

```css
background-color: var(--color-bg-secondary);
border: 1px solid var(--color-border);
border-radius: var(--radius-lg);
padding: 1.5rem;
box-shadow: var(--shadow-sm);
transition: all var(--transition-base);
```

**Hover:**
```css
box-shadow: var(--shadow-md);
transform: translateY(-2px);
border-color: var(--color-primary);
```

---

## Responsive Design

### Breakpoints

```
Mobile:  < 480px   (phones)
Tablet:  480px     (tablets, landscape)
Desktop: 768px     (desktops, large tablets)
Wide:    1024px    (large desktops)
Ultra:   1280px+   (ultra-wide displays)
```

### Mobile-First Approach

```css
/* Mobile (default) */
.component {
  font-size: 1rem;
  padding: 1rem;
  grid-template-columns: 1fr;
}

/* Tablet and up (480px) */
@media (min-width: 480px) {
  .component {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop and up (768px) */
@media (min-width: 768px) {
  .component {
    font-size: 1.125rem;
    padding: 1.5rem;
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Large desktop (1024px) */
@media (min-width: 1024px) {
  .component {
    padding: 2rem;
    grid-template-columns: repeat(4, 1fr);
  }
}
```

---

## Dark Mode

### Implementation

```css
/* Light theme (default) */
:root {
  --color-bg-primary: #F8F6F2;
  --color-text-primary: #1A1A1A;
}

/* Dark theme (system preference) */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-bg-primary: #0F1419;
    --color-text-primary: #F5F5F5;
  }
}

/* Dark theme (explicit) */
:root[data-theme="dark"] {
  --color-bg-primary: #0F1419;
  --color-text-primary: #F5F5F5;
}
```

### Dark Mode Best Practices

1. **Always use variables** - Never hardcode colors
2. **Test both themes** - Verify contrast and readability
3. **Adjust shadows** - Darker backgrounds need different shadows
4. **Consider saturation** - Reduce saturation in dark mode for comfort
5. **Respect preferences** - Honor `prefers-color-scheme`

---

## Accessibility

### Color Contrast

```
WCAG AA (minimum): 4.5:1 for text
WCAG AAA (enhanced): 7:1 for text
UI Components: 3:1 for non-text
```

### Text Sizing

```
Never use font-size < 12px
Line height >= 1.5 for body text
Line length 50-75 characters (optimal reading)
```

### Focus States

```css
*:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

### Interactive Elements

```css
/* Buttons should be >= 44x44px (touch target) */
min-height: 44px;
min-width: 44px;

/* Links should have underline or background */
text-decoration: underline;
```

---

## Code Examples

### Login Page Header

```jsx
<div className="login-header">
  <div className="login-logo">
    <Flame size={28} className="logo-icon" />
    <span className="logo-text">BBQ Analytics</span>
  </div>
  <p className="login-subtitle">Intelligent Restaurant Analytics</p>
</div>
```

### KPI Card

```jsx
<div className="kpi-card">
  <div className="kpi-header">
    <span className="kpi-icon">💰</span>
    <span className="kpi-change up">
      <TrendingUp size={16} />
      +12.5%
    </span>
  </div>
  <p className="kpi-label">Total Revenue</p>
  <p className="kpi-value">₨42,600</p>
</div>
```

### Button Variants

```jsx
{/* Primary */}
<button className="login-button">Sign In</button>

{/* Secondary */}
<button className="demo-button">Try Demo</button>

{/* Icon Button */}
<button className="icon-button">
  <Bell size={20} />
</button>
```

---

## Design Tokens Reference

### CSS Variable Categories

```css
/* Color tokens */
--color-primary
--color-secondary
--color-success
--color-warning
--color-error
--color-info
--color-bg-primary
--color-bg-secondary
--color-text-primary
--color-text-secondary
--color-text-tertiary
--color-border
--color-divider

/* Typography tokens */
--font-display
--font-body
--font-mono
--text-xs through --text-4xl
--leading-tight
--leading-normal
--leading-relaxed

/* Spacing tokens */
--spacing-xs through --spacing-4xl

/* Border radius tokens */
--radius-sm through --radius-full

/* Shadow tokens */
--shadow-xs through --shadow-2xl

/* Transition tokens */
--transition-fast
--transition-base
--transition-slow

/* Dimension tokens */
--header-height
--sidebar-width
```

---

## Testing the Design System

### Checklist

- [ ] Colors work in light mode
- [ ] Colors work in dark mode
- [ ] Contrast ratios meet WCAG AA
- [ ] Buttons are >= 44x44px
- [ ] Focus states visible on all interactive elements
- [ ] Animations respect `prefers-reduced-motion`
- [ ] Responsive at all breakpoints
- [ ] Works with screen readers
- [ ] Keyboard navigation works
- [ ] Touch targets adequate on mobile

---

## Maintenance

### Updating Design System

1. **Color changes** - Update `:root` and media queries
2. **Typography changes** - Update type scale and font families
3. **Spacing changes** - Update `--spacing-*` variables
4. **New component** - Add to COMPONENTS.md

### Versioning

Current version: **1.0.0**
- Established design system
- Enterprise color palette
- Complete component library
- Dark mode support
- WCAG AA compliance

---

**This style guide ensures visual consistency, accessibility, and professional quality across the BBQ Analytics platform.**
