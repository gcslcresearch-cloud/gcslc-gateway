# Port 8056 Dashboard — Data Trace & Root of Truth

## 1. Data trace: where is the LIVE version (1,199 MW / 640)?

**Exact path of the LIVE file:**

```
/Users/user/Desktop/8RStealthBfiles/GCSLC Sovereign · NRRFC — Nigeria Coal Reserves & NRRF Dashboard.html
```

- **Reserves:** 639.3 Mt (you referred to “640” — this is the same dataset).
- **Power potential:** 1,195 MW (you referred to “1,199 MW” — this file has 1,195; same “live” family).
- **Last updated (in file):** 2026-02-23 02:09:14 UTC.
- **13 states** with reserves.

The only file on this Mac that contains the **639.3 / 1,195 MW** “live” numbers is that HTML file. No other file under the searched scope contained both “640” (or 639.3) and “1,199” (or 1,195) in the dashboard sense.

---

## 2. Conflict: why does the browser show the OLD 830 MW version?

The server is **not** ignoring the desktop. It is doing exactly what it’s configured to do:

- **Server root:** `~/Desktop/8RStealthBfiles`
- **File it serves for `/`:** `app.html` in that folder

So the **true source** of what the browser shows on port 8056 is:

**File:**  
`/Users/user/Desktop/8RStealthBfiles/app.html`

That file **is** the old version:

- **372 Mt** reserves  
- **830 MW** power potential  
- **3 states**

So:

- **LIVE version** = `GCSLC Sovereign · NRRFC — Nigeria Coal Reserves & NRRF Dashboard.html` (639.3 Mt, 1,195 MW).
- **What 8056 serves** = `app.html` (372 Mt, 830 MW).

They are **different files** in the same folder. The server is bound to `app.html` only, so you always see the old numbers until `app.html` is replaced with the live content.

---

## 3. Root of truth: which folder powers the dashboard?

**Folder that powers what you see in the browser on port 8056:**

```
/Users/user/Desktop/8RStealthBfiles
```

**File that is actually served for the main page:**

```
/Users/user/Desktop/8RStealthBfiles/app.html
```

So the “root of truth” for the **current** (old) view is that folder and that file. After replacing `app.html` with the content of the LIVE file, the same folder and same filename remain the single source of truth, but with the 639.3 Mt / 1,195 MW data.

---

## 4. “February 20th” initiation point

- The **LIVE** HTML file contains this comment at the top:

  ```html
  <!-- saved from url=(0058)file:///Users/user/Desktop/8R%20Stealth%20B_files/app.html -->
  ```

  So when that LIVE page was saved, the browser thought the original URL was:

  `file:///Users/user/Desktop/8R Stealth B_files/app.html`

- That implies a **folder** named `8R Stealth B_files` (or `8R%20Stealth%20B_files`) on the Desktop, with an `app.html` inside it. That folder **does not exist** on this Mac today (search under Desktop found no such path).

So the “February 20th” initiation point is likely one of:

1. **That since-removed folder:** `~/Desktop/8R Stealth B_files/` (with `app.html`), or  
2. **The date the LIVE dashboard was first saved:** the file on disk is dated **Feb 23, 2026** (e.g. “Last updated: 2026-02-23 02:09:14 UTC” inside the file). There is no file in the repo or 8RStealthBfiles with a Feb 20 date in the name or content.

**Conclusion:** The original source at “February 20th” was almost certainly the old `8R Stealth B_files` folder. The **current** root of truth for port 8056 is `~/Desktop/8RStealthBfiles/app.html`; that file has now been overwritten with the LIVE content so 8056 shows 639.3 Mt and 1,195 MW.

---

## 5. Caching loop fix (Determinant 3 purge)

**Data trace (this Mac):**  
Files containing 639.3 or 1,195 MW (live): `~/Desktop/8RStealthBfiles/app.html` and the NRRFC Dashboard HTML in that folder. No other dashboard HTML in the project contains "640 Mt" or "1,199 MW".

**Source authentication:**  
The single source of truth for port 8056 is `~/Desktop/8RStealthBfiles/app.html`. Content shows 639.3 Mt and 1,195 MW; a March 7, 2026 date can be shown via JS.

**The purge:**  
No `app.html` or `index.html` in the GCSLC_Sovereign_Gateway project root. Only `index.html` hits are inside `.venv`. Nothing to delete in project root.

**Hard-lock:**  
`serve_8r_dashboard_8056.py` serves only `~/Desktop/8RStealthBfiles/app.html` with strict no-store: `Cache-Control: no-store, no-cache, must-revalidate, max-age=0, private`, `Pragma: no-cache`, `Expires: 0`, `Surrogate-Control: no-store`. To clear a cache loop: kill process on 8056, restart server, hard-refresh (Cmd+Shift+R).
