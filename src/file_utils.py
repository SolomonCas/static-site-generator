import os
import shutil
import pathlib

from utils import markdown_to_html_node, extract_title

def copy_contents(src, dst):
    print(os.listdir(src))

    if not os.path.exists(dst):
        os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            copy_contents(src_path, dst_path)
        else:
            shutil.copy(src_path, dst_path)
            print(f"{src_path} -> {dst_path}")

def copy_static_to_public(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)

    copy_contents(src, dst)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_path_markdown = ""
    template = ""

    with open(from_path, "r") as f:
        from_path_markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()


    html_node = markdown_to_html_node(from_path_markdown)
    html = html_node.to_html()
    title = extract_title(from_path_markdown)
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dst_path = os.path.join(dest_dir_path, item)

        if not os.path.isfile(src_path):
            generate_pages_recursive(src_path, template_path, dst_path)
        else:
            check_file = pathlib.Path(src_path)
            if check_file.suffix == ".md":
                dst_path = pathlib.Path(dst_path)
                dst_path = dst_path.with_suffix(".html")
                generate_page(src_path, template_path, dst_path)
