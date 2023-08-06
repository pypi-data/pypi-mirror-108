import plistlib
import os

def makePatch():
    patch_description = {
        "patches": [
            {
                "arch": "arm64",
                "name": "arm64"
            },
            {
                "arch": "armv7",
                "name": "armv7"
            },
            {
                "arch": "x86_64",
                "name": "x86_64"
            },
            {
                "arch": "i386",
                "name": "i386"
            },
        ]
    }

    patch_directory = os.path.join(os.curdir, 'patch')
    os.mkdir(patch_directory)

    # 生成架构描述Plist
    plist_path = os.path.join(patch_directory, 'patch.plist')
    with open(plist_path, 'wb') as fp:
        plistlib.dump(patch_description, fp)

    # 生成各个架构Patch的文件夹
    for patch in patch_description["patches"]:
        patch_arch_dir = os.path.join(patch_directory, patch["name"])
        os.mkdir(patch_arch_dir)

if __name__ == '__main__':
    makePatch()
