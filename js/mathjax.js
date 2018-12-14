if (typeof window.MathJax === "object") {
  window.MathJax.Hub.Config({
      messageStyle: "none",
      "HTML-CSS": {
          showMathMenu: false,
          linebreaks: { automatic: true, width: "container" } ,
          preferredFont: "STIX",
          availableFonts: ["STIX","TeX"],
          scale: 100,
          minScaleAdjust: 100
      },
      SVG: { linebreaks: { automatic: true, width: "container" } }
   });

  window.MathJax.Hub.Configured();
}
