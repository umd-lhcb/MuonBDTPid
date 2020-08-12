let
  pkgs = import <nixpkgs> { overlays = [(import ./nix/overlay)]; };
in

pkgs.mkShell {
  pname = "MuonBDTPid";
  buildInputs = with pkgs; [
    root5
  ];
}
