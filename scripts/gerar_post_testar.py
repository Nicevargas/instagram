# -*- coding: utf-8 -*-
"""
Gera o carrossel do post "comenta TESTAR" — a demonstracao ao vivo da
autoresposta (projeto instagram-autoresposta).

Deliberadamente separado do gerar_carrossel.py: aquele e o da agenda semanal,
com 9 slides e layout proprio. Este tem 5 e sai em arquivos proprios
(out/post_testar.html, slides_testar/), entao os dois convivem sem se
atropelar.

Mesmos tokens da marca, tirados do CSS do site — nao invente cor nem fonte.
O sistema visual aqui e mais denso que o semanal de proposito: fundo com
profundidade, tipografia grande e um card de conversa como peca central.

Uso:  python scripts/gerar_post_testar.py
"""
import base64
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ASSETS = REPO / "assets"
(REPO / "out").mkdir(exist_ok=True)
OUT = REPO / "out" / "post_testar.html"

# ---- tokens da marca (CSS do site) ----
BRAND_PRIMARY = "#E8728A"
BRAND_LIGHT = "#F4A6B5"
BRAND_DARK = "#A13B53"
LIGHT_BG = "#FDF9F9"
DARK_BG = "#140F11"

TOTAL = 5
HANDLE = "@nicevargas.mkt"


def data_uri(filename, mime):
    """Embute a imagem como data URI — caminho relativo quebra no export."""
    return f"data:{mime};base64," + base64.b64encode((ASSETS / filename).read_bytes()).decode()


LOGO = data_uri("icone_xicara.png", "image/png")
AVATAR = data_uri("eunice_avatar.jpg", "image/jpeg")


# ------------------------------------------------------------------ atmosfera

def glow(cor, tamanho, topo, esquerda, opacidade=0.5):
    """Halo desfocado. E o que tira o fundo de chapado sem pesar o arquivo."""
    return (f'<div class="deco" style="position:absolute;top:{topo}px;left:{esquerda}px;width:{tamanho}px;'
            f'height:{tamanho}px;border-radius:50%;background:{cor};opacity:{opacidade};'
            f'filter:blur(85px);z-index:0;pointer-events:none;"></div>')


GRAO = (
    "data:image/svg+xml;base64,"
    + base64.b64encode(
        b'<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120">'
        b'<filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.85" '
        b'numOctaves="3" stitchTiles="stitch"/></filter>'
        b'<rect width="120" height="120" filter="url(#n)" opacity="0.55"/></svg>'
    ).decode()
)


def grao(opacidade=0.05):
    """Textura fina por cima de tudo. Em tela grande e o que separa um fundo
    digital de um fundo impresso — some no thumb e aparece no zoom."""
    return (f'<div style="position:absolute;inset:0;background-image:url({GRAO});'
            f'background-size:120px 120px;opacity:{opacidade};z-index:1;'
            f'pointer-events:none;mix-blend-mode:overlay;"></div>')


def pilula(texto, escuro=True):
    """Etiqueta em capsula de vidro — substitui a tag de texto solto."""
    if escuro:
        fundo, borda, cor = "rgba(255,255,255,0.08)", "rgba(255,255,255,0.16)", "rgba(255,255,255,0.9)"
    else:
        fundo, borda, cor = "rgba(161,59,83,0.07)", "rgba(161,59,83,0.16)", BRAND_DARK
    return (f'<span style="display:inline-flex;align-items:center;gap:7px;background:{fundo};'
            f'border:1px solid {borda};border-radius:999px;padding:7px 14px;font-size:10px;'
            f'font-weight:700;letter-spacing:2.2px;color:{cor};text-transform:uppercase;'
            f'margin-bottom:14px;">'
            f'<span style="width:5px;height:5px;border-radius:50%;background:{BRAND_PRIMARY};'
            f'display:block;"></span>{texto}</span>')


def texto_gradiente(texto, tamanho, peso=800):
    """Recorte de gradiente no tipo. So no termo que importa — em bloco
    inteiro vira poluicao."""
    return (f'<span style="font-size:{tamanho}px;font-weight:{peso};letter-spacing:-2.2px;'
            f'background:linear-gradient(105deg,#FFD9E1 0%,{BRAND_LIGHT} 30%,{BRAND_PRIMARY} 72%,{BRAND_DARK} 128%);'
            f'-webkit-background-clip:text;background-clip:text;color:transparent;'
            f'display:inline-block;line-height:0.98;">{texto}</span>')


