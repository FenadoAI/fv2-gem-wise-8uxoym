# Jewellery Store Management System - Design System

## Theme Selection

**CUSTOM LUXURY JEWELLERY THEME**

This design system uses a dual-theme approach optimized for jewellery retail:
- **Public Catalog**: Luxurious gold/amber aesthetic with elegant typography for high-end jewellery presentation
- **Admin Dashboard**: Professional slate/neutral tones for efficient inventory and order management

## Foundations

### Color Tokens

#### Public Catalog Theme (Luxury Mode)
```css
--primary: 43 84% 42% /* Rich Gold - primary actions, jewelry accent */
--secondary: 43 20% 25% /* Deep Bronze - secondary actions */
--accent: 28 84% 55% /* Rose Gold - highlights, special offers */
--background: 40 25% 97% /* Warm Ivory - main background */
--card: 0 0% 100% /* Pure White - product cards */
--foreground: 30 15% 15% /* Rich Charcoal - main text */
--muted: 40 15% 92% /* Soft Cream - disabled states */
--border: 40 15% 85% /* Light Gold Border */
--ring: 43 84% 42% /* Gold Focus Ring */
```

#### Admin Dashboard Theme (Professional Mode)
```css
--primary: 215 84% 42% /* Professional Blue - primary actions */
--secondary: 215 20% 30% /* Deep Slate - secondary actions */
--accent: 215 50% 55% /* Sky Blue - data highlights */
--background: 220 15% 97% /* Cool Gray - main background */
--card: 0 0% 100% /* Pure White - data cards */
--foreground: 220 20% 15% /* Dark Slate - main text */
--muted: 220 15% 90% /* Light Gray - disabled states */
--border: 220 15% 82% /* Slate Border */
--ring: 215 84% 42% /* Blue Focus Ring */
```

#### Dark Mode Colors (Both Themes)
```css
/* Luxury Dark */
--background: 40 15% 9% /* Deep Brown-Black */
--card: 40 10% 14% /* Warm Dark Gray */
--foreground: 40 15% 95% /* Warm White */

/* Admin Dark */
--background: 220 15% 9% /* Cool Dark Gray */
--card: 220 10% 14% /* Slate Dark */
--foreground: 220 15% 95% /* Cool White */
```

#### Chart & Data Visualization Colors
```css
--chart-1: 43 84% 55% /* Gold */
--chart-2: 165 65% 45% /* Emerald */
--chart-3: 250 70% 55% /* Amethyst */
--chart-4: 20 80% 50% /* Ruby */
--chart-5: 200 75% 50% /* Sapphire */
```

### Typography Scale

**Primary Font**: 'Playfair Display' (Luxury headings, product names)
**Secondary Font**: 'Inter' (Body text, admin interface, data tables)
**Monospace Font**: 'JetBrains Mono' (SKU, order IDs, inventory codes)

```css
/* Headings - Luxury */
.luxury-h1 { font-family: 'Playfair Display'; font-size: 3rem; font-weight: 700; letter-spacing: -0.02em; }
.luxury-h2 { font-family: 'Playfair Display'; font-size: 2.25rem; font-weight: 600; letter-spacing: -0.01em; }
.luxury-h3 { font-family: 'Playfair Display'; font-size: 1.875rem; font-weight: 600; }

/* Headings - Admin */
.admin-h1 { font-family: 'Inter'; font-size: 2.25rem; font-weight: 700; }
.admin-h2 { font-family: 'Inter'; font-size: 1.875rem; font-weight: 600; }
.admin-h3 { font-family: 'Inter'; font-size: 1.5rem; font-weight: 600; }

/* Body Text */
.text-lg { font-size: 1.125rem; line-height: 1.75rem; }
.text-base { font-size: 1rem; line-height: 1.5rem; }
.text-sm { font-size: 0.875rem; line-height: 1.25rem; }
```

### Spacing & Grid System

**Base Unit**: 4px (0.25rem)
**Scale**: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96px
**Container Max-Width**: 1440px
**Breakpoints**: sm(640px), md(768px), lg(1024px), xl(1280px), 2xl(1536px)

### Iconography

