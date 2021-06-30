{ stdenv
, makeWrapper
, root
}:

stdenv.mkDerivation {
  pname = "addUBDTBranch";
  version = "0.1.2";

  src = builtins.path { path = ./../../src; name = "addUBDTBranch"; };

  nativeBuildInputs = [ makeWrapper ];
  buildInputs = [ root ];

  installPhase = ''
    mkdir -p $out/bin
    cp addUBDTBranchRun2 $out/bin
  '';
}
