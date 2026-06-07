<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MOONSIDE — Institutional Market Intelligence Platform</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#050507;--bg2:#08080C;--bg3:#0D0D12;--bg4:#111118;
  --surface:rgba(255,255,255,0.03);--surface2:rgba(255,255,255,0.055);
  --border:rgba(255,255,255,0.06);--border2:rgba(255,255,255,0.1);
  --accent:#7C3AED;--accent2:#A855F7;
  --text:#F5F5F7;--text2:#98989F;--text3:#3D3D45;
  --up:#34C759;--down:#FF3B30;--blue:#007AFF;--gold:#FF9F0A;
  --mono:'SF Mono','Menlo','Monaco','Courier New',monospace;
}
html{scroll-behavior:smooth}
body{
  font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','SF Pro Text','Helvetica Neue',Arial,sans-serif;
  background:var(--bg);color:var(--text);overflow-x:hidden;
  -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;
}
body::after{
  content:'';position:fixed;inset:0;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.025'/%3E%3C/svg%3E");
  pointer-events:none;z-index:9999;opacity:0.7;
}
::-webkit-scrollbar{width:3px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:rgba(124,58,237,0.35);border-radius:2px}

/* TICKER */
.ticker-wrap{width:100%;background:rgba(255,255,255,0.018);border-bottom:1px solid var(--border);overflow:hidden;height:36px;display:flex;align-items:center;}
.ticker-track{display:flex;gap:0;animation:ticker 60s linear infinite;white-space:nowrap;}
.ticker-track:hover{animation-play-state:paused}
@keyframes ticker{from{transform:translateX(0)}to{transform:translateX(-50%)}}
.tick-item{display:inline-flex;align-items:center;gap:8px;padding:0 24px;font-family:var(--mono);font-size:11px;border-right:1px solid var(--border);}
.tick-sym{color:var(--text2);font-weight:500;letter-spacing:0.04em}
.tick-price{color:var(--text);font-weight:400}
.tick-chg{font-size:10px;padding:1px 5px;border-radius:3px;font-weight:500}
.tick-up{color:var(--up);background:rgba(52,199,89,0.1)}
.tick-dn{color:var(--down);background:rgba(255,59,48,0.1)}
.tick-cat{font-size:8px;letter-spacing:0.1em;text-transform:uppercase;padding:2px 6px;border-radius:3px;font-weight:600;}
.cat-fx{background:rgba(0,122,255,0.12);color:#007AFF;border:1px solid rgba(0,122,255,0.2)}
.cat-crypto{background:rgba(255,159,10,0.12);color:#FF9F0A;border:1px solid rgba(255,159,10,0.2)}
.cat-idx{background:rgba(124,58,237,0.12);color:#A78BFA;border:1px solid rgba(124,58,237,0.2)}

/* NAV */
nav{position:sticky;top:0;z-index:100;height:52px;display:flex;align-items:center;justify-content:space-between;padding:0 48px;background:rgba(5,5,7,0.88);backdrop-filter:saturate(180%) blur(20px);-webkit-backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid var(--border);}
.nav-logo{display:flex;align-items:center;gap:10px;text-decoration:none;}
.nav-logo-mark{width:26px;height:26px;background:var(--accent);border-radius:7px;display:flex;align-items:center;justify-content:center;}
.nav-wordmark{font-size:14px;font-weight:700;letter-spacing:0.1em;color:var(--text);text-transform:uppercase}
.nav-links{display:flex;gap:28px;list-style:none;position:absolute;left:50%;transform:translateX(-50%);}
.nav-links a{font-size:12.5px;color:var(--text3);text-decoration:none;transition:color 0.15s;}
.nav-links a:hover{color:var(--text2)}
.nav-right{display:flex;align-items:center;gap:8px}
.nbtn{padding:6px 14px;border-radius:7px;font-size:12px;font-family:inherit;font-weight:500;cursor:pointer;transition:all 0.15s;text-decoration:none;display:inline-flex;align-items:center;}
.nbtn-ghost{background:transparent;border:1px solid var(--border2);color:var(--text2)}
.nbtn-ghost:hover{background:var(--surface2);color:var(--text)}
.nbtn-fill{background:var(--accent);border:1px solid transparent;color:#fff}
.nbtn-fill:hover{background:var(--accent2);box-shadow:0 0 18px rgba(124,58,237,0.3)}

/* HERO */
#hero{padding:96px 48px 80px;text-align:center;position:relative;overflow:hidden;}
.hero-orb-1{position:absolute;width:700px;height:500px;background:radial-gradient(ellipse,rgba(124,58,237,0.18) 0%,transparent 65%);top:-100px;left:50%;transform:translateX(-50%);filter:blur(80px);pointer-events:none;}
.hero-orb-2{position:absolute;width:300px;height:240px;background:radial-gradient(ellipse,rgba(80,20,180,0.1) 0%,transparent 65%);top:40%;left:5%;filter:blur(60px);pointer-events:none;}
.hero-orb-3{position:absolute;width:280px;height:220px;background:radial-gradient(ellipse,rgba(90,30,170,0.09) 0%,transparent 65%);top:35%;right:4%;filter:blur(60px);pointer-events:none;}
.hero-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,0.015) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.015) 1px,transparent 1px);background-size:64px 64px;mask-image:radial-gradient(ellipse 85% 70% at 50% 40%,black,transparent);pointer-events:none;}
.hero-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(124,58,237,0.09);border:1px solid rgba(124,58,237,0.22);border-radius:100px;padding:5px 14px;font-size:11px;color:#C4B5FD;letter-spacing:0.08em;text-transform:uppercase;font-weight:600;margin-bottom:28px;position:relative;z-index:1;animation:fadeUp 0.7s ease both;}
.hb-dot{width:5px;height:5px;border-radius:50%;background:var(--up);box-shadow:0 0 6px var(--up);animation:blink 2s infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.25}}
.hero-h{font-size:clamp(42px,5.8vw,78px);font-weight:700;line-height:1.03;letter-spacing:-0.04em;max-width:820px;margin:0 auto 20px;position:relative;z-index:1;animation:fadeUp 0.7s 0.08s ease both;color:var(--text);}
.hero-h-accent{background:linear-gradient(135deg,#C4B5FD 0%,#9333EA 50%,#C026D3 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-sub{font-size:16.5px;color:var(--text2);max-width:500px;margin:0 auto 38px;line-height:1.68;font-weight:300;position:relative;z-index:1;animation:fadeUp 0.7s 0.16s ease both;letter-spacing:-0.01em;}
.hero-ctas{display:flex;gap:12px;align-items:center;margin-bottom:64px;position:relative;z-index:1;justify-content:center;flex-wrap:wrap;animation:fadeUp 0.7s 0.24s ease both;}
.btn-p{padding:12px 24px;background:var(--accent);border:none;border-radius:10px;color:#fff;font-size:14px;font-family:inherit;font-weight:600;cursor:pointer;transition:all 0.2s;text-decoration:none;display:inline-flex;align-items:center;gap:7px;letter-spacing:-0.01em;box-shadow:0 0 0 1px rgba(124,58,237,0.25),0 8px 24px rgba(124,58,237,0.22);}
.btn-p:hover{background:var(--accent2);transform:translateY(-1px);box-shadow:0 0 0 1px rgba(168,85,247,0.35),0 16px 36px rgba(124,58,237,0.35);}
.btn-s{padding:12px 24px;background:rgba(255,255,255,0.04);border:1px solid var(--border2);border-radius:10px;color:var(--text2);font-size:14px;font-family:inherit;font-weight:400;cursor:pointer;transition:all 0.2s;text-decoration:none;display:inline-flex;align-items:center;gap:7px;}
.btn-s:hover{background:rgba(255,255,255,0.07);color:var(--text)}

/* HERO DASH */
.hero-dash{width:100%;max-width:1100px;margin:0 auto;position:relative;z-index:1;animation:fadeUp 0.7s 0.32s ease both;}
.dash-glow{position:absolute;bottom:-60px;left:50%;transform:translateX(-50%);width:75%;height:220px;background:radial-gradient(ellipse,rgba(124,58,237,0.28) 0%,transparent 65%);filter:blur(50px);pointer-events:none;}
.dash-frame{background:#0A0A0F;border:1px solid rgba(255,255,255,0.08);border-radius:14px;overflow:hidden;box-shadow:0 0 0 1px rgba(255,255,255,0.03),0 40px 80px rgba(0,0,0,0.75),0 80px 140px rgba(0,0,0,0.4);position:relative;z-index:1;}
.dash-tb{height:40px;display:flex;align-items:center;padding:0 16px;gap:6px;background:rgba(255,255,255,0.018);border-bottom:1px solid rgba(255,255,255,0.05);}
.wc{width:10px;height:10px;border-radius:50%}
.wc-r{background:#FF5F57}.wc-y{background:#FEBC2E}.wc-g{background:#28C840}
.dash-urlbar{flex:1;max-width:240px;margin-left:10px;height:22px;background:rgba(255,255,255,0.035);border:1px solid rgba(255,255,255,0.05);border-radius:5px;display:flex;align-items:center;padding:0 10px;gap:5px;font-size:10px;color:var(--text3);font-family:var(--mono);}
.dash-pill{padding:2px 9px;border-radius:4px;font-size:9.5px;font-family:var(--mono);font-weight:600;letter-spacing:0.04em;}
.pill-live{background:rgba(52,199,89,0.12);border:1px solid rgba(52,199,89,0.22);color:var(--up)}
.pill-ai{background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.22);color:#A78BFA}

/* MAIN APP LAYOUT */
.app-layout{display:grid;grid-template-columns:180px 1fr 200px;height:480px;}

/* SIDEBAR */
.app-sidebar{border-right:1px solid rgba(255,255,255,0.04);background:rgba(0,0,0,0.3);padding:14px 0;overflow:hidden;}
.sb-brand{padding:0 14px 12px;border-bottom:1px solid rgba(255,255,255,0.04);margin-bottom:6px;}
.sb-brand-name{font-size:11px;font-weight:700;letter-spacing:0.12em;color:#C4B5FD;text-transform:uppercase}
.sb-brand-tag{font-size:7.5px;color:var(--text3);letter-spacing:0.1em;text-transform:uppercase;margin-top:2px;display:block}
.sb-section{padding:8px 14px 2px;font-size:8px;letter-spacing:0.14em;text-transform:uppercase;color:var(--text3);font-weight:700;font-family:var(--mono);}
.sb-item{display:flex;align-items:center;gap:7px;padding:5.5px 14px;font-size:10.5px;color:var(--text3);cursor:pointer;transition:all 0.1s;line-height:1.2;}
.sb-item.on{color:var(--text);background:rgba(124,58,237,0.1);border-right:2px solid var(--accent)}
.sb-item:hover:not(.on){color:var(--text2);background:rgba(255,255,255,0.02)}
.sb-badge{margin-left:auto;font-size:7px;padding:1px 5px;border-radius:3px;background:rgba(124,58,237,0.18);color:#A78BFA;font-family:var(--mono);font-weight:700;}
.sb-badge-new{background:rgba(52,199,89,0.15);color:var(--up)}
.sb-badge-hot{background:rgba(255,159,10,0.15);color:#FF9F0A}

/* MAIN PANEL */
.app-main{padding:16px 18px;display:flex;flex-direction:column;gap:11px;overflow:hidden;background:var(--bg2);}
.app-main-hdr{display:flex;justify-content:space-between;align-items:center}
.app-main-title{font-size:13.5px;font-weight:600;letter-spacing:-0.02em}
.app-main-meta{font-size:9.5px;color:var(--text3);font-family:var(--mono)}
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:7px}
.kpi{background:rgba(255,255,255,0.022);border:1px solid rgba(255,255,255,0.055);border-radius:7px;padding:9px 11px;}
.kl{font-size:8px;letter-spacing:0.1em;text-transform:uppercase;color:var(--text3);margin-bottom:4px;font-family:var(--mono)}
.kv{font-size:16px;font-weight:700;letter-spacing:-0.03em;line-height:1}
.kbadge{font-size:8px;font-weight:600;padding:1px 5px;border-radius:3px;margin-top:3px;display:inline-block}
.kup{color:var(--up);background:rgba(52,199,89,0.1)}
.kdn{color:var(--down);background:rgba(255,59,48,0.1)}

/* TABS ROW */
.app-tabs{display:flex;gap:0;border-bottom:1px solid rgba(255,255,255,0.05);}
.atab{padding:5px 12px;font-size:10px;font-family:var(--mono);color:var(--text3);background:transparent;border:none;cursor:pointer;letter-spacing:0.05em;text-transform:uppercase;border-bottom:2px solid transparent;transition:all 0.15s;}
.atab.on{color:#C4B5FD;border-bottom-color:var(--accent)}

/* CHART */
.chart-blk{flex:1;background:rgba(255,255,255,0.016);border:1px solid rgba(255,255,255,0.05);border-radius:7px;padding:11px;display:flex;flex-direction:column;gap:7px;min-height:0;}
.cb-hdr{display:flex;justify-content:space-between;align-items:center}
.cb-label{font-size:9px;color:var(--text3);letter-spacing:0.05em;text-transform:uppercase;font-family:var(--mono)}
.cb-sig{font-size:8px;padding:2px 8px;border-radius:3px;font-weight:600;letter-spacing:0.07em;text-transform:uppercase;font-family:var(--mono);}
.sig-acc{background:rgba(52,199,89,0.1);border:1px solid rgba(52,199,89,0.25);color:var(--up)}
.sig-dist{background:rgba(255,59,48,0.1);border:1px solid rgba(255,59,48,0.25);color:var(--down)}
.chart-svg{flex:1;min-height:0}
.chart-svg svg{width:100%;height:100%}

/* TICKER ROW */
.ticker-row{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.trc{background:rgba(255,255,255,0.018);border:1px solid rgba(255,255,255,0.05);border-radius:6px;padding:8px 10px}
.trc-sym{font-size:11px;font-weight:700;color:#C4B5FD;letter-spacing:0.03em}
.trc-sub{font-size:8px;color:var(--text3);margin-top:1px;font-family:var(--mono)}
.trc-bar{width:100%;height:2.5px;background:rgba(255,255,255,0.07);border-radius:2px;margin-top:5px;overflow:hidden}
.trc-fill{height:100%;border-radius:2px}
.trc-pct{font-size:11.5px;font-weight:700;margin-top:3px}

/* RIGHT PANEL */
.app-right{border-left:1px solid rgba(255,255,255,0.04);background:rgba(0,0,0,0.18);padding:13px;display:flex;flex-direction:column;gap:9px;overflow:hidden;}
.rp-label{font-size:8px;letter-spacing:0.12em;text-transform:uppercase;color:var(--text3);font-weight:700;font-family:var(--mono)}
.flow-item{display:flex;justify-content:space-between;align-items:center;padding:4.5px 0;border-bottom:1px solid rgba(255,255,255,0.03);}
.fi-tick{font-size:11px;font-weight:700;letter-spacing:0.03em}
.fi-name{font-size:8px;color:var(--text3);margin-top:1px;font-family:var(--mono)}
.fi-net{font-size:10.5px;font-weight:700}
.fi-unit{font-size:8px;color:var(--text3)}
.ai-box{margin-top:auto;background:rgba(124,58,237,0.07);border:1px solid rgba(124,58,237,0.16);border-radius:7px;padding:10px;}
.ai-hd{display:flex;align-items:center;gap:5px;margin-bottom:6px}
.ai-dot{width:6px;height:6px;border-radius:50%;background:#7C3AED;box-shadow:0 0 8px rgba(124,58,237,0.8);animation:glow 2s ease-in-out infinite;}
@keyframes glow{0%,100%{box-shadow:0 0 6px rgba(124,58,237,0.7)}50%{box-shadow:0 0 14px rgba(168,85,247,0.9)}}
.ai-lbl{font-size:8px;color:#A78BFA;letter-spacing:0.12em;text-transform:uppercase;font-weight:700;font-family:var(--mono)}
.ai-txt{font-size:10px;color:var(--text2);line-height:1.55}
.ai-txt strong{color:#C4B5FD;font-weight:600}

/* TRUSTED */
.trusted{padding:36px 0 0;text-align:center;position:relative;z-index:1;animation:fadeUp 0.7s 0.4s ease both;}
.trust-lbl{font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:var(--text3);font-weight:500;margin-bottom:18px;font-family:var(--mono)}
.trust-logos{display:flex;justify-content:center;align-items:center;gap:40px;flex-wrap:wrap}
.tl{font-size:11.5px;font-weight:600;color:var(--text3);letter-spacing:0.08em;opacity:0.38;transition:opacity 0.2s;text-transform:uppercase}
.tl:hover{opacity:0.65}

/* SCROLL REVEAL */
.sr{opacity:0;transform:translateY(22px);transition:opacity 0.65s ease,transform 0.65s ease}
.sr.in{opacity:1;transform:translateY(0)}
.d1{transition-delay:0.1s}.d2{transition-delay:0.2s}.d3{transition-delay:0.3s}.d4{transition-delay:0.4s}

/* SECTION */
.section{padding:100px 0}
.container{max-width:1120px;margin:0 auto;padding:0 48px}
.eyebrow{display:inline-block;font-size:10px;letter-spacing:0.16em;text-transform:uppercase;color:#A78BFA;font-weight:700;margin-bottom:14px;font-family:var(--mono);}
.section-h{font-size:clamp(28px,3.6vw,48px);font-weight:700;letter-spacing:-0.035em;line-height:1.07;margin-bottom:16px;}
.section-p{font-size:15.5px;color:var(--text2);max-width:480px;line-height:1.7;font-weight:300}

/* METRICS */
#metrics{background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:64px 0;}
.mg{display:grid;grid-template-columns:repeat(4,1fr)}
.mi{padding:0 36px;border-right:1px solid var(--border);text-align:center}
.mi:last-child{border-right:none}
.mv{font-size:clamp(32px,3.8vw,48px);font-weight:700;letter-spacing:-0.04em;margin-bottom:5px;background:linear-gradient(135deg,#C4B5FD,#7C3AED);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.ml{font-size:12.5px;color:var(--text3);letter-spacing:0.03em}

/* FEATURE MATRIX — Fincept-style */
#features{background:var(--bg);border-top:1px solid var(--border)}
.feat-intro{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:end;margin-bottom:56px}
.feat-intro-right{font-size:15px;color:var(--text2);line-height:1.75;border-left:2px solid rgba(124,58,237,0.28);padding-left:22px;}

/* Module grid — big cards */
.module-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(255,255,255,0.05);border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,0.06);}
.module-card{background:var(--bg2);padding:32px 30px;position:relative;overflow:hidden;transition:background 0.22s;}
.module-card:hover{background:var(--bg3)}
.module-card::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(124,58,237,0.5),transparent);opacity:0;transition:opacity 0.22s;}
.module-card:hover::before{opacity:1}
.mc-num{position:absolute;top:20px;right:20px;font-size:44px;font-weight:700;color:rgba(124,58,237,0.06);line-height:1;letter-spacing:-0.05em;}
.mc-icon{width:40px;height:40px;background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.2);border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:17px;margin-bottom:16px;}
.mc-title{font-size:16.5px;font-weight:600;letter-spacing:-0.02em;margin-bottom:7px}
.mc-desc{font-size:13px;color:var(--text2);line-height:1.65;font-weight:300;margin-bottom:14px}
.mc-sub-features{display:flex;flex-direction:column;gap:4px;margin-bottom:12px}
.mc-sf{display:flex;align-items:center;gap:7px;font-size:11.5px;color:var(--text2);}
.mc-sf::before{content:'';width:4px;height:4px;border-radius:50%;background:var(--accent);flex-shrink:0}
.mc-tags{display:flex;flex-wrap:wrap;gap:4px;}
.mc-tag{font-size:9px;padding:2px 7px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);border-radius:3px;color:var(--text3);font-family:var(--mono);}

/* PLATFORM MODULES — Fincept-style full breakdown */
#platform{background:var(--bg2);border-top:1px solid var(--border)}
.platform-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:48px}
.platform-card{background:var(--bg3);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:0;overflow:hidden;transition:border-color 0.2s;}
.platform-card:hover{border-color:rgba(124,58,237,0.2)}
.pc-header{padding:20px 24px 16px;border-bottom:1px solid rgba(255,255,255,0.05);display:flex;align-items:center;gap:12px;}
.pc-h-icon{width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}
.pc-h-title{font-size:15px;font-weight:600;letter-spacing:-0.02em}
.pc-h-sub{font-size:10.5px;color:var(--text3);margin-top:2px;font-family:var(--mono)}
.pc-body{padding:16px 24px 20px;}
.pc-feat-list{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.pcfl-item{display:flex;align-items:flex-start;gap:7px;font-size:12px;color:var(--text2);line-height:1.4}
.pcfl-dot{width:3px;height:3px;border-radius:50%;background:var(--accent2);flex-shrink:0;margin-top:6px}

/* MARKET DATA SECTION */
#markets{background:var(--bg);border-top:1px solid var(--border)}
.mkt-tabs{display:flex;gap:2px;background:rgba(255,255,255,0.04);border:1px solid var(--border);border-radius:9px;padding:3px;width:fit-content;margin-bottom:36px;}
.mtab{padding:6px 16px;font-size:12px;font-family:inherit;font-weight:500;color:var(--text3);background:transparent;border:none;border-radius:7px;cursor:pointer;transition:all 0.18s;}
.mtab.on{background:rgba(124,58,237,0.18);color:var(--text);border:1px solid rgba(124,58,237,0.28)}
.mtab:hover:not(.on){color:var(--text2)}
.mkt-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.mkt-card{background:var(--bg3);border:1px solid rgba(255,255,255,0.06);border-radius:11px;padding:20px;transition:border-color 0.2s,box-shadow 0.2s;}
.mkt-card:hover{border-color:rgba(124,58,237,0.2);box-shadow:0 12px 32px rgba(0,0,0,0.3)}
.mkt-card-head{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px}
.mkt-sym{font-size:14.5px;font-weight:700;letter-spacing:0.02em}
.mkt-name{font-size:10px;color:var(--text3);margin-top:2px;font-family:var(--mono)}
.mkt-cat-badge{font-size:8px;padding:2px 7px;border-radius:4px;font-weight:600;letter-spacing:0.07em;font-family:var(--mono);}
.mkt-price{font-size:22px;font-weight:700;letter-spacing:-0.03em;line-height:1;margin-bottom:5px}
.mkt-row{display:flex;justify-content:space-between;align-items:center;margin-top:8px}
.mkt-chg{font-size:12.5px;font-weight:600;padding:3px 8px;border-radius:5px}
.mkt-chg-up{color:var(--up);background:rgba(52,199,89,0.1)}
.mkt-chg-dn{color:var(--down);background:rgba(255,59,48,0.1)}
.mkt-vol{font-size:9.5px;color:var(--text3);font-family:var(--mono)}
.sparkline{margin-top:12px}
.sparkline svg{width:100%;height:32px}

/* HOW IT WORKS */
#how{background:var(--bg2);border-top:1px solid var(--border);border-bottom:1px solid var(--border);}
.how-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(255,255,255,0.04);border-radius:14px;overflow:hidden;margin-top:52px;}
.how-step{background:var(--bg3);padding:36px 30px;position:relative}
.how-num{font-size:52px;font-weight:700;color:rgba(124,58,237,0.07);letter-spacing:-0.05em;line-height:1;margin-bottom:12px;}
.how-title{font-size:18px;font-weight:600;letter-spacing:-0.02em;margin-bottom:8px}
.how-desc{font-size:13px;color:var(--text2);line-height:1.68;font-weight:300}
.how-arr{position:absolute;top:36px;right:28px;font-size:20px;color:rgba(124,58,237,0.22);}

/* AI AGENTS SECTION */
#agents{background:var(--bg);border-top:1px solid var(--border)}
.agents-intro{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:start;margin-bottom:48px}
.agent-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.agent-card{background:var(--bg3);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:16px;transition:border-color 0.2s,transform 0.15s;}
.agent-card:hover{border-color:rgba(124,58,237,0.2);transform:translateY(-2px)}
.agent-icon{font-size:20px;margin-bottom:8px}
.agent-name{font-size:12.5px;font-weight:600;margin-bottom:4px;letter-spacing:-0.01em}
.agent-desc{font-size:11px;color:var(--text3);line-height:1.5}
.agent-badge{display:inline-block;font-size:8px;padding:1px 6px;border-radius:3px;margin-top:6px;font-family:var(--mono);font-weight:600;}

/* DATA SOURCES */
#data{background:var(--bg2);border-top:1px solid var(--border)}
.data-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:48px}
.data-card{background:var(--bg3);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:20px;transition:border-color 0.2s;}
.data-card:hover{border-color:rgba(124,58,237,0.18)}
.dc-cat{font-size:8px;letter-spacing:0.14em;text-transform:uppercase;color:var(--text3);font-weight:700;font-family:var(--mono);margin-bottom:12px;}
.dc-sources{display:flex;flex-direction:column;gap:5px}
.dc-s{font-size:11.5px;color:var(--text2);display:flex;align-items:center;gap:6px}
.dc-s::before{content:'';width:3px;height:3px;border-radius:50%;background:var(--accent);flex-shrink:0}

/* PRICING */
#pricing{background:var(--bg);border-top:1px solid var(--border)}
.pg{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:52px}
.price-card{background:var(--bg3);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:28px;position:relative;overflow:hidden;transition:border-color 0.2s,box-shadow 0.2s;}
.price-card:hover{border-color:rgba(124,58,237,0.22);box-shadow:0 18px 44px rgba(0,0,0,0.35)}
.price-card.featured{border-color:rgba(124,58,237,0.35);background:linear-gradient(160deg,rgba(124,58,237,0.06) 0%,var(--bg3) 100%);box-shadow:0 0 0 1px rgba(124,58,237,0.18),0 20px 50px rgba(0,0,0,0.45);}
.price-card.featured::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--accent),var(--accent2),transparent);}
.price-best{position:absolute;top:20px;right:20px;padding:2px 9px;border-radius:4px;font-size:8.5px;font-family:var(--mono);background:rgba(124,58,237,0.18);border:1px solid rgba(124,58,237,0.3);color:#C4B5FD;font-weight:700;letter-spacing:0.07em;}
.pt{font-size:11px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--text2);margin-bottom:12px;font-family:var(--mono)}
.pa{font-size:38px;font-weight:700;letter-spacing:-0.04em;line-height:1}
.pp{font-size:11px;color:var(--text3);margin-top:4px;margin-bottom:14px;font-family:var(--mono)}
.pd{font-size:12.5px;color:var(--text3);line-height:1.65;margin-bottom:16px}
.pdiv{height:1px;background:rgba(255,255,255,0.05);margin-bottom:16px}
.pf{display:flex;align-items:flex-start;gap:8px;font-size:12.5px;color:var(--text2);margin-bottom:8px;line-height:1.5}
.pcheck{color:var(--up);font-size:11px;flex-shrink:0;margin-top:2px}
.pcta{width:100%;margin-top:20px;padding:10px;border-radius:8px;font-size:12.5px;font-family:inherit;font-weight:500;cursor:pointer;transition:all 0.18s;}
.pcta-ghost{background:transparent;border:1px solid rgba(255,255,255,0.1);color:var(--text2)}
.pcta-ghost:hover{background:rgba(255,255,255,0.05);color:var(--text)}
.pcta-fill{background:var(--accent);border:1px solid transparent;color:#fff}
.pcta-fill:hover{background:var(--accent2);box-shadow:0 8px 22px rgba(124,58,237,0.3)}

/* CTA */
#cta{padding:140px 0;text-align:center;position:relative;overflow:hidden;}
.cta-orb{position:absolute;width:680px;height:480px;background:radial-gradient(ellipse,rgba(124,58,237,0.16) 0%,transparent 65%);left:50%;top:50%;transform:translate(-50%,-50%);filter:blur(80px);pointer-events:none;}
.cta-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,0.012) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.012) 1px,transparent 1px);background-size:52px 52px;mask-image:radial-gradient(ellipse 60% 75% at 50% 50%,black,transparent);pointer-events:none;}
.cta-inner{position:relative;z-index:1}
.cta-h{font-size:clamp(36px,5vw,68px);font-weight:700;letter-spacing:-0.04em;line-height:1.04;max-width:720px;margin:0 auto 20px;}
.cta-h em{font-style:italic;background:linear-gradient(135deg,#C4B5FD,#9333EA);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.cta-sub{font-size:16px;color:var(--text2);max-width:440px;margin:0 auto 36px;line-height:1.68;font-weight:300}
.cta-btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-bottom:22px}
.cta-note{font-size:11px;color:var(--text3);letter-spacing:0.04em;font-family:var(--mono)}

/* FOOTER */
footer{padding:32px 0;border-top:1px solid var(--border);background:var(--bg);}
.footer-inner{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}
.footer-brand{font-size:13px;font-weight:700;letter-spacing:0.1em;color:var(--text);text-transform:uppercase}
.footer-copy{font-size:11px;color:var(--text3);margin-top:3px;font-family:var(--mono)}
.footer-links{display:flex;gap:22px;flex-wrap:wrap}
.footer-links a{font-size:11.5px;color:var(--text3);text-decoration:none;transition:color 0.15s;font-family:var(--mono)}
.footer-links a:hover{color:var(--text2)}

@keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}

@media(max-width:900px){
  nav{padding:0 20px}.nav-links{display:none}
  #hero{padding:72px 20px 56px}
  .app-layout{display:none}
  .container{padding:0 20px}
  .feat-intro,.agents-intro{grid-template-columns:1fr;gap:24px}
  .module-grid{grid-template-columns:1fr}
  .platform-grid{grid-template-columns:1fr}
  .agent-grid{grid-template-columns:repeat(2,1fr)}
  .data-grid{grid-template-columns:repeat(2,1fr)}
  .mg{grid-template-columns:repeat(2,1fr)}
  .mi{padding:20px;border-right:none;border-bottom:1px solid var(--border)}
  .pg{grid-template-columns:1fr}
  .how-grid{grid-template-columns:1fr}
  .mkt-grid{grid-template-columns:1fr}
  .footer-inner{flex-direction:column;align-items:flex-start}
}
</style>
</head>
<body>

<!-- TICKER -->
<div class="ticker-wrap"><div class="ticker-track" id="tickerTrack"></div></div>

<!-- NAV -->
<nav>
  <a href="#" class="nav-logo">
    <div class="nav-logo-mark">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1.5C3.96 1.5 1.5 3.96 1.5 7S3.96 12.5 7 12.5 12.5 10.04 12.5 7 10.04 1.5 7 1.5zm0 9C5.07 10.5 3.5 8.93 3.5 7S5.07 3.5 7 3.5 10.5 5.07 10.5 7 8.93 10.5 7 10.5z" fill="white" fill-opacity="0.9"/><circle cx="7" cy="7" r="2" fill="white"/></svg>
    </div>
    <span class="nav-wordmark">Moonside</span>
  </a>
  <ul class="nav-links">
    <li><a href="#features">Modules</a></li>
    <li><a href="#platform">Platform</a></li>
    <li><a href="#agents">AI Agents</a></li>
    <li><a href="#markets">Markets</a></li>
    <li><a href="#pricing">Pricing</a></li>
    <li><a href="#">Docs</a></li>
  </ul>
  <div class="nav-right">
    <a href="#" class="nbtn nbtn-ghost">Sign In</a>
    <a href="#" class="nbtn nbtn-fill">Request Access</a>
  </div>
</nav>

<!-- HERO -->
<section id="hero">
  <div class="hero-orb-1"></div><div class="hero-orb-2"></div><div class="hero-orb-3"></div>
  <div class="hero-grid"></div>
  <div class="hero-badge"><div class="hb-dot"></div>Institutional Beta · IDX Intelligence Platform</div>
  <h1 class="hero-h">Institutional-grade intelligence<br><span class="hero-h-accent">for the Indonesian market</span></h1>
  <p class="hero-sub">Bandarmology, Foreign Flow, Smart Money, RRG Rotation, IPO Intelligence, Macro Analysis — unified into one platform. Backed by AI. Built for professionals.</p>
  <div class="hero-ctas">
    <a href="#" class="btn-p">Request Access <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M2 6.5h9M7.5 3l3.5 3.5L7.5 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
    <a href="#platform" class="btn-s">Explore Platform</a>
  </div>

  <!-- FULL APP MOCKUP -->
  <div class="hero-dash">
    <div class="dash-glow"></div>
    <div class="dash-frame">
      <div class="dash-tb">
        <div class="wc wc-r"></div><div class="wc wc-y"></div><div class="wc wc-g"></div>
        <div class="dash-urlbar"><span style="color:var(--up);font-size:9px">🔒</span>app.moonside.id</div>
        <!-- App-level tabs -->
        <div style="display:flex;gap:0;margin-left:18px;border-bottom:none;">
          <div style="padding:0 12px;font-size:9.5px;font-family:var(--mono);color:#C4B5FD;letter-spacing:0.05em;text-transform:uppercase;border-bottom:2px solid var(--accent);padding-bottom:10px;padding-top:0">📡 Market Live</div>
          <div style="padding:0 12px;font-size:9.5px;font-family:var(--mono);color:var(--text3);letter-spacing:0.05em;text-transform:uppercase;">📈 Market Data</div>
          <div style="padding:0 12px;font-size:9.5px;font-family:var(--mono);color:var(--text3);letter-spacing:0.05em;text-transform:uppercase;">📊 Sector</div>
          <div style="padding:0 12px;font-size:9.5px;font-family:var(--mono);color:var(--text3);letter-spacing:0.05em;text-transform:uppercase;">🗓️ Plan</div>
          <div style="padding:0 12px;font-size:9.5px;font-family:var(--mono);color:var(--text3);letter-spacing:0.05em;text-transform:uppercase;">⚡ Screener</div>
        </div>
        <div style="margin-left:auto;display:flex;gap:6px">
          <span class="dash-pill pill-live">● Live</span>
          <span class="dash-pill pill-ai">AI</span>
        </div>
      </div>
      <div class="app-layout">
        <!-- SIDEBAR -->
        <div class="app-sidebar">
          <div class="sb-brand">
            <div class="sb-brand-name">Moonside</div>
            <span class="sb-brand-tag">Intelligence Platform</span>
          </div>
          <div class="sb-section">Market Live</div>
          <div class="sb-item on">🌐 Index, Komoditas &amp; FX<span class="sb-badge">LIVE</span></div>
          <div class="sb-item">📰 Market News</div>
          <div class="sb-item">📋 Market Forecast</div>
          <div class="sb-section">Market Data</div>
          <div class="sb-item">📡 Rate Monitor<span class="sb-badge">BI/FED</span></div>
          <div class="sb-item">📉 Bond Yield</div>
          <div class="sb-item">💰 Dividend Tracker</div>
          <div class="sb-item">📈 IHSG History</div>
          <div class="sb-item">💱 Kurs IDR<span class="sb-badge sb-badge-new">NEW</span></div>
          <div class="sb-section">Sector &amp; Rotation</div>
          <div class="sb-item">📊 RRG Rotation</div>
          <div class="sb-item">🌍 Foreign Index</div>
          <div class="sb-item">🏦 Saham BUMN</div>
          <div class="sb-section">Screener</div>
          <div class="sb-item">⚡ Sigma Stock Insight</div>
          <div class="sb-item">📊 Fundamental Screen</div>
          <div class="sb-item">📋 Analisa IPO<span class="sb-badge sb-badge-hot">HOT</span></div>
          <div class="sb-item">🏦 Broker Summary</div>
        </div>
        <!-- MAIN -->
        <div class="app-main">
          <div class="app-main-hdr">
            <div class="app-main-title">Market Live — Index, Komoditas &amp; Forex</div>
            <div class="app-main-meta">IDX · 07.06.2026 · 15:42 WIB</div>
          </div>
          <!-- Sub-tab row -->
          <div class="app-tabs">
            <div class="atab on">🌐 Index &amp; FX</div>
            <div class="atab">📰 News</div>
            <div class="atab">📋 Forecast</div>
            <div class="atab">📝 Notes</div>
          </div>
          <div class="kpi-row">
            <div class="kpi"><div class="kl">IHSG</div><div class="kv" style="color:var(--up)">7,284</div><div><span class="kbadge kup">+1.24%</span></div></div>
            <div class="kpi"><div class="kl">Net Foreign</div><div class="kv" style="color:var(--up)">+2.14T</div><div><span class="kbadge kup">BUY</span></div></div>
            <div class="kpi"><div class="kl">DXY</div><div class="kv">104.2</div><div><span class="kbadge kdn">−0.18%</span></div></div>
            <div class="kpi"><div class="kl">BTC/USD</div><div class="kv" style="color:var(--up)">69.4K</div><div><span class="kbadge kup">+2.3%</span></div></div>
          </div>
          <div class="chart-blk">
            <div class="cb-hdr">
              <div class="cb-label">Broker Accumulation Flow · Top 20 Broker IDX</div>
              <div class="cb-sig sig-acc">ACCUMULATE ↑</div>
            </div>
            <div class="chart-svg">
              <svg viewBox="0 0 640 90" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
                <defs><linearGradient id="cg" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#7C3AED" stop-opacity="0.28"/><stop offset="100%" stop-color="#7C3AED" stop-opacity="0"/></linearGradient></defs>
                <line x1="0" y1="22" x2="640" y2="22" stroke="rgba(255,255,255,0.035)" stroke-width="1"/>
                <line x1="0" y1="45" x2="640" y2="45" stroke="rgba(255,255,255,0.035)" stroke-width="1"/>
                <line x1="0" y1="68" x2="640" y2="68" stroke="rgba(255,255,255,0.035)" stroke-width="1"/>
                <path d="M0,82 C60,76 100,66 160,56 C210,48 240,62 290,48 C330,36 360,25 410,19 C450,14 490,21 540,11 C570,6 610,4 640,2 L640,90 L0,90Z" fill="url(#cg)"/>
                <path d="M0,82 C60,76 100,66 160,56 C210,48 240,62 290,48 C330,36 360,25 410,19 C450,14 490,21 540,11 C570,6 610,4 640,2" fill="none" stroke="#A855F7" stroke-width="1.6" stroke-linecap="round"/>
                <circle cx="540" cy="11" r="3.5" fill="#7C3AED"/>
                <circle cx="540" cy="11" r="7" fill="none" stroke="rgba(124,58,237,0.4)" stroke-width="1.5"/>
              </svg>
            </div>
          </div>
          <div class="ticker-row">
            <div class="trc"><div class="trc-sym">BBCA</div><div class="trc-sub">Accumulation · 3d</div><div class="trc-bar"><div class="trc-fill" style="width:78%;background:var(--up)"></div></div><div class="trc-pct" style="color:var(--up)">78%</div></div>
            <div class="trc"><div class="trc-sym">BMRI</div><div class="trc-sub">Accumulation</div><div class="trc-bar"><div class="trc-fill" style="width:62%;background:var(--up)"></div></div><div class="trc-pct" style="color:var(--up)">62%</div></div>
            <div class="trc"><div class="trc-sym">GOTO</div><div class="trc-sub">Distribution</div><div class="trc-bar"><div class="trc-fill" style="width:41%;background:var(--down)"></div></div><div class="trc-pct" style="color:var(--down)">41%</div></div>
          </div>
        </div>
        <!-- RIGHT -->
        <div class="app-right">
          <div class="rp-label">Foreign Buy Today</div>
          <div class="flow-item"><div><div class="fi-tick" style="color:#C4B5FD">BBCA</div><div class="fi-name">Bank Central Asia</div></div><div style="text-align:right"><div class="fi-net" style="color:var(--up)">+847B</div><div class="fi-unit">IDR</div></div></div>
          <div class="flow-item"><div><div class="fi-tick" style="color:#C4B5FD">BMRI</div><div class="fi-name">Bank Mandiri</div></div><div style="text-align:right"><div class="fi-net" style="color:var(--up)">+421B</div><div class="fi-unit">IDR</div></div></div>
          <div class="flow-item"><div><div class="fi-tick" style="color:#C4B5FD">INDF</div><div class="fi-name">Indofood</div></div><div style="text-align:right"><div class="fi-net" style="color:var(--up)">+189B</div><div class="fi-unit">IDR</div></div></div>
          <div class="flow-item"><div><div class="fi-tick" style="color:var(--text2)">GOTO</div><div class="fi-name">GoTo Group</div></div><div style="text-align:right"><div class="fi-net" style="color:var(--down)">−218B</div><div class="fi-unit">IDR</div></div></div>
          <div class="flow-item"><div><div class="fi-tick" style="color:var(--text2)">TLKM</div><div class="fi-name">Telekomunikasi</div></div><div style="text-align:right"><div class="fi-net" style="color:var(--down)">−189B</div><div class="fi-unit">IDR</div></div></div>
          <div class="ai-box">
            <div class="ai-hd"><div class="ai-dot"></div><div class="ai-lbl">Sigma AI</div></div>
            <div class="ai-txt"><strong>BBCA</strong> 3-day institutional acc. Breakout 9,800 → 74% prob. <strong>DXY</strong> soft → EM inflow mode.</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="trusted">
    <div class="trust-lbl">Used by analysts at</div>
    <div class="trust-logos">
      <div class="tl">Mandiri Sekuritas</div>
      <div class="tl">BCA Sekuritas</div>
      <div class="tl">Mirae Asset</div>
      <div class="tl">Indo Premier</div>
      <div class="tl">Phillip Sekuritas</div>
    </div>
  </div>
</section>

<!-- METRICS -->
<section id="metrics">
  <div class="container">
    <div class="mg">
      <div class="mi sr"><div class="mv" data-target="900" data-sfx="+">0</div><div class="ml">IDX Stocks Tracked</div></div>
      <div class="mi sr d1"><div class="mv" data-target="48" data-sfx="">0</div><div class="ml">Broker Flows Daily</div></div>
      <div class="mi sr d2"><div class="mv" data-target="7" data-sfx=" Modules">0</div><div class="ml">Platform Modules</div></div>
      <div class="mi sr d3"><div class="mv" data-target="99.9" data-dec="1" data-sfx="%">0</div><div class="ml">Platform Uptime</div></div>
    </div>
  </div>
</section>

<!-- MODULE OVERVIEW — like Fincept feature table -->
<section id="features" class="section">
  <div class="container">
    <div class="feat-intro sr">
      <div>
        <span class="eyebrow">Platform Modules</span>
        <h2 class="section-h">Every edge,<br>in one terminal</h2>
        <p class="section-p">7 core modules, each a deep-dive intelligence layer. From broker fingerprinting to AI macro synthesis — institutional toolkit for the IDX.</p>
      </div>
      <div>
        <p class="feat-intro-right">MOONSIDE is not a screener. It's an intelligence terminal: equity analytics, macro monitoring, flow tracking, rotation modeling, IPO research, AI synthesis — all cross-referencing each other in a unified workspace.</p>
      </div>
    </div>

    <div class="module-grid sr d1">
      <!-- Module 1 -->
      <div class="module-card">
        <div class="mc-num">01</div>
        <div class="mc-icon">📡</div>
        <div class="mc-title">Market Live</div>
        <div class="mc-desc">Real-time pulse of the IDX — global indices, commodities, forex, and breaking market news in one unified dashboard.</div>
        <div class="mc-sub-features">
          <div class="mc-sf">Index, Komoditas &amp; Forex</div>
          <div class="mc-sf">Live Market News &amp; RSS Feed</div>
          <div class="mc-sf">Market Forecast &amp; Notes</div>
          <div class="mc-sf">Economic Calendar</div>
        </div>
        <div class="mc-tags"><span class="mc-tag">IHSG Live</span><span class="mc-tag">DXY</span><span class="mc-tag">Gold · Oil · CPO</span><span class="mc-tag">IDX News</span></div>
      </div>
      <!-- Module 2 -->
      <div class="module-card">
        <div class="mc-num">02</div>
        <div class="mc-icon">📈</div>
        <div class="mc-title">Market Data</div>
        <div class="mc-desc">Deep macro data layer — BI &amp; Fed rate monitors, bond yields, dividend tracker, inflation, and currency trends.</div>
        <div class="mc-sub-features">
          <div class="mc-sf">BI Rate &amp; Fed Rate Monitor</div>
          <div class="mc-sf">SBN / US Bond Yield + AI Analyst</div>
          <div class="mc-sf">Dividend Tracker + AI Analyst</div>
          <div class="mc-sf">Inflasi, IHSG History, Kurs IDR</div>
        </div>
        <div class="mc-tags"><span class="mc-tag">BI Rate</span><span class="mc-tag">FED Watch</span><span class="mc-tag">Yield Curve</span><span class="mc-tag">Dividend</span></div>
      </div>
      <!-- Module 3 -->
      <div class="module-card">
        <div class="mc-num">03</div>
        <div class="mc-icon">📊</div>
        <div class="mc-title">Sector &amp; Rotation</div>
        <div class="mc-desc">Relative rotation and sector positioning — RRG charts, index constituent tracking, conglomerate mapping, and BUMN analysis.</div>
        <div class="mc-sub-features">
          <div class="mc-sf">RRG Sector Rotation Chart</div>
          <div class="mc-sf">MSCI, FTSE, LQ45, IDX30, IDX80</div>
          <div class="mc-sf">Kompas100, Konglo, BUMN</div>
          <div class="mc-sf">Shareholder Flow Monitor</div>
        </div>
        <div class="mc-tags"><span class="mc-tag">RRG</span><span class="mc-tag">MSCI/FTSE</span><span class="mc-tag">Konglo</span><span class="mc-tag">BUMN</span></div>
      </div>
      <!-- Module 4 -->
      <div class="module-card">
        <div class="mc-num">04</div>
        <div class="mc-icon">🗓️</div>
        <div class="mc-title">Sigma Plan</div>
        <div class="mc-desc">Structured trading plan workflow — daily &amp; weekly plans with AI-generated trade setup, track record, and evaluation.</div>
        <div class="mc-sub-features">
          <div class="mc-sf">Daily Plan &amp; Track Record</div>
          <div class="mc-sf">Weekly Plan &amp; Summary</div>
          <div class="mc-sf">BSJP (Broker Summary Trade Plan)</div>
          <div class="mc-sf">AI Verdict &amp; Evaluation</div>
        </div>
        <div class="mc-tags"><span class="mc-tag">Trade Plan</span><span class="mc-tag">BSJP</span><span class="mc-tag">AI Verdict</span><span class="mc-tag">History</span></div>
      </div>
      <!-- Module 5 -->
      <div class="module-card">
        <div class="mc-num">05</div>
        <div class="mc-icon">⚡</div>
        <div class="mc-title">Sigma Screener</div>
        <div class="mc-desc">The intelligence engine — Sigma Score stock insight, fundamental screening, IPO analysis with prospectus bedah, and broker summary tracking.</div>
        <div class="mc-sub-features">
          <div class="mc-sf">Sigma Stock Insight (Score System)</div>
          <div class="mc-sf">Fundamental Screener + AI Analyst</div>
          <div class="mc-sf">Analisa IPO + Bedah Prospektus</div>
          <div class="mc-sf">Broker Summary &amp; Bandarmology</div>
        </div>
        <div class="mc-tags"><span class="mc-tag">Sigma Score</span><span class="mc-tag">IPO Intel</span><span class="mc-tag">Brosum</span><span class="mc-tag">Fundamental</span></div>
      </div>
      <!-- Module 6 -->
      <div class="module-card">
        <div class="mc-num">06</div>
        <div class="mc-icon">🔧</div>
        <div class="mc-title">Sigma Calc</div>
        <div class="mc-desc">Precision calculators for IDX-specific mechanics — ARA/ARB limits, average down sizing, and EM spread calculator.</div>
        <div class="mc-sub-features">
          <div class="mc-sf">ARA / ARB Price Calculator</div>
          <div class="mc-sf">Average Down Calculator</div>
          <div class="mc-sf">EM Spread Calculator</div>
        </div>
        <div class="mc-tags"><span class="mc-tag">ARA/ARB</span><span class="mc-tag">Avg Down</span><span class="mc-tag">EM Spread</span></div>
      </div>
    </div>
  </div>
</section>

<!-- PLATFORM DEEP DIVE -->
<section id="platform" class="section">
  <div class="container">
    <div class="sr" style="max-width:600px;margin-bottom:0">
      <span class="eyebrow">Deep Dive</span>
      <h2 class="section-h">What's inside each module</h2>
      <p class="section-p">Every module is a full intelligence workspace — not a single screen. Here's what's under the hood.</p>
    </div>
    <div class="platform-grid sr d1">
      <!-- Bandarmology -->
      <div class="platform-card">
        <div class="pc-header">
          <div class="pc-h-icon" style="background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.2)">◆</div>
          <div><div class="pc-h-title">Bandarmology Engine</div><div class="pc-h-sub">Broker fingerprinting · Accumulation detection</div></div>
        </div>
        <div class="pc-body">
          <div class="pc-feat-list">
            <div class="pcfl-item"><div class="pcfl-dot"></div>Broker Buy/Sell Summary per saham</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Net accumulation 3-day signal</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Concentration score — dominasi broker</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>BSJP (Broker Summary Trade Plan)</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Top accumulator ranking harian</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>AI scoring dari pola broker</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Volume spike detection</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Cross-validate dengan foreign flow</div>
          </div>
        </div>
      </div>
      <!-- Foreign Flow -->
      <div class="platform-card">
        <div class="pc-header">
          <div class="pc-h-icon" style="background:rgba(0,122,255,0.1);border:1px solid rgba(0,122,255,0.2)">⬡</div>
          <div><div class="pc-h-title">Foreign Capital Flow</div><div class="pc-h-sub">Cross-border institutional tracking</div></div>
        </div>
        <div class="pc-body">
          <div class="pc-feat-list">
            <div class="pcfl-item"><div class="pcfl-dot"></div>Net foreign buy/sell harian per saham</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>YTD &amp; MTD flow akumulasi</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Sektor-level flow breakdown</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>MSCI, FTSE, LQ45, IDX30 flow</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Free float integration (BEI data)</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Heatmap visualisasi intensitas</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Konglo &amp; BUMN positioning</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>AI correlation DXY + IDX</div>
          </div>
        </div>
      </div>
      <!-- Sigma Score -->
      <div class="platform-card">
        <div class="pc-header">
          <div class="pc-h-icon" style="background:rgba(255,159,10,0.1);border:1px solid rgba(255,159,10,0.2)">⚡</div>
          <div><div class="pc-h-title">Sigma Score System</div><div class="pc-h-sub">Multi-factor institutional scoring</div></div>
        </div>
        <div class="pc-body">
          <div class="pc-feat-list">
            <div class="pcfl-item"><div class="pcfl-dot"></div>Teknikal score (RSI, MACD, BB, ATR)</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Volume intelligence &amp; spike detection</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Bandar/broker accumulation score</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Fundamental score (ROE, DER, EPS)</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Momentum &amp; relative strength</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Smart Money zone detection (FVG, OB)</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Trade level calc (TP1, TP2, SL)</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Composite Sigma Score badge</div>
          </div>
        </div>
      </div>
      <!-- IPO Intel -->
      <div class="platform-card">
        <div class="pc-header">
          <div class="pc-h-icon" style="background:rgba(52,199,89,0.1);border:1px solid rgba(52,199,89,0.2)">⊕</div>
          <div><div class="pc-h-title">IPO Intelligence</div><div class="pc-h-sub">Pre-listing research &amp; prospectus analysis</div></div>
        </div>
        <div class="pc-body">
          <div class="pc-feat-list">
            <div class="pcfl-item"><div class="pcfl-dot"></div>Bedah Prospektus via AI (PDF upload)</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Valuasi &amp; fundamental pre-IPO</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Sektor comparables mapping</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Manajemen &amp; ownership analysis</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Risiko &amp; red flag detection</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Logika analisa IPO terstruktur</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>AI-generated investment thesis</div>
            <div class="pcfl-item"><div class="pcfl-dot"></div>Post-listing monitoring</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- AI AGENTS -->
<section id="agents" class="section" style="border-top:1px solid var(--border)">
  <div class="container">
    <div class="agents-intro sr">
      <div>
        <span class="eyebrow">AI Intelligence Layer</span>
        <h2 class="section-h">Multi-model AI<br>across every module</h2>
        <p class="section-p">MOONSIDE runs multiple AI models (Groq, Gemini, MiniMax) in parallel — each specialized for different analytical tasks across every platform module.</p>
      </div>
      <div style="display:flex;flex-direction:column;gap:10px;margin-top:8px">
        <div style="background:rgba(124,58,237,0.06);border:1px solid rgba(124,58,237,0.15);border-radius:10px;padding:16px 18px">
          <div style="font-size:9px;font-family:var(--mono);color:#A78BFA;letter-spacing:0.12em;text-transform:uppercase;font-weight:700;margin-bottom:8px">AI Providers</div>
          <div style="display:flex;gap:8px;flex-wrap:wrap">
            <span style="padding:3px 10px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:5px;font-size:11px;color:var(--text2);font-family:var(--mono)">Groq</span>
            <span style="padding:3px 10px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:5px;font-size:11px;color:var(--text2);font-family:var(--mono)">Gemini</span>
            <span style="padding:3px 10px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:5px;font-size:11px;color:var(--text2);font-family:var(--mono)">MiniMax</span>
          </div>
        </div>
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:16px 18px">
          <div style="font-size:9px;font-family:var(--mono);color:var(--text3);letter-spacing:0.12em;text-transform:uppercase;font-weight:700;margin-bottom:8px">Cooldown &amp; Rate Management</div>
          <div style="font-size:12px;color:var(--text2);line-height:1.55">Smart key rotation dengan automatic rate-limit detection — AI tetap tersedia meski satu provider throttled.</div>
        </div>
      </div>
    </div>
    <div class="agent-grid sr d1">
      <div class="agent-card">
        <div class="agent-icon">📊</div>
        <div class="agent-name">Bond Yield AI</div>
        <div class="agent-desc">Analisis kurva yield SBN Indonesia &amp; US Treasury — implication untuk ekuitas</div>
        <span class="agent-badge" style="background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.2);color:#A78BFA">Module: Market Data</span>
      </div>
      <div class="agent-card">
        <div class="agent-icon">💰</div>
        <div class="agent-name">Dividend AI</div>
        <div class="agent-desc">AI analyst untuk dividend tracker — screening yield &amp; sustainability analysis</div>
        <span class="agent-badge" style="background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.2);color:#A78BFA">Module: Market Data</span>
      </div>
      <div class="agent-card">
        <div class="agent-icon">📡</div>
        <div class="agent-name">Rate Monitor AI</div>
        <div class="agent-desc">Interpretasi FED Rate &amp; BI Rate — impact pada pasar modal &amp; nilai tukar IDR</div>
        <span class="agent-badge" style="background:rgba(52,199,89,0.1);border:1px solid rgba(52,199,89,0.2);color:var(--up)">FED + BI</span>
      </div>
      <div class="agent-card">
        <div class="agent-icon">⚡</div>
        <div class="agent-name">Sigma AI</div>
        <div class="agent-desc">Core stock analyst — Sigma Score interpretation, trade plan generation, risk assessment</div>
        <span class="agent-badge" style="background:rgba(255,159,10,0.1);border:1px solid rgba(255,159,10,0.2);color:#FF9F0A">Core Agent</span>
      </div>
      <div class="agent-card">
        <div class="agent-icon">📋</div>
        <div class="agent-name">IPO Analyst AI</div>
        <div class="agent-desc">Bedah prospektus, valuasi pre-IPO, red flag detection dari dokumen PDF</div>
        <span class="agent-badge" style="background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.2);color:#A78BFA">Module: Screener</span>
      </div>
      <div class="agent-card">
        <div class="agent-icon">📈</div>
        <div class="agent-name">Fundamental AI</div>
        <div class="agent-desc">Analisis fundamental screener — ROE, DER, EPS growth, sektor comparables</div>
        <span class="agent-badge" style="background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.2);color:#A78BFA">Module: Screener</span>
      </div>
      <div class="agent-card">
        <div class="agent-icon">🗓️</div>
        <div class="agent-name">Plan Evaluator AI</div>
        <div class="agent-desc">AI verdict untuk daily &amp; weekly trade plan — evaluasi hasil vs setup awal</div>
        <span class="agent-badge" style="background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.2);color:#A78BFA">Module: Plan</span>
      </div>
      <div class="agent-card">
        <div class="agent-icon">🌐</div>
        <div class="agent-name">Macro AI</div>
        <div class="agent-desc">Cross-referencing DXY, BTC, komoditas, &amp; BI rate terhadap positioning IDX</div>
        <span class="agent-badge" style="background:rgba(0,122,255,0.1);border:1px solid rgba(0,122,255,0.2);color:#007AFF">Global Macro</span>
      </div>
    </div>
  </div>
</section>

<!-- MARKET DATA -->
<section id="markets" class="section" style="background:var(--bg2);border-top:1px solid var(--border)">
  <div class="container">
    <div class="sr">
      <span class="eyebrow">Global Context</span>
      <h2 class="section-h">Forex · Crypto · Commodities</h2>
      <p class="section-p" style="margin-bottom:32px">Macro context terintegrasi langsung ke setiap sinyal ekuitas. DXY, USD/IDR, BTC dominance — semua ter-cross-reference ke IHSG.</p>
    </div>
    <div class="mkt-tabs sr">
      <button class="mtab on" onclick="switchMktTab(this,'forex')">Forex</button>
      <button class="mtab" onclick="switchMktTab(this,'crypto')">Crypto</button>
      <button class="mtab" onclick="switchMktTab(this,'commodities')">Commodities</button>
    </div>
    <div id="tab-forex" class="mkt-grid sr d1">
      <div class="mkt-card"><div class="mkt-card-head"><div><div class="mkt-sym">DXY</div><div class="mkt-name">US Dollar Index</div></div><span class="mkt-cat-badge" style="background:rgba(0,122,255,0.12);color:#007AFF;border:1px solid rgba(0,122,255,0.2)">FX</span></div><div class="mkt-price">104.23</div><div class="mkt-row"><span class="mkt-chg mkt-chg-dn">−0.18%</span><span class="mkt-vol">Vol 82.4B</span></div><div class="sparkline"><svg viewBox="0 0 200 32" preserveAspectRatio="none"><path d="M0,20 C20,18 40,14 60,16 C80,18 90,22 110,19 C130,16 150,12 170,10 C185,8 195,9 200,8" fill="none" stroke="#FF3B30" stroke-width="1.5" stroke-linecap="round"/></svg></div></div>
      <div class="mkt-card"><div class="mkt-card-head"><div><div class="mkt-sym">USD/IDR</div><div class="mkt-name">US Dollar / Rupiah</div></div><span class="mkt-cat-badge" style="background:rgba(0,122,255,0.12);color:#007AFF;border:1px solid rgba(0,122,255,0.2)">FX</span></div><div class="mkt-price">15,847</div><div class="mkt-row"><span class="mkt-chg mkt-chg-dn">+0.24%</span><span class="mkt-vol">IDR weakening</span></div><div class="sparkline"><svg viewBox="0 0 200 32" preserveAspectRatio="none"><path d="M0,16 C20,17 40,20 60,22 C80,24 100,21 120,24 C140,27 160,26 180,28 C190,29 196,30 200,30" fill="none" stroke="#FF3B30" stroke-width="1.5" stroke-linecap="round"/></svg></div></div>
      <div class="mkt-card"><div class="mkt-card-head"><div><div class="mkt-sym">EUR/USD</div><div class="mkt-name">Euro / US Dollar</div></div><span class="mkt-cat-badge" style="background:rgba(0,122,255,0.12);color:#007AFF;border:1px solid rgba(0,122,255,0.2)">FX</span></div><div class="mkt-price">1.0824</div><div class="mkt-row"><span class="mkt-chg mkt-chg-up">+0.31%</span><span class="mkt-vol">Pre-ECB</span></div><div class="sparkline"><svg viewBox="0 0 200 32" preserveAspectRatio="none"><path d="M0,26 C20,24 40,22 60,20 C80,18 100,20 120,16 C140,12 160,14 180,10 C190,8 196,7 200,7" fill="none" stroke="#34C759" stroke-width="1.5" stroke-linecap="round"/></svg></div></div>
      <div class="mkt-card"><div class="mkt-card-head"><div><div class="mkt-sym">GBP/USD</div><div class="mkt-name">British Pound</div></div><span class="mkt-cat-badge" style="background:rgba(0,122,255,0.12);color:#007AFF;border:1px solid rgba(0,122,255,0.2)">FX</span></div><div class="mkt-price">1.2718</div><div class="mkt-row"><span class="mkt-chg mkt-chg-up">+0.12%</span><span class="mkt-vol">BoE watch</span></div><div class="sparkline"><svg viewBox="0 0 200 32" preserveAspectRatio="none"><path d="M0,22 C30,20 50,24 80,20 C100,17 120,18 140,14 C155,11 175,13 200,10" fill="none" stroke="#34C759" stroke-width="1.5" stroke-linecap="round"/></svg></div></div>
      <div class="mkt-card"><div class="mkt-card-head"><div><div class="mkt-sym">USD/JPY</div><div class="mkt-name">US Dollar / Yen</div></div><span class="mkt-cat-badge" style="background:rgba(0,122,255,0.12);color:#007AFF;border:1px solid rgba(0,122,255,0.2)">FX</span></div><div class="mkt-price">155.42</div><div class="mkt-row"><span class="mkt-chg mkt-chg-dn">−0.05%</span><span class="mkt-vol">BoJ risk</span></div><div class="sparkline"><svg viewBox="0 0 200 32" preserveAspectRatio="none"><path d="M0,12 C20,14 40,16 60,18 C80,20 100,17 120,20 C140,22 160,20 180,22 C190,23 196,24 200,24" fill="none" stroke="#FF3B30" stroke-width="1.5" stroke-linecap="round"/></svg></div></div>
      <div class="mkt-card" style="border-color:rgba(124,58,237,0.2);background:linear-gradient(135deg,rgba(124,58,237,0.05),var(--bg3))"><div class="mkt-card-head"><div><div class="mkt-sym" style="color:#C4B5FD">FX Impact</div><div class="mkt-name">IDX Correlation AI</div></div><span class="mkt-cat-badge" style="background:rgba(124,58,237,0.12);color:#A78BFA;border:1px solid rgba(124,58,237,0.2)">AI</span></div><div style="font-size:12.5px;color:var(--text2);line-height:1.65;margin-top:6px">DXY softness di <strong style="color:#C4B5FD">104.2</strong> correlates dengan +1.2% IHSG weekly gain historis. USD/IDR di 15,847 — watch BI intervention signal.</div></div>
    </div>
    <div id="tab-crypto" class="mkt-grid sr d1" style="display:none">
      <div class="mkt-card"><div class="mkt-card-head"><div><div class="mkt-sym">BTC</div><div class="mkt-name">Bitcoin / USD</div></div><span class="mkt-cat-badge" style="background:rgba(255,159,10,0.12);color:#FF9F0A;border:1px solid rgba(255,159,10,0.2)">Crypto</span></div><div class="mkt-price">69,420</div><div class="mkt-row"><span class="mkt-chg mkt-chg-up">+2.34%</span><span class="mkt-vol">Vol $38.2B</span></div><div class="sparkline"><svg viewBox="0 0 200 32" preserveAspectRatio="none"><path d="M0,28 C20,24 40,22 60,18 C80,14 100,16 120,12 C140,8 160,10 180,7 C190,6 196,5 200,4" fill="none" stroke="#34C759" stroke-width="1.5" stroke-linecap="round"/></svg></div></div>
      <div class="mkt-card"><div class="mkt-card-head"><div><div class="mkt-sym">ETH</div><div class="mkt-name">Ethereum / USD</div></div><span class="mkt-cat-badge" style="background:rgba(255,159,10,0.12);color:#FF9F0A;border:1px solid rgba(255,159,10,0.2)">Crypto</span></div><div class="mkt-price">3,782</div><div class="mkt-row"><span class="mkt-chg mkt-chg-up">+1.87%</span><span class="mkt-vol">Vol $14.6B</span></div><div class="sparkline"><svg viewBox="0 0 200 32" preserveAspectRatio="none"><path d="M0,26 C20,22 40,20 60,16 C80,12 100,15 120,11 C140,7 160,9 180,6 C190,5 196,4 200,3" fill="none" stroke="#34C759" stroke-width="1.5" stroke-linecap="round"/></svg></div></div>
      <div class="mkt-card"><div class="mkt-card-head"><div><div class="mkt-sym">BTC.D</div><div class="mkt-name">Bitcoin Dominance</div></div><span class="mkt-cat-badge" style="background:rgba(255,159,10,0.12);color:#FF9F0A;border:1px solid rgba(255,159,10,0.2)">Crypto</span></div><div class="mkt-price">54.7%</div><div class="mkt-row"><span class="mkt-chg mkt-chg-up">+0.4%</span><span class="mkt-vol">Alt season risk</span></div><div class="sparkline"><svg viewBox="0 0 200 32" preserveAspectRatio="none"><path d="M0,18 C20,16 40,14 60,16 C80,18 100,14 120,12 C140,10 160,12 180,11 C190,11 196,10 200,10" fill="none" stroke="#34C759" stroke-width="1.5" stroke-linecap="round"/></svg></div></div>
      <div class="mkt-card"><div class="mkt-card-head"><div><div class="mkt-sym">SOL</div><div class="mkt-name">Solana / USD</div></div><span class="mkt-cat-badge" style="background:rgba(255,159,10,0.12);color:#FF9F0A;border:1px solid rgba(255,159,10,0.2)">Crypto</span></div><div class="mkt-price">182.4</div><div class="mkt-row"><span class="mkt-chg mkt-chg-up">+3.12%</span><span class="mkt-vol">Vol $4.8B</span></div><div class="sparkline"><svg viewBox="0 0 200 32" preserveAspectRatio="none"><path d="M0,30 C20,26 40,24 60,20 C80,16 100,18 120,13 C140,8 160,10 180,6 C190,4 196,4 200,3" fill="none" stroke="#34C759" stroke-width="1.5" stroke-linecap="round"/></svg></div></div>
      <div class="mkt-card"><div class="mkt-card-head"><div><div class="mkt-sym">TOTAL</div><div class="mkt-name">Crypto Market Cap</div></div><span class="mkt-cat-badge" style="background:rgba(255,159,10,0.12);color:#FF9F0A;border:1px solid rgba(255,159,10,0.2)">Crypto</span></div><div class="mkt-price">$2.48T</div><div class="mkt-row"><span class="mkt-chg mkt-chg-up">+1.9%</span><span class="mkt-vol">Risk-on mode</span></div><div class="sparkline"><svg viewBox="0 0 200 32" preserveAspectRatio="none"><path d="M0,26 C20,22 50,20 80,16 C100,13 120,15 140,11 C160,7 180,8 200,5" fill="none" stroke="#34C759" stroke-width="1.5" stroke-linecap="round"/></svg></div></div>
      <div class="mkt-card" style="border-color:rgba(255,159,10,0.2);background:linear-gradient(135deg,rgba(255,159,10,0.04),var(--bg3))"><div class="mkt-card-head"><div><div class="mkt-sym" style="color:#FF9F0A">Crypto Impact</div><div class="mkt-name">IDX Correlation AI</div></div><span class="mkt-cat-badge" style="background:rgba(124,58,237,0.12);color:#A78BFA;border:1px solid rgba(124,58,237,0.2)">AI</span></div><div style="font-size:12.5px;color:var(--text2);line-height:1.65;margin-top:6px">BTC di atas 68K historically precedes risk-on rotation ke EM equities. <strong style="color:#FF9F0A">IHSG</strong> tech-adjacent stocks (GOTO, EMTK) tunjukkan elevated beta correlation.</div></div>
    </div>
    <div id="tab-commodities" class="mkt-grid sr d1" style="display:none">
      <div class="mkt-card"><div class="mkt-card-head"><div><div class="mkt-sym">GOLD</div><div class="mkt-name">Gold Spot / USD</div></div><span class="mkt-cat-badge" style="background:rgba(255,159,10,0.12);color:#FF9F0A;border:1px solid rgba(255,159,10,0.2)">Commodity</span></div><div class="mkt-price">2,318</div><div class="mkt-row"><span class="mkt-chg mkt-chg-up">+0.42%</span><span class="mkt-vol">oz/USD</span></div><div class="sparkline"><svg viewBox="0 0 200 32" preserveAspectRatio="none"><path d="M0,22 C20,20 40,18 60,16 C80,14 100,16 120,12 C140,8 160,10 180,8 C190,7 196,6 200,6" fill="none" stroke="#34C759" stroke-width="1.5"/></svg></div></div>
      <div class="mkt-card"><div class="mkt-card-head"><div><div class="mkt-sym">CPO</div><div class="mkt-name">Crude Palm Oil</div></div><span class="mkt-cat-badge" style="background:rgba(255,159,10,0.12);color:#FF9F0A;border:1px solid rgba(255,159,10,0.2)">Commodity</span></div><div class="mkt-price">3,924</div><div class="mkt-row"><span class="mkt-chg mkt-chg-up">+1.14%</span><span class="mkt-vol">MYR/ton</span></div><div class="sparkline"><svg viewBox="0 0 200 32" preserveAspectRatio="none"><path d="M0,24 C20,22 40,20 60,18 C80,14 100,16 120,12 C140,10 160,11 180,8 C195,6 198,5 200,5" fill="none" stroke="#34C759" stroke-width="1.5"/></svg></div></div>
      <div class="mkt-card"><div class="mkt-card-head"><div><div class="mkt-sym">COAL</div><div class="mkt-name">Thermal Coal</div></div><span class="mkt-cat-badge" style="background:rgba(255,159,10,0.12);color:#FF9F0A;border:1px solid rgba(255,159,10,0.2)">Commodity</span></div><div class="mkt-price">124.5</div><div class="mkt-row"><span class="mkt-chg mkt-chg-dn">−0.88%</span><span class="mkt-vol">USD/ton</span></div><div class="sparkline"><svg viewBox="0 0 200 32" preserveAspectRatio="none"><path d="M0,8 C20,10 40,12 60,14 C80,16 100,14 120,18 C140,22 160,20 180,24 C190,26 196,27 200,28" fill="none" stroke="#FF3B30" stroke-width="1.5"/></svg></div></div>
      <div class="mkt-card"><div class="mkt-card-head"><div><div class="mkt-sym">WTI</div><div class="mkt-name">Crude Oil WTI</div></div><span class="mkt-cat-badge" style="background:rgba(255,159,10,0.12);color:#FF9F0A;border:1px solid rgba(255,159,10,0.2)">Commodity</span></div><div class="mkt-price">78.24</div><div class="mkt-row"><span class="mkt-chg mkt-chg-up">+0.66%</span><span class="mkt-vol">USD/bbl</span></div><div class="sparkline"><svg viewBox="0 0 200 32" preserveAspectRatio="none"><path d="M0,20 C20,18 40,16 60,14 C80,12 100,14 120,10 C140,8 160,10 180,8 C190,7 196,6 200,6" fill="none" stroke="#34C759" stroke-width="1.5"/></svg></div></div>
      <div class="mkt-card"><div class="mkt-card-head"><div><div class="mkt-sym">NICKEL</div><div class="mkt-name">Nickel LME</div></div><span class="mkt-cat-badge" style="background:rgba(255,159,10,0.12);color:#FF9F0A;border:1px solid rgba(255,159,10,0.2)">Commodity</span></div><div class="mkt-price">16,420</div><div class="mkt-row"><span class="mkt-chg mkt-chg-up">+1.22%</span><span class="mkt-vol">USD/ton</span></div><div class="sparkline"><svg viewBox="0 0 200 32" preserveAspectRatio="none"><path d="M0,24 C20,20 40,22 60,18 C80,14 100,16 120,12 C140,8 160,10 180,8 C190,7 198,6 200,6" fill="none" stroke="#34C759" stroke-width="1.5"/></svg></div></div>
      <div class="mkt-card" style="border-color:rgba(255,159,10,0.18);background:linear-gradient(135deg,rgba(255,159,10,0.04),var(--bg3))"><div class="mkt-card-head"><div><div class="mkt-sym" style="color:#FF9F0A">Commodity Impact</div><div class="mkt-name">IDX Sector AI</div></div><span class="mkt-cat-badge" style="background:rgba(124,58,237,0.12);color:#A78BFA;border:1px solid rgba(124,58,237,0.2)">AI</span></div><div style="font-size:12.5px;color:var(--text2);line-height:1.65;margin-top:6px">CPO rally mendukung <strong style="color:#FF9F0A">AALI, LSIP</strong>. Nickel momentum benefit <strong style="color:#FF9F0A">INCO, MDKA</strong>. Coal softness tekan PTBA near-term.</div></div>
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section id="how">
  <div class="container section">
    <div class="sr" style="text-align:center">
      <span class="eyebrow">Intelligence Pipeline</span>
      <h2 class="section-h">Signal to decision, in three steps</h2>
    </div>
    <div class="how-grid sr d1">
      <div class="how-step">
        <div class="how-num">01</div>
        <div class="how-title">Ingest &amp; Classify</div>
        <p class="how-desc">MOONSIDE ingests broker transactions dari IDX, foreign net flows harian, Forex rates, Crypto dominance, commodity prices, dan macro economic prints — classifying tiap signal berdasarkan institutional intent dan urgency.</p>
        <div class="how-arr">→</div>
      </div>
      <div class="how-step">
        <div class="how-num">02</div>
        <div class="how-title">Score &amp; Surface</div>
        <p class="how-desc">Sigma Score engine cross-validates 5 faktor — teknikal, volume, bandar, fundamental, dan momentum RS — lalu surface anomaly yang statistically significant dengan confidence level dan global macro overlay.</p>
        <div class="how-arr">→</div>
      </div>
      <div class="how-step">
        <div class="how-num">03</div>
        <div class="how-title">Plan &amp; Execute</div>
        <p class="how-desc">AI Research layer mentranslate raw signals jadi structured trade plans — lengkap dengan TP1, TP2, SL, entry zone, dan macro narrative. Track record otomatis tersimpan untuk evaluasi performance.</p>
      </div>
    </div>
  </div>
</section>

<!-- PRICING -->
<section id="pricing" class="section">
  <div class="container">
    <div class="sr" style="text-align:center">
      <span class="eyebrow" style="display:block;text-align:center">Access Tiers</span>
      <h2 class="section-h" style="text-align:center">Priced for serious operators</h2>
      <p class="section-p" style="text-align:center;margin:0 auto">Bukan untuk retail noise. Tiap tier deliver institutional-grade intelligence.</p>
    </div>
    <div class="pg sr d1">
      <div class="price-card">
        <div class="pt">Analyst</div>
        <div class="pa">Rp 299K</div>
        <div class="pp">per month</div>
        <p class="pd">Entry point untuk investor serius yang upgrade ke institutional-grade thinking.</p>
        <div class="pdiv"></div>
        <div class="pf"><span class="pcheck">✓</span>Market Live Dashboard</div>
        <div class="pf"><span class="pcheck">✓</span>Market Data (Rate, Yield, Dividend)</div>
        <div class="pf"><span class="pcheck">✓</span>Sector Rotation RRG</div>
        <div class="pf"><span class="pcheck">✓</span>Sigma Screener — top 30 stocks</div>
        <div class="pf"><span class="pcheck">✓</span>AI research briefs (5/day)</div>
        <div class="pf"><span class="pcheck">✓</span>Forex &amp; Crypto context</div>
        <button class="pcta pcta-ghost">Get Started</button>
      </div>
      <div class="price-card featured">
        <div class="price-best">MOST POPULAR</div>
        <div class="pt">Pro</div>
        <div class="pa">Rp 799K</div>
        <div class="pp">per month</div>
        <p class="pd">Full access ke MOONSIDE intelligence stack. Untuk portfolio manager &amp; professional trader.</p>
        <div class="pdiv"></div>
        <div class="pf"><span class="pcheck">✓</span>Semua fitur Analyst</div>
        <div class="pf"><span class="pcheck">✓</span>Sigma Screener — full IDX</div>
        <div class="pf"><span class="pcheck">✓</span>IPO Intelligence + Bedah Prospektus</div>
        <div class="pf"><span class="pcheck">✓</span>Sigma Plan (Daily, Weekly, BSJP)</div>
        <div class="pf"><span class="pcheck">✓</span>Track Record &amp; AI Evaluator</div>
        <div class="pf"><span class="pcheck">✓</span>Unlimited AI research briefs</div>
        <div class="pf"><span class="pcheck">✓</span>Full Forex + Crypto + Commodity</div>
        <div class="pf"><span class="pcheck">✓</span>Sigma Calc (ARA, Avg Down, EM)</div>
        <button class="pcta pcta-fill">Get Pro Access</button>
      </div>
      <div class="price-card">
        <div class="pt">Institutional</div>
        <div class="pa" style="font-size:32px">Custom</div>
        <div class="pp">annual · multi-seat</div>
        <p class="pd">White-glove deployment untuk asset manager, family office, dan sekuritas.</p>
        <div class="pdiv"></div>
        <div class="pf"><span class="pcheck">✓</span>Semua fitur Pro</div>
        <div class="pf"><span class="pcheck">✓</span>Dedicated data environment</div>
        <div class="pf"><span class="pcheck">✓</span>API access &amp; webhook integration</div>
        <div class="pf"><span class="pcheck">✓</span>Custom AI model tuning</div>
        <div class="pf"><span class="pcheck">✓</span>Dedicated account manager</div>
        <div class="pf"><span class="pcheck">✓</span>Priority SLA &amp; onboarding</div>
        <button class="pcta pcta-ghost">Contact Sales</button>
      </div>
    </div>
  </div>
</section>

<!-- CTA -->
<section id="cta">
  <div class="cta-orb"></div>
  <div class="cta-grid"></div>
  <div class="container cta-inner">
    <span class="eyebrow sr" style="display:block;text-align:center;margin-bottom:16px">Limited Access · By Application</span>
    <h2 class="cta-h sr">The edge exists.<br><em>Are you ready for it?</em></h2>
    <p class="cta-sub sr d1">MOONSIDE adalah invite-only selama institutional beta. Apply sekarang sebelum public launch.</p>
    <div class="cta-btns sr d2">
      <a href="#" class="btn-p" style="font-size:14.5px;padding:13px 28px">Apply for Access <svg width="13" height="13" viewBox="0 0 13 13" fill="none"><path d="M2 6.5h9M7.5 3l3.5 3.5L7.5 10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
      <a href="#" class="btn-s" style="font-size:14.5px;padding:13px 28px">Read Documentation</a>
    </div>
    <div class="cta-note sr d3">Application diproses dalam 48 jam · Verifikasi institutional wajib</div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="container footer-inner">
    <div>
      <div class="footer-brand">Moonside</div>
      <div class="footer-copy">© 2026 MOONSIDE. Institutional Market Intelligence for Indonesia.</div>
    </div>
    <div class="footer-links">
      <a href="#">Privacy</a><a href="#">Terms</a><a href="#">Security</a><a href="#">Docs</a><a href="#">Contact</a>
    </div>
  </div>
</footer>

<script>
// TICKER
const TICKERS=[
  {sym:'IHSG',price:'7,284',chg:'+1.24%',up:true,cat:'IDX'},
  {sym:'DXY',price:'104.23',chg:'−0.18%',up:false,cat:'FX'},
  {sym:'USD/IDR',price:'15,847',chg:'+0.24%',up:false,cat:'FX'},
  {sym:'EUR/USD',price:'1.0824',chg:'+0.31%',up:true,cat:'FX'},
  {sym:'GBP/USD',price:'1.2718',chg:'+0.12%',up:true,cat:'FX'},
  {sym:'USD/JPY',price:'155.42',chg:'−0.05%',up:false,cat:'FX'},
  {sym:'BTC/USD',price:'69,420',chg:'+2.34%',up:true,cat:'Crypto'},
  {sym:'ETH/USD',price:'3,782',chg:'+1.87%',up:true,cat:'Crypto'},
  {sym:'SOL',price:'182.4',chg:'+3.12%',up:true,cat:'Crypto'},
  {sym:'GOLD',price:'2,318',chg:'+0.42%',up:true,cat:'FX'},
  {sym:'CPO',price:'3,924',chg:'+1.14%',up:true,cat:'FX'},
  {sym:'COAL',price:'124.5',chg:'−0.88%',up:false,cat:'FX'},
  {sym:'WTI',price:'78.24',chg:'+0.66%',up:true,cat:'FX'},
  {sym:'LQ45',price:'847.3',chg:'+0.88%',up:true,cat:'IDX'},
  {sym:'BBCA',price:'9,750',chg:'+1.04%',up:true,cat:'IDX'},
  {sym:'BMRI',price:'5,925',chg:'+0.72%',up:true,cat:'IDX'},
  {sym:'BTC.D',price:'54.7%',chg:'+0.4%',up:true,cat:'Crypto'},
  {sym:'NICKEL',price:'16,420',chg:'+1.22%',up:true,cat:'FX'},
];
const catClass={IDX:'cat-idx',FX:'cat-fx',Crypto:'cat-crypto'};
(function(){
  const track=document.getElementById('tickerTrack');
  const items=[...TICKERS,...TICKERS];
  track.innerHTML=items.map(t=>`
    <div class="tick-item">
      <span class="tick-cat ${catClass[t.cat]||'cat-fx'}">${t.cat}</span>
      <span class="tick-sym">${t.sym}</span>
      <span class="tick-price">${t.price}</span>
      <span class="tick-chg ${t.up?'tick-up':'tick-dn'}">${t.chg}</span>
    </div>`).join('');
})();

// MARKET TABS
function switchMktTab(btn,id){
  document.querySelectorAll('.mtab').forEach(b=>b.classList.remove('on'));
  btn.classList.add('on');
  ['forex','crypto','commodities'].forEach(k=>{
    const el=document.getElementById('tab-'+k);
    if(el)el.style.display=(k===id)?'grid':'none';
  });
}

// SCROLL REVEAL
const io=new IntersectionObserver(entries=>{
  entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('in')});
},{threshold:0.04,rootMargin:'0px 0px -20px 0px'});
document.querySelectorAll('.sr').forEach(el=>io.observe(el));

