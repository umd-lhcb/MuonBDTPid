{ stdenv
, root
, cxxopts
}:

stdenv.mkDerivation {
  pname = "AddUBDTBranch";
  version = "0.2.4";

  src = builtins.path { path = ./../..; name = "AddUBDTBranch"; };

  buildInputs = [ root cxxopts ];

  installPhase = ''
    mkdir -p $out/bin
    mkdir -p $out/weights
    cp bin/AddUBDTBranchRun2 $out/bin
    cp bin/AddUBDTBranchRun2PidCalib $out/bin
    cp weights/weights_run2_all_cuts_ubdt.xml $out/weights/ubdt_run2.xml
  '';
}
