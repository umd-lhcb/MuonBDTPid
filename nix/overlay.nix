final: prev:

rec {
  root5 = prev.callPackage ./root5 {
    inherit (prev.darwin.apple_sdk.frameworks) Cocoa OpenGL;
    stdenv = if prev.stdenv.cc.isClang then prev.llvmPackages_5.stdenv else prev.gcc8Stdenv;
  };

  addUBDTBranch = prev.callPackage ./addUBDTBranch {
    root = root5;
    stdenv = if prev.stdenv.cc.isClang then prev.llvmPackages_5.stdenv else prev.gcc8Stdenv;
  };

  addUBDTBranchWrapped = prev.writeScriptBin "addUBDTBranch" ''
    unset LD_LIBRARY_PATH
    unset DYLD_LIBRARY_PATH

    exec ${final.addUBDTBranch}/bin/addUBDTBranchRun2 $@
  '';
}
