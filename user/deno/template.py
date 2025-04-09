pkgname = "deno"
pkgver = "2.2.6"
_v8ver = "135.0.0"
pkgrel = 0
build_wrksrc = "cli"
build_style = "cargo"
make_env = {
    "GN_ARGS": "use_custom_libcxx=false",
    "CLANG_BASE_PATH": "/usr",
    "V8_FROM_SOURCE": "1",
}
hostmakedepends = [
    "cargo-auditable",
    "gmake",
    "gn",
    "pkgconf",
    "ninja",
    "cmake",
    "ccache",
]
makedepends = [
    "zlib-ng-compat-devel",
    "rust-std",
    "zstd-devel",
    "sqlite-devel",
    "libexecinfo-devel",
    "glib-devel",
    "linux-headers",
]
depends = ["zstd", "sqlite"]
pkgdesc = "Runtime for JavaScript and TypeScript"
license = "MIT"
url = "https://github.com/denoland/deno"
source = [
    f"{url}/archive/refs/tags/v{pkgver}.tar.gz",
    f"https://static.crates.io/crates/v8/v8-{_v8ver}.crate",
]
source_paths = ["", "vendor/v8"]
sha256 = [
    "7a4bb87163f68de848faac5e49fee4a432fa83c8e9dcec53daa0c3d3178f3b82",
    "bc24d3e68c7e9b581fce2f0ceb9d1ad61565bf783a36d80d530ccf2be212a295",
]
tool_flags = {"RUSTFLAGS": ["-l", "execinfo"]}
# Check takes an extremely long time
options = ["!check"]


def pre_prepare(self):
    with open(f"{self.srcdir}/.cargo/config.toml", "a") as f:
        f.writelines(
            ["[patch.crates-io]\n", f"v8 = {{ path = '{source_paths[1]}' }}\n"]
        )


def post_prepare(self):
    from cbuild.util import cargo

    cargo.write_vendor_checksum(self, "v8", "")


def init_build(self):
    clang = self.do("clang", "--version", capture_output=True)
    clang_version = clang.stdout.decode("UTF-8").split()[2].split(".")[0]
    self.make_env["GN_ARGS"] += f" clang_version={clang_version}"


def post_install(self):
    self.install_license("../LICENSE.md")
