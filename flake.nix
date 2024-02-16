{
  description = "Adversarial Mastermind";

  inputs = {
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, flake-compat, flake-utils, nixpkgs, ... } @ inputs:
    flake-utils.lib.eachSystem
    [
      flake-utils.lib.system.x86_64-linux
    ]
    (
      system: let
        myPythonPackages = ps: with ps; [
          #numpy
          #pandas
        ];
        pkgs = import nixpkgs {
          inherit system;
        };
        lib = nixpkgs.lib;
      in rec {
        devShells.default = (pkgs.mkShell.override {stdenv = pkgs.gccStdenv;}) {
          packages = with pkgs; [
            (pkgs.python312.withPackages myPythonPackages)
          ];
          buildInputs = with pkgs; [
            qt5.qtwayland
            libsForQt5.qt5.wrapQtAppsHook
          ];
          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
            #Add any missing libraries a package may need
            pkgs.stdenv.cc.cc
          ];
          QT_PLUGIN_PATH = with pkgs.qt5; "${qtbase}/${qtbase.qtPluginPrefix}";
        };
      }
    );
}
