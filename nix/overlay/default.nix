self: super:

{
  root5 = super.callPackage ./root5 {
    inherit (super.darwin.apple_sdk.frameworks) Cocoa OpenGL;
    stdenv = if super.stdenv.cc.isClang then super.llvmPackages_5.stdenv else super.gcc8Stdenv;
  };
}
