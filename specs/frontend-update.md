# Frontend Update Specification: Modern, Elegant, Minimalist Design

## Design Philosophy
Our updated frontend design will embrace a clean, modern aesthetic with an emphasis on:
- Minimalist UI with intentional whitespace
- Clear visual hierarchy and typography
- Subtle animations and transitions for enhanced user experience
- Reduced visual noise and clutter
- Accessibility and responsive design

## Color Palette
Replace the current color scheme with a more refined palette:

### Light Theme
- Background: Clean whites and subtle grays 
  - Primary: #FFFFFF
  - Secondary: #F8FAFC
  - Tertiary: #F1F5F9
- Text: Darker, higher contrast for readability
  - Primary: #0F172A
  - Secondary: #334155
  - Tertiary: #64748B
- Accent: A more sophisticated primary color
  - Primary: #2563EB → #3B82F6 (gradient)
  - Secondary: #8B5CF6 → #A855F7 (gradient)
- Status Colors:
  - Success: #10B981
  - Warning: #F59E0B
  - Error: #EF4444
  - Info: #0EA5E9

### Dark Theme
- Background: Deep, rich blacks and dark grays
  - Primary: #0F172A
  - Secondary: #1E293B
  - Tertiary: #334155
- Text: Crisp whites and light grays
  - Primary: #F8FAFC
  - Secondary: #E2E8F0
  - Tertiary: #CBD5E1
- Accent: Brighter, more vibrant colors for dark mode
  - Primary: #3B82F6 → #60A5FA (gradient)
  - Secondary: #A855F7 → #C084FC (gradient)

## Typography
- Font Family: Replace with Inter as the primary font
- Font Weights: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)
- Line Height: 1.5 for body text, 1.2 for headings
- Font Sizes:
  - XS: 0.75rem (12px)
  - SM: 0.875rem (14px)
  - Base: 1rem (16px)
  - LG: 1.125rem (18px)
  - XL: 1.25rem (20px)
  - 2XL: 1.5rem (24px)
  - 3XL: 1.875rem (30px)
  - 4XL: 2.25rem (36px)

## Layout Updates

### Header
- Streamlined, flatter design with fewer visual elements
- Condensed navigation with dropdown for secondary links
- Simplified user profile menu
- Subtle shadow or border to separate from content
- Sticky positioning for improved navigation
- Better mobile menu with smooth animations

### Footer
- Reduced content and simplified layout
- Two-column design on mobile, four-column on desktop
- Smaller text and spacing
- Subtle background color to differentiate from main content

### Common Components
- Cards: Subtle shadows, rounded corners (12px), minimal borders
- Buttons: 
  - Primary: Gradient background, subtle hover effect
  - Secondary: Outlined or ghost style
  - Size options: SM, MD, LG
  - Consistent padding and border-radius
- Forms:
  - Floating labels
  - Inline validation
  - Simplified but elegant inputs
  - Subtle focus states

### Page Layouts
- Increased whitespace between sections
- Consistent container widths and padding
- Grid system with 64px gutters on desktop, 24px on mobile
- Mobile-first responsive design
- Max content width of 1280px with centered layout

## Specific Page Updates

### Homepage
- Hero section: Full-width background, larger typography, subtle animation
- Features: Card-based layout with icons, more spacing
- Testimonials: Add clean, minimalist testimonial section
- Call to action: Simplified with stronger visual hierarchy

### Dashboard
- Simplified layout with card-based components
- Data visualization with cleaner charts
- Better spacing and organization of content
- Quick action buttons prominently displayed

### Transcription Page
- Focus mode: Reduce distractions when transcribing
- Cleaner video player integration
- Improved text editor with better visual feedback
- Side-by-side layout on larger screens

### Subscription Page
- Cleaner pricing tables
- Visual differentiation between plans
- Simplified checkout process

## Animation and Interactions
- Subtle hover states for interactive elements
- Page transitions (fade in/out)
- Micro-interactions for buttons and form elements
- Loading states and skeleton screens

## Implementation Guidelines
- Use CSS variables for all colors, spacing, and typography
- Implement responsive design with mobile-first approach
- Ensure accessibility compliance (WCAG 2.1 AA)
- Optimize for performance (minimize CSS, use efficient selectors)
- Ensure dark mode implementation is complete and consistent

## Design System Components
- Create reusable components for:
  - Button variants
  - Form elements
  - Cards and containers
  - Typography styles
  - Icons and visual elements
  - Layout containers and grids 