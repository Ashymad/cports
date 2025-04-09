pkgname = "gn"
_date = "20250324"
pkgver = f"0_git{_date}"
pkgrel = 0
_gitrev = "6e8e0d6d4a151ab2ed9b4a35366e630c55888444"
hostmakedepends = ["ninja", "python"]
depends = ["ninja"]
pkgdesc = "Build system that generates ninja"
license = "BSD-3-Clause"
url = "https://gn.googlesource.com/gn"
source = f"https://gn.googlesource.com/gn/+archive/{_gitrev}.tar.gz"
sha256 = "a92009e8c07e35a6c9d660936886b33203f7842dcfa84bba244a9d274f8989e8"
hardening = ["vis", "cfi"]

tool_flags = {
    "CXXFLAGS": [
        f"-DLAST_COMMIT_POSITION_NUM={_date}",
        f'-DLAST_COMMIT_POSITION="{_date}"'
    ],
}

def prepare(self):
    with self.pushd(self.build_wrksrc):
        self.ln_s("/dev/null", "src/gn/last_commit_position.h")

def configure(self):
    self.do(
        "python",
        "./build/gen.py",
        "--no-last-commit-position",
        "--no-static-libstdc++",
        "--no-strip",
        "--allow-warnings",
    )


def build(self):
    self.do("ninja", f"-j{self.make_jobs}", "-C", "out")


def check(self):
    self.do("./out/gn_unittests")


def install(self):
    self.install_license("LICENSE")
    self.install_bin("out/gn")
