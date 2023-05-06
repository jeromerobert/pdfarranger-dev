# TODO: keep data_files until we find a better way
# Use this file for windows also and simplify setup_win32.py

import setuptools
import glob
import subprocess
import os
import shutil
from os.path import join
from setuptools.command.build import build
from setuptools.command.install import install

SHARE_FILES = [
    ("applications", ["data", "com.github.jeromerobert.pdfarranger.desktop"]),
    ("pdfarranger", ["data", "pdfarranger.ui"]),
    ("pdfarranger", ["data", "menu.ui"]),
    ("man/man1", ["doc", "pdfarranger.1"]),
    ("metainfo", ["data", "com.github.jeromerobert.pdfarranger.metainfo.xml"]),
]


class build_mo(setuptools.Command):
    description = "Build gettext .mo files"

    def initialize_options(self):
        self.build_base = None

    def finalize_options(self):
        self.set_undefined_options("build", ("build_base", "build_base"))

    def run(self):
        mo_dir = join(self.build_base, "mo")
        for filename in glob.glob(join("po", "*.po")):
            lang = os.path.basename(filename)[:-3]
            lang_dir = join(self.build_base, "mo", lang, "LC_MESSAGES")
            os.makedirs(lang_dir, exist_ok=True)
            subprocess.check_call(
                ["msgfmt", filename, "-o", join(lang_dir, "pdfarranger.mo")]
            )


def _dir_to_data_files(src_dir, target_dir):
    data_files = []
    for root, _, files in os.walk(src_dir):
        tgt = join(target_dir, os.path.relpath(root, src_dir))
        if files:
            data_files.append((tgt, [join(root, f) for f in files]))
    return data_files


class build_others(setuptools.Command):
    description = "Ensure icons, gettext and freedesktop files get installed"

    def initialize_options(self):
        self.install_base = None
        self.build_base = None
        self.outfiles = []

    def finalize_options(self):
        self.set_undefined_options("install", ("install_base", "install_base"))
        self.set_undefined_options("build", ("build_base", "build_base"))

    def run(self):
        src_icons = join("data", "icons")
        src_mo = join(self.build_base, "mo")
        data_files = self.distribution.data_files
        if data_files is None:
            data_files = []
            self.distribution.data_files = data_files
        tgt_icons = join("share", "icons")
        tgt_mo = join("share", "locale")
        for dst, src in SHARE_FILES:
            data_files.append((join("share", dst), [join(*src)]))
        data_files.extend(_dir_to_data_files(src_icons, tgt_icons))
        data_files.extend(_dir_to_data_files(src_mo, tgt_mo))


class install_others(setuptools.Command):
    description = "Install icons, gettext and freedesktop files"

    def initialize_options(self):
        self.install_base = None
        self.build_base = None
        self.outfiles = []

    def finalize_options(self):
        self.set_undefined_options("install", ("install_base", "install_base"))
        self.set_undefined_options("build", ("build_base", "build_base"))

    def run(self):
        share_dir = join(self.install_base, "share")
        src_icons = join("data", "icons")
        src_mo = join(self.build_base, "mo")
        # data_files has been removed so we manually copy files at their
        # installation location. pip uninstall will not work properly. This is
        # because the will of PyPA is that pip / setuptools are only used to
        # manage files in site-package folder. For GTK applications this is
        # impossible.
        tgt_icons = join(share_dir, "icons")
        tgt_mo = join(share_dir, "locale")
        for dst, src in SHARE_FILES:
            dst_dir = join(share_dir, dst)
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy(join(*src), join(dst_dir, src[-1]))
        shutil.copytree(src_icons, tgt_icons, dirs_exist_ok=True)
        shutil.copytree(src_mo, tgt_mo, dirs_exist_ok=True)


build.sub_commands.append(("build_mo", lambda _: True))
build.sub_commands.append(("build_others", lambda _: True))
install.sub_commands.append(("install_others", lambda _: True))
