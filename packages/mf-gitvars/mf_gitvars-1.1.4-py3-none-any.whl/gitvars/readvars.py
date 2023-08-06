# readvars.py
import json
from typing import Dict, Optional

import gitlab


def _read(project_id: str,
          gitlab_project: Optional[str] = None,
          var_prefix: Optional[str] = None
          ) -> Dict[str, Dict[str, str]]:
    # print(gitlab_project + " " + project_id)
    gl = gitlab.Gitlab.from_config()
    if gitlab_project:
        gl = gitlab.Gitlab.from_config(gitlab_project)
    project = gl.projects.get(project_id)
    p_variables = project.variables.list()
    var_dict = {}
    for v in p_variables:
        v_name = v.key
        if var_prefix:
            v_name = v.key.replace(var_prefix, "")
        if v.environment_scope not in var_dict:
            var_dict[v.environment_scope] = {}
        var_dict[v.environment_scope][v_name] = v.value

    # print(json.dumps(var_dict))
    return var_dict
