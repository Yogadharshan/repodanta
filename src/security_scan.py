from src.models import Repo

DANGEROUS_APIS = {
    "eval",
    "exec",
    "pickle",
    "pickle.load",
    "subprocess",
    "subprocess.run",
    "os.system",
    "open",
    "read",
    "write",
    "requests",
}


def scan_dangerous_calls(repo: Repo):

    findings = []

    for module in repo.modules.values():

        for fn in module.functions:

            for call in fn.calls:

                if any(api in call for api in DANGEROUS_APIS):

                    findings.append({
                        "module": module.module_id,
                        "function": fn.name,
                        "line": fn.start_line,
                        "call": call
                    })

    return findings