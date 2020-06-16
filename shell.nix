with import <nixpkgs> { };

(let cadCAD = pkgs.callPackage ./default.nix { inherit (pkgs) ; };
in pkgs.python36.withPackages (ps: [ cadCAD ps.pandas ])).env
