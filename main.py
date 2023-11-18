import glob
import markdown
import os
import shutil
import webbrowser


def prepare_structure():
    if os.path.isdir("build"):
        shutil.rmtree("build")
    os.mkdir("build")
    shutil.copyfile("src/style.css", "build/style.css")


def load_header(path):
    with open(path) as f:
        return f.read()


def create_html(header, md):
    return header.replace("{{replace}}", markdown.markdown(md))


def build_markdown(header, articles):
    for path in articles:
        article_name = path.split("/")[-1].split(".md")[0]

        if article_name == "index":
            continue

        with open(path) as f:
            print(f"Building {article_name}")
            html = create_html(header, f.read())
            out = open(f"build/{article_name}.html", "w")
            out.write(html)
            out.close()


def build_index(header, articles):
    index_template = open("src/index.md").read()

    links = []

    for path in articles:
        article_name = path.split("/")[-1].split(".md")[0]

        if article_name == "index":
            continue

        display_name = open(path).readline().split("# ")[1]
        links.append((display_name, f"{article_name}.html"))

    article_section = ""

    for name, ref in links:
        article_section += f"<li><a href=\"{ref}\">{name}</a><br></li>"

    body = index_template.replace("{{article_section}}", article_section)
    body = markdown.markdown(body)
    html = header.replace("{{replace}}", body)

    out = open("build/index.html", "w")
    out.write(html)
    out.close()


def build_project(header):
    articles = glob.glob("src/*.md")
    build_markdown(header, articles)
    build_index(header, articles)


if __name__ == "__main__":
    prepare_structure()
    header = load_header("src/header.html")

    build_project(header)
    url = f"file:///{os.getcwd()}/build/index.html"
    webbrowser.open(url, new=2)