def marca(escuro=True, tamanho=34):
    """O traco da xicara e escuro, entao a marca sempre vai sobre disco claro."""
    cor = "rgba(255,255,255,0.92)" if escuro else DARK_BG
    return (
        f'<div style="display:flex;align-items:center;gap:9px;position:relative;z-index:5;">'
        f'<div style="width:{tamanho}px;height:{tamanho}px;border-radius:50%;background:#fff;'
        f'display:flex;align-items:center;justify-content:center;flex-shrink:0;'
        f'box-shadow:0 2px 10px rgba(0,0,0,0.12);">'
        f'<img src="{LOGO}" style="width:{int(tamanho*0.7)}px;height:{int(tamanho*0.7)}px;'
        f'object-fit:contain;display:block;"></div>'
        f'<span style="font-size:11.5px;font-weight:700;letter-spacing:0.3px;color:{cor};">'
        f'Caf&eacute; com Internet</span></div>'
    )


def progresso(i, escuro):
    pct = ((i + 1) / TOTAL) * 100
    trilho = "rgba(255,255,255,0.14)" if escuro else "rgba(20,15,17,0.10)"
    barra = "#fff" if escuro else BRAND_PRIMARY
    rotulo = "rgba(255,255,255,0.45)" if escuro else "rgba(20,15,17,0.35)"
    return (
        f'<div style="position:absolute;bottom:0;left:0;right:0;padding:16px 30px 22px;z-index:20;'
        f'display:flex;align-items:center;gap:11px;">'
        f'<div style="flex:1;height:2.5px;background:{trilho};border-radius:2px;overflow:hidden;">'
        f'<div style="height:100%;width:{pct}%;background:{barra};border-radius:2px;"></div></div>'
        f'<span style="font-size:10.5px;color:{rotulo};font-weight:600;letter-spacing:0.5px;">'
        f'{i+1}/{TOTAL}</span></div>'
    )


def seta(escuro):
    cor = "rgba(255,255,255,0.4)" if escuro else "rgba(20,15,17,0.28)"
    fundo = "rgba(255,255,255,0.07)" if escuro else "rgba(20,15,17,0.05)"
    return (
        f'<div style="position:absolute;right:16px;top:50%;transform:translateY(-50%);z-index:20;'
        f'width:30px;height:30px;border-radius:50%;background:{fundo};display:flex;'
        f'align-items:center;justify-content:center;">'
        f'<svg width="17" height="17" viewBox="0 0 24 24" fill="none">'
        f'<path d="M9 5l7 7-7 7" stroke="{cor}" stroke-width="2.6" stroke-linecap="round" '
        f'stroke-linejoin="round"/></svg></div>'
    )


def slide(i, fundo, conteudo, escuro, ultimo=False):
    return (
        f'<div class="slide" style="min-width:420px;width:420px;height:525px;position:relative;'
        f'background:{fundo};overflow:hidden;box-sizing:border-box;isolation:isolate;">'
        f'{conteudo}{grao()}{progresso(i, escuro)}{"" if ultimo else seta(escuro)}</div>'
    )


def bolha(texto, do_robo, hora):
    """Balao de conversa. Emoji nao renderiza no Chromium headless — so texto."""
    if do_robo:
        estilo = ("background:#F1EFF0;color:#171214;border-radius:17px 17px 17px 5px;"
                  "align-self:flex-start;")
        cor_hora = "rgba(23,18,20,0.4)"
    else:
        estilo = (f"background:linear-gradient(135deg,{BRAND_PRIMARY},{BRAND_DARK});color:#fff;"
                  "border-radius:17px 17px 5px 17px;align-self:flex-end;")
        cor_hora = "rgba(255,255,255,0.7)"
    return (f'<div style="max-width:80%;{estilo}font-size:12.5px;line-height:1.42;'
            f'padding:10px 13px 7px;margin-bottom:8px;">{texto}'
            f'<div style="font-size:9px;color:{cor_hora};text-align:right;margin-top:3px;'
            f'letter-spacing:0.3px;">{hora}</div></div>')


def passo(numero, titulo, descricao, ultimo=False):
    """No da linha do tempo. A linha ligando os numeros e o que transforma
    tres frases soltas numa sequencia."""
    linha = ("" if ultimo else
             f'<div style="position:absolute;left:15px;top:32px;bottom:-14px;width:1.5px;'
             f'background:linear-gradient(to bottom,{BRAND_PRIMARY},rgba(232,114,138,0.12));"></div>')
    return (
        f'<div style="position:relative;padding-left:44px;padding-bottom:{0 if ultimo else 16}px;">'
        f'{linha}'
        f'<div style="position:absolute;left:0;top:0;width:31px;height:31px;border-radius:50%;'
        f'background:linear-gradient(135deg,{BRAND_PRIMARY},{BRAND_DARK});color:#fff;font-size:13px;'
        f'font-weight:800;display:flex;align-items:center;justify-content:center;'
        f'box-shadow:0 4px 12px rgba(232,114,138,0.35);">{numero}</div>'
        f'<div style="font-size:15.5px;font-weight:700;color:#181315;line-height:1.25;'
        f'margin-bottom:2px;">{titulo}</div>'
        f'<div style="font-size:12.5px;color:#8A7F80;line-height:1.4;">{descricao}</div></div>'
    )


