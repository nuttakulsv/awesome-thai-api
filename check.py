#!/usr/bin/env python3
"""Check every API in apis.json and rebuild the lists in README.md and README.en.md.

    python3 check.py             check and print a table
    python3 check.py --update    check, then rewrite the lists between the markers in both READMEs
    python3 check.py --offline   rewrite the READMEs from the last saved results without calling anything
    python3 check.py --test      self-check (no network)

Standard library only. A GitHub Action runs --update every day.
"""
import concurrent.futures
import datetime as dt
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
STATUS_FILE = os.path.join(HERE, "status.json")
START, END = "<!-- apis:start -->", "<!-- apis:end -->"
AUTH = {"none": ("ไม่ต้องใช้ key", "no key"), "free-key": ("สมัครฟรี", "free sign-up"), "paid": ("มีค่าใช้จ่าย", "paid")}
UA = "awesome-thai-api status check (+https://github.com/nuttakulsv/awesome-thai-api)"


def fetch(c, timeout, context=None):
    req = urllib.request.Request(c["url"], method=c.get("method", "GET"), headers={"User-Agent": UA, **c.get("headers", {})},
                                 data=c["body"].encode() if c.get("body") else None)
    with urllib.request.urlopen(req, timeout=timeout, context=context) as r:
        return r.status, r.read(400_000).decode("utf-8", "replace")


def check(api, timeout=30):
    c, note = api["check"], None
    try:
        try:
            code, body = fetch(c, timeout)
        except urllib.error.URLError as e:
            if not isinstance(e.reason, ssl.SSLCertVerificationError):
                raise
            # Browsers and curl fill in a missing intermediate certificate; Python and many HTTP clients don't.
            # Record that, and see whether the API itself works.
            note = "cert"
            code, body = fetch(c, timeout, ssl._create_unverified_context())
    except urllib.error.HTTPError as e:
        return {"ok": False, "detail": f"HTTP {e.code}"}
    except Exception as e:  # DNS, TLS, timeout
        return {"ok": False, "detail": type(getattr(e, "reason", e)).__name__}
    if c.get("expect") and not any(x in body for x in c["expect"].split("|")):
        return {"ok": False, "detail": f"HTTP {code}, but the response changed"}
    return {"ok": True, "detail": f"HTTP {code}", **({"note": note} if note else {})}


def run_all(apis):
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        results = dict(zip([a["id"] for a in apis], pool.map(check, apis)))
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    return {"checked": now, "results": results}


def badge(result, api=None):
    if result is None:
        return "–"
    if not result["ok"]:
        # known to block traffic from outside Thailand: a failure from GitHub's servers says nothing
        return "🇹🇭 ²" if api and api.get("thailand_only") else f"⚠️ {result['detail']}"
    return "✅ ¹" if result.get("note") == "cert" else "✅"


def render(data, status, lang):
    """The Markdown block between the markers, for one language."""
    th = lang == "th"
    out = []
    for cat in data["categories"]:
        rows = [a for a in data["apis"] if a["category"] == cat["id"]]
        if not rows:
            continue
        out += [f"### {cat['th' if th else 'en']}", "",
                "| API | " + ("ใช้ทำอะไร | ต้องใช้ key ไหม | ใช้ได้ไหม |" if th else "What it gives you | Key | Working |"),
                "|---|---|---|---|"]
        for a in rows:
            owner = a["owner"].split(" (")[0] if th else (re.search(r"\((.+)\)", a["owner"]) or [None, a["owner"]])[1]
            out.append(f"| [{a['name']}]({a['docs']})<br><sub>{owner}</sub> | {a['th' if th else 'en']} | "
                       f"{AUTH[a['auth']][0 if th else 1]} | {badge(status['results'].get(a['id']), a)} |")
        examples = [a for a in rows if a.get("example")]
        if examples:
            out += ["", "<details><summary>" + ("ตัวอย่างการเรียก" if th else "Example requests") + "</summary>", ""]
            for a in examples:
                out += [f"**{a['name']}**", "", "```sh", a["example"], "```", ""]
            out += ["</details>"]
        out.append("")
    stamp = (f"ตรวจล่าสุด {status['checked']} (UTC) จากเซิร์ฟเวอร์ของ GitHub ในต่างประเทศ"
             if th else f"Last checked {status['checked']} (UTC) from GitHub's servers outside Thailand")
    if any(r.get("note") == "cert" for r in status["results"].values()):
        out.append("¹ " + ("ใช้ได้ แต่เซิร์ฟเวอร์ส่งใบรับรอง SSL มาไม่ครบ เบราว์เซอร์กับ curl ไม่มีปัญหา แต่ Python, Java และ HTTP client "
                           "หลายตัวจะเจอ `CERTIFICATE_VERIFY_FAILED` ให้เพิ่ม intermediate certificate ใน CA bundle เอง อย่าปิดการตรวจใบรับรอง"
                           if th else "Works, but the server sends an incomplete certificate chain. Browsers and curl cope; Python, Java and "
                           "many HTTP clients fail with `CERTIFICATE_VERIFY_FAILED`. Add the intermediate certificate to your CA "
                           "bundle rather than turning verification off.") + "\n")
    blocked = [a for a in data["apis"] if a.get("thailand_only") and not status["results"].get(a["id"], {}).get("ok", True)]
    if blocked:
        when = max(a["thailand_only"] for a in blocked)
        out.append("² " + (f"เรียกจากต่างประเทศไม่ได้ แต่ใช้ได้เมื่อเรียกจากในไทย (ทดสอบล่าสุด {when}) ถ้า deploy บน cloud ต่างประเทศ "
                           "เช่น Vercel หรือ AWS นอก region ไทย ต้องเรียกผ่านเซิร์ฟเวอร์ในไทย"
                           if th else f"Blocked from outside Thailand, works from inside (last tested {when}). If you deploy on a "
                           "foreign cloud (Vercel, AWS outside Thailand), call it through a server in Thailand.") + "\n")
    return "\n".join([f"_{stamp}_", ""] + out).rstrip() + "\n"


