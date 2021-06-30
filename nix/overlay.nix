final: prev:

{
  root5-ubdt = prev.callPackage ./root5 {
    inherit (prev.darwin.apple_sdk.frameworks) Cocoa OpenGL;
    stdenv = if prev.stdenv.cc.isClang then prev.llvmPackages_5.stdenv else prev.gcc8Stdenv;
  };

  addUBDTBranch = prev.callPackage ./addUBDTBranch {
    root = final.root5-ubdt;
    stdenv = if prev.stdenv.cc.isClang then prev.llvmPackages_5.stdenv else prev.gcc8Stdenv;
  };

  addUBDTBranchWrapped = prev.writeScriptBin "addUBDTBranch" ''
    unset LD_LIBRARY_PATH
    unset DYLD_LIBRARY_PATH

    exec ${final.addUBDTBranch}/bin/addUBDTBranchRun2 $@
  '';
}
