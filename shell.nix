let
  pkgs = import <nixpkgs> { overlays = [(import ./nix/overlay)]; };
in

pkgs.mkShell {
  pname = "MuonBDTPid";
  buildInputs = with pkgs; [
    python2
    root5
  ];
}
