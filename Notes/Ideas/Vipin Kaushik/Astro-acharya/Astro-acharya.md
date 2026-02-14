# 🌌 Technical Specification: Vedic "Astro-Core" Engine

**Domain:** High-Performance Vedic Astrology (Jyotish)

**Architecture:** Go Microservice (C-Wrapper)

**Tier:** Advanced/Acharya Level

---

## 1. Mathematical Core (The Precision Layer)

To eliminate "bloat," the engine offloads heavy orbital mechanics to the **Swiss Ephemeris** but handles Vedic corrections at the Go-runtime level.

- **Sidereal Transformation:** * Implementation of **Ayanamsha** via $Sidereal = Tropical - Ayanamsha$.
    
    - Support for **Lahiri, Raman, KP, and Pushya-paksha**.
        
    - **Custom Offset:** Capability for advanced users to input a manual DMS (Degree-Minute-Second) offset.
        
- **Node Logic:** Toggle between **True Node** (pulsating path) and **Mean Node** (average path) for Rahu/Ketu.
    
- **Coordinate Precision:** Minimum of 6 decimal places for longitude calculations to prevent "Varga-slippage" (where a planet appears in the wrong D-chart).
    

---

## 2. Advanced Calculation Blocks (The "Acharya" Tier)

### 2.1. The Varga Compiler (Divisional Charts)

Unlike standard software, this engine treats **Shodashvargas (16 Divisions)** as a single data matrix.

- **Precision Focus:** High-speed calculation of **D-60 (Shastiamsha)**. Since the D-60 changes every ~2 minutes, the backend must use high-precision GPS-based Local Mean Time (LMT) corrections.
    
- **Varga Vishwa:** A 20-point scoring system evaluating planetary strength across all divisions.
    

### 2.2. Shadbala (Six-Fold Strength Engine)

A vector-based calculation system to determine the actual "potency" of a planet.

- **Sthana Bala:** Positional strength (Exaltation, Varga strength).
    
- **Dig Bala:** Directional strength (e.g., Jupiter/Mercury in the 1st House).
    
- **Drik Bala (Aspectual Vector):** The most complex block. The engine must calculate the total numerical "drishiti" (aspect) every planet exerts on every other planet using a 0 to 60 _Virupa_ scale.
    

### 2.3. Ashtakavarga (Energy Grid)

- **Bindu Matrix:** A $12 \times 7$ grid calculating the "benefic dots" contributed by each planet to each house.
    
- **SAV (Sarvashtakavarga):** The total tally used for "Marketing Insights" (e.g., identifying high-energy months for a client).
    

---

## 3. Advanced Timing & "The Compiler"

### 3.1. Multi-Clock Dasha System

- **Standard:** Vimshottari (120-year cycle).
    
- **Conditional Dashas:** Implementation of **Yogini, Chara, and Ashtottari** dashas based on specific birth conditions (e.g., birth during day/night or specific Tithis).
    
- **Dasha-Transit Overlap:** The "Trigger" logic. The engine monitors when a current Transit planet crosses the degree of a Dasha Lord in the natal chart.
    

### 3.2. Upagrahas & Special Points

- **Non-Luminous Bodies:** Calculation of **Gulika** and **Mandi** based on _Dinaman_ (length of day) and _Ratriman_ (length of night).
    
- **Sahams:** Mathematical "Points of Interest" (Arabic Parts) for Marriage, Travel, and Wealth.
    

---

## 4. UI/UX Strategy: "Modern Astro-Design"

- **SVG Rendering:** The Go backend sends a JSON coordinate object. The Frontend Wrapper (React/Next.js) renders the North or South Indian chart as an **interactive SVG**.
    
- **Responsive Heatmaps:** Using Ashtakavarga data to create "Success Heatmaps" that look like modern stock market charts.
    
- **Glassmorphic Overlays:** Professional, clean tooltips that show planetary dignity (Exalted, Moolatrikona, etc.) on hover.
    

---

## 5. Motherboard Integration (The Business Logic)

- **Inventory Tracking:** The Client (Astrologer) sets "Consultation Slots" and "Remedy Inventory" (Gemstones/Mantras) in the Motherboard.
    
- **The "Remedy" Bridge:** When the Astro-Engine identifies a "Weak Moon," the Motherboard UI dynamically shows the client's "Pearl Inventory" as a suggested remedy.
    
- **Marketing Automation:** The Sales Team receives alerts when a client enters a significant _Antardasha_ (sub-period), allowing for timely outreach.
    

---

### How to Build This (For Your Team):

1. **Backend:** Create a Go microservice that wraps the C-library `swisseph`.
    
2. **Concurrency:** Use `goroutines` to calculate all 16 Vargas and Shadbala simultaneously.
    
3. **Caching:** Store birth chart results in the **Client MongoDB** to avoid redundant heavy calculations.
    
4. **Security:** Ensure the "Natal Data" is encrypted, as it is highly sensitive PII (Personally Identifiable Information).