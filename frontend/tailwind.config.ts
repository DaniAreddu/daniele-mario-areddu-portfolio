import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: "#211F1C",
          soft: "#38352F",
          faint: "#5C574C",
        },
        paper: {
          DEFAULT: "#F7F3EC",
          warm: "#EFE8DA",
          line: "#DCD3C0",
        },
        cobalt: {
          DEFAULT: "#1E3FE0",
          soft: "#3454E8",
          dim: "#152C9E",
        },
      },
      fontFamily: {
        serif: ["'Fraunces'", "'Iowan Old Style'", "Georgia", "serif"],
        sans: ["'Inter'", "-apple-system", "BlinkMacSystemFont", "'Segoe UI'", "sans-serif"],
        mono: ["'IBM Plex Mono'", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      maxWidth: {
        editorial: "1440px",
      },
      letterSpacing: {
        tightest: "-0.04em",
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        "fade-up": "fade-up 0.6s cubic-bezier(0.16, 1, 0.3, 1) both",
      },
    },
  },
  plugins: [],
} satisfies Config;