**Library**: Lucide React (already installed)
**Icon Sizes**: 16px (sm), 20px (base), 24px (lg), 32px (xl)
**Key Icons**: Diamond, ShoppingBag, Package, Users, BarChart3, Settings, Eye, Edit, Trash2, Plus, Filter, Search

## Components

### Product Card (Public Catalog)
**Anatomy**: Image container, title, price, category badge, quick-view button
**Variants**: Grid (default), List, Featured (larger, gradient border)
**States**: Default, Hover (scale 1.02, shadow elevation), Loading (skeleton), Out-of-Stock (grayscale overlay)
**Styling**: Rounded corners (12px), subtle shadow, gold border on hover, image aspect ratio 4:5
**Accessibility**: Alt text for images, keyboard navigation, ARIA labels

### Data Table (Admin)
**Anatomy**: Header row, sortable columns, row actions menu, pagination footer
**Variants**: Compact (dense spacing), Default, Comfortable (extra padding)
**States**: Default, Sorting (arrow indicators), Selected (blue background), Loading (shimmer effect)
**Styling**: Zebra striping (subtle), sticky header, row hover (light blue), border between sections
**Accessibility**: Sortable with keyboard, screen reader announcements, focus visible

### Button Component
**Anatomy**: Icon (optional), Label, Loader (replacing content)
**Variants**:
- Primary (solid gold/blue background)
- Secondary (outline with border)
- Ghost (transparent, text only)
- Destructive (red for delete actions)
**States**: Default, Hover (brightness +10%), Active (scale 0.98), Disabled (opacity 50%), Loading (spinner)
**Unique Styling**: Curved edges (border-radius: 24px for large buttons), subtle shadow, gradient on hover for primary
**Accessibility**: Focus ring (3px offset), disabled state clear, loading announced

### Card Component
**Anatomy**: Container, Header (optional), Content area, Footer (optional)
**Variants**: Default, Elevated (larger shadow), Bordered (solid border), Gradient-edge (partial gold borders on corners)
**States**: Default, Hover (slight elevation increase), Selected (gold/blue border)
**Unique Styling**: Only top-right and bottom-left borders visible for "gradient-edge" variant
**Accessibility**: Semantic HTML, proper heading hierarchy

### Form Inputs
**Anatomy**: Label, Input field, Helper text, Error message, Icon (optional)
**Variants**: Text, Number, Select, Textarea, File-upload, Date-picker
**States**: Default, Focus (ring color), Error (red border), Disabled (gray background), Success (green border)
**Styling**: Rounded (8px), clear focus states, floating labels on luxury forms
**Accessibility**: Label association, error announcements, required indicators

### Badge Component
**Anatomy**: Text label, optional icon
**Variants**: Default, Success (green), Warning (amber), Error (red), Info (blue), Custom (jewel-toned)
**Styling**: Small rounded (16px), uppercase text, semibold font, jewel-inspired colors (Emerald, Ruby, Sapphire badges)
**Accessibility**: Sufficient contrast ratios, semantic color meanings

### Navigation (Dual Interface)
**Public**: Horizontal menu, category dropdowns, search bar, cart icon with count badge
**Admin**: Vertical sidebar, collapsible sections by role (Staff/Manager/Owner), quick-action buttons
**States**: Active (gold/blue indicator), Hover, Expanded/Collapsed
**Unique Styling**: Dotted border under active public nav items, sidebar with gradient background in admin
**Accessibility**: Skip links, keyboard navigation, current page announced

### Modal/Dialog
**Anatomy**: Overlay (backdrop), Container, Header (title + close), Content, Footer (actions)
**Variants**: Small (400px), Medium (600px), Large (900px), Fullscreen
**States**: Opening (fade + scale animation), Closing, Scrollable-content
**Styling**: Rounded (16px), subtle shadow, blur backdrop effect
**Accessibility**: Focus trap, ESC to close, ARIA dialog role, return focus on close

### Image Gallery
**Anatomy**: Main display (large), Thumbnail strip (scrollable), Zoom control, Navigation arrows
**Variants**: Single image, Multi-image carousel, Grid gallery
**States**: Default, Zoomed (modal view), Loading (blur-up placeholder)
**Styling**: High-quality image optimization, smooth transitions, elegant controls with gold accents
**Accessibility**: Alt text, keyboard navigation, announced image count

