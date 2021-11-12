import os
import sys
import argparse

from jinja2 import Environment, PackageLoader, select_autoescape

import n5links


def generate_toc(root_dir, exclude_dirs, nghost, n5server, template):
    print(f"Finding volumes in {root_dir} (excluding {exclude_dirs})")
    vol_attrs = n5links.find_volumes(root_dir, exclude_dirs)

    print(f"Constructing links for {len(vol_attrs)} volumes")
    links = n5links.links_for_volumes(vol_attrs, nghost=nghost, n5server=n5server)

    print("Rendering template")
    column_names = 'sample stage section version offset offset_link link'.split()

    return template.render(root_dir=root_dir,
                           entries=links.values(),
                           column_names=column_names)


def main():
    print(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument('--root-dir', default='/nrs/flyem/render/n5')
    parser.add_argument('--exclude-dirs', nargs='*', default=['Z0720_07m_BR', 'Z0720-07m_BR_Sec07', 'Z0720_07m_VNC', 'Z1217_33m_BR', 'Z1217_33m_VNC'])
    parser.add_argument('--nghost', default='http://renderer-data4.int.janelia.org:8080/ng')
    parser.add_argument('--n5server', default='http://renderer-data4.int.janelia.org:8080/n5/flyem')
    parser.add_argument('--out', default='flyem-n5-toc.html')
    args = parser.parse_args()

    env = Environment(
        loader=PackageLoader("n5toc"),
        autoescape=select_autoescape()
    )
    template = env.get_template('n5toc.html.jinja')

    toc = generate_toc(args.root_dir, args.exclude_dirs, args.nghost, args.n5server, template)

    toc_path = os.path.abspath(args.out)
    with open(toc_path, "w") as toc_file:
        toc_file.write(toc)

    print(f'Wrote toc to {toc_path}')


if __name__ == "__main__":
    main()
