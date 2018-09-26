if (typeof window.MathJax === "object") {
  window.MathJax.Hub.Config({
      messageStyle: "none",
      scale: 100,
      "HTML-CSS": {
          showMathMenu: false,
          linebreaks: { automatic: true, width: "container" } ,
          preferredFont: "STIX",
          availableFonts: ["STIX","TeX"]
      },
      SVG: { linebreaks: { automatic: true, width: "container" } }
   });

  window.MathJax.Hub.Configured();
}
