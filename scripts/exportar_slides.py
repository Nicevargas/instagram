"""
Exporta cada slide do carrossel como JPEG 1080x1350, pronto para o Instagram.

Detalhes que importam e ja custaram erro:
  - O layout FICA em 420x525. Quem amplia e o device_scale_factor.
    Se voce trocar o viewport para 1080x1350, o texto encolhe e tudo quebra.
  - Espera 3,5s pelas fontes do Google antes do primeiro print.
  - Converte para JPEG porque a Meta documenta apenas esse formato.

Uso:  python scripts/exportar_slides.py
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
SP = REPO / "out"
OUT = REPO / "slides"
OUT.mkdir(parents=True, exist_ok=True)
TOTAL, VIEW_W, VIEW_H = 9, 420, 525
SCALE = 1080 / 420

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": VIEW_W, "height": VIEW_H},
                                device_scale_factor=SCALE)
        await page.set_content((SP/"carrossel.html").read_text(encoding="utf-8"),
                               wait_until="networkidle")
        await page.wait_for_timeout(3500)           # fontes do Google
        await page.evaluate("""() => {
            document.querySelectorAll('.ig-header,.ig-dots,.ig-actions,.ig-caption')
                .forEach(e => e.style.display='none');
            const f=document.querySelector('.ig-frame');
            f.style.cssText='width:420px;height:525px;max-width:none;border-radius:0;box-shadow:none;overflow:hidden;margin:0;';
            const v=document.querySelector('.carousel-viewport');
            v.style.cssText='width:420px;height:525px;overflow:hidden;cursor:default;';
            document.body.style.cssText='padding:0;margin:0;display:block;overflow:hidden;';
        }""")
        await page.wait_for_timeout(600)
        for i in range(TOTAL):
            await page.evaluate("""(i)=>{const t=document.querySelector('.carousel-track');
                t.style.transition='none';t.style.transform='translateX('+(-i*420)+'px)';}""", i)
            await page.wait_for_timeout(400)
            png = OUT / f"slide_{i+1:02d}.png"
            await page.screenshot(path=str(png),
                clip={"x":0,"y":0,"width":VIEW_W,"height":VIEW_H})
            # Meta documenta apenas JPEG para publicacao de imagem
            jpg = OUT / f"slide_{i+1:02d}.jpg"
            Image.open(png).convert("RGB").save(jpg, "JPEG", quality=92, optimize=True)
            png.unlink()
            im = Image.open(jpg)
            print(f"  slide_{i+1:02d}.jpg  {im.size[0]}x{im.size[1]}  {jpg.stat().st_size/1024:.0f} KB")
        await b.close()

asyncio.run(main())
