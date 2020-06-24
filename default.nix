{ pkgs ? import <nixpkgs> { }, stdenv ? pkgs.stdenv, fetchPypi ? pkgs.fetchPypi
, pythonPkgs ? pkgs.python36Packages
, buildPythonPackage ? pythonPkgs.buildPythonPackage }:

buildPythonPackage rec {
  pname = "cadCAD";
  version = "0.4.15";

  # Nix allows fetching the project source from different locations
  #src = fetchPypi {
  #  inherit pname version;
  #  sha256 = "4f2a4d39e4ea601b9ab42b2db08b5918a9538c168cff1c6895ae26646f3d73b1";
  #};
  # src = builtins.fetchGit {
  #   url = "git@github.com:BlockScience/cadCAD.git";
  #   ref = "master";
  # };
  src = ./.;

  # In future, when tests are introduced, this can be updated to 'true'
  doCheck = false;

  buildInputs = with pythonPkgs; [
    wheel
    pytest
    parameterized
  ];
  checkInputs = [ ];
  propagatedBuildInputs = with pythonPkgs; [
    pandas
    pathos
    fn
    funcy
    tabulate
  ];

  meta = with stdenv.lib; {
    description =
      "Design, test and validate complex systems through simulation in Python";
    homepage = "https://github.com/BlockScience/cadCAD";
    license = licenses.mit;
    # maintainers = with maintainers; [ benschza ];
    platforms = platforms.unix;
  };
}
