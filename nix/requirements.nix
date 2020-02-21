# generated using pypi2nix tool (version: 2.0.4)
# See more at: https://github.com/nix-community/pypi2nix
#
# COMMAND:
#   pypi2nix -V python37 -r requirements.txt
#

{ pkgs ? import <nixpkgs> {},
  overrides ? ({ pkgs, python }: self: super: {})
}:

let

  inherit (pkgs) makeWrapper;
  inherit (pkgs.stdenv.lib) fix' extends inNixShell;

  pythonPackages =
  import "${toString pkgs.path}/pkgs/top-level/python-packages.nix" {
    inherit pkgs;
    inherit (pkgs) stdenv;
    python = pkgs.python37;
  };

  commonBuildInputs = [];
  commonDoCheck = false;

  withPackages = pkgs':
    let
      pkgs = builtins.removeAttrs pkgs' ["__unfix__"];
      interpreterWithPackages = selectPkgsFn: pythonPackages.buildPythonPackage {
        name = "python37-interpreter";
        buildInputs = [ makeWrapper ] ++ (selectPkgsFn pkgs);
        buildCommand = ''
          mkdir -p $out/bin
          ln -s ${pythonPackages.python.interpreter} \
              $out/bin/${pythonPackages.python.executable}
          for dep in ${builtins.concatStringsSep " "
              (selectPkgsFn pkgs)}; do
            if [ -d "$dep/bin" ]; then
              for prog in "$dep/bin/"*; do
                if [ -x "$prog" ] && [ -f "$prog" ]; then
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
          ln -s ${pythonPackages.python.executable} \
              python3
          popd
        '';
        passthru.interpreter = pythonPackages.python;
      };

      interpreter = interpreterWithPackages builtins.attrValues;
    in {
      __old = pythonPackages;
      inherit interpreter;
      inherit interpreterWithPackages;
      mkDerivation = args: pythonPackages.buildPythonPackage (args // {
        nativeBuildInputs = (args.nativeBuildInputs or []) ++ args.buildInputs;
      });
      packages = pkgs;
      overrideDerivation = drv: f:
        pythonPackages.buildPythonPackage (
          drv.drvAttrs // f drv.drvAttrs // { meta = drv.meta; }
        );
      withPackages = pkgs'':
        withPackages (pkgs // pkgs'');
    };

  python = withPackages {};

  generated = self: {
    "cadcad" = python.mkDerivation {
      name = "cadcad-0.3.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/a4/46/a81e647da687f5229d0636dd29ad7444e2c3b147ca4242680b5b34130454/cadCAD-0.3.1.tar.gz";
        sha256 = "29364d588d1075701e143054ee15470bcad09820f2bc6a936233333a8c8645ac";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."fn"
        self."funcy"
        self."pandas"
        self."pathos"
        self."tabulate"
        self."wheel"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/BlockScience/cadCAD";
        license = "LICENSE.txt";
        description = "cadCAD: a differential games based simulation software package for research, validation, and         Computer Aided Design of economic systems";
      };
    };

    "cython" = python.mkDerivation {
      name = "cython-0.29.15";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/d9/82/d01e767abb9c4a5c07a6a1e6f4d5a8dfce7369318d31f48a52374094372e/Cython-0.29.15.tar.gz";
        sha256 = "60d859e1efa5cc80436d58aecd3718ff2e74b987db0518376046adedba97ac30";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://cython.org/";
        license = licenses.asl20;
        description = "The Cython compiler for writing C extensions for the Python language.";
      };
    };

    "dill" = python.mkDerivation {
      name = "dill-0.3.1.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/c7/11/345f3173809cea7f1a193bfbf02403fff250a3360e0e118a1630985e547d/dill-0.3.1.1.tar.gz";
        sha256 = "42d8ef819367516592a825746a18073ced42ca169ab1f5f4044134703e7a049c";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://pypi.org/project/dill";
        license = licenses.bsdOriginal;
        description = "serialize all of python";
      };
    };

    "fn" = python.mkDerivation {
      name = "fn-0.4.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/a2/32/9d184dc2e8225af558e155a3865d610df8533d5d48a2ed5943bf8a30a137/fn-0.4.3.tar.gz";
        sha256 = "f8cd80cdabf15367a2f07e7a9951fdc013d7200412743d85b88f2c896c95bada";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kachayev/fn.py";
        license = "Copyright 2013 Alexey Kachayev";
        description = "Implementation of missing features to enjoy functional programming in Python";
      };
    };

    "funcy" = python.mkDerivation {
      name = "funcy-1.14";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ce/4b/6ffa76544e46614123de31574ad95758c421aae391a1764921b8a81e1eae/funcy-1.14.tar.gz";
        sha256 = "75ee84c3b446f92e68a857c2267b15a1b49c631c9d5a87a5f063cd2d6761a5c4";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/Suor/funcy";
        license = licenses.bsdOriginal;
        description = "A fancy and practical functional tools";
      };
    };

    "multiprocess" = python.mkDerivation {
      name = "multiprocess-0.70.9";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/58/17/5151b6ac2ac9b6276d46c33369ff814b0901872b2a0871771252f02e9192/multiprocess-0.70.9.tar.gz";
        sha256 = "9fd5bd990132da77e73dec6e9613408602a4612e1d73caf2e2b813d2b61508e5";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."dill"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://pypi.org/project/multiprocess";
        license = licenses.bsdOriginal;
        description = "better multiprocessing and multithreading in python";
      };
    };

    "numpy" = python.mkDerivation {
      name = "numpy-1.14.5";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/d5/6e/f00492653d0fdf6497a181a1c1d46bbea5a2383e7faf4c8ca6d6f3d2581d/numpy-1.14.5.zip";
        sha256 = "a4a433b3a264dbc9aa9c7c241e87c0358a503ea6394f8737df1683c7c9a102ac";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.numpy.org";
        license = licenses.bsdOriginal;
        description = "NumPy: array processing for numbers, strings, records, and objects.";
      };
    };

    "pandas" = python.mkDerivation {
      name = "pandas-1.0.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/02/c3/e8c56de02d6c52f8541feca2fd77117e8ae4956f7b3e5cdbed726624039b/pandas-1.0.1.tar.gz";
        sha256 = "3c07765308f091d81b6735d4f2242bb43c332cc3461cae60543df6b10967fe27";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [
        self."cython"
        self."numpy"
        self."setuptools"
        self."wheel"
      ];
      propagatedBuildInputs = [
        self."numpy"
        self."python-dateutil"
        self."pytz"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://pandas.pydata.org";
        license = licenses.bsdOriginal;
        description = "Powerful data structures for data analysis, time series, and statistics";
      };
    };

    "pathos" = python.mkDerivation {
      name = "pathos-0.2.5";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/c6/a2/cd59f73d5ede4f122687bf8f63de5d671c9561e493ca699241f05b038278/pathos-0.2.5.tar.gz";
        sha256 = "21ae2cb1d5a76dcf57d5fe93ae8719c7339f467e246163650c08ccf35b87c846";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
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
      name = "pox-0.2.7";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/6c/9a/957818485aa165ce93b646aeb20181215bb415c9dca8345bdbe23b08ae67/pox-0.2.7.tar.gz";
        sha256 = "06afe1a4a1dbf8b47f7ad5a3c1d8ada9104c64933a1da11338269a2bd8642778";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://pypi.org/project/pox";
        license = licenses.bsdOriginal;
        description = "utilities for filesystem exploration and automated builds";
      };
    };

    "ppft" = python.mkDerivation {
      name = "ppft-1.6.6.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/5b/16/9e83c2aa45949ee9cd6e8731275acdaeb6c624b8728d6598196c65074f3e/ppft-1.6.6.1.tar.gz";
        sha256 = "9e2173042edd5cc9c7bee0d7731873f17fcdce0e42e4b7ab68857d0de7b631fc";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://pypi.org/project/ppft";
        license = licenses.bsdOriginal;
        description = "distributed and parallel python";
      };
    };

    "python-dateutil" = python.mkDerivation {
      name = "python-dateutil-2.8.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/be/ed/5bbc91f03fa4c839c4c7360375da77f9659af5f7086b7a7bdda65771c8e0/python-dateutil-2.8.1.tar.gz";
        sha256 = "73ebfe9dbf22e832286dafa60473e4cd239f8592f699aa5adaf10050e6e1823c";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [
        self."setuptools"
        self."setuptools-scm"
        self."wheel"
      ];
      propagatedBuildInputs = [
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://dateutil.readthedocs.io";
        license = licenses.bsdOriginal;
        description = "Extensions to the standard Python datetime module";
      };
    };

    "pytz" = python.mkDerivation {
      name = "pytz-2019.3";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/82/c3/534ddba230bd4fbbd3b7a3d35f3341d014cca213f369a9940925e7e5f691/pytz-2019.3.tar.gz";
        sha256 = "b02c06db6cf09c12dd25137e563b31700d3b80fcc4ad23abb7a315f2789819be";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pythonhosted.org/pytz";
        license = licenses.mit;
        description = "World timezone definitions, modern and historical";
      };
    };

    "setuptools" = python.mkDerivation {
      name = "setuptools-45.2.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/68/75/d1d7b7340b9eb6e0388bf95729e63c410b381eb71fe8875cdfd949d8f9ce/setuptools-45.2.0.zip";
        sha256 = "89c6e6011ec2f6d57d43a3f9296c4ef022c2cbf49bab26b407fe67992ae3397f";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/setuptools";
        license = licenses.mit;
        description = "Easily download, build, install, upgrade, and uninstall Python packages";
      };
    };

    "setuptools-scm" = python.mkDerivation {
      name = "setuptools-scm-3.5.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b2/f7/60a645aae001a2e06cf4b8db2fba9d9f36b8fd378f10647e3e218b61b74b/setuptools_scm-3.5.0.tar.gz";
        sha256 = "5bdf21a05792903cafe7ae0c9501182ab52497614fa6b1750d9dbae7b60c1a87";
};
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [
        self."setuptools"
        self."wheel"
      ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/setuptools_scm/";
        license = licenses.mit;
        description = "the blessed package to manage your versions by scm tags";
      };
    };

    "six" = python.mkDerivation {
      name = "six-1.14.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/21/9f/b251f7f8a76dec1d6651be194dfba8fb8d7781d10ab3987190de8391d08e/six-1.14.0.tar.gz";
        sha256 = "236bdbdce46e6e6a3d61a337c0f8b763ca1e8717c03b369e87a7ec7ce1319c0a";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/benjaminp/six";
        license = licenses.mit;
        description = "Python 2 and 3 compatibility utilities";
      };
    };

    "tabulate" = python.mkDerivation {
      name = "tabulate-0.8.6";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/c4/41/523f6a05e6dc3329a5660f6a81254c6cd87e5cfb5b7482bae3391d86ec3a/tabulate-0.8.6.tar.gz";
        sha256 = "5470cc6687a091c7042cee89b2946d9235fe9f6d49c193a4ae2ac7bf386737c8";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/astanin/python-tabulate";
        license = licenses.mit;
        description = "Pretty-print tabular data";
      };
    };

    "wheel" = python.mkDerivation {
      name = "wheel-0.34.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/75/28/521c6dc7fef23a68368efefdcd682f5b3d1d58c2b90b06dc1d0b805b51ae/wheel-0.34.2.tar.gz";
        sha256 = "8788e9155fe14f54164c1b9eb0a319d98ef02c160725587ad60f14ddc57b6f96";
};
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [
        self."setuptools"
      ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/wheel";
        license = licenses.mit;
        description = "A built-package format for Python";
      };
    };
  };
  localOverridesFile = ./requirements_override.nix;
  localOverrides = import localOverridesFile { inherit pkgs python; };
  commonOverrides = [
        (let src = pkgs.fetchFromGitHub { owner = "nix-community"; repo = "pypi2nix-overrides"; rev = "100c15ec7dfe7d241402ecfb1e796328d0eaf1ec"; sha256 = "0akfkvdakcdxc1lrxznh1rz2811x4pafnsq3jnyr5pn3m30pc7db"; } ; in import "${src}/overrides.nix" { inherit pkgs python; })
  ];
  paramOverrides = [
    (overrides { inherit pkgs python; })
  ];
  allOverrides =
    (if (builtins.pathExists localOverridesFile)
     then [localOverrides] else [] ) ++ commonOverrides ++ paramOverrides;

in python.withPackages
   (fix' (pkgs.lib.fold
            extends
            generated
            allOverrides
         )
   )