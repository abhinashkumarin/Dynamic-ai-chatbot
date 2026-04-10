/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ai: {
          dark:    "#07090f",
          card:    "#0d1117",
          border:  "#161b22",
          accent:  "#58a6ff",
          purple:  "#bc8cff",
          green:   "#3fb950",
          orange:  "#d29922",
          pink:    "#f778ba",
          red:     "#f85149",
          muted:   "#484f58",
          text:    "#c9d1d9",
        }
      },
      fontFamily: {
        display: ["'Syne'", "sans-serif"],
        body:    ["'DM Sans'", "sans-serif"],
        mono:    ["'JetBrains Mono'", "monospace"],
      },
      animation: {
        "fade-up":    "fadeUp 0.4s cubic-bezier(0.34,1.56,0.64,1) forwards",
        "glow-pulse": "glowPulse 2s ease-in-out infinite",
        "scan":       "scan 6s linear infinite",
        "float":      "float 5s ease-in-out infinite",
      },
      keyframes: {
        fadeUp: {
          from: { opacity: 0, transform: "translateY(14px) scale(0.97)" },
          to:   { opacity: 1, transform: "translateY(0) scale(1)" },
        },
        glowPulse: {
          "0%,100%": { boxShadow: "0 0 8px rgba(88,166,255,0.3)" },
          "50%":     { boxShadow: "0 0 24px rgba(88,166,255,0.7)" },
        },
        scan: {
          from: { backgroundPosition: "0 0" },
          to:   { backgroundPosition: "0 100%" },
        },
        float: {
          "0%,100%": { transform: "translateY(0)" },
          "50%":     { transform: "translateY(-8px)" },
        },
      },
    },
  },
  plugins: [],
};
