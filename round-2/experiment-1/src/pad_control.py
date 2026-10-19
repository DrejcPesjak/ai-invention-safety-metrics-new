"""Control for the padded-batch logits test: is the residual difference PADDING
or just bf16 batching numerics? Compares equal-length (unpadded) prompts."""
import os; os.environ['HF_HOME']=os.getcwd()+'/hf_home'
import json, torch
from lib_model import Runner, pos_ids
rn=Runner('Qwen/Qwen3-0.6B',None)
texts=["Tell me about the sea.","Tell me about the sky.","Tell me about the sun.","Tell me about the sea."]
enc=rn.encode(texts)
print('lengths',enc['attention_mask'].sum(1).tolist())
_h,lg_b=rn.last_token_states(texts,batch=4)
import torch as T
sing=T.cat([rn.last_token_states([t],batch=1)[1] for t in texts])
mad=float((lg_b-sing).abs().max()); sc=float(lg_b.abs().max())
print(json.dumps({'equal_length_max_abs_diff':mad,'scale':sc,'relative':mad/sc}))
json.dump({'equal_length_max_abs_diff':mad,'logit_scale':sc,'relative_diff':mad/sc,
 'note':'same prompts, equal token lengths -> NO padding involved; any residual is bf16 batched-GEMM numerics'},
 open('results/padding_control.json','w'),indent=2)
