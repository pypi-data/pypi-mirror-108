# printvars.py
from typing import Dict, Optional
from colorama import Fore, Back, Style

def _prettyprint(glvars: Dict[str, Dict[str, str]]):
    # print(str(glvars))
    global_vars = glvars.get("*", {})
    for envtype in glvars:
        vars = glvars[envtype]
        if envtype != "*":
            vars = {**vars, **global_vars}
        printvars = []
        for v in vars:
            printvars.append(f"{v}={vars[v]}")
        printvars = sorted(printvars)
        printheader(envtype)
        print(f"\n🦁 {Fore.CYAN}{Style.BRIGHT}Exports{Style.NORMAL}\n")
        for p in printvars:
            print(f"export {p}")
        print(f"{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}\n🤖 {Style.BRIGHT}IntelliJ{Style.NORMAL}\n")
        intellij = ";".join(printvars)
        print(f"{intellij}{Style.RESET_ALL}")
    print("\n")
    return

def printheader(envtype):
    if envtype == "*":
        envtype = "🌎 Global (only)"
    else:
        envtype = f"{envtype}"
    print(f"\n{Style.BRIGHT}{Fore.LIGHTYELLOW_EX}*****************************************")
    print(f"Environment: {envtype}")
    print(f"*****************************************{Style.NORMAL}")
    return
