with import <nixpkgs> { };

(let cadCAD = pkgs.callPackage ./default.nix { inherit (pkgs) ; };
in pkgs.python37.withPackages (ps: [ cadCAD ])).env
