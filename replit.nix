{ pkgs }: {
  deps = [
    pkgs.mkinitcpio-nfs-utils
    pkgs.unzip
    pkgs.wget
    pkgs.imagemagick
    pkgs.vim
  ];
}

