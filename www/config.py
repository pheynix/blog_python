from config_default import configs as default
from config_override import configs as override


def merge(default, override):
	r = {}
	for k, v in default.items():
		if k in override:
			if isinstance(v, dict):
				r[k] = merge(v, override[k])
			else:
				r[k] = override[k]
		else:
			r[k] = v
	return r


configs = merge(default, override)