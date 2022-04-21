final: prev:

{
  root5-ubdt = prev.callPackage ./root5 {
    inherit (prev.darwin.apple_sdk.frameworks) Cocoa OpenGL;
    stdenv = if prev.stdenv.cc.isClang then prev.llvmPackages_5.stdenv else prev.gcc8Stdenv;
  };

  AddUBDTBranch = prev.callPackage ./AddUBDTBranch {
    root = final.root5-ubdt;
    stdenv = if prev.stdenv.cc.isClang then prev.llvmPackages_5.stdenv else prev.gcc8Stdenv;
  };

  AddUBDTBranchWrapped = prev.writeScriptBin "AddUBDTBranch" ''
    unset LD_LIBRARY_PATH
    unset DYLD_LIBRARY_PATH

    exec ${final.AddUBDTBranch}/bin/AddUBDTBranchRun2 $@ -x ${final.AddUBDTBranch}/weights/ubdt_run2.xml
  '';

  AddUBDTBranchPidCalibWrapped = prev.writeScriptBin "AddUBDTBranchPidCalib" ''
    unset LD_LIBRARY_PATH
    unset DYLD_LIBRARY_PATH

    exec ${final.AddUBDTBranch}/bin/AddUBDTBranchRun2PidCalib $@ -x ${final.AddUBDTBranch}/weights/ubdt_run2.xml
  '';
}
