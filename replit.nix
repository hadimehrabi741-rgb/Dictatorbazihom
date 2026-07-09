{pkgs}: {
  deps = [
    pkgs.which
    pkgs.git
    pkgs.openssl
    pkgs.libffi
    pkgs.zlib
    pkgs.pkg-config
    pkgs.libtool
    pkgs.automake
    pkgs.autoconf
    pkgs.gradle
    pkgs.openjdk17
    pkgs.unzip
  ];
}
