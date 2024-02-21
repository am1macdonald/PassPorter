/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./templates/**/*.{html,jinja,jinja2}"], theme: {
        extend: {},
    }, plugins: [
        require('@tailwindcss/forms'),
    ],
}

