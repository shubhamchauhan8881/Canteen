/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html"],
  plugins: [require('daisyui'),],
  
  daisyui: {
    themes:[
      {
        light: {
          ...require("daisyui/src/theming/themes")["light"],
          "primary": "#000000",
          "secondary": "#E8D4C3", //lightbrown

          "info" : "#5d4037",

          "accent": "#76460c", // dark brown
          // "neutral": "white",
          "base-100": "#252525",


          // "info": "#0068ff",
          // "success": "#009b6e",
          // "warning": "#b92e00",
          // "error": "#fe456d",
        },
      },
    ],
  }
}

