# Maintainer: alessandro (gort818) <gort818@gmail.com>

pkgname=ddgtk
pkgver=0.1
pkgrel=1
pkgdesc='A fronted Gui to dd for making bootable usb disks'
arch=('i686' 'x86_64')
license=('GPL3')
url="https://github.com/gort818/${pkgname%-git}"
depends=('python3' 'python-gobject' 'gtk3' 'vte' 'meson')
options=('!emptydirs')
source=('ddgtk::git+https://github.com/gort818/ddgtk#branch=master')
sha1sums=('SKIP')
provides=("${pkgname%-git}")
conflicts=("${pkgname%-git}")

pkgver() {
	cd "${pkgname%-git}"
	git describe --tags | sed 's/\([^-]*-g\)/r\1/;s/-/./g'
}

build() {
	cd "$srcdir/${pkgname%-git}"
	meson build
	cd "$srcdir/${pkgname%-git}/build"
	ninja
}
package() {
    cd "$srcdir/${pkgname%-git}/build"
    sudo ninja install
}
