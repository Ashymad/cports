pkgname = "libexecinfo"
pkgver = "10.1"
pkgrel = 1
build_wrksrc = f"src/lib/{pkgname}"
build_style = "makefile"
make_cmd = "bmake"
hostmakedepends = [
    "bmake",
]
makedepends = [
    "elfutils-devel",
]
depends = [
    "elfutils",
]
pkgdesc = "Lbsidjhsadkjh"
maintainer = "Ashymad <ashymad@posteo.net>"
license = "BSD-2-Clause"
url = "https://www.netbsd.org"
source = (
    f"https://cdn.netbsd.org/pub/NetBSD/NetBSD-{pkgver}/source/sets/src.tgz"
)
sha256 = "4f9cbe87cf7ec9024345cd433908d355b4b91e22b1dac62b375179352e6be399"
tool_flags = {
    "CFLAGS": [
        "-Iinclude",
        "-D__END_DECLS=",
        "-D__BEGIN_DECLS=",
        "-D__RCSID(x)=",
        "-D__printflike(x,y)=",
    ],
    "LDFLAGS": ["-lelf"],
}

def prepare(self):
    with self.pushd(self.build_wrksrc):
        self.mkdir("include/sys", parents=True)
        self.ln_s("/dev/null", "include/sys/cdefs.h")

@subpackage(f"{pkgname}-devel")
def _(self):
    return self.default_devel()

def post_install(self):
    self.install_license("../../distrib/notes/common/legal.common")

def check(self):
    pass
