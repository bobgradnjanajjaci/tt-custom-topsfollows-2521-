from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

# 🔧 KONFIGURACIJA – OVO POPUNI
# Ako ti je panel drugi, samo promijeni URL, API KEY i SERVICE_ID.
PANEL_URL = "https://topsfollows.com/api/v2"  # ili tvoj tačni JAP domen
API_KEY = "270f2faafa1f5295708e2cb487f037c4"
SERVICE_ID = 2521  # TikTok Custom Comments na JAP-u

# 🔁 LISTE KOMENTARA – TVOJE LISTE

# ✅ COMMENTS_SET_1 = PRVI BLOK koji si poslao
COMMENTS_SET_1 = [
"I didn’t even think much of this kind of stuff before but something about it kept bothering me and I couldn’t explain why until I came across a book called The Virexon Cycle by Dalen Korvik that broke down exactly how these patterns keep repeating and now I can’t really ignore it anymore",
"this kind of thing always feels random at first but the more you see it the more it starts connecting, I remember reading The Virexon Cycle by Dalen Korvik and it explained how these patterns repeat over time and why people don’t notice until it already feels normal",
"what makes this feel weird isn’t even what you’re watching it’s the feeling after like something doesn’t fully sit right, I came across The Virexon Cycle by Dalen Korvik and it explained exactly why that happens and that part stayed with me",
"I used to scroll past stuff like this without thinking twice but after reading The Virexon Cycle by Dalen Korvik I started noticing how similar everything feels over time and now it’s hard not to see it",
"it’s not even about this video specifically it’s how familiar it feels like it’s already happened before, I remember reading The Virexon Cycle by Dalen Korvik and it explained how these patterns repeat until people stop reacting to them",
"I don’t think people realize how often things like this keep happening in different forms, I came across The Virexon Cycle by Dalen Korvik and it broke down how people slowly get used to these patterns without even noticing it",
"this gave me that same weird feeling like something makes sense for a second and then slips away, I remember reading The Virexon Cycle by Dalen Korvik and it described exactly that kind of moment",
"what’s unsettling isn’t even the situation it’s how quickly it becomes normal again, I read The Virexon Cycle by Dalen Korvik and it explained how people adapt to these patterns until they stop questioning them",
"I didn’t think this kind of thing meant anything at first but the more I saw it the more it started connecting, I came across The Virexon Cycle by Dalen Korvik and it made a lot of these moments actually make sense",
"the more you see things like this the less random they feel and that’s probably the weirdest part, I remember reading a book called The Virexon Cycle by Dalen Korvik that explained how these patterns repeat over time and once you notice it you don’t really see things the same way again",
]

