import json
import sys
from pathlib import Path

import httpx
import typer

app = typer.Typer(help="cherenkov Security CLI - Precision in Sovereignty")

API_BASE = "http://localhost:8000/api/v1"


def get_headers():
    token = (
        Path(".cherenkov_token").read_text().strip() if Path(".cherenkov_token").exists() else ""
    )
    return {"Authorization": f"Bearer {token}"}


@app.command()
def scan(
    url: str = typer.Argument(..., help="Target URL to scan"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, sarif)"),
):
    """Run a full security scan against a target URL."""
    try:
        with httpx.Client(timeout=300) as client:
            typer.echo(f"[*] Initiating scan for: {url}")
            resp = client.post(f"{API_BASE}/scan", json={"url": url}, headers=get_headers())
            resp.raise_for_status()
            result = resp.json()

            if format == "sarif":
                # Fetch SARIF export if requested
                scan_id = result.get("scan_id")
                sarif_resp = client.get(
                    f"{API_BASE}/reports/{scan_id}/sarif", headers=get_headers()
                )
                sarif_resp.raise_for_status()
                typer.echo(json.dumps(sarif_resp.json(), indent=2))
            else:
                typer.echo(json.dumps(result, indent=2))

    except Exception as e:
        typer.echo(f"[!] Scan failed: {e}", err=True)
        sys.exit(1)


@app.command()
def report(
    scan_id: str = typer.Argument(..., help="ID of the scan to report"),
    format: str = typer.Option("pdf", "--format", "-f", help="Report format (pdf, sarif)"),
):
    """Generate and download a security report."""
    try:
        with httpx.Client() as client:
            url = f"{API_BASE}/reports/{scan_id}/{format}"
            resp = client.get(url, headers=get_headers())
            resp.raise_for_status()

            output_file = f"report_{scan_id}.{format}"
            with open(output_file, "wb") as f:
                f.write(resp.content)
            typer.echo(f"[+] Report saved to: {output_file}")

    except Exception as e:
        typer.echo(f"[!] Report generation failed: {e}", err=True)
        sys.exit(1)


@app.command()
def login(
    username: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, hide_input=True),
):
    """Authenticate with the Cherenkov API."""
    try:
        with httpx.Client() as client:
            resp = client.post(
                "http://localhost:8000/api/v1/auth/login",
                data={"username": username, "password": password},
            )
            resp.raise_for_status()
            token = resp.json().get("access_token")
            Path(".cherenkov_token").write_text(token)
            typer.echo("[+] Authentication successful. Token saved to .cherenkov_token")
    except Exception as e:
        typer.echo(f"[!] Login failed: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    app()