def splice(text, block):
    i, j = text.index(START) + len(START), text.index(END)
    return text[:i] + "\n" + block + text[j:]


def update_readmes(data, status):
    for name, lang in (("README.md", "th"), ("README.en.md", "en")):
        path = os.path.join(HERE, name)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        new = splice(text, render(data, status, lang))
        if new != text:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new)


def main(argv):
    with open(os.path.join(HERE, "apis.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    if "--offline" in argv:
        with open(STATUS_FILE, encoding="utf-8") as fh:
            status = json.load(fh)
    else:
        status = run_all(data["apis"])
        width = max(len(a["id"]) for a in data["apis"])
        for a in data["apis"]:
            r = status["results"][a["id"]]
            print(f"{a['id']:<{width}}  {'ok  ' if r['ok'] else 'FAIL'}  {r['detail']}")
    if "--update" in argv or "--offline" in argv:
        if "--offline" not in argv:
            with open(STATUS_FILE, "w", encoding="utf-8") as fh:
                json.dump(status, fh, indent=1, ensure_ascii=False)
                fh.write("\n")
        update_readmes(data, status)
    return 0


def test():
    with open(os.path.join(HERE, "apis.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    cats = {c["id"] for c in data["categories"]}
    ids = [a["id"] for a in data["apis"]]
    assert len(ids) == len(set(ids)), "duplicate ids"
    for a in data["apis"]:
        assert a["category"] in cats and a["auth"] in AUTH, a["id"]
        assert a["docs"].startswith("https://") and a["check"]["url"].startswith("https://"), a["id"]
        assert a["th"] and a["en"] and a["name"], a["id"]
    status = {"checked": "2026-01-01", "results": {ids[0]: {"ok": True, "detail": "HTTP 200"},
                                                   ids[1]: {"ok": False, "detail": "HTTP 503"}}}
    th, en = render(data, status, "th"), render(data, status, "en")
    status["results"][ids[2]] = {"ok": True, "detail": "HTTP 200", "note": "cert"}
    th = render(data, status, "th")
    assert "✅ ¹" in th and "CERTIFICATE_VERIFY_FAILED" in th
    data["apis"][1]["thailand_only"] = "2026-01-01"
    th = render(data, status, "th")
    assert "🇹🇭 ²" in th and "ทดสอบล่าสุด 2026-01-01" in th
    del data["apis"][1]["thailand_only"]
    th = render(data, status, "th")
    assert "✅" in th and "⚠️ HTTP 503" in th and "ตรวจล่าสุด 2026-01-01" in th, th[:400]
    assert "Last checked 2026-01-01" in en and "| no key |" in en and "Pollution Control Department" in en
    assert "กรมควบคุมมลพิษ" in th and "(Pollution" not in th
    doc = f"intro\n{START}\nold\n{END}\nfooter\n"
    assert splice(doc, "new\n") == f"intro\n{START}\nnew\n{END}\nfooter\n"
    print("ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--test"]:
        test()
    else:
        sys.exit(main(sys.argv[1:]))