## Patterns

### Product Catalog Browsing
**Flow**: Landing > Category > Product List (filtered) > Product Detail > COD Order Form
**Key Elements**: Filter sidebar (categories, price range, materials), Sort dropdown, Product grid with lazy loading
**Accessibility**: Filter controls keyboard accessible, clear filter applied indicators, loading states announced

### Inventory Management
**Flow**: Admin Dashboard > Inventory List > Add/Edit Item Form > Save Confirmation
**Key Elements**: Search & filter toolbar, bulk actions, inline editing, image upload with preview
**Accessibility**: Table keyboard navigation, form validation messages, success/error announcements

### Order Processing
**Flow**: Order List > Order Detail > Status Update > Print Invoice
**Key Elements**: Status badges, timeline view, customer info card, item list, action buttons
**Accessibility**: Status changes announced, print-friendly styles, keyboard shortcuts

### Role-Based Dashboard
**Flow**: Login > Role Detection > Appropriate Dashboard (Staff/Manager/Owner view)
**Key Elements**: Metric widgets (revenue, orders, inventory alerts), quick-action cards, recent activity feed
**Accessibility**: Widget summaries for screen readers, skip to main content, clear role indicators

## Theming

### Theme Toggle Implementation
```javascript
// Dual theme system
const themes = {
  catalog: 'luxury',
  admin: 'professional'
}

// Apply based on route
if (route.includes('/admin')) {
  document.documentElement.setAttribute('data-theme', 'professional')
} else {
  document.documentElement.setAttribute('data-theme', 'luxury')
}

// Dark mode toggle (works with both themes)
document.documentElement.classList.toggle('dark')
```

### CSS Variable Mapping
All components use CSS custom properties that automatically adapt to active theme and dark mode state.

## Animation & Micro-interactions

**Library**: Framer Motion
**Principles**: Subtle, purposeful, performant (60fps), reduced for motion preferences

### Key Animations
- **Card Hover**: Scale 1.02, shadow elevation, duration 200ms, ease-out
- **Button Click**: Scale 0.98, duration 100ms, spring physics
- **Modal Entry**: Fade + scale from 0.95, backdrop blur increase, duration 300ms
- **List Item Stagger**: Children animate in sequence, 50ms delay between items
- **Image Load**: Blur-up from placeholder, fade-in duration 400ms
- **Toast Notifications**: Slide-in from top-right, auto-dismiss after 5s, swipe-to-dismiss
- **Loading States**: Shimmer effect for skeletons, spinner for buttons, pulse for images
- **Filter Apply**: Smooth height transition for results, fade-out old items, fade-in new items
- **Unique Effects**:
  - Gold shimmer on "Add to Cart" button hover (luxury catalog)
  - Particle effect on successful order submission
  - Smooth parallax scroll on product detail images

### Hover States
- Buttons: Brightness increase, subtle shadow growth
- Cards: Lift effect (translateY -2px), shadow expansion
- Links: Underline slide-in animation (left to right)
- Table Rows: Background color fade-in
- Icons: Rotate or bounce effect on interactive icons

## Dark Mode & Color Contrast Rules (Critical)

### Implementation Requirements
- Always use explicit colors - never rely on browser defaults or component variants like `variant="outline"`
- Force dark mode with CSS: `html { color-scheme: dark; }` and `meta name="color-scheme" content="dark"`
- Use high contrast ratios: minimum 4.5:1 for normal text, 3:1 for large text
- Override browser defaults with `!important` for form elements: `input, textarea, select { background-color: #000000 !important; color: #ffffff !important; }`
- Test in both light and dark system modes - system dark mode can override custom styling
- Use semantic color classes instead of component variants: `className="bg-gray-800 text-gray-300 border border-gray-600"` not `variant="outline"`
- Create CSS custom properties for consistency across components
- Quick debugging: check if using `variant="outline"`, add explicit colors, use `!important` if needed, test system modes

### Color Contrast Checklist (apply to all components)
- [ ] No `variant="outline"` or similar browser-dependent styles
- [ ] Explicit background and text colors specified
- [ ] High contrast ratios (4.5:1+ for text, 3:1+ for large text)
- [ ] Tested with system dark mode ON and OFF
- [ ] Form elements have forced dark styling
- [ ] Badges and buttons use custom classes, not default variants
- [ ] Placeholder text has proper contrast
- [ ] Focus states are visible and accessible

