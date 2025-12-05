#!/usr/bin/env python3
"""
Script pour vérifier et mettre à jour automatiquement les URLs des providers.

Usage:
    uv run check_urls.py              # Vérifie les URLs, affiche les changements
    uv run check_urls.py --update     # Met à jour settings.py si redirections
    uv run check_urls.py --commit     # Update + git commit automatique
"""

import argparse
import re
import subprocess
import sys
from urllib.parse import urlparse

import cloudscraper
import requests

SETTINGS_FILE = "scrapddl/settings.py"
README_FILE = "README.md"

# Mapping: variable name -> provider name
PROVIDERS = {
    "ED_DOMAIN": "Extrem Down",
    "ZT_DOMAIN": "Zone Telechargement",
    "WC_DOMAIN": "Wawacity",
    "TR_DOMAIN": "Tirexo",
    "AT_DOMAIN": "Annuaire Telechargement",
}

# TLDs alternatifs à tester quand un site est down
ALTERNATIVE_TLDS = [
    ".live", ".irish", ".ws", ".cc", ".best", ".plus", ".ink",
    ".art", ".uno", ".vet", ".org", ".com", ".net", ".re", ".cx",
]


def get_current_domains() -> dict[str, str]:
    """Lit les domaines actuels depuis settings.py"""
    domains = {}
    pattern = re.compile(r'^(\w+_DOMAIN)\s*=\s*["\']([^"\']+)["\']')

    with open(SETTINGS_FILE, "r") as f:
        for line in f:
            match = pattern.match(line.strip())
            if match:
                var_name, url = match.groups()
                domains[var_name] = url

    return domains


def check_url_accessible(url: str, timeout: int = 10) -> tuple[bool, str | None]:
    """
    Vérifie si une URL est accessible.
    Retourne (accessible, url_finale_si_redirect)
    """
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, allow_redirects=True, timeout=timeout)

        if response.status_code < 400:
            final_url = response.url
            original_domain = urlparse(url).netloc
            final_domain = urlparse(final_url).netloc

            if original_domain != final_domain:
                parsed = urlparse(final_url)
                new_base = f"{parsed.scheme}://{parsed.netloc}/"
                return True, new_base

            return True, None

        return False, None

    except requests.exceptions.RequestException:
        return False, None


def find_alternative_url(url: str) -> str | None:
    """
    Essaie de trouver une URL alternative qui fonctionne
    en testant différents TLDs.
    """
    parsed = urlparse(url)
    domain = parsed.netloc

    # Extraire le nom de base sans TLD
    # ex: www.extrem-down.live -> www.extrem-down
    parts = domain.rsplit(".", 1)
    if len(parts) != 2:
        return None

    base_domain = parts[0]

    for tld in ALTERNATIVE_TLDS:
        test_domain = f"{base_domain}{tld}"
        test_url = f"{parsed.scheme}://{test_domain}/"

        if test_url == url:
            continue

        try:
            accessible, redirect_url = check_url_accessible(test_url, timeout=8)
            if accessible:
                return redirect_url or test_url
        except Exception:
            continue

    return None


def check_url_redirect(url: str) -> tuple[str | None, str | None]:
    """
    Vérifie si une URL redirige vers un autre domaine.
    Si le site est down, essaie des TLDs alternatifs.
    Retourne (nouveau_domaine, erreur) - l'un des deux est None
    """
    try:
        # Essayer avec cloudscraper d'abord (bypass Cloudflare)
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, allow_redirects=True, timeout=15)

        final_url = response.url
        original_domain = urlparse(url).netloc
        final_domain = urlparse(final_url).netloc

        if original_domain != final_domain:
            # Construire la nouvelle URL de base
            parsed = urlparse(final_url)
            new_base = f"{parsed.scheme}://{parsed.netloc}/"
            return new_base, None

        return None, None

    except requests.exceptions.RequestException as e:
        # Le site est down, essayer des TLDs alternatifs
        return None, str(e)