S = []

# ---------------------------------------------------------------- 1 — GANCHO
S.append(slide(0, DARK_BG, f'''
  {glow(BRAND_PRIMARY, 320, 210, 150, 0.42)}
  {glow(BRAND_DARK, 260, -70, -110, 0.45)}
  <div style="position:absolute;inset:0;z-index:5;display:flex;flex-direction:column;
       justify-content:space-between;padding:34px 34px 74px;">
    {marca()}
    <div>
      {pilula("Bastidor")}
      <div style="font-size:43px;font-weight:800;color:#fff;letter-spacing:-2px;line-height:1.0;">
        Comenta</div>
      <div style="margin:2px 0 4px;">{texto_gradiente("TESTAR", 68)}</div>
      <div style="font-size:43px;font-weight:800;color:#fff;letter-spacing:-2px;line-height:1.0;
           margin-bottom:18px;">aqui embaixo</div>
      <p style="font-size:15.5px;line-height:1.45;color:rgba(255,255,255,0.62);margin:0;
         font-weight:500;">N&atilde;o sou eu que vou te responder.</p>
    </div>
  </div>
''', True))

# ------------------------------------------------------- 2 — A CONVERSA REAL
S.append(slide(1, "#0F0B0D", f'''
  {glow(BRAND_PRIMARY, 300, 30, 130, 0.30)}
  <div style="position:absolute;inset:0;z-index:5;display:flex;flex-direction:column;
       justify-content:space-between;padding:34px 34px 74px;">
    {marca()}

    <div style="background:#fff;border-radius:19px;overflow:hidden;
         box-shadow:0 22px 50px rgba(0,0,0,0.5);">
      <div style="display:flex;align-items:center;gap:9px;padding:11px 14px;
           border-bottom:1px solid #EFECED;">
        <img src="{AVATAR}" style="width:31px;height:31px;border-radius:50%;object-fit:cover;
             display:block;">
        <div style="flex:1;">
          <div style="font-size:12.5px;font-weight:700;color:#171214;line-height:1.2;">{HANDLE}</div>
          <div style="font-size:10px;color:#9B9294;">ativo agora</div>
        </div>
        <div style="display:flex;gap:3px;">
          <span style="width:3.5px;height:3.5px;border-radius:50%;background:#C9C3C5;"></span>
          <span style="width:3.5px;height:3.5px;border-radius:50%;background:#C9C3C5;"></span>
          <span style="width:3.5px;height:3.5px;border-radius:50%;background:#C9C3C5;"></span>
        </div>
      </div>
      <div style="display:flex;flex-direction:column;padding:14px 13px 10px;background:#fff;">
        {bolha("TESTAR", False, "20:41")}
        {bolha("Oi! Chegou aqui em segundos &mdash; e n&atilde;o fui eu que digitei.", True, "20:41")}
      </div>
    </div>

    <div>
      <div style="font-size:31px;font-weight:800;color:#fff;letter-spacing:-1.3px;line-height:1.08;">
        Em segundos,<br>no seu direct.</div>
      <p style="font-size:14.5px;line-height:1.45;color:rgba(255,255,255,0.55);margin:11px 0 0;">
         Eu posso estar dormindo.</p>
    </div>
  </div>
''', True))