// COUNTER
const counters=[
  {el:document.querySelector('.mi:nth-child(1) .mv'),target:900,sfx:'+',dec:0,final:'900+'},
  {el:document.querySelector('.mi:nth-child(2) .mv'),target:48,sfx:'',dec:0,final:'48'},
  {el:document.querySelector('.mi:nth-child(3) .mv'),target:7,sfx:' Modules',dec:0,final:'7 Modules'},
  {el:document.querySelector('.mi:nth-child(4) .mv'),target:99.9,sfx:'%',dec:1,final:'99.9%'},
];
let counted=false;
new IntersectionObserver(entries=>{
  if(!entries[0].isIntersecting||counted)return;
  counted=true;
  counters.forEach(c=>{
    if(!c.el)return;
    let start=null;
    function step(ts){
      if(!start)start=ts;
      const p=Math.min((ts-start)/1600,1);
      const ease=1-Math.pow(1-p,3);
      const v=c.target*ease;
      c.el.textContent=(c.dec?v.toFixed(c.dec):Math.floor(v))+c.sfx;
      if(p<1)requestAnimationFrame(step);
      else c.el.textContent=c.final;
    }
    requestAnimationFrame(step);
  });
},{threshold:0.3}).observe(document.getElementById('metrics'));
</script>
</body>
</html>
