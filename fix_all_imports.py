from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent

TARGET_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx"}

def log(msg: str) -> None:
    print(f"[fix] {msg}")

def verify_structure() -> None:
    required = [ROOT / "app", ROOT / "src", ROOT / "package.json"]
    missing = [p for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Projectstructuur lijkt niet te kloppen. Ontbreekt: "
            + ", ".join(str(p.relative_to(ROOT)) for p in missing)
        )

def fix_babel() -> None:
    babel_file = ROOT / "babel.config.js"
    content = """module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo']
  };
};
"""
    babel_file.write_text(content, encoding="utf-8")
    log("babel.config.js bijgewerkt")

def fix_tsconfig() -> None:
    tsconfig_file = ROOT / "tsconfig.json"
    if not tsconfig_file.exists():
        log("tsconfig.json niet gevonden, overgeslagen")
        return

    try:
        data = json.loads(tsconfig_file.read_text(encoding="utf-8"))
    except Exception:
        log("tsconfig.json kon niet als JSON gelezen worden, overgeslagen")
        return

    compiler_options = data.get("compilerOptions", {})
    compiler_options.pop("paths", None)
    data["compilerOptions"] = compiler_options

    tsconfig_file.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    log("tsconfig.json bijgewerkt")

def get_relative_src_prefix(file_path: Path) -> str:
    rel_parent = file_path.parent.relative_to(ROOT)
    depth = len(rel_parent.parts)
    return "../" * depth + "src/"

def normalize_duplicate_src(text: str) -> str:
    # ruim dubbele src-segmenten op
    for _ in range(5):
        new_text = text
        new_text = new_text.replace("src/src/", "src/")
        new_text = new_text.replace("../src/src/", "../src/")
        new_text = new_text.replace("../../src/src/", "../../src/")
        new_text = new_text.replace("../../../src/src/", "../../../src/")
        new_text = new_text.replace("../../../../src/src/", "../../../../src/")
        if new_text == text:
            break
        text = new_text
    return text

def replace_alias_imports(text: str, prefix: str) -> str:
    # "@/src/..." -> "<prefix>..."
    text = re.sub(r"from\s+'@/src/", f"from '{prefix}", text)
    text = re.sub(r'from\s+"@/src/', f'from "{prefix}', text)

    # "@/..." -> "<prefix>..."
    text = re.sub(r"from\s+'@/", f"from '{prefix}", text)
    text = re.sub(r'from\s+"@/', f'from "{prefix}', text)

    return text

def fix_file(file_path: Path) -> None:
    text = file_path.read_text(encoding="utf-8")
    original = text

    prefix = get_relative_src_prefix(file_path)
    text = normalize_duplicate_src(text)
    text = replace_alias_imports(text, prefix)
    text = normalize_duplicate_src(text)

    if text != original:
        file_path.write_text(text, encoding="utf-8")
        log(f"Aangepast: {file_path.relative_to(ROOT)}")

def main() -> None:
    log(f"Project root: {ROOT}")
    verify_structure()
    fix_babel()
    fix_tsconfig()

    for folder_name in ("app", "src"):
        folder = ROOT / folder_name
        for file_path in folder.rglob("*"):
            if file_path.is_file() and file_path.suffix in TARGET_EXTENSIONS:
                fix_file(file_path)

    print()
    log("Klaar.")
    log("Start nu opnieuw met:")
    print("  npx expo start -c")

if __name__ == "__main__":
    main()