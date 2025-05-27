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
    "ff752fdad88180912bf9ca57f8d866a4f7951dd226557834ff3f7dc771f744b3",
    "5861d62596971e448da865320a9ac547e2526fdf9eaf4fb40bf8a9f465bccecb",
]
tool_flags = {"RUSTFLAGS": ["-l", "execinfo"]}
# Check takes an extremely long time
options = ["!check", "!lto"]


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
