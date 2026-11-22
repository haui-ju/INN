#!/usr/bin/env python3
"""Lector y escritor de un subconjunto de YAML, con comentarios (solo biblioteca estándar).

Soporta: mapas anidados (sangría de 2 espacios), listas con «- » (de escalares o de mapas),
escalares (texto con o sin comillas, enteros, decimales, true/false, null), «{}» y «[]»
vacíos y comentarios «#». Todo lo demás (anclas, listas o mapas en línea con contenido,
bloques multilínea, tabuladores) se rechaza con la línea y la causa.

  loads(texto) -> objeto
  dumps(objeto, comentario=None) -> texto
      comentario(ruta) -> texto breve o None; ruta es «a.b» y «lista[].campo» para elementos.
"""
import json
import re

INDENT = 2


class YamlError(ValueError):
    def __init__(self, msg, line=None):
        super().__init__(f"línea {line}: {msg}" if line else msg)
        self.line = line


# ---------------------------------------------------------------- lectura
def _strip_comment(s):
    """Quita el comentario final respetando comillas."""
    q = None
    i = 0
    while i < len(s):
        c = s[i]
        if q:
            if q == '"' and c == "\\":
                i += 2
                continue
            if c == q:
                if q == "'" and s[i + 1:i + 2] == "'":
                    i += 2
                    continue
                q = None
        elif c in "\"'":
            q = c
        elif c == "#" and (i == 0 or s[i - 1] in " \t"):
            return s[:i]
        i += 1
    return s


def _split_key(s):
    """Si s empieza con «clave:» devuelve (clave, resto); si no, None."""
    s = s.strip()
    if not s:
        return None
    if s[0] in "\"'":
        q = s[0]
        i = 1
        while i < len(s):
            if q == '"' and s[i] == "\\":
                i += 2
                continue
            if s[i] == q:
                if q == "'" and s[i + 1:i + 2] == "'":
                    i += 2
                    continue
                break
            i += 1
        else:
            return None
        key = _scalar(s[:i + 1], 0)
        rest = s[i + 1:]
        if rest.startswith(":") and (len(rest) == 1 or rest[1] == " "):
            return str(key), rest[1:].strip()
        return None
    m = re.match(r"^([^\s:#\[\]{},&*!|>'\"%@`-][^:]*?|-[^\s:][^:]*?)\s*:(?:\s+(.*))?$", s)
    if m:
        return m.group(1), (m.group(2) or "").strip()
    return None


def _scalar(t, line):
    t = t.strip()
    if t == "" or t in ("null", "~", "Null", "NULL"):
        return None
    if t in ("true", "True", "TRUE"):
        return True
    if t in ("false", "False", "FALSE"):
        return False
    if t == "{}":
        return {}
    if t == "[]":
        return []
    if t[0] == '"':
        if len(t) < 2 or t[-1] != '"':
            raise YamlError("comillas dobles sin cerrar", line)
        try:
            return json.loads(t)
        except json.JSONDecodeError:
            raise YamlError("texto entre comillas dobles inválido", line)
    if t[0] == "'":
        if len(t) < 2 or t[-1] != "'":
            raise YamlError("comillas simples sin cerrar", line)
        return t[1:-1].replace("''", "'")
    if t[0] in "[{&*!|>%@`":
        raise YamlError(f"construcción YAML no soportada: «{t[:20]}»", line)
    if re.fullmatch(r"-?\d+", t):
        return int(t)
    if re.fullmatch(r"-?\d+\.\d+", t):
        return float(t)
    return t


def loads(text):
    rows = []
    for n, raw in enumerate(text.splitlines(), 1):
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise YamlError("no se permiten tabuladores en la sangría", n)
        body = _strip_comment(raw).rstrip()
        if not body.strip():
            continue
        ind = len(body) - len(body.lstrip(" "))
        rows.append((ind, body.strip(), n))
    if not rows:
        return None
    val, i = _block(rows, 0, rows[0][0])
    if i != len(rows):
        raise YamlError("sangría inesperada", rows[i][2])
    return val


def _block(rows, i, ind):
    if rows[i][1].startswith("- ") or rows[i][1] == "-":
        return _list(rows, i, ind)
    return _map(rows, i, ind)


