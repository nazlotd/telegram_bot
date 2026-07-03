from html import escape
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = PROJECT_ROOT / "MENU_MINDMAP.html"


MENU_SECTIONS = [
    {
        "class_name": "purple",
        "title": "User Main Menu",
        "description": "Menu utama yang user nampak selepas /start atau /menu.",
        "items": [
            "OR",
            "GE",
            "4 RM10_PERAYAAN",
            "COUNTER A,B / P.WING / STANDEE",
            "DATE INFO",
        ],
    },
    {
        "class_name": "blue",
        "title": "Promo Categories",
        "description": "Pilihan promo yang user boleh buka untuk tengok gambar.",
        "items": [
            "OR 1 - OR 5: 2 gambar + effective date",
            "GE 1 - GE 5: 2 gambar + effective date",
            "4 RM10: 1 gambar + effective date",
            "COUNTER A/B: 2 gambar + effective date",
            "P.WING: 1 gambar + effective date",
        ],
    },
    {
        "class_name": "cyan",
        "title": "Standee Submenu",
        "description": "Submenu khas untuk item standee tanpa tarikh.",
        "items": [
            "STANDEE",
            "CAT: 1 gambar tanpa effective date",
            "DETTOL: 1 gambar tanpa effective date",
            "DUTH LADY: 1 gambar tanpa effective date",
        ],
    },
    {
        "class_name": "green",
        "title": "Admin Update Flow",
        "description": "Flow admin untuk update gambar promo dan simpan perubahan.",
        "items": [
            "UPDATE OR / GE: pilih nombor 1-5",
            "Upload Gambar A dan Gambar B",
            "Masukkan tarikh mula dan tarikh tamat",
            "Preview promo sebelum simpan",
            "CONFIRM UPDATE atau CANCEL UPDATE",
        ],
    },
    {
        "class_name": "yellow",
        "title": "Admin Tools",
        "description": "Menu admin untuk pantau user, promo dan data bot.",
        "items": [
            "PROMO LIST",
            "USER LIST",
            "ADMIN STATS",
            "STORAGE INFO",
            "BACKUP DATA",
            "RESTORE DATA",
        ],
    },
    {
        "class_name": "orange",
        "title": "Data & Deploy",
        "description": "Fail penting yang menyokong bot dan deployment Railway.",
        "items": [
            "data.json: simpan promo dan file_id gambar",
            "users.json: simpan rekod user",
            "intro.jpeg: gambar intro bot",
            "runtime.txt: Python 3.11.9",
            "mise.toml: fix Railway Python install",
        ],
    },
]