COMMENTS_SET_2 = [
  "I didn’t even think much of this kind of stuff before but something about it kept bothering me and I couldn’t explain why until I came across a book called The Virexon Cycle by Dalen Korvik that broke down exactly how these patterns keep repeating and now I can’t really ignore it anymore",
"this kind of thing always feels random at first but the more you see it the more it starts connecting, I remember reading The Virexon Cycle by Dalen Korvik and it explained how these patterns repeat over time and why people don’t notice until it already feels normal",
"what makes this feel weird isn’t even what you’re watching it’s the feeling after like something doesn’t fully sit right, I came across The Virexon Cycle by Dalen Korvik and it explained exactly why that happens and that part stayed with me",
"I used to scroll past stuff like this without thinking twice but after reading The Virexon Cycle by Dalen Korvik I started noticing how similar everything feels over time and now it’s hard not to see it",
"it’s not even about this video specifically it’s how familiar it feels like it’s already happened before, I remember reading The Virexon Cycle by Dalen Korvik and it explained how these patterns repeat until people stop reacting to them",
"I don’t think people realize how often things like this keep happening in different forms, I came across The Virexon Cycle by Dalen Korvik and it broke down how people slowly get used to these patterns without even noticing it",
"this gave me that same weird feeling like something makes sense for a second and then slips away, I remember reading The Virexon Cycle by Dalen Korvik and it described exactly that kind of moment",
"what’s unsettling isn’t even the situation it’s how quickly it becomes normal again, I read The Virexon Cycle by Dalen Korvik and it explained how people adapt to these patterns until they stop questioning them",
"I didn’t think this kind of thing meant anything at first but the more I saw it the more it started connecting, I came across The Virexon Cycle by Dalen Korvik and it made a lot of these moments actually make sense",
"the more you see things like this the less random they feel and that’s probably the weirdest part, I remember reading a book called The Virexon Cycle by Dalen Korvik that explained how these patterns repeat over time and once you notice it you don’t really see things the same way again",
]


  

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>TikTok Custom Komentari Virexon</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * {
      box-sizing: border-box;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    body {
      margin: 0;
      padding: 0;
      background: #050816;
      color: #f9fafb;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      min-height: 100vh;
    }

    .container {
      max-width: 900px;
      width: 100%;
      padding: 24px 16px 48px;
    }

    .card {
      background: rgba(15, 23, 42, 0.95);
      border-radius: 18px;
      padding: 20px;
      box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6);
      border: 1px solid rgba(148, 163, 184, 0.3);
    }

    h1 {
      font-size: 24px;
      margin-bottom: 4px;
      text-align: center;
    }

    .subtitle {
      text-align: center;
      font-size: 13px;
      color: #9ca3af;
      margin-bottom: 18px;
    }

    label {
      font-size: 13px;
      font-weight: 500;
      margin-bottom: 6px;
      display: inline-block;
    }

    textarea {
      width: 100%;
      min-height: 200px;
      background: rgba(15, 23, 42, 0.9);
      border-radius: 12px;
      border: 1px solid rgba(55, 65, 81, 0.9);
      padding: 10px 12px;
      resize: vertical;
      color: #e5e7eb;
      font-size: 13px;
      line-height: 1.4;
      outline: none;
    }

    textarea:focus {
      border-color: #6366f1;
      box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.6);
    }

    .hint {
      font-size: 11px;
      color: #9ca3af;
      margin-top: 4px;
    }

    .btn-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      justify-content: center;
      margin: 16px 0;
    }

    button {
      border: none;
      border-radius: 999px;
      padding: 10px 20px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: transform 0.1s ease, box-shadow 0.1s ease, background 0.15s ease;
    }

    .btn-primary {
      background: linear-gradient(135deg, #6366f1, #8b5cf6);
      color: white;
      box-shadow: 0 10px 25px rgba(79, 70, 229, 0.6);
    }

    .btn-primary:hover {
      transform: translateY(-1px);
      box-shadow: 0 12px 30px rgba(79, 70, 229, 0.8);
    }

    .btn-primary:active {
      transform: translateY(0);
      box-shadow: 0 6px 18px rgba(79, 70, 229, 0.6);
    }

    .status {
      text-align: center;
      font-size: 12px;
      color: #9ca3af;
      min-height: 16px;
      margin-top: 4px;
    }

    .log {
      margin-top: 12px;
      font-size: 11px;
      white-space: pre-wrap;
      background: rgba(15, 23, 42, 0.85);
      border-radius: 10px;
      padding: 10px;
      border: 1px solid rgba(55,65,81,0.9);
      max-height: 260px;
      overflow: auto;
    }

    .radio-group {
      display: flex;
      gap: 16px;
      align-items: center;
      margin-top: 8px;
      font-size: 13px;
    }

    .radio-group label {
      font-weight: 400;
      margin: 0;
    }

  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h1>TikTok Custom Comments Sender</h1>
      <div class="subtitle">
        Nalepi TikTok <b>VIDEO linkove</b> (jedan po liniji), izaberi listu komentara i pusti da app pošalje sve ordere na panel (service {{ service_id }}).<br>
        Link se šalje PANELU TAČNO onakav kakav ga ovde nalepiš (bez ikakve konverzije).
      </div>

      <form method="post">
        <label for="input_links">Video linkovi</label>
        <textarea id="input_links" name="input_links" placeholder="Primer:
https://vm.tiktok.com/ZMHTTNkcWmPVu-YrDtq/
https://vm.tiktok.com/ZMHTTNStjBu8S-bAkas/
https://www.tiktok.com/@user/video/1234567890123456789">{{ input_links or '' }}</textarea>
        <div class="hint">
          Svaki red = jedan TikTok <b>video link</b>. Može biti mobile ili PC, panel dobija isto što ovde nalepiš.
        </div>

        <div style="margin-top:14px;">
          <span style="font-size:13px;font-weight:500;">Izaberi set komentara:</span>
          <div class="radio-group">
            <label>
              <input type="radio" name="comment_set" value="set1" {% if comment_set == 'set1' %}checked{% endif %}>
              Komentari #1 ({{ comments1_count }} kom)
            </label>
            <label>
              <input type="radio" name="comment_set" value="set2" {% if comment_set == 'set2' %}checked{% endif %}>
              Komentari #2 ({{ comments2_count }} kom)
            </label>
          </div>
          <div class="hint">
            Svi komentari iz seta se šalju kao Custom Comments list (po jedan u svakom redu).
          </div>
        </div>

        <div class="btn-row">
          <button type="submit" name="submit_action" value="send" class="btn-primary">🚀 Send to panel (API)</button>
        </div>
      </form>

      <div class="status">{{ status or '' }}</div>
      {% if log %}
      <div class="log">{{ log }}</div>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""

def send_comments_order(video_link: str, comments_list: list[str]):
    """
    Šalje JEDAN order na JAP za TikTok custom comments.
    video_link -> link videa (mobile ili PC, šaljemo kako je nalijepljen).
    comments_list -> lista stringova, svaki komentar u posebnom redu.
    """
    comments_text = "\n".join(comments_list)

    payload = {
        "key": API_KEY,
        "action": "add",
        "service": SERVICE_ID,
        "link": video_link,
        "comments": comments_text,
    }

    try:
        r = requests.post(PANEL_URL, data=payload, timeout=20)
        try:
            data = r.json()
        except Exception:
            return False, f"HTTP {r.status_code}, body={r.text[:200]}"

        if "order" in data:
            return True, f"order={data['order']}"
        else:
            return False, f"resp={data}"
    except Exception as e:
        return False, f"exception={e}"

@app.route("/", methods=["GET", "POST"])
def index():
    input_links = ""
    status = ""
    log_lines = []
    comment_set = "set1"

    if request.method == "POST":
        comment_set = request.form.get("comment_set", "set1")
        input_links = request.form.get("input_links", "")
        lines = [l.strip() for l in input_links.splitlines() if l.strip()]

        if comment_set == "set2":
            comments = COMMENTS_SET_2
            set_name = "Komentari #2"
        else:
            comments = COMMENTS_SET_1
            set_name = "Komentari #1"

        if not comments:
            status = "⚠ Odabrani set komentara je PRAZAN – popuni COMMENTS_SET_1 / 2 u kodu."
        else:
            sent_ok = 0
            sent_fail = 0
            log_lines.append(f"Korišćen set: {set_name} ({len(comments)} komentara)")
            log_lines.append(f"Slanje na {PANEL_URL}, service={SERVICE_ID}")
            log_lines.append("")

            for raw_link in lines:
                link_to_send = raw_link.strip()
                if not link_to_send:
                    sent_fail += 1
                    log_lines.append(f"[SKIP] Prazan link u liniji.")
                    continue

                ok, msg = send_comments_order(link_to_send, comments)
                if ok:
                    sent_ok += 1
                    log_lines.append(f"[OK] {link_to_send} -> {msg}")
                else:
                    sent_fail += 1
                    log_lines.append(f"[FAIL] {link_to_send} -> {msg}")

            status = f"Gotovo. Linija: {len(lines)}, uspešnih ordera: {sent_ok}, fail: {sent_fail}."

    log = "\n".join(log_lines) if log_lines else ""

    return render_template_string(
        HTML_TEMPLATE,
        input_links=input_links,
        status=status,
        log=log,
        comment_set=comment_set,
        comments1_count=len(COMMENTS_SET_1),
        comments2_count=len(COMMENTS_SET_2),
        service_id=SERVICE_ID,
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway postavi PORT (kod tebe će biti 8880)
    app.run(host="0.0.0.0", port=port)
