def check_all_urls(domains: dict[str, str], try_alternatives: bool = True) -> dict[str, dict]:
    """Vérifie toutes les URLs et retourne les résultats"""
    results = {}

    for var_name, url in domains.items():
        provider = PROVIDERS.get(var_name, var_name)
        print(f"Vérification {provider}... ", end="", flush=True)

        new_url, error = check_url_redirect(url)

        if error:
            print(f"DOWN", end="", flush=True)

            if try_alternatives:
                print(f" - recherche alternative... ", end="", flush=True)
                alt_url = find_alternative_url(url)

                if alt_url:
                    print(f"TROUVÉ -> {alt_url}")
                    results[var_name] = {"status": "redirect", "old": url, "new": alt_url}
                else:
                    print(f"AUCUNE")
                    results[var_name] = {"status": "error", "error": error, "old": url}
            else:
                print(f" ({error})")
                results[var_name] = {"status": "error", "error": error, "old": url}

        elif new_url:
            print(f"REDIRECTION -> {new_url}")
            results[var_name] = {"status": "redirect", "old": url, "new": new_url}
        else:
            print("OK")
            results[var_name] = {"status": "ok", "old": url}

    return results


def update_settings(results: dict[str, dict]) -> list[str]:
    """Met à jour settings.py avec les nouvelles URLs"""
    changes = []

    with open(SETTINGS_FILE, "r") as f:
        content = f.read()

    for var_name, result in results.items():
        if result["status"] == "redirect":
            old_url = result["old"]
            new_url = result["new"]

            # Remplacer l'ancienne URL par la nouvelle
            pattern = rf'({var_name}\s*=\s*["\']){re.escape(old_url)}(["\'])'
            replacement = rf"\g<1>{new_url}\g<2>"
            new_content = re.sub(pattern, replacement, content)

            if new_content != content:
                content = new_content
                provider = PROVIDERS.get(var_name, var_name)
                changes.append(f"{provider}: {old_url} -> {new_url}")

    if changes:
        with open(SETTINGS_FILE, "w") as f:
            f.write(content)

    return changes


def update_readme(results: dict[str, dict]) -> int:
    """Met à jour README.md avec les nouvelles URLs"""
    count = 0

    with open(README_FILE, "r") as f:
        content = f.read()

    for var_name, result in results.items():
        if result["status"] == "redirect":
            old_url = result["old"]
            new_url = result["new"]

            # Remplacer toutes les occurrences de l'ancienne URL
            if old_url in content:
                content = content.replace(old_url, new_url)
                count += 1

    if count:
        with open(README_FILE, "w") as f:
            f.write(content)

    return count


def git_commit(changes: list[str]) -> bool:
    """Crée un commit git avec les changements"""
    if not changes:
        return False

    try:
        # Stage settings.py et README.md
        subprocess.run(["git", "add", SETTINGS_FILE, README_FILE], check=True)

        # Créer le message de commit
        message = "Update provider URLs\n\n" + "\n".join(f"- {c}" for c in changes)

        # Commit
        subprocess.run(["git", "commit", "-m", message], check=True)
        print(f"\nCommit créé avec {len(changes)} changement(s)")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Erreur git: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Vérifie et met à jour les URLs des providers"
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Met à jour settings.py si des redirections sont détectées",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Met à jour et crée un commit git automatiquement",
    )
    parser.add_argument(
        "--no-search",
        action="store_true",
        help="Ne pas chercher d'alternatives si un site est down",
    )
    args = parser.parse_args()

    print("=== Vérification des URLs des providers ===\n")

    # Lire les domaines actuels
    domains = get_current_domains()
    if not domains:
        print("Aucun domaine trouvé dans settings.py")
        sys.exit(1)

    # Vérifier les URLs
    results = check_all_urls(domains, try_alternatives=not args.no_search)

    # Compter les redirections
    redirects = [r for r in results.values() if r["status"] == "redirect"]
    errors = [r for r in results.values() if r["status"] == "error"]

    print(f"\n=== Résumé ===")
    print(f"Providers vérifiés: {len(results)}")
    print(f"Redirections détectées: {len(redirects)}")
    print(f"Erreurs: {len(errors)}")

    if not redirects:
        print("\nAucune mise à jour nécessaire.")
        sys.exit(0)

    # Mise à jour si demandé
    if args.update or args.commit:
        print("\n=== Mise à jour des fichiers ===")
        changes = update_settings(results)
        readme_count = update_readme(results)

        if changes:
            print(f"settings.py: {len(changes)} URL(s) mise(s) à jour:")
            for change in changes:
                print(f"  - {change}")

            if readme_count:
                print(f"README.md: {readme_count} URL(s) mise(s) à jour")

            # Commit si demandé
            if args.commit:
                print("\n=== Commit git ===")
                git_commit(changes)
        else:
            print("Aucun changement effectué.")
    else:
        print("\nUtilisez --update pour mettre à jour settings.py et README.md")
        print("Utilisez --commit pour mettre à jour et créer un commit")


if __name__ == "__main__":
    main()
