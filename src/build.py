"""Builds index.html (the CV) in the repository root from src/cv-src.html.
Usage: python src/build.py"""
import base64, pathlib

# Address of the portfolio site, used by the "Portfolio" buttons.
PORTFOLIO_URL = "https://rayvan-alifarlo.netlify.app/"

R = pathlib.Path(__file__).parent
b64 = lambda p: base64.b64encode((R / p).read_bytes()).decode()
def font(name, fam, w, st='normal'):
    return f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};font-display:swap;src:url(data:font/woff2;base64,{b64("assets/fonts/" + name + ".woff2")}) format("woff2")}}'
fonts = (font('libre-bodoni-latin-wght-normal', 'Libre Bodoni Variable', '400 700')
         + font('libre-bodoni-latin-wght-italic', 'Libre Bodoni Variable', '400 700', 'italic')
         + font('public-sans-latin-wght-normal', 'Public Sans Variable', '100 900'))
h = (R / 'cv-src.html').read_text(encoding='utf-8').replace('/*{{FONTS}}*/', fonts)
h = h.replace('{{PORTFOLIO_URL}}', PORTFOLIO_URL)
h = h.replace('/*{{PHOTO}}*/', 'data:image/webp;base64,' + b64('assets/img/me.webp'))
for p in (R / 'assets/logos').glob('*.webp'):
    h = h.replace('/*{{LOGO_' + p.stem.upper() + '}}*/', 'data:image/webp;base64,' + b64('assets/logos/' + p.name))
h = h.replace('/*{{ENGINE_CSS}}*/', (R / 'engine/scrollcraft.css').read_text(encoding='utf-8'))
h = h.replace('/*{{ENGINE_JS}}*/', (R / 'engine/scrollcraft.js').read_text(encoding='utf-8').replace('</script', '<\\/script'))
(R.parent / 'index.html').write_text(h, encoding='utf-8')
print('index.html', len(h) // 1024, 'KB, placeholders left:', h.count('{{'))
