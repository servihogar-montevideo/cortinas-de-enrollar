from pathlib import Path
from urllib.parse import urljoin
from xml.sax.saxutils import escape
import sys
if len(sys.argv)!=2 or not sys.argv[1].startswith('https://'):
 raise SystemExit('Uso: python generar_sitemap.py https://USUARIO.github.io/REPOSITORIO/')
base=sys.argv[1].rstrip('/')+'/'
root=Path(__file__).resolve().parent
urls=[]
for p in sorted(root.rglob('index.html')):
 rel=p.relative_to(root).as_posix()
 urls.append(urljoin(base,rel[:-10] if rel!='index.html' else ''))
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{escape(u)}</loc></url>\n' for u in urls)+'</urlset>\n'
(root/'sitemap.xml').write_text(xml,encoding='utf-8')
(root/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+base+'sitemap.xml\n',encoding='utf-8')
for page in root.rglob('index.html'):
 rel=page.relative_to(root).as_posix()
 canonical=urljoin(base,rel[:-10] if rel!='index.html' else '')
 html=page.read_text(encoding='utf-8')
 if '<link rel="canonical"' not in html:
  html=html.replace('</head>',f'<link rel="canonical" href="{escape(canonical)}"><meta property="og:url" content="{escape(canonical)}"></head>')
  page.write_text(html,encoding='utf-8')
print('Sitemap y URLs canónicas creados con',len(urls),'URLs:',base+'sitemap.xml')
