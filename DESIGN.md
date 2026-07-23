---
name: Indigo Utility
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#464555'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#777587'
  outline-variant: '#c7c4d8'
  surface-tint: '#4d44e3'
  primary: '#3525cd'
  on-primary: '#ffffff'
  primary-container: '#4f46e5'
  on-primary-container: '#dad7ff'
  inverse-primary: '#c3c0ff'
  secondary: '#505f76'
  on-secondary: '#ffffff'
  secondary-container: '#d0e1fb'
  on-secondary-container: '#54647a'
  tertiary: '#7e3000'
  on-tertiary: '#ffffff'
  tertiary-container: '#a44100'
  on-tertiary-container: '#ffd2be'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e2dfff'
  primary-fixed-dim: '#c3c0ff'
  on-primary-fixed: '#0f0069'
  on-primary-fixed-variant: '#3323cc'
  secondary-fixed: '#d3e4fe'
  secondary-fixed-dim: '#b7c8e1'
  on-secondary-fixed: '#0b1c30'
  on-secondary-fixed-variant: '#38485d'
  tertiary-fixed: '#ffdbcc'
  tertiary-fixed-dim: '#ffb695'
  on-tertiary-fixed: '#351000'
  on-tertiary-fixed-variant: '#7b2f00'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  display-hero:
    fontFamily: Hanken Grotesk
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  code-sm:
    fontFamily: Geist
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
  label-caps:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1280px
  gutter: 1.5rem
  section-gap: 2rem
  stack-sm: 0.5rem
  stack-md: 1rem
  page-margin-mobile: 1rem
  page-margin-desktop: 2.5rem
---

## Brand & Style
The design system is centered on a "developer-friendly utility" aesthetic. It prioritizes clarity, precision, and logical structure to facilitate efficient CRUD operations. The brand personality is professional, reliable, and modern, aiming to evoke a sense of organized control for technical users. 

The style utilizes a **Corporate / Modern** approach with high-performance utility influences. It leans into a clean, systematic interface where whitespace is used to separate concerns rather than just for decoration. Visual noise is minimized to ensure that data entry and system status remain the primary focus.

## Colors
The palette is dominated by **Deep Indigo (#4F46E5)** for primary actions and system-critical focus states. This is balanced against a **Soft Slate (#F8FAFC)** background to reduce eye strain during prolonged use. 

- **Primary:** Used for the main "Create" button, active navigation, and primary form focus.
- **Secondary:** Slate-600 is used for secondary metadata and icons to maintain a neutral hierarchy.
- **Surface:** Pure white is reserved for high-priority containers like the CRUD table and modal forms.
- **Status:** Standard semantic colors should be used for success (Emerald), warning (Amber), and error (Rose) states, tinted slightly to match the saturation of the Indigo primary.

## Typography
This design system employs **Hanken Grotesk** for its clean, contemporary feel and excellent legibility in density-heavy interfaces. To reinforce the "developer-friendly" aspect, **Geist** is used for labels, metadata, and technical information like IP addresses.

- **Hero Section:** Uses `display-hero` for the greeting to establish immediate context.
- **Data Tables:** Column headers use `label-caps` in a medium slate color to distinguish structure from data. Cell content uses `body-sm`.
- **Footer:** IP info and versioning use `code-sm` to signify technical/system-generated data.

## Layout & Spacing
The layout follows a **Fixed Grid** approach for the central content area to maintain readability of data rows, centered within a fluid viewport. 

- **Hero Section:** Spans the full width of the container, providing high-contrast padding (3rem vertical) to separate the greeting from the operational area.
- **Data Table:** Uses a 12-column internal grid. Name spans 5 columns, Gender 2, Age 2, and Actions 3.
- **Responsive Behavior:** On mobile, the 12-column grid collapses to a single column stack. The table transforms into a "card list" view where each CRUD entry is its own white surface.
- **Footer:** Anchored to the bottom of the viewport or content (whichever is taller), featuring a horizontal flex layout for IP metadata.

## Elevation & Depth
The design system uses **Tonal Layers** and **Low-Contrast Outlines** to create depth without relying on heavy shadows, maintaining a "flat-plus" utility look.

- **Level 0 (Background):** Soft Slate (#F8FAFC) - the base canvas.
- **Level 1 (Cards/Table):** White (#FFFFFF) with a 1px solid border (#E2E8F0). This is the primary interactive surface.
- **Level 2 (Dropdowns/Modals):** White with a subtle ambient shadow (0px 4px 12px rgba(0, 0, 0, 0.05)) to indicate temporary overlay.
- **Interaction:** Hovering over a table row should trigger a slight tonal shift (Slate-50) rather than a shadow change.

## Shapes
A **Rounded** (0.5rem) language is applied across the system to soften the technical nature of the CRUD application, making it feel more like a modern SaaS product.

- **Buttons & Inputs:** 0.5rem (8px) radius.
- **Cards & Data Tables:** 0.75rem (12px) for the outer container to create a distinct framing effect.
- **Tags/Chips:** 1rem (Pill-shaped) for gender indicators or status badges to provide a visual break from the linear table structure.

## Components
- **Buttons:** Primary buttons use a solid Indigo background with white text. Secondary/Ghost buttons use a Slate-100 background or just a Slate-200 border.
- **CRUD Table:** Features a sticky header with a subtle bottom border. Rows have a 48px minimum height for touch-target accessibility.
- **Input Fields:** Use a 1px Slate-200 border that transitions to 2px Indigo on focus. Labels sit 4px above the input.
- **Action Icons:** Use minimalist line icons (20px) for Edit/Delete actions, using Slate-400 as a default and shifting to Indigo (Edit) or Rose (Delete) on hover.
- **Hero Card:** A distinct container with a subtle gradient (Indigo-600 to Indigo-700) or a clean white background with a thick 4px Indigo left-border to denote its importance.
- **Footer Metadata:** Small badges or plain text using the `code-sm` typography, separated by vertical dividers.