# generated using pypi2nix tool (version: 1.8.1)
# See more at: https://github.com/garbas/pypi2nix
#
# COMMAND:
#   pypi2nix -V 3.6 -r req-no-dep.txt
#

{ pkgs ? import <nixpkgs> {}
}:

let

  inherit (pkgs) makeWrapper;
  inherit (pkgs.stdenv.lib) fix' extends inNixShell;

  pythonPackages =
  import "${toString pkgs.path}/pkgs/top-level/python-packages.nix" {
    inherit pkgs;
    inherit (pkgs) stdenv;
    python = pkgs.python36;
    # patching pip so it does not try to remove files when running nix-shell
    overrides =
      self: super: {
        bootstrapped-pip = super.bootstrapped-pip.overrideDerivation (old: {
          patchPhase = old.patchPhase + ''
            sed -i               -e "s|paths_to_remove.remove(auto_confirm)|#paths_to_remove.remove(auto_confirm)|"                -e "s|self.uninstalled = paths_to_remove|#self.uninstalled = paths_to_remove|"                  $out/${pkgs.python35.sitePackages}/pip/req/req_install.py
          '';
        });
      };
  };

  commonBuildInputs = [];
  commonDoCheck = false;

  withPackages = pkgs':
    let
      pkgs = builtins.removeAttrs pkgs' ["__unfix__"];
      interpreter = pythonPackages.buildPythonPackage {
        name = "python36-interpreter";
        buildInputs = [ makeWrapper ] ++ (builtins.attrValues pkgs);
        buildCommand = ''
          mkdir -p $out/bin
          ln -s ${pythonPackages.python.interpreter}               $out/bin/${pythonPackages.python.executable}
          for dep in ${builtins.concatStringsSep " "               (builtins.attrValues pkgs)}; do
            if [ -d "$dep/bin" ]; then
              for prog in "$dep/bin/"*; do
                if [ -f $prog ]; then
                  ln -s $prog $out/bin/`basename $prog`
                fi
              done
            fi
          done
          for prog in "$out/bin/"*; do
            wrapProgram "$prog" --prefix PYTHONPATH : "$PYTHONPATH"
          done
          pushd $out/bin
          ln -s ${pythonPackages.python.executable} python
          ln -s ${pythonPackages.python.executable}               python3
          popd
        '';
        passthru.interpreter = pythonPackages.python;
      };
    in {
      __old = pythonPackages;
      inherit interpreter;
      mkDerivation = pythonPackages.buildPythonPackage;
      packages = pkgs;
      overrideDerivation = drv: f:
        pythonPackages.buildPythonPackage (drv.drvAttrs // f drv.drvAttrs //                                            { meta = drv.meta; });
      withPackages = pkgs'':
        withPackages (pkgs // pkgs'');
    };

  python = withPackages {};

  generated = self: {

    "dill" = python.mkDerivation {
      name = "dill-0.3.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/39/7a/70803635c850e351257029089d38748516a280864c97cbc73087afef6d51/dill-0.3.0.tar.gz"; sha256 = "993409439ebf7f7902d9de93eaa2a395e0446ff773d29f13dc46646482f76906"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://pypi.org/project/dill";
        license = licenses.bsdOriginal;
        description = "serialize all of python";
      };
    };



    "fn" = python.mkDerivation {
      name = "fn-0.4.3";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/a2/32/9d184dc2e8225af558e155a3865d610df8533d5d48a2ed5943bf8a30a137/fn-0.4.3.tar.gz"; sha256 = "f8cd80cdabf15367a2f07e7a9951fdc013d7200412743d85b88f2c896c95bada"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kachayev/fn.py";
        license = "Copyright 2013 Alexey Kachayev";
        description = "Implementation of missing features to enjoy functional programming in Python";
      };
    };



    "funcy" = python.mkDerivation {
      name = "funcy-1.13";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/a0/50/68e2202b1d3913a0fcef9ac53b9909a47da2f022844ae043f9425777352b/funcy-1.13.tar.gz"; sha256 = "918f333f675d9841ec7d77b9f0d5a272ed290393a33c8ef20e605847de89b1c3"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/Suor/funcy";
        license = licenses.bsdOriginal;
        description = "A fancy and practical functional tools";
      };
    };



    "multiprocess" = python.mkDerivation {
      name = "multiprocess-0.70.8";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/50/40/b23b1ddd3cb0e072fdbec5f458e8369df48643a3b04dfb55365a63a51687/multiprocess-0.70.8.tar.gz"; sha256 = "fc6b2d8f33e7d437a82c6d1c2f1673ae20a271152a1ac6a18571d10308de027d"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."dill"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://pypi.org/project/multiprocess";
        license = licenses.bsdOriginal;
        description = "better multiprocessing and multithreading in python";
      };
    };



    "pathos" = python.mkDerivation {
      name = "pathos-0.2.4";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/ed/6f/c6d34bda9f6383b693418f7b2340e8e6692e5a0ed154e918c09399fbf2ec/pathos-0.2.4.tar.gz"; sha256 = "610dc244b6b5c240396ae392bb6f94d7e990b0062d4032c5e9ab00b594ed8720"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."dill"
      self."multiprocess"
      self."pox"
      self."ppft"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://pypi.org/project/pathos";
        license = licenses.bsdOriginal;
        description = "parallel graph management and execution in heterogeneous computing";
      };
    };



    "pox" = python.mkDerivation {
      name = "pox-0.2.6";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/b0/8e/e8095866c3b512f9ef844ad20669e0c4785da1784dcfd282377896ffd3b1/pox-0.2.6.tar.gz"; sha256 = "47cb160322922c54590be447f08aa43f04875a3e53eee89963a757ebb5eb1376"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://pypi.org/project/pox";
        license = licenses.bsdOriginal;
        description = "utilities for filesystem exploration and automated builds";
      };
    };



    "ppft" = python.mkDerivation {
      name = "ppft-1.6.6.1";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/5b/16/9e83c2aa45949ee9cd6e8731275acdaeb6c624b8728d6598196c65074f3e/ppft-1.6.6.1.tar.gz"; sha256 = "9e2173042edd5cc9c7bee0d7731873f17fcdce0e42e4b7ab68857d0de7b631fc"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."dill"
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://pypi.org/project/ppft";
        license = licenses.bsdOriginal;
        description = "distributed and parallel python";
      };
    };



    "six" = python.mkDerivation {
      name = "six-1.12.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/dd/bf/4138e7bfb757de47d1f4b6994648ec67a51efe58fa907c1e11e350cddfca/six-1.12.0.tar.gz"; sha256 = "d16a0141ec1a18405cd4ce8b4613101da75da0e9a7aec5bdd4fa804d0e0eba73"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/benjaminp/six";
        license = licenses.mit;
        description = "Python 2 and 3 compatibility utilities";
      };
    };



    "tabulate" = python.mkDerivation {
      name = "tabulate-0.8.3";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/c2/fd/202954b3f0eb896c53b7b6f07390851b1fd2ca84aa95880d7ae4f434c4ac/tabulate-0.8.3.tar.gz"; sha256 = "8af07a39377cee1103a5c8b3330a421c2d99b9141e9cc5ddd2e3263fea416943"; };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://bitbucket.org/astanin/python-tabulate";
        license = licenses.mit;
        description = "Pretty-print tabular data";
      };
    };

  };
  localOverridesFile = ./requirements_override.nix;
  overrides = import localOverridesFile { inherit pkgs python; };
  commonOverrides = [

  ];
  allOverrides =
    (if (builtins.pathExists localOverridesFile)
     then [overrides] else [] ) ++ commonOverrides;

in python.withPackages
   (fix' (pkgs.lib.fold
            extends
            generated
            allOverrides
         )
   )