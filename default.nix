{ pkgs ? import <nixpkgs> { }, stdenv ? pkgs.stdenv, fetchPypi ? pkgs.fetchPypi
, pythonPkgs ? pkgs.python37Packages
, buildPythonPackage ? pythonPkgs.buildPythonPackage }:

buildPythonPackage rec {
  pname = "cadCAD";
  version = "0.4.15";

  #src = fetchPypi {
  #  inherit pname version;
  #  sha256 = "4f2a4d39e4ea601b9ab42b2db08b5918a9538c168cff1c6895ae26646f3d73b1";
  #};
  # src = builtins.fetchGit {
  #   url = "git@github.com:BlockScience/cadCAD.git";
  #   ref = "master";
  # };
  src = ./.;

  doCheck = false; # TODO: correct or disclude integration tests

  buildInputs = [ ];
  checkInputs = [ ];
  propagatedBuildInputs = with pythonPkgs; [
    numpy
    pandas
    pathos
    fn
    tabulate
    funcy
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