# --------------------------------------------------------- 3 — COMO FUNCIONA
S.append(slide(2, LIGHT_BG, f'''
  <div class="deco" style="position:absolute;top:-120px;right:-120px;width:400px;height:400px;border-radius:50%;
       background:radial-gradient(circle,{BRAND_LIGHT} 0%,transparent 66%);opacity:0.55;z-index:0;"></div>
  <div class="deco" style="position:absolute;bottom:-140px;left:-120px;width:320px;height:320px;border-radius:50%;
       background:radial-gradient(circle,{BRAND_PRIMARY} 0%,transparent 68%);opacity:0.22;z-index:0;"></div>
  <div style="position:absolute;inset:0;z-index:5;display:flex;flex-direction:column;
       justify-content:space-between;padding:34px 34px 74px;">
    {marca(escuro=False)}
    <div>
      {pilula("Como funciona", escuro=False)}
      <div style="font-size:31px;font-weight:800;color:#181315;letter-spacing:-1.3px;
           line-height:1.08;margin-bottom:24px;">Ele l&ecirc;, confere<br>e responde.</div>
      {passo(1, "L&ecirc; o seu coment&aacute;rio", "Qualquer post, a qualquer hora")}
      {passo(2, "Confere se voc&ecirc; me segue", "Em tempo real, na hora")}
      {passo(3, "Manda a mensagem certa", "Se ainda n&atilde;o segue, te convida", ultimo=True)}
      <div style="margin-top:22px;padding-top:16px;border-top:1px solid rgba(161,59,83,0.10);font-size:13px;color:#8A7F80;line-height:1.45;">Sem app de terceiro, sem mensalidade.</div>
    </div>
  </div>
''', False))

# ----------------------------------------------------------------- 4 — O PONTO
S.append(slide(3, f"linear-gradient(158deg,{BRAND_DARK} 0%,#7E2C40 48%,{DARK_BG} 100%)", f'''
  {glow(BRAND_PRIMARY, 280, 250, -60, 0.35)}
  <div style="position:absolute;inset:0;z-index:5;display:flex;flex-direction:column;
       justify-content:space-between;padding:34px 34px 74px;">
    {marca()}
    <div>
      {pilula("O ponto")}
      <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:6px;">
        <span style="font-size:76px;font-weight:800;color:#fff;letter-spacing:-4px;
              line-height:0.85;">1</span>
        <span style="font-size:34px;font-weight:800;color:rgba(255,255,255,0.92);
              letter-spacing:-1.4px;">tarde.</span>
      </div>
      <p style="font-size:16px;line-height:1.5;color:rgba(255,255,255,0.78);margin:0 0 20px;">
         Foi o que levou pra montar isso, conversando com uma IA &mdash; do zero at&eacute; no ar.</p>
      <div style="background:rgba(255,255,255,0.10);border:1px solid rgba(255,255,255,0.16);
           border-radius:15px;padding:15px 17px;">
        <p style="font-size:15.5px;line-height:1.45;color:#fff;margin:0;font-weight:600;">
           O que era mensalidade de ferramenta virou conversa.</p>
      </div>
    </div>
  </div>
''', True))

# --------------------------------------------------------------------- 5 — CTA
S.append(slide(4, "#0F0B0D", f'''
  {glow(BRAND_PRIMARY, 330, 185, 45, 0.62)}
  {glow(BRAND_DARK, 300, -90, 165, 0.5)}
  <div style="position:absolute;inset:0;z-index:5;display:flex;flex-direction:column;
       align-items:center;justify-content:center;text-align:center;padding:34px 34px 74px;">
    <div style="margin-bottom:26px;">{marca(tamanho=40)}</div>
    <div style="font-size:11px;font-weight:700;letter-spacing:3px;color:rgba(255,255,255,0.55);
         text-transform:uppercase;margin-bottom:14px;">Sua vez</div>
    <div style="font-size:38px;font-weight:800;color:#fff;letter-spacing:-1.6px;line-height:1.0;
         margin-bottom:4px;">Comenta</div>
    <div style="background:linear-gradient(135deg,{BRAND_PRIMARY} 0%,{BRAND_DARK} 100%);
         border-radius:999px;padding:13px 34px;margin-bottom:22px;
         box-shadow:0 12px 34px rgba(232,114,138,0.42);">
      <span style="font-size:46px;font-weight:800;color:#fff;letter-spacing:-2px;
            line-height:0.98;display:inline-block;">TESTAR</span>
    </div>
    <p style="font-size:16.5px;line-height:1.45;color:rgba(255,255,255,0.85);margin:0;
       max-width:270px;">e me diz o que voc&ecirc; achou.</p>
  </div>
''', True, ultimo=True))


dots = "".join(
    f'<div class="dot" style="width:6px;height:6px;border-radius:50%;'
    f'background:{"#262626" if i==0 else "#c7c7c7"};"></div>' for i in range(TOTAL)
)

