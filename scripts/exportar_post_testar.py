# -*- coding: utf-8 -*-
"""
Confere e exporta os slides do post "comenta TESTAR".

Faz as duas coisas de uma vez: detecta texto transbordando, monta a folha de
contato (todos lado a lado, que e como se pega erro que o preview arrastavel
esconde) e exporta JPEG 1080x1350.

Detalhes que ja custaram erro no pipeline semanal, repetidos aqui de proposito:
  - O layout FICA em 420x525. Quem amplia e o device_scale_factor. Trocar o
    viewport para 1080x1350 encolhe o texto e quebra tudo.
  - Espera 3,5s pelas fontes do Google antes do primeiro print.
  - Converte para JPEG porque a Meta documenta apenas esse formato.

Escreve em slides_testar/ para nao passar por cima do carrossel semanal.

Uso:  python scripts/exportar_post_testar.py
"""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "out" / "post_testar.html"
QA = REPO / "out" / "qa_testar"
OUT = REPO / "slides_testar"
QA.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

VIEW_W, VIEW_H = 420, 525
SCALE = 1080 / 420

LIMPAR_MOLDURA = """() => {
    document.querySelectorAll('.ig-header,.ig-dots,.ig-actions,.ig-caption')
      .forEach(e => e.style.display='none');
    const f=document.querySelector('.ig-frame');
    f.style.cssText='width:420px;height:525px;max-width:none;border-radius:0;box-shadow:none;overflow:hidden;margin:0;';
    const v=document.querySelector('.carousel-viewport');
    v.style.cssText='width:420px;height:525px;overflow:hidden;cursor:default;';
    document.body.style.cssText='padding:0;margin:0;display:block;overflow:hidden;';
}"""

IR_PARA = """(i)=>{const t=document.querySelector('.carousel-track');
    t.style.transition='none';t.style.transform='translateX('+(-i*420)+'px)';}"""


async def main():
    async with async_playwright() as p:
        navegador = await p.chromium.launch()

        # ---- passo 1: conferencia em escala 1, barata ----
        pagina = await navegador.new_page(viewport={"width": VIEW_W, "height": VIEW_H},
                                          device_scale_factor=1)
        await pagina.set_content(SRC.read_text(encoding="utf-8"), wait_until="networkidle")
        await pagina.wait_for_timeout(3500)
        await pagina.evaluate(LIMPAR_MOLDURA)
        await pagina.wait_for_timeout(400)

        total = await pagina.evaluate("() => document.querySelectorAll('.slide').length")
        print(f"Slides encontrados: {total}")

        # Os halos passam da borda de proposito e sao recortados pelo overflow.
        # Medi-los junto transformava a checagem em alarme falso permanente.
        transbordo = await pagina.evaluate("""() => {
            document.querySelectorAll('.deco').forEach(d=>d.style.display='none');
            const fora=[];
            document.querySelectorAll('.slide').forEach((s,i)=>{
              if (s.scrollHeight > s.clientHeight + 2) fora.push([i+1, s.scrollHeight, s.clientHeight]);
            });
            document.querySelectorAll('.deco').forEach(d=>d.style.display='');
            return fora;
        }""")
        print("TRANSBORDO (slide, altura_real, altura_limite):", transbordo if transbordo else "nenhum")

        for i in range(total):
            await pagina.evaluate(IR_PARA, i)
            await pagina.wait_for_timeout(250)
            await pagina.screenshot(path=str(QA / f"qa_{i+1}.png"),
                                    clip={"x": 0, "y": 0, "width": VIEW_W, "height": VIEW_H})

        # ---- passo 2: export final, ampliado pelo device_scale_factor ----
        final = await navegador.new_page(viewport={"width": VIEW_W, "height": VIEW_H},
                                         device_scale_factor=SCALE)
        await final.set_content(SRC.read_text(encoding="utf-8"), wait_until="networkidle")
        await final.wait_for_timeout(3500)
        await final.evaluate(LIMPAR_MOLDURA)
        await final.wait_for_timeout(600)

        for i in range(total):
            await final.evaluate(IR_PARA, i)
            await final.wait_for_timeout(400)
            png = OUT / f"slide_{i+1:02d}.png"
            await final.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": VIEW_W, "height": VIEW_H})
            imagem = Image.open(png).convert("RGB")
            if imagem.size != (1080, 1350):
                imagem = imagem.resize((1080, 1350), Image.LANCZOS)
            imagem.save(OUT / f"slide_{i+1:02d}.jpg", quality=95)
            png.unlink()
            print(f"  slide_{i+1:02d}.jpg  {imagem.size[0]}x{imagem.size[1]}")

        await navegador.close()

    # ---- folha de contato: todos lado a lado ----
    imagens = [Image.open(QA / f"qa_{i}.png") for i in range(1, total + 1)]
    colunas = 3
    linhas = (total + colunas - 1) // colunas
    pad, rotulo = 18, 26
    w, h = imagens[0].size
    folha = Image.new("RGB", (colunas * w + pad * (colunas + 1),
                              linhas * (h + rotulo) + pad * (linhas + 1)), "#E8E8E8")
    desenho = ImageDraw.Draw(folha)
    for i, im in enumerate(imagens):
        c, r = i % colunas, i // colunas
        x, y = pad + c * (w + pad), pad + r * (h + rotulo + pad)
        desenho.text((x + 2, y), f"SLIDE {i+1}", fill="#5A5254")
        folha.paste(im, (x, y + rotulo))
    caminho = REPO / "out" / "folha_de_contato_testar.png"
    folha.save(caminho, quality=95)
    print(f"\nFolha de contato: {caminho}")
    print(f"JPEGs prontos em: {OUT}")


asyncio.run(main())