## Design Guidelines

### Do's
- Use high-quality product images with consistent aspect ratios
- Maintain generous white space in luxury catalog for elegance
- Keep admin tables dense but readable (comfortable line-height)
- Use jewel-toned colors for status badges (emerald for success, ruby for urgent)
- Implement skeleton loaders for perceived performance
- Add subtle animations to enhance premium feel
- Ensure touch targets are minimum 44x44px
- Provide clear visual feedback for all interactions

### Don'ts
- Don't use generic stock photos - jewellery requires authentic imagery
- Don't overcrowd admin interface - prioritize key metrics
- Don't use harsh color transitions - maintain elegance
- Don't forget loading states - jewellery images are large files
- Don't sacrifice accessibility for aesthetics
- Don't use auto-playing carousels without controls
- Don't hide critical actions behind multiple clicks

## Responsive Breakpoints

### Mobile First Approach
**xs (0-639px)**: Single column, stacked navigation, collapsible filters, large touch targets
**sm (640-767px)**: 2-column product grid, expandable sidebar
**md (768-1023px)**: 3-column grid, visible sidebar (admin), horizontal nav (catalog)
**lg (1024-1279px)**: 4-column grid, full sidebar, enhanced filters
**xl (1280px+)**: 5-column grid, dashboard widgets side-by-side, maximum content width 1440px

## Code Implementation Notes

### Theme CSS Structure
```css
[data-theme="luxury"] {
  --primary: 43 84% 42%;
  --font-heading: 'Playfair Display', serif;
}

[data-theme="professional"] {
  --primary: 215 84% 42%;
  --font-heading: 'Inter', sans-serif;
}

.dark[data-theme="luxury"] {
  --background: 40 15% 9%;
}
```

### Component Class Pattern
```javascript
// Use semantic Tailwind classes
<button className="bg-primary text-primary-foreground hover:brightness-110 rounded-3xl px-6 py-3 shadow-md transition-all duration-200 hover:shadow-lg">
  Order via COD
</button>
```

### Unique Style Examples
```css
/* Partial border card */
.card-gradient-edge {
  border: none;
  position: relative;
}
.card-gradient-edge::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 40px;
  height: 2px;
  background: linear-gradient(to right, transparent, var(--primary));
}
.card-gradient-edge::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 2px;
  background: linear-gradient(to left, transparent, var(--primary));
}

/* Dotted hover effect for nav */
.nav-link::after {
  content: '';
  display: block;
  width: 0;
  height: 2px;
  background: var(--primary);
  border-bottom: 2px dotted var(--primary);
  transition: width 0.3s ease;
}
.nav-link:hover::after {
  width: 100%;
}
```

## Additional Creative Styling Ideas

### Unique UI Touches
1. **Gold Foil Effect**: Buttons with subtle gradient that shifts on hover (gold to rose-gold for luxury theme)
2. **Faceted Borders**: Diamond-inspired geometric clip-path on featured product cards
3. **Shimmer Loading**: Animated gradient shimmer across skeleton loaders (luxury feel)
4. **Floating Action Button**: Fixed position with shadow halo and subtle pulse animation for "Quick Add Item" (admin)
5. **Glass Morphism Cards**: Semi-transparent cards with backdrop-blur for modal overlays
6. **Ornamental Dividers**: Decorative SVG dividers between sections (luxury catalog only)
7. **Radial Hover Glow**: Subtle radial gradient glow emanating from cursor position on product cards
8. **Torn Edge Effect**: Subtle torn-paper edge effect on sale/offer badges
9. **Parallax Scroll**: Multi-layer parallax on hero sections (luxury catalog)
10. **Kinetic Typography**: Letter-spacing animation on luxury headings during scroll-into-view

### Playful Admin Enhancements
- Dashboard metric cards with animated counting numbers
- Success confetti animation on completing large orders
- Drag-and-drop with smooth spring physics for inventory reordering
- Color-coded quick filters that "snap" into place with haptic-like feedback
- Expandable data rows with smooth height animation and nested content indent