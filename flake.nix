{
  description = "Muon PID with an uboost BDT.";

  inputs = {
    root-curated.url = "github:umd-lhcb/root-curated";
    nixpkgs.follows = "root-curated/nixpkgs";
    flake-utils.follows = "root-curated/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, root-curated }:
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

            # Dev
            (python3.withPackages (ps: with ps; [
              black
            ]))
          ];
        };
      });
}
