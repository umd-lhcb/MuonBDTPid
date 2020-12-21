{
  description = "Muon PID with an uboost BDT.";

  inputs = rec {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-20.09";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    {
      overlay = import ./nix/overlay.nix;
    }
    //
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlay ];
        };
      in
      {
        devShell = pkgs.mkShell {
          pname = "MuonBDTPid";
          buildInputs = with pkgs; [
            python2
            root5

            # Debug
            gdb
            cgdb
            gdbgui
            valgrind
          ];
        };
      });
}
