# Como publicar um carrossel no Instagram

Pipeline do **@nicevargas.mkt** / Café com Internet.
Do zero ao post no ar em 4 comandos.

---

## O caminho rápido

```bash
cd C:/Users/eunic/claude-instagram

python scripts/gerar_carrossel.py      # 1. monta o HTML
python scripts/conferir_slides.py      # 2. confere (folha de contato em out/)
python scripts/exportar_slides.py      # 3. exporta JPEG 1080x1350 em slides/
python scripts/publish_instagram.py --images "slides/slide_*.jpg" --caption "$(cat slides/legenda.txt)" --dry-run
```

Se o dry-run passar, repita o último comando **sem** `--dry-run`.

> Sempre olhe a folha de contato antes de exportar. Ver os slides lado a lado
> pega erro que o preview arrastável esconde — foi assim que apareceram a
> pílula esticada e o degradê passando por cima do rosto.

---

## Onde mexer para uma nova semana

Só o `scripts/gerar_carrossel.py`:

| O quê | Onde |
|---|---|
| Agenda resumida | lista `week` (slide 2) |
| Um card por compromisso | slides 3, 4 e 5 |
| Episódios publicados | lista `eps` (slide 6) |
| Quantidade de slides | constante `TOTAL` (ajuste também em `exportar_slides.py` e `conferir_slides.py`) |

Cores e fonte saíram do CSS do site e não precisam mudar:
rosé `#E8728A`, vinho `#A13B53`, **Hanken Grotesk**.

A legenda fica em `slides/legenda.txt`. Limites: 2.200 caracteres, 30 hashtags.

---

## Identidade da marca

| Token | Valor | Origem |
|---|---|---|
| `BRAND_PRIMARY` | `#E8728A` | CSS do site (16 elementos) |
| `BRAND_DARK` | `#A13B53` | CSS do site (7 elementos) |
| Fonte | Hanken Grotesk | CSS do site (884 elementos) |
| Logo | `assets/icone_xicara.png` | `agencia.curtatche.com.br/icone_xicara_sf.png` |

O site `agencia.curtatche.com.br` é só um `<iframe>` apontando para
`podcast-nu-blush.vercel.app` — o conteúdo real está lá.

### Fotos

Não versionadas (ficam no `.gitignore`). Origem no Google Drive:

- Pasta: `1BuHUSkOcz8la5L2P0CIfz2l1oclBcjB5`
- Foto usada: `1yNtwBlK0zUZsT4lgf2nyK1hk0apq-cUN` (camisa branca, fundo preto)
- Baixar: `https://lh3.googleusercontent.com/d/<ID>=w2000`

Para achar uma foto na pasta sem abrir uma por uma, baixe miniaturas
(`=w220`) e ordene por brilho médio com `PIL.ImageStat` — foi assim que
isolei as de fundo escuro em segundos.

---

## Armadilhas já resolvidas

Cada uma custou uma tentativa fracassada. Estão corrigidas no código, mas
saber o porquê evita reintroduzir.

**Host de imagem.** A API da Meta não aceita upload local — exige URL pública.
O `catbox.moe` está inacessível desta rede e o `0x0.st` desativou uploads
(HTTP 503). O `tmpfiles.org` devolve HTML, não o arquivo. **A solução é servir
do próprio repositório** via `raw.githubusercontent.com`, que entrega
`image/jpeg` de verdade. O script faz isso sozinho (commit + push + URL).

**Erros temporários da Meta.** A API devolve `is_transient: True` com alguma
frequência ao criar container. Não é falha sua — o script repete com espera
crescente (4s, 8s, 16s). Sem isso, a publicação inteira aborta.

**Emoji no console.** O terminal do Windows usa cp1252 e quebra ao imprimir 👇.
O script força UTF-8 na saída. Isso afeta só a tela; a legenda sempre foi
para a API em UTF-8.

**PNG vs JPEG.** A Meta documenta apenas JPEG. O `exportar_slides.py` já
converte. Não pule esse passo.

**Escala do export.** O layout **fica** em 420×525 e quem amplia para 1080 é o
`device_scale_factor`. Se você trocar o viewport para 1080×1350 direto, o
texto encolhe e o espaçamento quebra.

**Emoji nos slides.** O Chromium headless não tem fonte de emoji colorido —
eles saem como manchas cinzas. Use SVG inline (função `icon()` no gerador).

**Imagem que cruza dois slides.** A foto de continuidade é uma imagem de
2100×1312 (dois slides de largura) posicionada com `left: 0` no slide 6 e
`left: -420px` no 7. Ao montar a tela dupla, **estique as colunas da borda**
da foto para preencher as sobras — preenchimento chapado cria uma emenda
vertical visível.

---

## Credenciais

`.env` (nunca versionado):

```
INSTAGRAM_BUSINESS_ID=17841403275865899
INSTAGRAM_ACCESS_TOKEN=IGAA...
INSTAGRAM_API_BASE=https://graph.instagram.com
META_API_VERSION=v23.0
```

Rota: **Instagram API with Instagram Login** (`graph.instagram.com`, token
`IGAA...`, endpoints via `/me`). **Não** é a rota de Página do Facebook —
aquela falhou porque o token de usuário vinha sem `pages_show_list`.

Token dura ~60 dias. Renovar:

```bash
curl "https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=SEU_TOKEN"
```

Conferir se está vivo:

```bash
python scripts/publish_instagram.py --images "slides/slide_01.jpg" --caption "teste" --dry-run
```

Permissões concedidas: publicar, ler mídia, **mensagens** e **comentários**
(estas duas servem para a automação do "EU QUERO").

Cota: 100 publicações por 24h.

---

## Checklist antes de publicar

- [ ] Folha de contato revisada, slides lado a lado
- [ ] Datas e horários batem com o site
- [ ] Legenda dentro de 2.200 caracteres e 30 hashtags
- [ ] Dry-run passou
- [ ] Se a legenda promete DM, a automação está no ar