HTML = f'''<meta charset="utf-8">
<title>Post &mdash; comenta TESTAR</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  *{{box-sizing:border-box;}}
  body{{margin:0;padding:28px 12px;background:#EFEFEF;display:flex;justify-content:center;
       font-family:'Hanken Grotesk',system-ui,sans-serif;}}
  div,p,span,h1,h2{{font-family:'Hanken Grotesk',system-ui,sans-serif;}}
  .ig-frame{{width:420px;background:#fff;border-radius:10px;overflow:hidden;
       box-shadow:0 2px 18px rgba(0,0,0,0.10);}}
  .ig-header{{display:flex;align-items:center;gap:10px;padding:11px 14px;border-bottom:1px solid #EFEFEF;}}
  .carousel-viewport{{width:420px;height:525px;overflow:hidden;position:relative;cursor:grab;}}
  .carousel-track{{display:flex;transition:transform .32s cubic-bezier(.4,0,.2,1);will-change:transform;}}
  .ig-dots{{display:flex;justify-content:center;gap:5px;padding:11px 0 7px;}}
  .ig-actions{{display:flex;gap:15px;padding:5px 14px 8px;}}
  .ig-caption{{padding:0 14px 15px;font-size:13px;color:#262626;line-height:1.45;}}
</style>

<div class="ig-frame">
  <div class="ig-header">
    <div style="width:33px;height:33px;border-radius:50%;background:#fff;border:1px solid #EFEFEF;
         display:flex;align-items:center;justify-content:center;">
         <img src="{LOGO}" style="width:24px;height:24px;object-fit:contain;display:block;"></div>
    <div>
      <div style="font-size:13px;font-weight:700;color:#262626;line-height:1.2;">{HANDLE}</div>
      <div style="font-size:11px;color:#8E8E8E;">Caf&eacute; com Internet &middot; S&atilde;o Paulo</div>
    </div>
  </div>

  <div class="carousel-viewport" id="vp">
    <div class="carousel-track" id="track">{"".join(S)}</div>
  </div>

  <div class="ig-dots" id="dots">{dots}</div>

  <div class="ig-actions">
    <svg width="23" height="23" viewBox="0 0 24 24" fill="none" stroke="#262626" stroke-width="1.7"><path d="M20.8 4.6a5.5 5.5 0 00-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 00-7.8 7.8l1.1 1L12 21l7.7-7.6 1.1-1a5.5 5.5 0 000-7.8z"/></svg>
    <svg width="23" height="23" viewBox="0 0 24 24" fill="none" stroke="#262626" stroke-width="1.7"><path d="M21 11.5a8.4 8.4 0 01-9 8.4 8.4 8.4 0 01-3.8-.9L3 20.5l1.5-4.4A8.4 8.4 0 013.6 12a8.4 8.4 0 018.4-8.4h.5a8.4 8.4 0 018 8z"/></svg>
    <svg width="23" height="23" viewBox="0 0 24 24" fill="none" stroke="#262626" stroke-width="1.7"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg>
    <svg width="23" height="23" viewBox="0 0 24 24" fill="none" stroke="#262626" stroke-width="1.7" style="margin-left:auto;"><path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z"/></svg>
  </div>

  <div class="ig-caption">
    <strong>{HANDLE}</strong> Comenta TESTAR e v&ecirc; o que acontece. Arrasta pro lado &#128072;
    <div style="font-size:10px;color:#8E8E8E;letter-spacing:.4px;margin-top:7px;">AGORA</div>
  </div>
</div>

<script>
(function(){{
  var track=document.getElementById('track'), vp=document.getElementById('vp');
  var dots=[].slice.call(document.querySelectorAll('#dots .dot'));
  var i=0, total={TOTAL}, W=420, x0=null, dx=0;
  function go(n){{
    i=Math.max(0,Math.min(total-1,n));
    track.style.transform='translateX('+(-i*W)+'px)';
    dots.forEach(function(d,k){{d.style.background = k===i ? '#262626' : '#c7c7c7';}});
  }}
  vp.addEventListener('pointerdown',function(e){{x0=e.clientX;dx=0;track.style.transition='none';vp.setPointerCapture(e.pointerId);}});
  vp.addEventListener('pointermove',function(e){{if(x0===null)return;dx=e.clientX-x0;track.style.transform='translateX('+(-i*W+dx)+'px)';}});
  vp.addEventListener('pointerup',function(){{if(x0===null)return;track.style.transition='';
    if(dx<-45)go(i+1); else if(dx>45)go(i-1); else go(i); x0=null;}});
  document.addEventListener('keydown',function(e){{if(e.key==='ArrowRight')go(i+1);if(e.key==='ArrowLeft')go(i-1);}});
  go(0);
}})();
</script>
'''

OUT.write_text(HTML, encoding="utf-8")
print(f"HTML gerado: {OUT}")
print(f"Slides: {TOTAL}  |  Tamanho: {len(HTML)/1024:.1f} KB")
