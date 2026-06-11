import requests
import os
import re


class ConfluenceHTTP:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

    def get(self, cql, start=0, limit=25):
        query = {
            'cql': cql,
            'start': start,
            'limit': limit
        }
        response = requests.get(
            self.base_url,
            headers=self.headers,
            params=query
        )
        response.raise_for_status()
        return response.json()

    def get_page_body(self, page_id):
        url = self.base_url.replace("/search", f"/{page_id}") + "?expand=body.storage"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_all_pages(self, cql="type=page"):
        pages = []
        start = 0
        limit = 25
        while True:
            result = self.get(cql, start=start, limit=limit)
            pages.extend(result.get("results", []))
            if result.get("size", 0) < limit:
                break
            start += limit
        return pages

    def get_page_pdf(self, page_id):
        url = self.base_url.replace("/rest/api/content/search", f"/spaces/flyingpdf/pdfpageexport.action?pageId={page_id}")
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.content

    def dump_all_pages(self, output_dir, cql="type=page"):
        os.makedirs(output_dir, exist_ok=True)
        pages = self.get_all_pages(cql)
        print(f"Found {len(pages)} pages. Downloading...")

        for i, page in enumerate(pages, 1):
            page_id = page["id"]
            title = page["title"]
            safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)

            try:
                full_page = self.get_page_body(page_id)
                body = full_page.get("body", {}).get("storage", {}).get("value", "")
                html = f"<html><head><meta charset='utf-8'><title>{title}</title></head><body><h1>{title}</h1>{body}</body></html>"
                filename = f"{safe_title}.html"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"  [{i}/{len(pages)}] Saved: {filename}")
            except Exception as e:
                print(f"  [{i}/{len(pages)}] Failed: {title} - {e}")

        print(f"Done. Pages saved to: {output_dir}")

if __name__ == "__main__":
    client = ConfluenceHTTP(
        base_url="https://wiki.allshare.net/rest/api/content/search",
        token="<add-access-token>"
    )
    spaces = input("Enter space keys to download (comma-separated, or leave empty for all): ").strip()
    if spaces:
        space_list = [s.strip() for s in spaces.split(",")]
        cql = "type=page AND (" + " OR ".join(f'space="{s}"' for s in space_list) + ")"
    else:
        cql = "type=page"
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "confluence_pages")
    client.dump_all_pages(output_dir, cql=cql)