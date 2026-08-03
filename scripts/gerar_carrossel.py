# -*- coding: utf-8 -*-
"""
Gera o carrossel do Cafe com Internet (skill instagram-carousel).

PARA UMA NOVA SEMANA, mexa so nestes pontos:
  - lista `week`       -> agenda resumida (slide 2)
  - slides 3, 4 e 5    -> um card por compromisso
  - lista `eps`        -> episodios publicados (slide 6)
  - `TOTAL`            -> se mudar a quantidade de slides
Cores e fontes vieram do CSS do site e nao precisam mudar.

Uso:  python scripts/gerar_carrossel.py
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
(REPO / "out").mkdir(exist_ok=True)
OUT = REPO / "out" / "carrossel.html"

# ---- Sistema de cores derivado da cor primaria do site (#E8728A) ----
BRAND_PRIMARY = "#E8728A"
BRAND_LIGHT   = "#F4A6B5"
BRAND_DARK    = "#A13B53"
LIGHT_BG      = "#FDF9F9"
LIGHT_BORDER  = "#F0E4E6"
DARK_BG       = "#1A1416"
GRADIENT      = f"linear-gradient(165deg, {BRAND_DARK} 0%, {BRAND_PRIMARY} 50%, {BRAND_LIGHT} 100%)"

TOTAL = 9
HANDLE = "@nicevargas.mkt"
BRAND = "Cafe com Internet"

MUTED_LIGHT = "#8A7F80"
MUTED_DARK  = "rgba(255,255,255,0.55)"


def progress(i, light):
    pct = ((i + 1) / TOTAL) * 100
    track = "rgba(0,0,0,0.08)" if light else "rgba(255,255,255,0.12)"
    fill = BRAND_PRIMARY if light else "#fff"
    label = "rgba(0,0,0,0.3)" if light else "rgba(255,255,255,0.4)"
    return (
        f'<div style="position:absolute;bottom:0;left:0;right:0;padding:16px 28px 20px;z-index:10;'
        f'display:flex;align-items:center;gap:10px;">'
        f'<div style="flex:1;height:3px;background:{track};border-radius:2px;overflow:hidden;">'
        f'<div style="height:100%;width:{pct}%;background:{fill};border-radius:2px;"></div></div>'
        f'<span style="font-size:11px;color:{label};font-weight:500;">{i+1}/{TOTAL}</span></div>'
    )


def arrow(light):
    bg = "rgba(0,0,0,0.06)" if light else "rgba(255,255,255,0.08)"
    st = "rgba(0,0,0,0.25)" if light else "rgba(255,255,255,0.35)"
    return (
        f'<div style="position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;display:flex;'
        f'align-items:center;justify-content:center;background:linear-gradient(to right,transparent,{bg});">'
        f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none">'
        f'<path d="M9 6l6 6-6 6" stroke="{st}" stroke-width="2.5" stroke-linecap="round" '
        f'stroke-linejoin="round"/></svg></div>'
    )


import base64

ASSETS = REPO / "assets"


def data_uri(filename, mime):
    """Embute a imagem como data URI - caminho relativo quebra no export."""
    b64 = base64.b64encode((ASSETS / filename).read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


LOGO = data_uri("icone_xicara.png", "image/png")
AVATAR = data_uri("eunice_avatar.jpg", "image/jpeg")
WIDE = data_uri("eunice_wide.jpg", "image/jpeg")


def wide_photo(offset_px):
    """A mesma foto cobre dois slides. offset 0 = metade esquerda (so o braco
    aparece na borda), offset -420 = metade direita (a figura inteira).
    No swipe a imagem se completa, criando continuidade entre os cards."""
    return (f'<img src="{WIDE}" style="position:absolute;top:0;left:{offset_px}px;'
            f'width:840px;height:525px;object-fit:cover;z-index:0;">')


def icon(name, color, size=17):
    """SVG inline - emoji nao renderiza no Chromium headless."""
    paths = {
        "coffee": '<path d="M17 8h1a4 4 0 010 8h-1"/><path d="M3 8h14v9a4 4 0 01-4 4H7a4 4 0 01-4-4V8z"/>'
                  '<line x1="6" y1="1.5" x2="6" y2="4"/><line x1="10" y1="1.5" x2="10" y2="4"/>'
                  '<line x1="14" y1="1.5" x2="14" y2="4"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15 14"/>',
        "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/>',
        "mic": '<path d="M12 1.5a3 3 0 00-3 3v7a3 3 0 006 0v-7a3 3 0 00-3-3z"/>'
               '<path d="M19 10v1.5a7 7 0 01-14 0V10"/><line x1="12" y1="18.5" x2="12" y2="22.5"/>',
    }
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{paths[name]}</svg>')


def tag(text, color):
    return (f'<span class="sans" style="display:inline-block;font-size:10px;font-weight:700;'
            f'letter-spacing:2px;color:{color};margin-bottom:14px;text-transform:uppercase;">{text}</span>')


def logo_lockup(on_dark=False, on_grad=False, size=44):
    """Logo real do site. O tra&ccedil;o da x&iacute;cara e escuro, entao a marca sempre
    vai sobre um disco claro - em fundo escuro ela sumiria."""
    name_color = "#fff" if (on_dark or on_grad) else DARK_BG
    return (
        f'<div style="display:flex;align-items:center;gap:11px;">'
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:#fff;display:flex;'
        f'align-items:center;justify-content:center;flex-shrink:0;">'
        f'<img src="{LOGO}" style="width:{int(size*0.72)}px;height:{int(size*0.72)}px;'
        f'object-fit:contain;display:block;"></div>'
        f'<span class="sans" style="font-size:13px;font-weight:700;letter-spacing:0.5px;'
        f'color:{name_color};">Caf&eacute; com Internet</span></div>'
    )


def slide(i, bg_css, content, light, last=False, center=False):
    justify = "center" if center else "flex-end"
    return (
        f'<div class="slide" style="min-width:420px;width:420px;height:525px;position:relative;'
        f'background:{bg_css};display:flex;flex-direction:column;justify-content:{justify};'
        f'padding:0 36px 62px;overflow:hidden;box-sizing:border-box;">'
        f'{content}{progress(i, light)}{"" if last else arrow(light)}</div>'
    )


# ---------------------------------------------------------------- SLIDES

S = []

# 1 - HERO
S.append(slide(0, LIGHT_BG, f'''
  <div style="position:absolute;top:-70px;right:-70px;width:230px;height:230px;border-radius:50%;
       background:{BRAND_PRIMARY};opacity:0.07;"></div>
  <div style="position:absolute;top:34px;left:36px;">{logo_lockup()}</div>
  {tag("Semana de 10 a 16 de agosto", BRAND_PRIMARY)}
  <h1 class="serif" style="font-size:34px;font-weight:700;color:{DARK_BG};line-height:1.1;
      letter-spacing:-0.5px;margin:0 0 14px;">3 encontros.<br>2 est&uacute;dios.<br>
      <span style="color:{BRAND_PRIMARY};">Vagas contadas.</span></h1>
  <p class="sans" style="font-size:14px;color:{MUTED_LIGHT};line-height:1.55;margin:0 0 24px;max-width:290px;">
      A agenda da semana do Caf&eacute; com Internet &mdash; e como entrar nela.</p>
  <div style="display:flex;align-items:center;gap:12px;">
    <img src="{AVATAR}" style="width:56px;height:56px;border-radius:50%;object-fit:cover;
         border:2.5px solid {BRAND_PRIMARY};display:block;">
    <div>
      <div class="sans" style="font-size:13px;font-weight:700;color:{DARK_BG};">Eunice Vargas</div>
      <div class="sans" style="font-size:11px;color:{MUTED_LIGHT};letter-spacing:0.3px;">
        Host do Caf&eacute; com Internet</div>
    </div>
  </div>
''', True, center=True))

# 2 - A SEMANA
week = [
    ("SEG", "10", "Grava&ccedil;&atilde;o &middot; Teia Pinheiros", "11h &ndash; 12h30"),
    ("QUI", "14", "Workshop Canva AI 2.0", "10h &ndash; 15h"),
    ("QUI", "14", "Grava&ccedil;&atilde;o &middot; Teia Vergueiro", "17h &ndash; 18h30"),
]
rows = "".join(
    f'<div style="display:flex;align-items:center;gap:14px;padding:13px 0;'
    f'border-bottom:1px solid rgba(255,255,255,0.09);">'
    f'<div style="min-width:44px;text-align:center;">'
    f'<div class="sans" style="font-size:9px;font-weight:700;letter-spacing:1.5px;color:{BRAND_LIGHT};">{d}</div>'
    f'<div class="serif" style="font-size:24px;font-weight:700;color:#fff;line-height:1;">{n}</div></div>'
    f'<div style="flex:1;"><div class="sans" style="font-size:13.5px;font-weight:600;color:#fff;'
    f'margin-bottom:2px;">{t}</div>'
    f'<div class="sans" style="font-size:11.5px;color:{MUTED_DARK};">{h}</div></div></div>'
    for d, n, t, h in week
)
S.append(slide(1, DARK_BG, f'''
  {tag("Agenda", BRAND_LIGHT)}
  <h2 class="serif" style="font-size:29px;font-weight:700;color:#fff;line-height:1.12;
      letter-spacing:-0.4px;margin:0 0 18px;">O que acontece<br>essa semana</h2>
  <div>{rows}</div>
''', False))

# 3 - SEGUNDA
S.append(slide(2, LIGHT_BG, f'''
  {tag("Segunda, 10 de agosto", BRAND_PRIMARY)}
  <h2 class="serif" style="font-size:30px;font-weight:700;color:{DARK_BG};line-height:1.12;
      letter-spacing:-0.4px;margin:0 0 18px;">Grava&ccedil;&atilde;o no<br>Teia Pinheiros</h2>
  <div style="display:flex;flex-direction:column;gap:11px;margin-bottom:18px;">
    <div style="display:flex;align-items:center;gap:12px;">
      {icon("clock", BRAND_PRIMARY)}
      <span class="sans" style="font-size:14px;font-weight:600;color:{DARK_BG};">11:00 &ndash; 12:30</span></div>
    <div style="display:flex;align-items:flex-start;gap:12px;">
      <span style="margin-top:1px;">{icon("pin", BRAND_PRIMARY)}</span>
      <span class="sans" style="font-size:13px;color:{MUTED_LIGHT};line-height:1.45;">
        Rua Sumidouro, 580<br>Pinheiros &middot; S&atilde;o Paulo</span></div>
    <div style="display:flex;align-items:center;gap:12px;">
      {icon("mic", BRAND_PRIMARY)}
      <span class="sans" style="font-size:13px;color:{MUTED_LIGHT};">Audit&oacute;rio SampaCast</span></div>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;">
    <span class="sans" style="font-size:11px;font-weight:600;padding:6px 13px;background:{BRAND_PRIMARY};
      color:#fff;border-radius:20px;">Apenas 2 vagas</span>
    <span class="sans" style="font-size:11px;padding:6px 13px;background:#fff;border:1px solid {LIGHT_BORDER};
      color:{MUTED_LIGHT};border-radius:20px;">Participa&ccedil;&atilde;o gratuita</span>
  </div>
''', True))

# 4 - WORKSHOP
S.append(slide(3, DARK_BG, f'''
  {tag("Quinta, 14 de agosto", BRAND_LIGHT)}
  <h2 class="serif" style="font-size:28px;font-weight:700;color:#fff;line-height:1.12;
      letter-spacing:-0.4px;margin:0 0 14px;">Canva AI 2.0 para<br>Empreendedores</h2>
  <div style="padding:14px 16px;background:rgba(0,0,0,0.22);border-radius:12px;
       border:1px solid rgba(255,255,255,0.08);margin-bottom:16px;">
    <p class="sans" style="font-size:14px;color:{BRAND_LIGHT};font-style:italic;line-height:1.42;margin:0;">
      &ldquo;Voc&ecirc; trava na hora de criar posts para divulgar seu neg&oacute;cio?&rdquo;</p>
  </div>
  <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:16px;">
    <span class="sans" style="font-size:13px;color:rgba(255,255,255,0.82);">&#10003;&nbsp;&nbsp;Criar conte&uacute;do ao vivo com IA</span>
    <span class="sans" style="font-size:13px;color:rgba(255,255,255,0.82);">&#10003;&nbsp;&nbsp;Configurar a identidade da sua marca</span>
    <span class="sans" style="font-size:13px;color:rgba(255,255,255,0.82);">&#10003;&nbsp;&nbsp;Sair com posts prontos para publicar</span>
  </div>
  <div class="sans" style="font-size:11.5px;color:{MUTED_DARK};line-height:1.5;">
    Workshop presencial &middot; 10h &agrave;s 15h<br>Teia Centro &middot; R. Dr. Braulio Gomes, 139</div>
''', False))

# 5 - QUINTA GRAVACAO
S.append(slide(4, LIGHT_BG, f'''
  {tag("Quinta, 14 de agosto", BRAND_PRIMARY)}
  <h2 class="serif" style="font-size:30px;font-weight:700;color:{DARK_BG};line-height:1.12;
      letter-spacing:-0.4px;margin:0 0 18px;">Grava&ccedil;&atilde;o no<br>Teia Vergueiro</h2>
  <div style="display:flex;flex-direction:column;gap:11px;margin-bottom:16px;">
    <div style="display:flex;align-items:center;gap:12px;">
      {icon("clock", BRAND_PRIMARY)}
      <span class="sans" style="font-size:14px;font-weight:600;color:{DARK_BG};">17:00 &ndash; 18:30</span></div>
    <div style="display:flex;align-items:flex-start;gap:12px;">
      <span style="margin-top:1px;">{icon("pin", BRAND_PRIMARY)}</span>
      <span class="sans" style="font-size:13px;color:{MUTED_LIGHT};line-height:1.45;">
        Vergueiro, 1000<br>Liberdade &middot; S&atilde;o Paulo</span></div>
  </div>
  <div style="padding:13px 15px;background:#fff;border-left:3px solid {BRAND_PRIMARY};border-radius:8px;
       margin-bottom:14px;">
    <p class="sans" style="font-size:12.5px;color:{MUTED_LIGHT};line-height:1.45;margin:0;">
      Mesmo dia do workshop &mdash; ele termina 15h.<br><strong style="color:{DARK_BG};">D&aacute; tempo dos dois.</strong></p>
  </div>
  <div style="display:flex;gap:8px;">
    <span class="sans" style="font-size:11px;font-weight:600;padding:6px 13px;
      background:{BRAND_PRIMARY};color:#fff;border-radius:20px;">Apenas 2 de 3 vagas</span>
    <span class="sans" style="font-size:11px;padding:6px 13px;background:#fff;border:1px solid {LIGHT_BORDER};
      color:{MUTED_LIGHT};border-radius:20px;">Participa&ccedil;&atilde;o gratuita</span>
  </div>
''', True))

# 6 - PUBLICACOES
eps = [
    ("Por que 90% dos podcasts fracassam?", "30 min &middot; 30 de julho", "01"),
    ("A mentira do homem forte", "Oliver Mathias &middot; 49 min &middot; 18 de julho", "02"),
    ("O treinamento que trava seu crescimento", "Simone N. de Azevedo &middot; 15 de julho", "03"),
]
ep_rows = "".join(
    f'<div style="display:flex;align-items:flex-start;gap:14px;padding:12px 0;'
    f'border-bottom:1px solid rgba(255,255,255,0.09);">'
    f'<span class="serif" style="font-size:22px;font-weight:300;color:{BRAND_LIGHT};min-width:30px;'
    f'line-height:1.1;">{n}</span><div style="flex:1;">'
    f'<div class="sans" style="font-size:13.5px;font-weight:600;color:#fff;line-height:1.3;'
    f'margin-bottom:3px;">{t}</div>'
    f'<div class="sans" style="font-size:11px;color:{MUTED_DARK};">{m}</div></div></div>'
    for t, m, n in eps
)
S.append(slide(5, DARK_BG, f'''
  {wide_photo(0)}
  <div style="position:absolute;inset:0;z-index:1;background:linear-gradient(to right,
       {DARK_BG} 58%, rgba(26,20,22,0.82) 78%, rgba(26,20,22,0.35) 100%);"></div>
  <div style="position:relative;z-index:2;">
    {tag("No ar agora", BRAND_LIGHT)}
    <h2 class="serif" style="font-size:29px;font-weight:700;color:#fff;line-height:1.12;
        letter-spacing:-0.4px;margin:0 0 16px;">Epis&oacute;dios para<br>ouvir hoje</h2>
    <div>{ep_rows}</div>
  </div>
''', False))

# 7 - QUEM TE RECEBE (fundo escuro: o retrato ganha destaque e o blazer
# turquesa vira acento em vez de brigar com o ros&eacute; da marca)
S.append(slide(6, DARK_BG, f'''
  {wide_photo(-420)}
  <div style="position:absolute;inset:0;z-index:1;background:linear-gradient(to top,
       {DARK_BG} 0%, rgba(26,20,22,0.93) 24%, rgba(26,20,22,0.5) 40%, rgba(26,20,22,0) 60%);"></div>
  <div style="position:relative;z-index:2;">
    {tag("Quem te recebe", BRAND_LIGHT)}
    <h2 class="serif" style="font-size:29px;font-weight:700;color:#fff;line-height:1.12;
        letter-spacing:-0.4px;margin:0 0 10px;">Eunice Vargas</h2>
    <p class="sans" style="font-size:12.5px;color:rgba(255,255,255,0.78);line-height:1.5;
        margin:0 0 14px;max-width:280px;">
      Host do Caf&eacute; com Internet. Conduz as grava&ccedil;&otilde;es e o workshop de IA.</p>
    <div style="display:flex;gap:7px;flex-wrap:wrap;">
      <span class="sans" style="font-size:10.5px;padding:5px 11px;background:rgba(255,255,255,0.11);
        border-radius:20px;color:{BRAND_LIGHT};">444 epis&oacute;dios publicados</span>
      <span class="sans" style="font-size:10.5px;padding:5px 11px;background:rgba(255,255,255,0.11);
        border-radius:20px;color:{BRAND_LIGHT};">{HANDLE}</span>
    </div>
  </div>
''', False))

# 8 - COMO PARTICIPAR
steps = [
    ("01", "Escolha a data", "Agenda aberta no site, por unidade"),
    ("02", "Reserve sua vaga", "A equipe confirma seu hor&aacute;rio"),
    ("03", "Grave e receba os cortes", "Edi&ccedil;&atilde;o dos trechos inclusa"),
]
step_rows = "".join(
    f'<div style="display:flex;align-items:flex-start;gap:15px;padding:12px 0;'
    f'border-bottom:1px solid {LIGHT_BORDER};">'
    f'<span class="serif" style="font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;'
    f'line-height:1;">{n}</span><div style="flex:1;">'
    f'<div class="sans" style="font-size:14px;font-weight:600;color:{DARK_BG};margin-bottom:2px;">{t}</div>'
    f'<div class="sans" style="font-size:12px;color:{MUTED_LIGHT};">{d}</div></div></div>'
    for n, t, d in steps
)
S.append(slide(7, LIGHT_BG, f'''
  {tag("Como participar", BRAND_PRIMARY)}
  <h2 class="serif" style="font-size:30px;font-weight:700;color:{DARK_BG};line-height:1.12;
      letter-spacing:-0.4px;margin:0 0 16px;">Sem burocracia,<br>sem custo</h2>
  <div>{step_rows}</div>
''', True))

# 9 - CTA
S.append(slide(8, GRADIENT, f'''
  <div style="display:flex;flex-direction:column;align-items:center;text-align:center;">
    {logo_lockup(on_grad=True, size=48)}
    <h2 class="serif" style="font-size:31px;font-weight:700;color:#fff;line-height:1.14;
        letter-spacing:-0.5px;margin:22px 0 12px;">Sua pauta merece<br>um est&uacute;dio.</h2>
    <p class="sans" style="font-size:13.5px;color:rgba(255,255,255,0.82);line-height:1.5;
        margin:0 0 24px;max-width:280px;">Participa&ccedil;&atilde;o gratuita, cortes prontos
        para as suas redes.</p>
    <div style="display:inline-flex;align-items:center;gap:8px;padding:13px 30px;background:{LIGHT_BG};
        color:{BRAND_DARK};font-weight:700;font-size:14px;border-radius:28px;" class="sans">
        Reserve sua grava&ccedil;&atilde;o</div>
    <p class="sans" style="font-size:12px;color:rgba(255,255,255,0.75);margin:20px 0 0;">
        {HANDLE}<br><span style="color:rgba(255,255,255,0.55);">agencia.curtatche.com.br</span></p>
  </div>
''', False, last=True, center=True))

dots = "".join(
    f'<div class="dot" style="width:6px;height:6px;border-radius:50%;'
    f'background:{"#262626" if i==0 else "#c7c7c7"};"></div>' for i in range(TOTAL)
)

HTML = f'''<meta charset="utf-8">
<title>Carrossel &mdash; Semana Caf&eacute; com Internet</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  *{{box-sizing:border-box;}}
  body{{margin:0;padding:28px 12px;background:#EFEFEF;display:flex;justify-content:center;
       font-family:'Hanken Grotesk',system-ui,sans-serif;}}
  .serif,.sans{{font-family:'Hanken Grotesk',system-ui,sans-serif;margin:0;}}
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
    <strong>{HANDLE}</strong> A semana do Caf&eacute; com Internet: 3 encontros, 2 est&uacute;dios
    e vagas contadas. Arrasta pro lado &#128072;
    <div style="font-size:10px;color:#8E8E8E;letter-spacing:.4px;margin-top:7px;">H&Aacute; 2 HORAS</div>
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

# ---- Versao estatica: sem JavaScript, todos os slides empilhados ----
labels = ["Gancho", "A semana", "Seg 10/08", "Qui 14/08 - Workshop",
          "Qui 14/08 - Gravacao", "Publicacoes", "Quem te recebe", "Como participar", "CTA"]
blocks = "".join(
    f'<div style="margin-bottom:26px;">'
    f'<div style="font-size:12px;font-weight:700;letter-spacing:1.5px;color:#8A7F80;'
    f'text-transform:uppercase;margin-bottom:8px;">Slide {i+1} &middot; {labels[i]}</div>'
    f'<div style="width:420px;box-shadow:0 2px 14px rgba(0,0,0,.13);border-radius:8px;'
    f'overflow:hidden;">{s}</div></div>'
    for i, s in enumerate(S)
)
STATIC = f'''<meta charset="utf-8">
<title>Carrossel est&aacute;tico &mdash; Semana Caf&eacute; com Internet</title>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  *{{box-sizing:border-box;}}
  body{{margin:0;padding:30px 16px;background:#EFEFEF;
       font-family:'Hanken Grotesk',system-ui,sans-serif;display:flex;
       flex-direction:column;align-items:center;}}
  .serif,.sans{{font-family:'Hanken Grotesk',system-ui,sans-serif;margin:0;}}
  h1{{font-size:19px;color:#1A1416;margin:0 0 22px;font-weight:700;}}
</style>
<h1>Semana Caf&eacute; com Internet &mdash; {TOTAL} slides</h1>
{blocks}
'''
STATIC_OUT = OUT.parent / "carrossel_estatico.html"
STATIC_OUT.write_text(STATIC, encoding="utf-8")
print(f"Estatico (sem JS): {STATIC_OUT}")
