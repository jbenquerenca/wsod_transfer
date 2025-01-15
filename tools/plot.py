# read train from log and plots metrics
import os, matplotlib.pyplot as plt, numpy as np, sys
if len(sys.argv) == 1: print("You forgot the log path!"); exit()
with open(sys.argv[1]) as f: 
    best_models = {m:None for m in ["reasonable", "reasonable_small", "heavy", "all"]}
    best_mr = {m:100 for m in ["reasonable", "reasonable_small", "heavy", "all"]}
    results = {m:list() for m in ["models", "reasonable", "reasonable_small", "heavy", "all"]}
    lines = f.read().splitlines()
    for i, l in enumerate(lines):
        if "Reasonable" in l:
            try:
                sl = l.split()

                model = lines[i+1].split()[8]
                reasonable = float(sl[5].split("%")[0])/100
                reasonable_small = float(sl[7].split("%")[0])/100
                heavy = float(sl[9].split("%")[0])/100
                _all = float(sl[11].split("%")[0])/100

                if reasonable < best_mr["reasonable"]:
                    best_mr["reasonable"] = reasonable
                    best_models["reasonable"] = model

                if reasonable_small < best_mr["reasonable_small"]:
                    best_mr["reasonable_small"] = reasonable_small
                    best_models["reasonable_small"] = model
                
                if heavy < best_mr["heavy"]:
                    best_mr["heavy"] = heavy
                    best_models["heavy"] = model

                if _all < best_mr["all"]:
                    best_mr["all"] = _all
                    best_models["all"] = model

                results["models"].append(model)
                results["reasonable"].append(reasonable)
                results["reasonable_small"].append(reasonable_small)
                results["heavy"].append(heavy)
                results["all"].append(_all)

            except: continue
            
print(results)
for m, bmr in best_mr.items(): print(f"{m}\n Model {best_models[m]}: {bmr}")
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
x_axis, y_axis = "iter", "mr"
# Plot for reasonable
ax1.set_title('reasonable')
ax1.set_xlabel(x_axis)
ax1.set_ylabel(y_axis)
ax1.plot(results["models"], results["reasonable"], "-o")
ax1.set_xticklabels(results["models"], rotation=90)

# Plot for reasonable_small
ax2.set_title('reasonable_small')
ax2.set_xlabel(x_axis)
ax2.set_ylabel(y_axis)
ax2.plot(results["models"], results["reasonable_small"], "-o")
ax2.set_xticklabels(results["models"], rotation=90)

# Plot for heavy
ax3.set_title('heavy')
ax3.set_xlabel(x_axis)
ax3.set_ylabel(y_axis)
ax3.plot(results["models"], results["heavy"], "-o")
ax3.set_xticklabels(results["models"], rotation=90)

# Plot for all
ax4.set_title('all')
ax4.set_xlabel(x_axis)
ax4.set_ylabel(y_axis)
ax4.plot(results["models"], results["all"], "-o")
ax4.set_xticklabels(results["models"], rotation=90)

plt.tight_layout()
plt.savefig('plots.png', bbox_inches='tight')
plt.close()
