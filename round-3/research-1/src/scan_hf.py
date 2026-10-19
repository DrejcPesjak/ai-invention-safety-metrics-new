import json, urllib.request, urllib.parse, re, time
def api(path, params):
    url="https://huggingface.co/api/"+path+"?"+urllib.parse.urlencode(params)
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r: return json.load(r)
        except Exception as e:
            err=e; time.sleep(2)
    return None
terms=["abliterated","gabliterated","MPOA","orthogonal-reflection-bounded","heretic","Derestricted","uncensored","norm-preserving","biprojected","Josiefied","obliterated"]
bad=re.compile(r'gguf|awq|gptq|-mlx|mxfp4|nvfp4|fp8|-4bit|-8bit|-6bit|bnb|exl|imatrix|MNN|W8A8|W4A16|int4|-Q\d', re.I)
seen={}
for t in terms:
    for sort in ["downloads","lastModified"]:
        d=api("models", {"search":t,"limit":200,"sort":sort,"direction":-1})
        if not d: print("FAIL",t); continue
        for m in d:
            mid=m["modelId"]
            if bad.search(mid): continue
            seen.setdefault(mid, {"term":t,"downloads":m.get("downloads")})
print("candidates:", len(seen))
out=[]
for mid,meta in seen.items():
    info=api("models/"+mid, {})
    if not info: continue
    sf=(info.get("safetensors") or {})
    tot=sf.get("total")
    if not tot: continue
    if tot>4.2e9: continue
    cd=info.get("cardData") or {}
    out.append({"repo_id":mid,"params":tot,"base_model":cd.get("base_model"),
                "tags":[x for x in (info.get("tags") or []) if x in ("mlx","gguf")],
                "downloads":info.get("downloads"),"term":meta["term"],
                "created":info.get("createdAt"),"pipeline":info.get("pipeline_tag")})
out.sort(key=lambda x:-(x["downloads"] or 0))
json.dump(out, open("hf_sub4b_candidates.json","w"), indent=1)
print("sub-4.2B:", len(out))
for o in out[:80]: print(f'{o["repo_id"]:70s} {o["params"]/1e9:.2f}B {o["downloads"]} {o["base_model"]}')
