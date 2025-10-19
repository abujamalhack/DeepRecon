# replit.nix
{ pkgs }: {
  deps = [
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.python3Packages.virtualenv
    pkgs.chromium
    pkgs.chromedriver
    pkgs.git
    pkgs.psutil
    pkgs.cacert
  ];
  
  env = {
    PYTHONPATH = "./";
    REPLIT_ENVIRONMENT = "production";
  };
}
