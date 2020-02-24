{ nixpkgs ? import <nixpkgs> { } }:

with import <nixpkgs> { };

let channels = rec { requirements = import ./nix/requirements.nix { }; };
in with channels;

let
  pkgs = [
    python37
    python37Packages.pip
    python37Packages.setuptools
    python37Packages.virtualenvwrapper
    python37Packages.numpy
    python37Packages.pandas
  ];

  deps = builtins.attrValues requirements.packages;

in nixpkgs.stdenv.mkDerivation {
  name = "env";
  buildInputs = [ pkgs deps ];
}
