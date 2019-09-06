self: super:
{
  customPython =
      (import ./requirements.nix { pkgs = self; });
}
