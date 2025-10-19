# replit.nix
{ pkgs }: {
  deps = [
    pkgs.python3
    pkgs.chromium
    pkgs.chromedriver
    pkgs.python3Packages.pip
    pkgs.python3Packages.virtualenv
  ];
}
