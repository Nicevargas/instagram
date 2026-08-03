"""
Confere os slides antes de exportar: detecta texto transbordando e gera
uma folha de contato com todos lado a lado.

Ver os slides juntos pega erro que o preview arrastavel esconde -- foi
assim que apareceram a pilula esticada e o degrade por cima do rosto.

Uso:  python scripts/conferir_slides.py
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

REPO = Path(__file__).resolve().parent.parent
SP = REPO / "out"
OUT = SP / "qa"; OUT.mkdir(parents=True, exist_ok=True)
TOTAL, W, H = 9, 420, 525

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        await page.set_content((SP/"carrossel.html").read_text(encoding="utf-8"), wait_until="networkidle")
        await page.wait_for_timeout(3000)
        await page.evaluate("""() => {
            document.querySelectorAll('.ig-header,.ig-dots,.ig-actions,.ig-caption').forEach(e=>e.style.display='none');
            const f=document.querySelector('.ig-frame');
            f.style.cssText='width:420px;height:525px;max-width:none;border-radius:0;box-shadow:none;overflow:hidden;margin:0;';
            const v=document.querySelector('.carousel-viewport');
            v.style.cssText='width:420px;height:525px;overflow:hidden;cursor:default;';
            document.body.style.cssText='padding:0;margin:0;display:block;overflow:hidden;';
        }""")
        await page.wait_for_timeout(400)
        # detecta transbordo de conteudo em cada slide
        overflow = await page.evaluate("""() => {
            const out=[];
            document.querySelectorAll('.slide').forEach((s,i)=>{
              if (s.scrollHeight > s.clientHeight + 2) out.push([i+1, s.scrollHeight, s.clientHeight]);
            });
            return out;
        }""")
        print("TRANSBORDO (slide, altura_real, altura_limite):", overflow if overflow else "nenhum")
        for i in range(TOTAL):
            await page.evaluate("""(i)=>{const t=document.querySelector('.carousel-track');
                t.style.transition='none';t.style.transform='translateX('+(-i*420)+'px)';}""", i)
            await page.wait_for_timeout(250)
            await page.screenshot(path=str(OUT/f"qa_{i+1}.png"), clip={"x":0,"y":0,"width":W,"height":H})
        await b.close()

    # folha de contato: todos os slides lado a lado
    from PIL import Image, ImageDraw
    imgs = [Image.open(OUT / f"qa_{i}.png") for i in range(1, TOTAL + 1)]
    cols = 3
    rows = (TOTAL + cols - 1) // cols
    pad, lbl = 18, 26
    w, h = imgs[0].size
    sheet = Image.new("RGB", (cols * w + pad * (cols + 1),
                              rows * (h + lbl) + pad * (rows + 1)), "#E8E8E8")
    d = ImageDraw.Draw(sheet)
    for i, im in enumerate(imgs):
        c, r = i % cols, i // cols
        x, y = pad + c * (w + pad), pad + r * (h + lbl + pad)
        d.text((x + 2, y), f"SLIDE {i+1}", fill="#5A5254")
        sheet.paste(im, (x, y + lbl))
    folha = SP / "folha_de_contato.png"
    sheet.save(folha, quality=95)
    print(f"Folha de contato: {folha}")

asyncio.run(main())
