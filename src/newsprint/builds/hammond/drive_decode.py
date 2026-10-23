import json, base64, glob, os, sys
out="/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/dump"
for p in glob.glob("/root/.claude/projects/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/tool-results/mcp-Google_Drive-download_file_content-*.txt"):
    try: d=json.load(open(p))
    except Exception as e: print("bad",p,e); continue
    t=d.get("title") or d.get("id")
    dst=os.path.join(out,t)
    if os.path.exists(dst): continue
    open(dst,"wb").write(base64.b64decode(d["content"])); print("saved",t,os.path.getsize(dst))