STYLE = """
    :root {
      --bg: #f8fbff;
      --ink: #121722;
      --muted: #4b5563;
      --purple: #c05be8;
      --blue: #53a7e8;
      --cyan: #52dce2;
      --green: #7ee46b;
      --yellow: #f1d85f;
      --orange: #f5a553;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--ink);
      font-family: Arial, Helvetica, sans-serif;
      padding: 24px;
    }

    .page {
      width: min(1180px, 100%);
      margin: 0 auto;
      background: #fff;
      border: 1px solid #e5e7eb;
      box-shadow: 0 18px 48px rgba(15, 23, 42, 0.08);
      padding: 26px 28px 34px;
    }

    h1 {
      margin: 0 0 28px;
      padding: 0 0 18px;
      font-size: 34px;
      line-height: 1.1;
      border-bottom: 7px solid #a9d6ff;
      letter-spacing: 0;
    }

    .mindmap {
      display: grid;
      grid-template-columns: 190px 1fr;
      gap: 34px;
      align-items: center;
    }

    .root {
      min-height: 640px;
      display: grid;
      grid-template-columns: 1fr 12px;
      align-items: center;
      gap: 14px;
    }

    .root-title {
      font-size: 34px;
      font-weight: 800;
      line-height: 1.15;
      text-align: center;
    }

    .root-bar {
      height: 430px;
      border-radius: 999px;
      background: linear-gradient(
        to bottom,
        var(--purple),
        var(--blue),
        var(--cyan),
        var(--green),
        var(--yellow),
        var(--orange)
      );
    }

    .branches {
      display: grid;
      gap: 22px;
      position: relative;
    }

    .branch {
      display: grid;
      grid-template-columns: 270px 1fr;
      gap: 26px;
      align-items: start;
      position: relative;
    }

    .branch::before {
      content: "";
      position: absolute;
      left: -30px;
      top: 24px;
      width: 34px;
      border-top: 4px solid var(--color);
      border-radius: 999px;
    }

    .branch-head {
      display: grid;
      grid-template-columns: 18px 1fr;
      gap: 10px;
      align-items: start;
      position: relative;
    }

    .dot {
      width: 18px;
      height: 18px;
      margin-top: 5px;
      border-radius: 50%;
      background: var(--color);
      box-shadow: 0 0 0 5px color-mix(in srgb, var(--color), white 72%);
    }

    .title {
      font-size: 23px;
      line-height: 1.15;
      font-weight: 800;
      margin: 0 0 7px;
    }

    .desc {
      margin: 0;
      max-width: 210px;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.35;
    }

    .items {
      display: grid;
      gap: 8px;
      position: relative;
      padding-left: 20px;
    }

    .items::before {
      content: "";
      position: absolute;
      left: 0;
      top: 18px;
      bottom: 18px;
      border-left: 3px solid var(--color);
      border-radius: 999px;
    }

    .item {
      min-height: 35px;
      display: grid;
      align-items: center;
      padding: 7px 12px;
      border: 2px dashed #111827;
      border-radius: 8px;
      background: color-mix(in srgb, var(--color), white 78%);
      font-size: 14px;
      font-weight: 700;
      text-align: center;
      position: relative;
    }

    .item::before {
      content: "";
      position: absolute;
      left: -22px;
      top: 50%;
      width: 20px;
      border-top: 3px solid var(--color);
    }

    .purple { --color: var(--purple); }
    .blue { --color: var(--blue); }
    .cyan { --color: var(--cyan); }
    .green { --color: var(--green); }
    .yellow { --color: var(--yellow); }
    .orange { --color: var(--orange); }

    @media (max-width: 860px) {
      h1 {
        font-size: 26px;
      }

      .mindmap {
        grid-template-columns: 1fr;
      }

      .root {
        min-height: auto;
        grid-template-columns: 1fr;
      }

      .root-bar {
        width: 100%;
        height: 10px;
      }

      .branch {
        grid-template-columns: 1fr;
      }

      .branch::before,
      .items::before,
      .item::before {
        display: none;
      }

      .items {
        padding-left: 0;
      }
    }
"""


def render_section(section):
    items = "\n".join(
        f'            <div class="item">{escape(item)}</div>'
        for item in section["items"]
    )
    return f"""        <section class="branch {escape(section["class_name"])}">
          <div class="branch-head">
            <div class="dot"></div>
            <div>
              <h2 class="title">{escape(section["title"])}</h2>
              <p class="desc">{escape(section["description"])}</p>
            </div>
          </div>
          <div class="items">
{items}
          </div>
        </section>"""


def render_html():
    sections = "\n\n".join(render_section(section) for section in MENU_SECTIONS)
    return f"""<!doctype html>
<html lang="ms">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NazsBot Menu Mind Map</title>
  <style>
{STYLE}
  </style>
</head>
<body>
  <main class="page">
    <h1>NazsBot Menu & Admin Structure</h1>

    <section class="mindmap">
      <section class="root">
        <div class="root-title">NazsBot<br>Telegram<br>Bot</div>
        <div class="root-bar"></div>
      </section>

      <section class="branches">
{sections}
      </section>
    </section>
  </main>
</body>
</html>
"""


def main():
    OUTPUT_FILE.write_text(render_html(), encoding="utf-8")
    print(f"Generated {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