def _map(rows, i, ind):
    out = {}
    while i < len(rows) and rows[i][0] == ind and not (rows[i][1].startswith("- ") or rows[i][1] == "-"):
        _, content, n = rows[i]
        kv = _split_key(content)
        if kv is None:
            raise YamlError(f"se esperaba «clave: valor», se encontró «{content[:30]}»", n)
        key, rest = kv
        if key in out:
            raise YamlError(f"clave repetida «{key}»", n)
        i += 1
        if rest == "":
            if i < len(rows) and (rows[i][0] > ind or (rows[i][0] == ind and (rows[i][1].startswith("- ") or rows[i][1] == "-"))):
                out[key], i = _block(rows, i, rows[i][0])
            else:
                out[key] = None
        else:
            out[key] = _scalar(rest, n)
    if i < len(rows) and rows[i][0] > ind:
        raise YamlError("sangría inesperada", rows[i][2])
    return out, i


def _list(rows, i, ind):
    out = []
    while i < len(rows) and rows[i][0] == ind and (rows[i][1].startswith("- ") or rows[i][1] == "-"):
        _, content, n = rows[i]
        rest = content[1:].strip()
        if rest == "":
            i += 1
            if i < len(rows) and rows[i][0] > ind:
                v, i = _block(rows, i, rows[i][0])
            else:
                v = None
            out.append(v)
        elif _split_key(rest) is not None:
            # elemento mapa: la primera clave está en esta línea, el resto alineado debajo
            sub_ind = ind + (len(content) - len(content[1:].lstrip()))
            rows[i] = (sub_ind, rest, n)
            v, i = _map(rows, i, sub_ind)
            out.append(v)
        else:
            out.append(_scalar(rest, n))
            i += 1
    return out, i


# ---------------------------------------------------------------- escritura
_PLAIN = re.compile(r"^[^\W\d_][^#:\n]*$|^[\w][^#:\n]*$", re.UNICODE)


def _fmt(v):
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, dict) and not v:
        return "{}"
    if isinstance(v, list) and not v:
        return "[]"
    if isinstance(v, str):
        reservado = v in ("null", "~", "true", "false", "True", "False", "Null", "NULL", "TRUE", "FALSE", "")
        numero = re.fullmatch(r"-?\d+(\.\d+)?", v) is not None
        if (not reservado and not numero and _PLAIN.match(v) and v == v.strip()
                and not v.startswith(("- ", "[", "{", "&", "*", "!", "|", ">", "%", "@", "`", "'", '"'))
                and " #" not in v and ": " not in v):
            return v
        return json.dumps(v, ensure_ascii=False)
    raise YamlError(f"tipo no soportado al escribir: {type(v).__name__}")


def _key(k):
    s = str(k)
    return s if re.fullmatch(r"[\w][\w .\-]*", s, re.UNICODE) and s == s.strip() and not re.fullmatch(r"-?\d+", s) else json.dumps(s, ensure_ascii=False)


def dumps(obj, comentario=None):
    lines = []
    cm = comentario or (lambda ruta: None)

    def tail(path):
        c = cm(path)
        return f"  # {c}" if c else ""

    def put(prefix, k, v, path, ind):
        key = _key(k)
        sub = f"{path}.{k}" if path else str(k)
        if isinstance(v, dict) and v:
            lines.append(f"{prefix}{key}:{tail(sub)}")
            emit_map(v, sub, ind + INDENT)
        elif isinstance(v, list) and v:
            lines.append(f"{prefix}{key}:{tail(sub)}")
            emit_list(v, sub + "[]", ind + INDENT)
        else:
            lines.append(f"{prefix}{key}: {_fmt(v)}{tail(sub)}")

    def emit_map(d, path, ind):
        for k, v in d.items():
            put(" " * ind, k, v, path, ind)

    def emit_list(items, path, ind):
        for it in items:
            pad = " " * ind
            if isinstance(it, dict) and it:
                first = True
                for k, v in it.items():
                    put(f"{pad}- " if first else f"{pad}  ", k, v, path, ind + INDENT)
                    first = False
            elif isinstance(it, (dict, list)) and it:
                raise YamlError("listas anidadas no soportadas al escribir")
            else:
                lines.append(f"{pad}- {_fmt(it)}")

    if isinstance(obj, dict) and obj:
        emit_map(obj, "", 0)
    elif isinstance(obj, list) and obj:
        emit_list(obj, "[]", 0)
    else:
        lines.append(_fmt(obj))
    return "\n".join(lines) + "\n"
